""" Goal is to fine tuning and Inference using GLINER model.
    for ANY dataset.

    -->
       No harcoding of dataset fields,names
       Need to normalize the raw NER datase into intermediat NER format:
           ["dataset_id", "dataset_cat1", "text_id",  "text", "ner_list",  "info_json" ]

       Input of the model will be this parquet(  ["dataset_id",  ...,  "text", "ner_list",  "info_json" ])    

              Never change: 
                   NormalizedNER_dataset --> Preppro --> Code Train 

              Change
                 Dataset XXXX -->  NormalizedNER_dataset
                 --> Need a custom function for each dataset.


    ### Install
    pip intall gliner utilmy fire

    ### Usage
    cd asearch/
    mkdir -p ./ztmp/data/         ### ztmp is in .gitignore


    export cfg="config/ner/ner_cfg.yaml"
    

    python nlp/ner_gliner.py data_converter_collnll2003    --dirout ztmp/models/gliner/mymodel/

    python nlp/ner_gliner.py run_train     --cfg $cfg  --dirout ztmp/exp/
    
    python nlp/ner_gliner.py run_predict   --cfg $cfg  --dirout ztmp/models/gliner/mymodel/



  
  
   https://www.freecodecamp.org/news/getting-started-with-ner-models-using-huggingface/ 
   

   https://arxiv.org/html/2402.10573v2

"""
import os, json, pandas as pd, numpy as np 
from types import SimpleNamespace, Dict
from box import Box

from datasets import load_dataset, concatenate_datasets
from gliner import GLiNER
import torch
from transformers import get_cosine_schedule_with_warmup

from utilmy import (pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob, config_load,
                    json_save, json_load)
from utilmy import log, log2



##########################################################################################################
CONFIG_DEFAULT = Box(
        num_steps        = 4,  # number of training iteration
        train_batch_size = 2,
        eval_every       = 4 // 2,   # evaluation/saving steps
        save_directory   = "./ztmp/exp/ztest/gliner/", # where to save checkpoints
        warmup_ratio     = 0.1,    # warmup steps
        device           = "cpu",
        lr_encoder       = 1e-5,   # learning rate for backbone
        lr_others        = 5e-5,   # learning rate for other parameters
        freeze_token_rep = False,  # freeze of not backbone
        
        # Parameters for set_sampling_params
        max_types          = 25,   # maximum number of entity types during training
        shuffle_types      = True, # if shuffle or not entity types
        random_drop        = True, # randomly drop entity types
        max_neg_type_ratio = 1,    # ratio of positive/negative types, 1 mean 50%/50%, 2 mean 33%/66%, 3 mean 25%/75% ...
        max_len            = 384   # maximum sentence length
  )



######Dataset ############################################################################################
NER_COLSTARGET       = ["dataset_id", "dataset_cat1", "text_id",  "text", "ner_list",  "info_json" ]
NER_COLSTARGET_TYPES = ["str", "int64"  "str", "list", "str", "str" ]





##########################################################################################################
def test1():
    def cleanup(dir):
        from glob import glob
        files = glob(os.path.join(dir, "*"))
        for f in files:
            os.remove(f)
    
    
    test_dir = "./ztmp/test"

    data_converter_collnll2003( dirout=test_dir, nrows=100)
    json = nerparquet_load_to_json_gliner(test_dir)
    print(json[0])
    # length of dataset
    assert len(json) == 100
    assert json[0].keys() == {'tokenized_text', 'ner'}


    ### other part to be quicly tested

    cleanup(test_dir)
    os.rmdir(test_dir)



def test_all1():
     data_converter_collnll2003(dirout="ztmp/data/ner/norm/conll2003",  nrows=1000)




###########################################################################################################
####### Datalod Custom ####################################################################################
def hash_textid(xstr:str, n_chars=1000, seed=123):
  import xxhash  
  return xxhash.xxh64_intdigest(str(xstr)[:n_chars], seed=seed) - len(xstr)




