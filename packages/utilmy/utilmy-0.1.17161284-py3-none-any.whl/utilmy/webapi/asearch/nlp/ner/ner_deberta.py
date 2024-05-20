# -*- coding: utf-8 -*-
"""NER Deberta

   ### Install
    https://colab.research.google.com/drive/1x-LlluSePdD1ekyItadNNQuvlOc65Qpz

    !pip install utilmy fire python-box

    !pip install -q -U bitsandbytes peft accelerate  transformers==4.37.2
    !pip install datasets transformers fastembed simsimd
    !pip install -q seqeval


   ### Dataset Download
    cd ./ztmp/
    git clone https://github.com/arita37/data2.git   data
    cd data
    git checkout text
    cd ../../

       #### Dataset
       ls ./ztmp/data/data/ner_geo/


   ### Input dataset:
        REQUIRED_SCHEMA_GLOBAL_v1 = [
            ("text_id",  "int64", "global unique ID for   text"),

            ("text", "str", " Core text "),

            ("ner_list", "list", " List of triplets (str_idx_start, str_idx_end, ner_tag) "),
                 str_idx_start : index start of tag inside   String.
                 str_idx_end:    index start of tag inside   String.
            ]



        OPTIONAL_SCHEMA_GLOBAL_v1 = [
            ("text_id",  "int64", "global unique ID for   text"),
            ("text_id2", "int64", "text_id from original dataset"),

            ("dataset_id",  "str",   "URL of   dataset"),
            ("dataset_cat", "str",   "Category tags : english/news/"),

            ("dt", "float64", "Unix timestamps"),

            ("title", "str", " Title "),
            ("summary", "str", " Summary "),
            ("info_json", "str", " Extra info in JSON string format "),


            ("cat1", "str", " Category 1 or label "),
            ("cat2", "str", " Category 2 or label "),
            ("cat3", "str", " Category 3 or label "),
            ("cat4", "str", " Category 4 or label "),
            ("cat5", "str", " Category 5 or label "),

        ]






"""

if "Import":
    import time,  json,re, os, pandas as pd, numpy as np,copy
    from dataclasses import dataclass
    from typing import Optional, Union
    from box import Box


    import datasets 
    from datasets import load_dataset, Dataset, load_metric
    # If issue dataset: please restart session and run cell again
    from transformers import (
        BitsAndBytesConfig,
        GenerationConfig,
        HfArgumentParser,
        TrainingArguments,
        Trainer,

        AutoTokenizer,
        AutoModelForSeq2SeqLM,
        AutoModelForMultipleChoice,        
        AutoModelForTokenClassification,DataCollatorForTokenClassification, #### NER Tasks

        ### LLM
        AutoModelForCausalLM,
        PhiForCausalLM,

    )
    # from transformers.models.qwen2.modeling_qwen2 import
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy
    from seqeval.metrics import f1_score, precision_score, recall_score, classification_report

    import spacy, torch
    from pylab import cm, matplotlib

    from utilmy import (date_now, date_now, pd_to_file,log,pd_read_file, os_makedirs,
                        glob_glob, json_save, json_load, config_load
    )



####################################################################################
####### Custom dataset XXX #########################################################
global NCLASS, L2I, i2l
NCLASS =0
L2I={}
i2l={}

def  dataXX_load_prepro():
    """ 
    Sample data:

            query	answer	answerfull	answer_fmt
        0	find kindergarten and tech startup in Crack...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Cracker Barrel Old Cou...
        1	This afternoon, I have an appointment to Mitsu...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Mitsuwa Marketplace',c...
        2	find train and embassy near by Brooklyn Bri...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Brooklyn Bridge Park S...
        3	This afternoon, I have an appointment to Nowhe...	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Nowhere',city='New Yor...
        4	This afternoon, I have an appointment to Wawa....	b'{"name":"search_places","args":{"place_name"...	b'{"name":"search_places","args":{"place_name"...	search_places(location='Wawa',country='US',loc...


    """
    dirout0='./ztmp/out/ner_geo'
    dt = date_now(fmt="%Y%m%d_%H%M%S")
    dirout= os.path.join(dirout0, dt)
    os.makedirs(dirout)


    ##### Load Data #################################################
    #cd ./ztmp/
    #git clone https://github.com/arita37/data2.git   data
    #cd data
    #git checkout text
    dirtrain = "./ztmp/data/data/ner_geo/df_10000_1521.parquet"
    dirtest  = "./ztmp/data/data/ner_geo/df_1000.parquet"

    df        = pd_read_file(dirtrain)#.sample(2000)
    log(df)
    df_test   = pd_read_file(dirtest)#.head(100)
    log(df_test)

    cols0 = [ "query",	"answer",	"answerfull",	"answer_fmt"]
    assert df[cols0].shape
    assert df_test[cols0].shape

    colsmap= {"query": "text",}
    df      = df.rename(columns= colsmap)
    df_test = df.rename(columns= colsmap)


    #### Data Enhancement ##########################################
    ex= []
    for i in range(200):
        r = df.sample(1).iloc[0].to_dict()
        query = r["text"]
        s = np.random.randint(len(query))
        if np.random.random()>0.5:
            query = query + f', around {s}km. '
        else:
            query = f'around {s} km. ' + query
        r["text"] = query
        ex.append(r)

    # query = query + ", around 8km."
    df  = pd.concat([df, pd.DataFrame(ex)])

    df["ner_list"]      = df.apply(dataXX_fun_prepro_text_predict, axis=1)
    df_test["ner_list"] = df_test.apply(dataXX_fun_prepro_text_predict, axis=1)
    log( df.head() )
    log( df_test.sample(1).to_dict())


   ################################################################ 
   ###### External validation ##################################### 
    ner_model_input_validate_columns(df)
    ner_model_input_validate_columns(df_test)

    return df, df_test