def dataXX_load_prepro():
    dirtrain = "./ztmp/data/data/conll2003/"
    dirtrain = "./ztmp/data/data/conll2003/"

    d_train:dict = nerparquet_load_to_json_gliner( dirtrain, nrows=1000000)
    d_val:dict   = nerparquet_load_to_json_gliner( dirtval, nrows=1000000)

    return d_train, d_val


def dataXX_create_label_mapper():

    global NCLASS, L2I, i2L

    NER_TAG ={}
    NCLASS = len(NER_TAG)
    l2I = {}
    i2L = {}

    return L2I, i2L




###########################################################################################################
####### Dataloder Commmon #################################################################################
def nerparquet_load_to_json_gliner( dirin="ztmp/data/ner/norm/conll2003", nrows=1000000)->Dict:
    """Load NER data from a parquet or a JSON file and convert it to a JSON format.

    Input:  parquet file like this
            ["dataset_id", "dataset_cat1", "text_id",  "text", "ner_list",  "info_json" ]


    Output: Gliner Model JSON format
        Target Format             0          1         2       3     4      5
        [{  "tokenized_text": ["State", "University", "of", "New", "York", "Press", ",", "1997", "."],

                                 Token_start  tokenid_end
            "ner":            [ [ 0,         5,                     "Publisher" ] ]
                                State University of New York Press 
        },
  
      data_val = {
        "entity_types": ["Person", 'Event Reservation'],  ### TODO: Remove the entity hardcoding
        "samples": data_train[:10]}

    """
    if ".json" in dirin: 
         djson = json_load(dirin)
         return djson


    log("######## Start conversion dataframe to json format...")
    df = pd_read_file( dirin + "/*.parquet", nrows= nrows)
    assert len(df[NER_COLSTARGET])>0

    djson = []
    for i, row in df.iterrows():
      #### dd ={"tokenized_text" : df.at[i, "text"], "ner" : ner_list}
      dd = nerparquet_tokenizer_to_json_gliner(row['text'], row["ner_list"], sep=" ")
      djson.append(dd)

    return djson


def nerparquet_tokenizer_to_json_gliner(text:str, ner_list:list, sep=" "):
      """ Reformat  NER data by tokenizing  text and creating a new list of NER entities.

      Parameters:
          text (str):  input text to be tokenized.
          ner_list (List[Tuple[int, int, str]]):  list of NER entities in  format (start_index, end_index, tag).
          sep (str, optional):  separator used to split  text. Defaults to " ".

      Returns:       
            Target Frormat[{  "tokenized_text": ["State", "University", "of", "New", "York", "Press", ",", "1997", "."],
                              "ner":            [ [ 0, 5, "Publisher" ] ]
            },
      """
      ner_list = []  
      token_text_list = []
      token_id1 = 0
      for (idx1, idx2, tag ) in ner_list:
         ### idx1, idx2 are String indexes
         idx1, idx2 = int(idx1), int(idx2)  ### because parquet is saved as string. 
         tag = str(tag)

         llist =  text[idx1:idx2+1].split(sep)
         token_text_list = token_text_list + llist ### add token list to token_text_list

         ### token_id1 are List indexes
         token_id2 = len(token_text_list) - 1
         ner_list.append( [token_id1, token_id2, tag,]  )         
         token_id1 = token_id2 + 1

      dd ={"tokenized_text" : token_text_list, "ner" : ner_list}
      return dd






##########################################################################################################
##########################################################################################################
def exp_create_exp_folder( task="ner_deberta", dirout="./ztmp/exp", cc=None:dict):
    """Create an experiment folder with a timestamped directory name and save   configuration object as a JSON file.
    Args:
        task (str, optional):   name of   task. Defaults to "ner_deberta".
        dirout (str, optional):   output directory. Defaults to "./ztmp/exp".
        cc (Box, optional):   configuration object. Defaults to None.
    """
    dt = date_now(fmt="%Y%m%d/%H%M%S")
    dirout0 = dirout
    cc.dirout = f"{dirout0}/{dt}"
    dirout = cc.dirout
    os_makedirs(dirout)
    json_save({"cc": cc }, f"{dirout}/{task}.json")
    return cc




def run_train(cfg=None, cfg_name="ner_gliner", dirout="./ztmp/exp", istest=1):
    """ 
       python nlp/ner/ner_deberta.py run_train  --dirout ztmp/exp   --cfg config/traina/train1.yaml --cfg_name ner_deberta

       python nlp/ner_gliner.py  run_train  --dirout  --cfg "ztmp/myconfig.yaml"

       Args:

          cfg (dict)      : Configuration dictionary (default is None).  "ztmp/myconfig.yaml"
          dirout (str)    : Output directory path (default is None).
          model_name (str): Name of model to use (default is "urchade/gliner_small").
          dirdata (str)   : Directory path of data to use (default is "data/sample_data.json").

    """
    log("###### Config Load   #############################################")
    cc = Box()
    cfg0 = config_load(cfg)
    cfg0 = cfg0.get(cfg_name, None) if cfg0 is not None else None


    log("###### User Params   #############################################")
    n_train = 20 if istest == 1 else 1000000000
    n_val   = 5  if istest == 1 else 1000000000

    if cfg0 is not None :
       cc = copy.deepcopy(cfg0) 

    else:
        cc.model_name='gliner/gliner-small'

        #### Data name
        cc.dataloader_name = "dataXX_load_prepro"
        cc.datamapper_name = "dataXX_create_label_mapper"

        cc.n_train = n_train
        cc.n_val   = n_val
    
        #### Train Args
        aa                = CONFIG_DEFAULT
        aa.num_steps      = 2
        aa.save_directory = dirout + "/train_log/"
        aa.eval_every     = aa.num_steps // 2
        aa.device         = "cpu"
        cc.hf_args_train = copy.deepcopy(aa)
        os_makedirs(aa.save_directory)

        ### HF model
        cc.hf_args_model_init = {}
        cc.hf_args_model_init.model_name = cc.model_name
        # cc.hf_args_model_init.num_labels = NCLASS*2+1 ## due to BOI notation

    cc.cfg      = cfg
    cc.cfg_name = cfg_name

    log("###### Experiment Folder   #######################################")
    cc = exp_create_exp_folder(task="ner_deberta", dirout=dirout, cc=cc)
    log(cc.dirout)


    log("###### Model : Training params ##############################")
    args = TrainingArguments( ** dict(cc.hf_args_train))


    log("###### User Data Load   #############################################")
    from utilmy import load_function_uri
    # dataloader_fun = load_function_uri(dataloader_name)
    # datamapper_fun = load_function_uri(datamapper_name]

    dataloader_fun = globals()[cc.dataloader_name]
    datamapper_fun = globals()[cc.datamapper_name]  ### dataXX_create_label_mapper()

    data_train:dict, json_val:dict = dataloader_fun()  ## = dataXX_load_prepro()
    L2I, i2L, NCLASS               = datamapper_fun()  ## Label to Index, Index to Label

    data_train, data_val = data_train[:cc.n_train], data_val.iloc[:cc.n_val]


    cc.data ={}
    cc.data.cols          = columns
    cc.data.cols_required = ["text", "ner_list" ]
    cc.data.ner_format    = ["start", "end", "type", "value"]  
    #cc.data.cols_remove   = ['overflow_to_sample_mapping', 'offset_mapping', ] + columns
    cc.data.L2I           = L2I     ### label to Index Dict
    cc.data.i2l           = i2l     ### Index to Label Dict
    cc.data.nclass        = NCLASS  ### Number of NER Classes.

    log("##### Model Load", cc.model_name)
    #### available models: https://huggingface.co/urchade
    model = GLiNER.from_pretrained(cc.model_name)


    log("##### Train start")
    train(model, cc.hf_args_train, train_data= data_train, eval_data= data_val)


    dirfinal = f"{dirout}/final/"
    log("##### Model Save", dirfinal)
    os_makedirs(dirfinal) 
    model.save_pretrained( dirfinal)