def dataXX_fun_prepro_text_predict(row):
    """
       # Location, address, city, country, location_type, type_exclude
       # Location_type=\[(.*?)\],location_type_exclude=\[(.*?)\]

    """
    text  = row['answer_fmt']
    query = row["text"]
    # location = re.findall(r"location='(.*?)'", p[0])
    pattern = r"location='(.*?)',"
    matches = re.findall(pattern, text)
    values = []
    if len(matches):
        assert len(matches) == 1, matches
        values.append(
            {
                'type':'location',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )

    pattern = r"city='(.*?)',"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        values.append(
            {
                'type':'city',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )
    pattern = r"country='(.*?)',"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches

        values.append(
            {
                'type':'country',
                'value': matches[0],
                'start': query.index(matches[0]),
                'end' : query.index(matches[0]) + len(matches[0])
            }
        )

    pattern = r"location_type=\[(.*?)\]"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        if len(matches[0].strip()):
            for i in matches[0].split(","):
                x = i.strip()
                if x[0] == "'" and x[-1] == "'":
                    x=x[1:-1]
                if x not in query:
                    print(x, query)
                values.append(
                    {
                        'type':'location_type',
                        'value': x,
                        'start': query.index(x),
                        'end' : query.index(x) + len(x)
                    }
                )

    pattern = r"location_type_exclude=\[(.*?)\]"
    matches = re.findall(pattern, text)
    if len(matches):
        assert len(matches) == 1, matches
        if len(matches[0].strip()):
            for i in matches[0].split(","):
                x = i.strip()
                if x[0] == "'" and x[-1] == "'":
                    x=x[1:-1]
                values.append(
                    {
                    'type':'location_type_exclude',
                    'value': x,

                    'start': query.index(x),
                    'end' : query.index(x) + len(x)
                    }
                )
    return values


def dataXX_fun_extract_from_answer_full(row):
    """  
        #             address': '4700 Gilbert Ave',
        #    'city': 'Chicago',
        #    'country': 'United States',
        #    'location_type': 'hot dog stand and viewpoint',
        #    'location_type_exclude': [],
        #     query = row["text"]

    """
    dict_i4 = json.loads(row['answerfull'])['args']
    query = row["text"]
    values =[]
    for key, value in dict_i4.items():
        if key=='place_name':
            key='location'
        if key =='radius' or key=='navigation_style':continue
        if key =='location_type':
            value = value.split("and")
            value = [i.strip() for i in value]
            values.extend([{
                'type':key,
                'value': i,
                'start': query.index(i),
                'end': query.index(i) + len(i)
            } for i in value])
        elif key =='location_type_exclude':
            if isinstance(value, str):
                value = value.split("and")
                value = [i.strip() for i in value]
                values.extend([{
                    'type':key,
                    'value': i,
                    'start': query.index(i),
                    'end': query.index(i) + len(i)
                } for i in value])
            else:
                assert len(value) == 0
        else:
            if value.strip() not in query:
                print(value, 'x', query, 'x', key)
            values.append(
                {
                    'type': key,
                    'value': value.strip(),
                    'start': query.index(value.strip()),
                    'end': query.index(value.strip()) + len(value.strip())
                }
            )
    return values


def dataXX_create_label_mapper():
    
    global NCLASS, L2I, i2L
    NCLASS=5

    L2I = {
    }
    for index, c in enumerate(['location', 'city', 'country', 'location_type', 'location_type_exclude']):
        L2I[f'B-{c}'] = index
        L2I[f'I-{c}'] = index + NCLASS
    L2I['O'] = NCLASS*2
    L2I['Special'] = -100
    L2I

    i2l = {}
    for k, v in L2I.items():
        i2l[v] = k
    i2l[-100] = 'Special'

    i2l = dict(i2l)
    log(i2l)

    return L2I, i2l, NCLASS



################################################################################
########## Custom dataset XXX Eval  #############################################
def dataXX_predict_generate_text_fromtags(dfpred, dirout="./ztmp/metrics/"):
    """  Generate text from TAGS

    """
    if isinstance(dfpred, str):
       dfpred= pd_read_file(dfpred)
    assert dfpred[[ "ner_list", "pred_ner_list"  ]].shape


    def create_answer_from_tag(tag):
      # name=f'location={}'
      tag=sorted(tag, key=lambda x:x['start'])
      final_answer = ""
      list_location_type = []
      list_location_exclude = []
      for t in tag:
        text  =t.get('text') if 'text' in t else t.get("value")

        if t['type']not in ['location_type', 'location_type_exclude']:
          key = t['type']
          final_answer += f'{key}={text}\n'

        elif t['type'] == 'location_type':
          list_location_type.append(text)

        elif t['type'] == 'location_type_exclude':
          list_location_exclude.append(text)

      if len(list_location_type):
        text = " and ".join(list_location_type)
        final_answer += f'location_type={text}\n'

      if len(list_location_exclude):
        text = " and ".join(list_location_exclude)
        final_answer += f'list_location_exclude={text}\n'
      return final_answer

    #####  Generate nornalized answer from tag
    dfpred['text_true_str'] = dfpred["ner_list"].apply(create_answer_from_tag)
    dfpred['text_pred_str'] = dfpred["pred_ner_list"].apply(create_answer_from_tag)

    pd_to_file(dfpred, dirout + '/dfpred_text_generated.parquet', show=1)



def dataXX_fun_answer_clean(ss:str):
  ss = ss.replace("search_places(", "")
  return ss













####################################################################################
####### Google colab ###############################################################
def init_googledrive(shortcut="phi2"):
    import os
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir(f"/content/drive/MyDrive/{shortcut}/")
    # ! ls .
    #! pwd
    #! ls ./traindata/
    #ls




########################################################################################
##################### Tokenizer helper ################################################
def token_fix_beginnings(labels):
    """Fix   beginning of a list of labels by adjusting   labels based on certain conditions.
    Args:
        labels (list): A list of labels.        
    # tokenize and add labels    
    """
    for i in range(1,len(labels)):
        curr_lab = labels[i]
        prev_lab = labels[i-1]
        if curr_lab in range(NCLASS,NCLASS*2):
            if prev_lab != curr_lab and prev_lab != curr_lab - NCLASS:
                labels[i] = curr_lab -NCLASS
    return labels



def tokenize_and_align_labels(examples:dict, tokenizer,  L2I:dict):
    """Tokenizes  given examples and aligns  labels.
    Args:
        examples (dict): A dictionary containing  examples to be tokenized and labeled.
            - "text" (str):  query string to be tokenized.
            - "ner_list" (list): A list of dictionaries representing  entity tags.
                Each dictionary should have  following keys:
                - 'start' (int):  start position of  entity tag.
                - 'end' (int):  end position of  entity tag.
                - 'type' (str):  type of  entity tag.

    Returns:
        dict: A dictionary containing  tokenized and labeled examples.
            It has  following keys:
            - 'input_ids' (list): A list of input ids.
            - 'attention_mask' (list): A list of attention masks.
            - 'labels' (list): A list of labels.
            - 'token_type_ids' (list, optional): A list of token type ids. Only present if 'token_type_ids' is present in  input dictionary.
    """

    o = tokenizer(examples["text"],
                  return_offsets_mapping=True,
                  return_overflowing_tokens=True)
    offset_mapping = o["offset_mapping"]
    o["labels"] = []
    for i in range(len(offset_mapping)):
        labels = [L2I['O'] for i in range(len(o['input_ids'][i]))]
        for tag in examples["ner_list"]:
            label_start = tag['start']
            label_end = tag['end']
            label = tag['type']
            for j in range(len(labels)):
                token_start = offset_mapping[i][j][0]
                token_end = offset_mapping[i][j][1]
                if token_start == label_start:
                    labels[j] = L2I[f'B-{label}']
                if token_start > label_start and token_end <= label_end:
                    labels[j] = L2I[f'I-{label}']

        for k, input_id in enumerate(o['input_ids'][i]):
            if input_id in [0,1,2]:
                labels[k] = -100

        labels = token_fix_beginnings(labels)

        o["labels"].append(labels)

    o['labels']         = o['labels'][0]
    o['input_ids']      = o['input_ids'][0]
    o['attention_mask'] = o['attention_mask'][0]
    if 'token_type_ids' in o:o['token_type_ids'] = o['token_type_ids'][0]
    return o



@dataclass
class DataCollatorForLLM:
    tokenizer         : PreTrainedTokenizerBase
    padding           : Union[bool, str, PaddingStrategy] = True
    max_length        : Optional[int] = None
    pad_to_multiple_of: Optional[int] = None

    def __call__(self, features):
        label_name        = 'label' if 'label' in features[0].keys() else 'labels'
        labels            = [feature.pop(label_name) for feature in features]
        max_length_labels = max([len(i) for i in labels])
        labels_pad        = np.zeros((len(labels), max_length_labels, )) + -100
        for index in range(len(labels)):
#             print(len(labels[index]), labels[index])
            labels_pad[index, : len(labels[index])] = labels[index]

        batch_size         = len(features)
        flattened_features = features
        batch = self.tokenizer.pad(
            flattened_features,
            padding            = self.padding,
            max_length         = self.max_length,
            pad_to_multiple_of = self.pad_to_multiple_of,
            return_tensors     = 'pt',
        )
        batch['labels'] = torch.from_numpy(labels_pad).long()

        return batch




#################################################################################
def metrics_calc(p,):
    global L2I, i2l

    metric = datasets.load_metric("seqeval")
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [i2l[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [i2l[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall"   : results["overall_recall"],
        "f1"       : results["overall_f1"],
        "accuracy" : results["overall_accuracy"],
    }




#################################################################################†
def ner_model_input_validate_columns(df):
    assert df[["text", "ner_list" ]].shape
    rowset = set(df[ "ner_list"].values[0][0].keys())
    assert rowset == {"start", "end", "type", "value"}, f"error {rowset}"


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



def run_train(cfg=None, cfg_name="ner_deberta", dirout="./ztmp/exp", istest=1):
    """ 
       python nlp/ner/ner_deberta.py run_train  --dirout ztmp/exp   --cfg config/traina/train1.yaml --cfg_name ner_deberta

    """
    global NCLASS, L2I, i2L    
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
        cc.model_name='microsoft/deberta-v3-base'

        #### Data name
        cc.dataloader_name = "dataXX_load_prepro"
        cc.datamapper_name = "dataXX_create_label_mapper"

        cc.n_train = n_train
        cc.n_val   = n_val

        #### Train Args
        aa = Box({})
        aa.output_dir                  = f"{dirout}/log_train"
        aa.per_device_train_batch_size = 64
        aa.gradient_accumulation_steps = 1
        aa.optim                       = "adamw_hf"
        aa.save_steps                  = min(100, cc.n_train-1)
        aa.logging_steps               = min(50,  cc.n_train-1)
        aa.learning_rate               = 1e-5
        aa.max_grad_norm               = 2
        aa.max_steps                   = -1
        aa.num_train_epochs                  = 2
        aa.warmup_ratio                = 0.2 # 20%  total step warm-up
        # lr_schedulere_type='constant'
        aa.evaluation_strategy = "epoch"
        aa.logging_strategy    = "epoch"
        aa.save_strategy       = "epoch"

        cc.hf_args_train = copy.deepcopy(aa)

        ### HF model
        cc.hf_args_model_init = {}
        cc.hf_args_model_init.model_name = cc.model_name
        cc.hf_args_model_init.num_labels = NCLASS*2+1 ## due to BOI notation

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

    df, df_val       = dataloader_fun()  ## = dataXX_load_prepro()
    L2I, i2L, NCLASS = datamapper_fun()  ## Label to Index, Index to Label

    columns = df.columns.tolist()
    df, df_val = df.iloc[:cc.n_train], df_val.iloc[:cc.n_val]


    cc.data ={}
    cc.data.cols          = columns
    cc.data.cols_required = ["text", "ner_list" ]
    cc.data.ner_format    = ["start", "end", "type", "value"]  
    cc.data.cols_remove   = ['overflow_to_sample_mapping', 'offset_mapping', ] + columns
    cc.data.L2I           = L2I     ### label to Index Dict
    cc.data.i2l           = i2l     ### Index to Label Dict
    cc.data.nclass        = NCLASS  ### Number of NER Classes.

    ner_model_input_validate_columns(df)
    ner_model_input_validate_columns(df_val)    


    ################# Generic Code ###########################################  
    log("###### Dataloader setup  ############################################")
    tokenizer = AutoTokenizer.from_pretrained(cc.model_name)

    assert set(df[ "ner_list"].values[0][0].keys()) == {"start", "end", "type", "value"}
    ds_train = Dataset.from_pandas(df)
    ds_train = ds_train.map(tokenize_and_align_labels, fn_kwargs={'tokenizer': tokenizer, "L2I": L2I})
    dataset_train = ds_train.remove_columns(['overflow_to_sample_mapping', 'offset_mapping', ] + columns)


    assert set(df_val[ "ner_list"].values[0][0].keys()) == {"start", "end", "type", "value"}
    ds_valid   = Dataset.from_pandas(df_val)
    ds_valid   = ds_valid.map(tokenize_and_align_labels, fn_kwargs={'tokenizer': tokenizer, "L2I": L2I})
    dataset_valid = ds_valid.remove_columns(['overflow_to_sample_mapping', 'offset_mapping',]+ columns)


    batch = DataCollatorForLLM(tokenizer)([dataset_train[0], dataset_train[1]])
    log(dataset_valid[0])
    log(batch)


    log("######### Model : Init #########################################")
    model = AutoModelForTokenClassification.from_pretrained(cc.model_name, num_labels=NCLASS*2+1)


    # for i in model.deberta.parameters():
    #   i.requires_grad=False

    log("######### Model : Training start ##############################")
    tokenizer.pad_token = tokenizer.eos_token

    trainer = Trainer(model, args,
        train_dataset= dataset_train,
        eval_dataset = dataset_valid,
        data_collator= DataCollatorForLLM(tokenizer),
        tokenizer    = tokenizer,
        compute_metrics=metrics_calc,
    )

    json_save(cc, f'{dirout}/config.json')
    trainer_output=trainer.train()
    log(trainer_output)

    cc['metrics_trainer'] = trainer_output.metrics
    json_save(cc, f'{dirout}/config.json')


    log("######### Model : Eval #########################################")
    preds_proba, labels, _ = trainer.predict(dataset_valid)
    preds_class            = np.argmax(preds_proba, axis=-1)

    df_val['preds_proba']  = preds_proba
    df_val['preds_class']  = preds_class
    df_val['ner_list_pred']     = df_val['preds_class'].apply(lambda x : x)   

    # df_val['preds_labels'] = labels
    
    assert df[[ "text", "ner_list", "pred_ner_list"     ]].shape
    log( metrics_ner_accuracy(df_val["ner_list"].iloc[0], df_val["preds_class"].iloc[0]) )    
    df_val['accuracy'] = df_val.apply(lambda x: metrics_ner_accuracy(x["ner_list"], 
                                                                     x['pred_ner_list']),axis=1 )

    pd_to_file(df_val, f'{dirout}/dfval_pred_ner.parquet', show=1)  



def run_text_generator_from_tag(dirin, dirout):
    #### Generate answer/text from TAG
    pass 





################################################################################
########## Eval with Visualization Truth   #####################################
def ner_text_visualize(row:dict, title='visualize_model-predicted', ner_refs:list=None, ner_colors_dict:list=None,
                       jupyter=True):
    """Visualizes   named entity recognition results for a given text row.
    Args:
        row (dict):  text row to visualize.
        title (str, optional):  title of   visualization. Defaults to 'visualize_model-predicted'.
        ner_refs (list, optional): A list of entity references to include in   visualization. Defaults to None.
        ner_colors_dict (dict, optional): A dictionary mapping entity references to colors. Defaults to None.
        jupyter (bool, optional): Flag indicating whether   visualization is being rendered in Jupyter Notebook. Defaults to True.

    """
    if ner_colors_dict is None:
        ner_colors_dict = {
                'location': '#8000ff',
                'city': '#2b7ff6',
                'country': '#2adddd',
                'location_type': '#80ffb4',
                'location_type_exclude': 'd4dd80',
                'Other': '#007f00',
        }

    if ner_refs is None:
       # ner_refs = ['location', 'city', 'country', 'location_type', 'location_type_exclude'] + ['Other']
       ner_refs = [ key for key in ner_colors_dict.keys() ]

    text = row["text"]
    tags = row["ner_list"]
    ents = [{'start': k['start'], 'end': k['end'], 'label': k['type']} for k in tags if k['type'] !='Other']

    doc2 = {
        "text": text,
        "ents": ents,
        "title": title
    }

    options = {"ents": ner_refs, "colors": ner_colors_dict}
    spacy.displacy.render(doc2, style="ent", options=options, manual=True, jupyter=jupyter)


def eval_visualize_tag(dfpred=Union[str, pd.DataFrame], dirout="./ztmp/metrics/", ner_colors_dict=None):
    """ Visualizes   predicted tags for a given dataset of NER tasks.

    python nlp/ner_deberta.py --dfpred "./ztmp/exp/ner_train/dfpred_ner.parquet"    --dirout "./ztmp/exp/ner_train/"

    dfpred[[ "pred_class", "input_ids", "offset_mapping", "text"  ]]

    Args:
        dfpred (Union[str, pd.DataFrame]):   path to   CSV file containing   predicted tags or a Pandas DataFrame with   predicted tags. Default is None.
        dirout (str):   directory where   output file will be saved. Default is './ztmp/metrics/'.
        ner_colors_dict (dict): A dictionary mapping entity types to colors. Default is None.

    """ 
    if isinstance(dfpred, str):
        dfpred = pd_read_file(dfpred)

    assert dfpred[[ "text", "input_ids", "offset_mapping", "pred_ner_list"  ]]

    if ner_colors_dict is None:
        ner_colors_dict = {'location': '#8000ff',
                    'city': '#2b7ff6',
                    'country': '#2adddd',
                    'location_type': '#80ffb4',
                    'location_type_exclude': 'd4dd80',
                    'Other': '#007f00',}

    preds_class = dfpred['pred_ner_list'].values
    valid       = dfpred[[ "input_ids", "offset_mapping", "text"  ]].to_dict(orient="records")


    def get_class(c):
        if c == NCLASS*2: return 'Other'
        else: return i2l[c][2:]

    def pred2span(pred, example, viz=False, test=False):
        #     example_id = example['id']
        n_tokens = len(example['input_ids'])
        #     print(n_tokens, len(example['offset_mapping']))
        classes = []
        all_span = []
        for i, c in enumerate(pred.tolist()):
            if i == n_tokens-1:
                break
            if i == 0:
                cur_span = example['offset_mapping'][0][i]
                classes.append(get_class(c))
            elif i > 0 and (c == pred[i-1] or (c-NCLASS) == pred[i-1]):
                cur_span[1] = example['offset_mapping'][0][i][1]
            else:
                all_span.append(cur_span)
                cur_span = example['offset_mapping'][0][i]
                classes.append(get_class(c))
        all_span.append(cur_span)

        text = example["text"]

        # map token ids to word (whitespace) token ids
        predstrings = []
        for span in all_span:
            span_start  = span[0]
            span_end    = span[1]
            before      = text[:span_start]
            token_start = len(before.split())
            if len(before) == 0:    token_start = 0
            elif before[-1] != ' ': token_start -= 1

            num_tkns   = len(text[span_start:span_end+1].split())
            tkns       = [str(x) for x in range(token_start, token_start+num_tkns)]
            predstring = ' '.join(tkns)
            predstrings.append(predstring)

        row = {  "text": text, "ner_list": []}
        es = []
        for c, span, predstring in zip(classes, all_span, predstrings):
            if c!='Other':
              e = {
                'type': c,
                'predictionstring': predstring,
                'start': span[0],
                'end': span[1],
                'text': text[span[0]:span[1]]
              }
              es.append(e)
        row["ner_list"] = es

        if viz: ner_text_visualize(row)

        return row


    ##### Check Visulaize
    def ner_text_visualize2(x):
        return ner_text_visualize(x, title='ground-truth', ner_colors_dict=ner_colors_dict )

    ner_text_visualize2(valid[32])

    #### Check Values
    predicts= [pred2span(preds_class[i], valid[i], viz=False) for i in range(len(valid))]
    ner_text_visualize(predicts[0]   )
    ner_text_visualize(predicts[2]   )
    ner_text_visualize(predicts[12]  )
    ner_text_visualize(predicts[400] )
    ner_text_visualize(predicts[328] )

    predicts = pd.DataFrame(predicts)
    pd_to_file( predicts, dirout + '/predict_ner_visualize.parquet' )
    # pred = pd.read_csv("nguyen/20240215_171305/predict.csv")
    # pred
    # pred = pred[["text", "ner_list"]]
    # eval(pred.ner_tag.iloc[0])
    # pred["ner_list"] = pred["ner_list"].apply(eval)






################################################################################
########## Eval with embedding ground Truth  ###################################
def eval_check_with_embed(df_test, col1='gt_answer_str', col2='predict_answer_str',  dirout="./ztmp/metrics/"):
    """Evaluate   performance of a model using embeddings for ground truth and predictions.

    Args:
        df_test (pandas.DataFrame or str):   test dataset to evaluate. If a string is provided, it is assumed to be a file path and   dataset is loaded from that file.
        col1 (str, optional):   name of   column containing   ground truth answers. Defaults to 'gt_answer_str'.
        col2 (str, optional):   name of   column containing   predicted answers. Defaults to 'predict_answer_str'.
        dirout (str, optional):   directory to save   evaluation metrics. Defaults to './ztmp/metrics/'.
    """

    df_test = pd_add_embed(df_test, col1, col2, add_similarity=1, colsim ='sim')

    log( df_test['sim'].describe())
    log( df_test[[col1, col2]].sample(1))

    pd_to_file( df_test[["text", col1, col2, 'sim']],
                f'{dirout}/predict_sim_cosine.parquet') 

    cc = Box({})
    cc['metric_sim'] = df_test['sim'].describe().to_dict()
    json_save(cc, f"{dirout}/metrics_sim_cosine.json")



def metrics_ner_accuracy(tags:list, preds:list):
    """Calculate   accuracy metric for named entity recognition (NER) task.
    Args:
        tags (List[Dict]): List of dictionaries representing   ground truth tags.
                            contains   'start' index, 'value', and 'type' of a tag.

        preds (List[Dict]): List of dictionaries representing   predicted tags.
                            contains   'start' index, 'text', and 'type' of a tag.

    Returns:
        Dict: Dictionary containing   accuracy metric for each tag type

    """
    tags  = sorted(tags, key=lambda x:x['start'])
    preds = sorted(preds, key=lambda x:x['start'])
    acc = {}
    acc_count = {}
    for tag in tags:
        value    = tag['value']
        tag_type = tag['type']

        if tag_type not in acc:
            acc[tag_type] = 0
            acc_count[tag_type] = 0

        acc_count[tag_type] += 1

        for p in preds:
           if p['type'] == tag_type and p['text'].strip() == value.strip():

              acc[tag_type]+= 1

    total_acc = sum(acc.values()) / sum(acc_count.values())
    acc       = {tag: v/acc_count[tag] for tag, v in acc.items() }

    acc['total_acc'] = total_acc
    return acc


def qdrant_embed(wordlist:list[str], model_name="BAAI/bge-small-en-v1.5", size=128, model=None):
    """ pip install fastembed

    Docs:

         BAAI/bge-small-en-v1.5 384   0.13
         BAAI/bge-base-en       768   0.14
         sentence-transformers/all-MiniLM-L6-v2   0.09

        ll= list( qdrant_embed(['ik', 'ok']))


        ### https://qdrant.github.io/fastembed/examples/Supported_Models/
        from fastembed import TextEmbedding
        import pandas as pd
        pd.set_option("display.max_colwidth", None)
        pd.DataFrame(TextEmbedding.list_supported_models())


    """
    from fastembed.embedding import FlagEmbedding as Embedding

    if model is None:
       model = Embedding(model_name= model_name, max_length= 512)

    vectorlist = model.embed(wordlist)
    return np.array([i for i in vectorlist])


def sim_cosinus_fast(v1:list, v2:list)-> float :
   ### %timeit sim_cosinus_fast(ll[0], ll[1])  0.3 microSec
   import simsimd
   dist = simsimd.cosine(v1, v2)
   return dist


def sim_cosinus_fast_list(v1:list[list], v2:list[list])-> list[float] :
   ### %timeit sim_cosinus_fast(ll[0], ll[1])  0.3 microSec
   import simsimd
   vdist = []
   for x1,x2 in zip(v1, v2):
       dist = simsimd.cosine(x1, x2)
       vdist.append(dist)
   return vdist


def pd_add_embed(df, col1:str="col_text1", col2:str="col_text2", size_embed=128, add_similarity=1, colsim=None):
    """
    df=  pd_add_embed(df, 'answer', 'answerfull', add_similarity=1)
    df['sim_answer_answerfull'].head(1)


    """
    v1 = qdrant_embed(df[col1].values)
    #     return v1
    df[col1 + "_vec"] = list(v1)

    #    if col2 in df.columns:
    v1 = qdrant_embed(df[col2].values)
    df[col2 + "_vec"] = list(v1)

    if add_similarity>0:
      colsim2 = colsim if colsim is not None else f'sim_{col1}_{col2}'
      vdist   = sim_cosinus_fast_list(df[col1 + "_vec"].values, df[col2 + "_vec"].values)
      df[ colsim2 ] = vdist
    return df


def  pd_add_sim_fuzzy_score(df:pd.DataFrame, col1='answer_fmt', col2='answer_pred_clean'):
  # pip install rapidfuzz
  from rapidfuzz import fuzz
  df['dist2'] = df[[col1, col2]].apply(lambda x: fuzz.ratio( x[col1], x[col2]), axis=1)
  return df




###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




""" 

(py39) \W$        python nlp/ner/ner_deberta.py run_train  --dirout ztmp/exp 
###### Config Load   #############################################
Config: Using /Users/macair/conda3/envs/py39/lib/python3.9/site-packages/utilmy/configs/myconfig/config.yaml
Config: Loading  /Users/macair/conda3/envs/py39/lib/python3.9/site-packages/utilmy/configs/myconfig/config.yaml
Config: Cannot read file /Users/macair/conda3/envs/py39/lib/python3.9/site-packages/utilmy/configs/myconfig/config.yaml 'str' object has no attribute 'suffix'
Config: Using default config
{'field1': 'test', 'field2': {'version': '1.0'}}
###### User Params   #############################################
######### Model : Training params ##############################
###### User Data Load   #############################################
                                                  answer  ...                                              query
0      b'{"name":"search_places","args":{"place_name"...  ...  find  kindergarten and tech startup  in  Crack...
1      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Mitsu...
2      b'{"name":"search_places","args":{"place_name"...  ...  find  train and embassy  near by  Brooklyn Bri...
3      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Nowhe...
4      b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Wawa....
...                                                  ...  ...                                                ...
9997   b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. show me  fashion ...
9998   b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Fort Lauderdale. ...
9999   b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Naples. search  portuguese re...
10000  b'{"name":"search_places","args":{"place_name"...  ...  list some   indoor cycling and speakeasy  arou...
10001  b'{"name":"search_places","args":{"place_name"...  ...  find  fabric store and driving range  in  Hors...

[10002 rows x 4 columns]
                                                 answer  ...                                              query
0     b'{"name":"search_places","args":{"place_name"...  ...  This afternoon, I have an appointment to Barde...
1     b'{"name":"search_places","args":{"place_name"...  ...  provide  college and alternative healthcare  n...
2     b'{"name":"search_places","args":{"place_name"...  ...  list some   mountain and public artwork  near ...
3     b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. what are     te...
4     b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Naples. give me  rest area an...
...                                                 ...  ...                                                ...
996   b'{"name":"search_places","args":{"place_name"...  ...  provide  miniature golf and field  at  Apni Ma...
997   b'{"name":"search_places","args":{"place_name"...  ...  Next week, I am going to US. what are     ba...
998   b'{"name":"search_places","args":{"place_name"...  ...   I need to visit Fort Snelling.  provide  medi...
999   b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Houston.  find  t...
1000  b'{"name":"search_places","args":{"place_name"...  ...  Tomorrow, I am travelling to Madison. provide ...

[1001 rows x 4 columns]
                                              answer  ...                                           ner_list
0  b'{"name":"search_places","args":{"place_name"...  ...  [{'type': 'location', 'value': 'Cracker Barrel...
1  b'{"name":"search_places","args":{"place_name"...  ...  [{'type': 'location', 'value': 'Mitsuwa Market...
2  b'{"name":"search_places","args":{"place_name"...  ...  [{'type': 'location', 'value': 'Brooklyn Bridg...
3  b'{"name":"search_places","args":{"place_name"...  ...  [{'type': 'location', 'value': 'Nowhere', 'sta...
4  b'{"name":"search_places","args":{"place_name"...  ...  [{'type': 'location', 'value': 'Wawa', 'start'...

[5 rows x 5 columns]
{'answer': {9431: b'{"name":"search_places","args":{"place_name":"","address":"","city":"Los Angeles","country":"","location_type":"temple and island","location_type_exclude":[],"radius":"","navigation_style":""}}'}, 'answer_fmt': {9431: "search_places(city='Los Angeles',location_type=['temple', 'island'],location_type_exclude=[])"}, 'answerfull': {9431: b'{"name":"search_places","args":{"place_name":"R\xc5\xbdpublique Caf\xc5\xbd Bakery & R\xc5\xbdpublique Restaurant","address":"624 S La Brea Ave","city":"Los Angeles","country":"US","location_type":"temple and island","location_type_exclude":[],"radius":2,"navigation_style":"driving"}}'}, 'text': {9431: 'list some   temple and island  near  Los Angeles.'}, 'ner_list': {9431: [{'type': 'city', 'value': 'Los Angeles', 'start': 37, 'end': 48}, {'type': 'location_type', 'value': 'temple', 'start': 12, 'end': 18}, {'type': 'location_type', 'value': 'island', 'start': 23, 'end': 29}]}}
{0: 'B-location', 5: 'I-location', 1: 'B-city', 6: 'I-city', 2: 'B-country', 7: 'I-country', 3: 'B-location_type', 8: 'I-location_type', 4: 'B-location_type_exclude', 9: 'I-location_type_exclude', 10: 'O', -100: 'Special'}
###### Dataloader setup  ############################################
/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/convert_slow_tokenizer.py:550: UserWarning:   sentencepiece tokenizer that you are converting to a fast tokenizer uses   byte fallback option which is not implemented in   fast tokenizers. In practice this means that   fast version of   tokenizer can produce unknown tokens whereas   sentencepiece version would have converted these unknown tokens into a sequence of byte tokens matching   original piece of text.
  warnings.warn(
Map: 100%|████████████████████████████████████| 20/20 [00:00<00:00, 715.56 examples/s]
Map: 100%|██████████████████████████████████████| 5/5 [00:00<00:00, 995.42 examples/s]
You're using a DebertaV2TokenizerFast tokenizer. Please note that with a fast tokenizer, using   `__call__` method is faster than using a method to encode   text followed by a call to   `pad` method to get a padded encoding.
{'input_ids': [1, 433, 14047, 263, 3539, 7647, 267, 56693, 24057, 2951, 4631, 4089, 80872, 260, 2], 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'labels': [-100, 10, 10, 10, 10, 3, 10, 10, 0, 5, 5, 5, 10, 10, -100]}
{'__index_level_0__': tensor([0, 1]), 'input_ids': tensor([[    1,   433, 14047,   263,  3539,  7647,   267, 56693, 24057,  2951,
          4631,  4089, 80872,   260,     2,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0],
        [    1,   329,  2438,   261,   273,   286,   299,  3198,   264, 63526,
          6608, 21289,   260,   350, 26026,   263,  4526,   441, 63526,  6608,
         21289,   267,   846,   260,     2]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1]]), 'labels': tensor([[-100,   10,   10,   10,   10,    3,   10,   10,    0,    5,    5,    5,
           10,   10, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100,
         -100],
        [-100,   10,   10,   10,   10,   10,   10,   10,   10,   10,    0,    5,
           10,   10,   10,   10,   10,   10,   10,   10,   10,   10,   10,   10,
         -100]])}
######### Model : Init #########################################
/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/torch/_utils.py:831: UserWarning: TypedStorage is deprecated. It will be removed in   future and UntypedStorage will be   only storage class. This should only matter to you if you are using storages directly.  To access UntypedStorage directly, use tensor.untyped_storage() instead of tensor.storage()
  return self.fget.__get__(instance, owner)()
Some weights of DebertaV2ForTokenClassification were not initialized from   model checkpoint at microsoft/deberta-v3-base and are newly initialized: ['classifier.bias', 'classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
######### Model : Training start ##############################
/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/accelerate/accelerator.py:436: FutureWarning: Passing   following arguments to `Accelerator` is deprecated and will be removed in version 1.0 of Accelerate: dict_keys(['dispatch_batches', 'split_batches', 'even_batches', 'use_seedable_sampler']). Please pass an `accelerate.DataLoaderConfiguration` instead: 
dataloader_config = DataLoaderConfiguration(dispatch_batches=None, split_batches=False, even_batches=True, use_seedable_sampler=True)
  warnings.warn(
/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/optimization.py:457: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use   PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
{'loss': 1.6418, 'grad_norm': 15.783073425292969, 'learning_rate': 1e-05, 'epoch': 1.0}
 50%|█████████████████████████▌                         | 1/2 [00:08<00:08,  8.61s/it/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py:540: FutureWarning: load_metric is deprecated and will be removed in   next major version of datasets. Use 'evaluate.load' instead, from   new library 🤗 Evaluate: https://huggingface.co/docs/evaluate
  metric = datasets.load_metric("seqeval")
Traceback (most recent call last):
  File "/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py", line 1038, in <module>
    fire.Fire()
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/fire/core.py", line 143, in Fire
    component_trace = _Fire(component, args, parsed_flag_args, context, name)
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/fire/core.py", line 477, in _Fire
    component, remaining_args = _CallAndUpdateTrace(
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/fire/core.py", line 693, in _CallAndUpdateTrace
    component = fn(*varargs, **kwargs)
  File "/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py", line 701, in run_train
    trainer_output=trainer.train()
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/trainer.py", line 1780, in train
    return inner_training_loop(
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/trainer.py", line 2213, in _inner_training_loop
    self._maybe_log_save_evaluate(tr_loss, grad_norm, model, trial, epoch, ignore_keys_for_eval)
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/trainer.py", line 2577, in _maybe_log_save_evaluate
    metrics = self.evaluate(ignore_keys=ignore_keys_for_eval)
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/trainer.py", line 3365, in evaluate
    output = eval_loop(
  File "/Users/macair/conda3/envs/py39/lib/python3.9/site-packages/transformers/trainer.py", line 3656, in evaluation_loop
    metrics = self.compute_metrics(EvalPrediction(predictions=all_preds, label_ids=all_labels))
  File "/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py", line 545, in metrics_calc
    true_predictions = [
  File "/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py", line 546, in <listcomp>
    [i2l[p] for (p, l) in zip(prediction, label) if l != -100]
  File "/Users/macair/gitdev/uutilmy/utilmy_dev/utilmy/webapi/asearch/nlp/ner/ner_deberta.py", line 546, in <listcomp>
    [i2l[p] for (p, l) in zip(prediction, label) if l != -100]

"""