def run_train_v1(cfg:dict=None, cfg_name:str=None, dirout:str="ztmp/exp", 
              model_name:str="urchade/gliner_small",
              dirdata_train="./ztmp/data/ner/normalized/mydataset/",   
              dirdata_val=None,   
              
              device  = "cpu"):
  """A function to train a model using specified configuration and data.

  python nlp/ner_gliner.py  run_train  --dirout  --cfg "ztmp/myconfig.yaml"

  Parameters:
      cfg (dict)      : Configuration dictionary (default is None).  "ztmp/myconfig.yaml"
      dirout (str)    : Output directory path (default is None).
      model_name (str): Name of model to use (default is "urchade/gliner_small").
      dirdata (str)   : Directory path of data to use (default is "data/sample_data.json").

  Returns:
      None
  """
  dt      = date_now(fmt="%Y%m%d/%H%M%S")
  dirout2 = f"{dirout}/{dt}"


  log("##### Load Config", cfg_name)
  cfg    = config_load(cfg)  ### String path for config
  config = cfg.get(cfg_name, None) if isinstance(cfg, dict) else None
  if config is None:
    config = CONFIG_DEFAULT
    nsteps = 2
    config.num_steps      = nsteps
    config.save_directory = dirout2
    config.eval_every     = nsteps // 2
    config.device         = device
    

  log("##### Load data", dirdata_train)
  #### evaluation only support fix entity types (but can be easily extended)
  #### Want to rreplace by dataframe load
  data_train : dict = nerparquet_load_to_json_gliner(dirdata_train)

  if dirdata_val is None :
    data_val = {
        "entity_types": ["Person", 'Event Reservation'],  ### TODO: Remove the entity hardcoding
        "samples": data_train[:10]}
  else:
    data_val : dict = nerparquet_load_to_json_gliner(dirdata_val)



  log("##### Model Load", model_name)
  #### available models: https://huggingface.co/urchade
  model = GLiNER.from_pretrained(model_name)


  log("##### Train start")
  train(model, config, train_data= data_train, eval_data= data_val)


  dirfinal = f"{dirout2}/final/"
  log("##### Model Save", dirfinal)
  os_makedirs(dirfinal) 
  model.save_pretrained( dirfinal)




def run_predict(cfg:dict=None, dirmodel="ztmp/models/gliner/small", 
                dirdata="ztmp/data/text.csv",
                coltext="text",
                dirout="ztmp/data/ner/predict/",
                kbatch=100):
  """Function to run prediction using a pre-trained GLiNER model.

    python nlp/ner_gliner.py --dirdata "ztmp/data/text.csv"     --coltext text    --dirout ztmp/data/ner/predict/data1/


    predict_entities(self, text, labels, flat_ner=True, threshold=0.5, multi_label=False):

  Parameters:
      cfg (dict): Configuration dictionary (default is None).
      dirmodel (str): Directory path of pre-trained model (default is "ztmp/models/gliner/small").
      dirdata (str): Directory path of input data (default is "ztmp/data/text.csv").

  #log(model.predict("My name is John Doe and I love my car. I bought a new car in 2020."))

  """
  model = GLiNER.from_pretrained(dirmodel, local_files_only=True)
  log(model)
  model.eval()

  df = pd_read_file(dirdata)
  log(df[coltext].shape)

  df["ner_list_pred"] = df[coltext].apply(lambda x: model.predict(x))
  pd_to_file(df, dirout +"/df_predict_ner.parquet", show=1)



##########################################################################################################
def train(model, config, train_data, eval_data=None):

    cc = Box({})
    cc.config = dict(config)

    model = model.to(config.device)

    # Set sampling parameters from config
    model.set_sampling_params(
        max_types=config.max_types, 
        shuffle_types=config.shuffle_types, 
        random_drop=config.random_drop, 
        max_neg_type_ratio=config.max_neg_type_ratio, 
        max_len=config.max_len
    )
    
    model.train()

    train_loader = model.create_dataloader(train_data, batch_size=config.train_batch_size, shuffle=True)
    optimizer    = model.get_optimizer(config.lr_encoder, config.lr_others, config.freeze_token_rep)

    n_warmup_steps = int(config.num_steps * config.warmup_ratio) if config.warmup_ratio < 1 else  int(config.warmup_ratio)


    scheduler = get_cosine_schedule_with_warmup(optimizer,
        num_warmup_steps=n_warmup_steps,
        num_training_steps=config.num_steps)

    iter_train_loader = iter(train_loader)

    log("###### training Start Epoch...")
    for step in range(0, config.num_steps):
        try:
            x = next(iter_train_loader)
        except StopIteration:
            iter_train_loader = iter(train_loader)
            x = next(iter_train_loader)

        for k, v in x.items():
            if isinstance(v, torch.Tensor):
                x[k] = v.to(config.device)

        loss = model(x)  # Forward pass
            
        # Check if loss is nan
        if torch.isnan(loss):
            continue

        loss.backward()        # Compute gradients
        optimizer.step()       # Update parameters
        scheduler.step()       # Update learning rate schedule
        optimizer.zero_grad()  # Reset gradients

        descrip = f"step: {step} | epoch: {step // len(train_loader)} | loss: {loss.item():.2f}"
        log(descrip)

        if (step + 1) % config.eval_every == 0:
            model.eval()            
            if eval_data is not None:
                results, f1 = model.evaluate(eval_data["samples"], flat_ner=True, threshold=0.5,
                                      batch_size=12,
                                      entity_types=eval_data["entity_types"])

                log(f"Step={step}\n{results}")


            dirout2 = f"{config.save_directory}/finetuned_{step}"
            os_makedirs(dirout2)                
            model.save_pretrained(dirout2)
            #json_save(cc.to_dict(), f"{config.save_directory}/config.json")
            model.train()





##########################################################################################################
################## Legal Benchmark ########################################################################
def data_load_legalDoc(cfg=None, dirin=r"", dirout=r""):
  """ Convert data to json 
  Input : csv or parquet file

  Target Frormat
  [
  {
    "tokenized_text": ["State", "University", "of", "New", "York", "Press", ",", "1997", "."],
    "ner": [ [ 0, 5, "Publisher" ] ]
  }
  ],
  
  """
  def find_indices_in_list(text, start_pos, end_pos):
        words = text.split(" ")
        cumulative_length = 0
        start_index = None
        end_index = None

        for i, word in enumerate(words):
            word_length = len(word) + 1  # Add 1 for the space character
            cumulative_length += word_length

            if start_index is None and cumulative_length > start_pos:
                start_index = i

            if cumulative_length > end_pos:
                end_index = i
                break

        return start_index, end_index

  def convert_to_target(data):
        #### Is it easier for you : faster for you ???, OK, no pb
     
        lowercase_values = {
        'COURT': 'court',
        'PETITIONER': 'petitioner',
        'RESPONDENT': 'respondent',
        'JUDGE': 'judge',
        'LAWYER': 'lawyer',
        'DATE': 'date',
        'ORG': 'organization',
        'GPE': 'geopolitical entity',
        'STATUTE': 'statute',
        'PROVISION': 'provision',
        'PRECEDENT': 'precedent',
        'CASE_NUMBER': 'case_number',
        'WITNESS': 'witness',
        'OTHER_PERSON' : 'OTHER_PERSON'
        }

        targeted_format = []

        for value in data:
            tokenized_text = value['data']['text'].split(" ")      
            ner_tags = []

            for results in value["annotations"][0]['result']:
                ner_list = []
                start, end = find_indices_in_list(value['data']['text'], results['value']['start'],results['value']['end'])
                
                ner_list.append(start)
                ner_list.append(end)
                
                for label in results['value']['labels']:
                    ner_tags.append(ner_list + [lowercase_values[label]])

            targeted_format.append({"tokenized_text" : tokenized_text, "ner":ner_tags})

        return targeted_format

  with open(dirin,'r') as f:
      data = json.load(f)

  data = convert_to_target(data)

#   cfg = config_load(cfg)
#   df = pd_read_file(dirin)
  #df["tokenized_text"] = df["text"].apply(lambda x: x.split())
  # 
#   data= df[[ "tokenized_text", "ner"]].to_json(dirout, orient="records")
  log(str(data)[:100])
  json_save(data, dirout)



##########################################################################################################
def run_train_v2(cfg:dict=None, cfg_name:str=None, dirout:str="ztmp/exp", 
              model_name:str="urchade/gliner_small",
              dirdata=r"D:/github/myutil/utilmy/webapi/asearch/ddata/Legal_NER_Dataset.json"):
  """A function to train a model using specified configuration and data.
  Parameters:
      cfg (dict): Configuration dictionary (default is None).
      dirout (str): Output directory path (default is None).
      model_name (str): Name of model to use (default is "urchade/gliner_small").
      dirdata (str): Directory path of data to use (default is "data/sample_data.json").

  Returns:
      None
  """
  dt      = date_now(fmt="%Y%m%d/%H%M%S")
  device  = "cpu"
  dirout2 = f"{dirout}/{dt}"


  cfg    = config_load(cfg)
  config = cfg.get(cfg_name, None) if isinstance(cfg, dict) else None
  if config is None:
    config = CONFIG_DEFAULT
    nsteps = 2
    config.num_steps      = nsteps
    config.save_directory = dirout2
    config.eval_every     = nsteps // 2
    config.device         = device
    

  #### evaluation only support fix entity types (but can be easily extended)
  data  = json_load(dirdata)
  eval_data = {
      "entity_types": ['court', 'petitioner', 'respondent', 'judge', 'lawyer', 'date', 'organization', 'geopolitical entity', 'statute', 'provision', 'precedent', 'case_number', 'witness', 'OTHER_PERSON'],
      "samples": data[:10]
  }


  log("##### Model Load", model_name)
  #### available models: https://huggingface.co/urchade
  model = GLiNER.from_pretrained(model_name)


  log("##### Train start")
  train(model, config, data, eval_data)

  dirfinal = f"{dirout2}/final/"
  log("##### Model Save", dirfinal)
  os_makedirs(dirfinal) 
  model.save_pretrained( dirfinal)







###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()






""" 
#### All results
    You need to Copy ALL the outputs, always
    ---> its easier, faster. Faster is best, Simple is best, Fast and efficient: OK ?
    COPY PASTE evetything here, every time.



    ### Run fine tunning
    cd asearch/nlp  
    python3 ./ner_gliner.py  run_train_v2 --dirdata  "./ztmp/data/Legal_NER_Dataset.json"  --dirout "./ztmp/models/gliner/small"

    
    ### Output   
        Config: Using default config
        {'field1': 'test', 'field2': {'version': '1.0'}}
        ##### Model Load urchade/gliner_small
        ##### Train start
        ###### training Start Epoch...
        step: 0 | epoch: 0 | loss: 12.55
        Step=0
        P: 15.79%       R: 23.08%       F1: 18.75%

        step: 1 | epoch: 0 | loss: 5.64
        Step=1
        P: 17.65%       R: 23.08%       F1: 20.00%


        ## rename your train to run_train_v2
                rename the function to _v2
                  --> easy and simple, ok ?
          Do not delete my code OK N??????????

        Your file has issue your re-write my original code,
        THATS BAD

        you should copy and rename the function, OK ?

        Let arrange the file now.
         let add your code in my repo and push it

         
                   

         
    ## Metrics F1 is 0.20 ( F1 is a bit low, now ?)
        Previous project: how much was your F1 level :  0.61

        which model ? best score by using GRU with Glove. F1 level: 0




        





        
    

"""





##########################################################################################################
def zzzz_data_to_json(cfg=None, dirin="ztmp/data.csv", dirout="ztmp/data/ner/sample_data.json"):
  """ Convert data to json 
  Input : csv or parquet file


  
  """
  cfg = config_load(cfg)
  df  = pd_read_file(dirin)

  data= df[[ "tokenized_text", "ner"]].to_json(dirout, orient="records")
  log(str(data)[:100])
  json_save(data, dirout)

