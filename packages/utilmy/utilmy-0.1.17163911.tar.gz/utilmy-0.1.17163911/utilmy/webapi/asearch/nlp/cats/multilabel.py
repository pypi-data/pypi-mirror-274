""" 
### Install
    pip install fire utilmy


    git clone 
    git checkout devtorch

    cd webapi/asearch/nlp
    mkdir -p ztmp
    python mutilabel.py run_train --device "cpu"



    ttps://www.kaggle.com/datasets/spsayakpaul/arxiv-paper-abstracts

    For label = "cs.ML"
    Cat1 : cs
    Cat2:  ML



### Fine Tuning Strategies using LLM and SetFit

    https://medium.com/@xmikex83/using-large-language-models-to-train-smaller-ones-ee64ff3e4bd3

    https://huggingface.co/MoritzLaurer/deberta-v3-large-zeroshot-v2.0






"""
if "Import":
    import time,  json,re, os, pandas as pd, numpy as np,copy
    from dataclasses import dataclass
    from typing import Optional, Union
    from box import Box

    from collections import Counter
    from sklearn.metrics import f1_score    

    import datasets 
    from datasets import load_dataset, Dataset, load_metric
    import evaluate
    # If issue dataset: please restart session and run cell again
    from transformers import (
        BitsAndBytesConfig,
        GenerationConfig,
        HfArgumentParser,
        TrainingArguments,
        Trainer,

        AutoTokenizer,
        AutoModelForMultipleChoice,        
        AutoModelForSemanticSegmentation,
        AutoModelForSequenceClassification,

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
                        glob_glob, json_save, json_load, config_load,
                        dict_merge_into
    )

    from util_exp import (exp_create_exp_folder, exp_config_override, exp_get_filelist)



#################################################################################################
######## Dataloder Customize ####################################################################
def data_arxiv_load(dirin="./ztmp/data/category/arxiv/"):

    flist = glob_glob(dirin)
    if len(flist)< 1: 
        #### Download from https://www.kaggle.com/datasets/spsayakpaul/arxiv-paper-abstracts
        kaggle_donwload("https://www.kaggle.com/datasets/spsayakpaul/arxiv-paper-abstracts", dirout= dirin )


    df = pd_read_file(dirin, sep="\t")
    log(df.head(5).T, df.columns, df.shape)

    ##### Custom to Arxiv dataset
    df["label2"] = df["terms"].apply(lambda x:  sorted(x.split(",")) )  # ['cs.CV', 'cs.AI', 'cs.LG']
    df["cat1"] = df["label2"].apply(lambda x: x[0].split(".")[0])  # "cs"
    df["cat2"] = df["label2"].apply(lambda x: x[0].split(".")[1])  # "CV"
    df["cat3"] = df["label2"].apply(lambda x: x[1].split(".")[0] if len(x)>0 else "NA" )  # "cs"
    df["cat4"] = df["label2"].apply(lambda x: x[1].split(".")[1] if len(x)>0 else "NA")  # "AI"

    df["labels"] = df.apply(lambda x: x["cat1"] + "," + x["cat2"] + "," + x["cat3"] + "," + x["cat4"], axis=1)

    n_train = int(len(df)*0.8)
    df_val  = df.iloc[n_train:,:]
    df      = df.iloc[:n_train,:]

    return df, df_val


def data_arxiv_create_label_mapper(dirin="./ztmp/data/category/arxiv/"):

    df, df_val = pd_read_file(dirin)

    label_all = df["labels"].tolist() + df_val["labels"].tolist()
    label_all = list(set(label_all))
    
    label_all = [x for x in label_all if x is not None]


    I2L = {}

    l2I = {}          


    meta_dict = {"label_nunique" : {
                 "cat1": 3, "cat2": 5, "cat3": 6, "cat4": 7, }}

    NLABEL_TOTAL = sum([  cnt for key,cnt in meta_dict["label_nunique"].items()])   

    return I2L, L2I, NLABEL_TOTAL, meta_dict 






########################################################################################
##################### Data Validator ###################################################
def data_tokenize_split(df, tokenizer, L2I,cc):
    cols         = list(df.columns)
    max_length   = cc.data.sequence_max_length
    NLABEL_TOTAL = cc.data.nlabel_total
 

    def preprocess_function(row):
        ### Label split and encoding
        if isinstance( row['labels'], str):
            all_labels = [x.strip() for x in  row['labels'].split(',') ]

        labels = [0 for i in range(len(NLABEL_TOTAL))]
        for label in all_labels:
            label_id = L2I.get(label, NLABEL_TOTAL - 1)  ### One Label for unknown
            labels[label_id] = 1

        #### Text tokenizer
        out = tokenizer(row["text"], truncation=True, padding=True, max_length= max_length,
                   return_offsets_mapping= False,
                   return_overflowing_tokens=False)

        out["labels"] = labels           
        # output["input_ids"] = output.pop("input_ids")  # Add input_ids to  output
        return out

    #### Encode texts
    assert df[[ "text", "labels" ]].shape
    ds = Dataset.from_pandas(df)
    ds = ds.map(preprocess_function, batched=True)


    #### Filter labels with only a single instance
    label_counts = Counter([tuple(label) for label in ds["labels"]])
    valid_labels = [label for label, count in label_counts.items() if count > 1]
    ds           = ds.filter(lambda example: tuple(example["labels"]) in valid_labels)

    #### Reduce columns
    ds           = ds.remove_columns( cols)
    # ds = ds.remove_columns(['overflow_to_sample_mapping', 'offset_mapping', ] + cols)
    return ds






#################################################################################################
######## Dataloder Common #######################################################################
def data_load_convert_todict(dirin=".ztmp/arxiv_data.csv", fun_name="dataset_arxiv", label_nunique=None):
    """  Create custom category from raw label
         ['cs.CV', 'cs.AI', 'cs.LG']

    """ 
    from utilmy import load_function_uri
    dataset_loader_fun = globals()[fun_name]
    df, meta_dict = dataset_loader_fun(dirin)


    label_nunique = meta_dict.get("label_nunique")  ## number of unique categories per label
    if label_nunique is None:
        label_nunique = {"cat1": 3, "cat2": 5, "cat3": 6, "cat4": 7, }


    ####### Big OneHot Encoded  ######################################
    colslabel     = [  key for key in label_nunique.keys()]       
    n_class_total = sum([  label_nunique[key] for key in label_nunique.keys()])

    for collabel in colslabel:    
       df[ f"{collabel}_onehot"] = cat_to_onehot(df[collabel].values , ndim= label_nunique[collabel])

    df["cat_all_onehot"] = df.apply(lambda x :  sum( [x[ci+"_onehot"] for ci in colslabel ] )  ,axis=1 )


    # Convert DataFrame to a dictionary
    data = {
        "text":    df["text"].tolist(),
        "labels":  df["cat_all_onehot"].values.tolist(),
    }
    return data, label_nunique, n_class_total




def cat_to_onehot(cat_val:list, ndim=None):
    """ 
        # Example usage
        categories = ['2', '0', '1', '2']  # Example category indices as strings
        ndim = 3  # Number of unique categories
        encoded = encode_categories(categories, ndim)
        print(encoded)

    """
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np    

    ndim= ndim if ndim is not None else len(np.unique(cat_val))

    # Ensure  input is an array
    categories = np.array(cat_val).reshape(-1, 1)
    
    # Create  OneHotEncoder with  specified number of dimensions
    encoder = OneHotEncoder(categories=[np.arange(ndim)], sparse=False)    
    onehot = encoder.fit_transform(categories)
    return onehot






########################################################################################
##################### Tokenizer helper ################################################







#################################################################################
######################## Train ##################################################
def run_train(cfg=None, cfg_name="ner_deberta", dirout="./ztmp/exp", istest=1):
    """ 
       python nlp/ner/ner_deberta.py run_train  --dirout ztmp/exp   --cfg config/traina/train1.yaml --cfg_name ner_deberta

    """
    global NCLASS, L2I, I2L    
    log("###### Config Load   #############################################")
    cfg0 = config_load(cfg)
    cfg0 = cfg0.get(cfg_name, None) if cfg0 is not None else None


    log("###### User Params   #############################################")
    cc = Box()
    cc.model_name='microsoft/deberta-v3-base'

    #### Data name
    cc.dataloader_name = "data_arxiv_load"
    cc.datamapper_name = "data_arxiv_create_label_mapper"

    cc.n_train = 5  if istest == 1 else 1000000000
    cc.n_val   = 2  if istest == 1 else 1000000000

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
    aa.num_train_epochs            = 1
    aa.warmup_ratio                = 0.2 # 20%  total step warm-up
    # lr_schedulere_type='constant'
    aa.evaluation_strategy = "epoch"
    aa.logging_strategy    = "epoch"
    aa.save_strategy       = "epoch"
    cc.hf_args_train = copy.deepcopy(aa)

    ### HF model
    cc.hf_args_model_init = {}
    cc.hf_args_model_init.model_name = cc.model_name


    #### Override by Yaml config  #####################################
    cc = exp_config_override(cc, cfg0, cfg, cfg_name)


    log("###### Experiment Folder   #######################################")
    cc = exp_create_exp_folder(task="ner_deberta", dirout=dirout, cc=cc)
    log(cc.dirout)
    del dirout


    log("###### Model : Training params ##############################")
    args = TrainingArguments( ** dict(cc.hf_args_train))


    log("###### User Data Load   #############################################")
    from utilmy import load_function_uri
    # dataloader_fun = load_function_uri(dataloader_name)
    # datamapper_fun = load_function_uri(datamapper_name]

    dataloader_fun = globals()[cc.dataloader_name]
    datamapper_fun = globals()[cc.datamapper_name]  ### dataXX_create_label_mapper()

    df, df_val       = dataloader_fun()  ## = dataXX_load_prepro()
    L2I, I2L, NLABEL_TOTAL, meta_dict = datamapper_fun()  ## Label to Index, Index to Label

    columns = df.columns.tolist()
    df, df_val = df.iloc[:cc.n_train], df_val.iloc[:cc.n_val]


    cc.data ={}
    cc.data.cols          = columns
    cc.data.cols_required = ["text", "labels" ]
    #cc.data.ner_format    = ["start", "end", "type", "value"]  
    cc.data.cols_remove   = ['overflow_to_sample_mapping', 'offset_mapping', ] + columns
    cc.data.L2I           = L2I     ### label to Index Dict
    cc.data.I2L           = I2L     ### Index to Label Dict
    # cc.data.nclass        = NCLASS  ### Number of NER Classes.
    cc.data.ntotal        = NLABEL_TOTAL  ### Number of NER Classes.

    cc.hf_args_model_init.num_labels = NLABEL_TOTAL ## due to BOI notation

 


    ################# Generic Code ###########################################  
    log("###### Dataloader setup  ############################################")
    tokenizer = AutoTokenizer.from_pretrained(cc.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    dataset_train = data_tokenize_split(df,     tokenizer, L2I,cc)    
    dataset_valid = data_tokenize_split(df_val, tokenizer, L2I,cc)    

    # batch = DataCollatorForLLM(tokenizer)([dataset_train[0], dataset_train[1]])
    # log(dataset_valid[0])
    # log(batch)
    from transformers import DataCollatorWithPadding
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


    log("######### Model : Init #########################################")
    model = AutoModelForSequenceClassification.from_pretrained(cc.model_name, 
                               num_labels= cc.hf_args_model_init.num_labels,
                               id2label= I2L, label2id= L2I,
                               problem_type = "multi_label_classification")

    # for i in model.deberta.parameters():
    #   i.requires_grad=False

    log("######### Model : Training start ##############################")
    trainer = Trainer(model, args,
        train_dataset= dataset_train,
        eval_dataset = dataset_valid,
        data_collator= data_collator,
        tokenizer    = tokenizer,
        compute_metrics=metrics_calc_callback_train,
    )

    json_save(cc, f'{cc.dirout}/config.json')
    trainer_output = trainer.train()
    trainer.save_model( f"{cc.dirout}/model")

    cc['metrics_trainer'] = trainer_output.metrics
    json_save(cc, f'{cc.dirout}/config.json', show=1)


    log("######### Model : Eval Predict  ######################################")
    preds_proba, labels, _ = trainer.predict(dataset_valid)
    df_val                 = pd_predict_format(df_val, preds_proba, labels)
    assert df_val[[  "pred_proba", "pred_labels",     ]].shape


    log("######### Model : Eval Metrics #######################################")    
    assert df_val[[ "text", "labels", "pred_labels"     ]].shape
    df_val = metrics_calc_full(df_val,)

    pd_to_file(df_val, f'{cc.dirout}/dfval_pred_labels.parquet', show=1)  


def pd_predict_format(df_val:pd.DataFrame, preds_proba:list, labels:list, 
                      offset_mapping: list)->pd.DataFrame:
    """ preds_proba: (batch, seq, NCLASS*2+1)    [-3.52225840e-01  5.51

        labels:      (batch,seq)  [[-100   10   10   10   10    3   5    5   10   10 -100 -100]
                                   [-100   10   10   10   10     10   10 -100]]
        pred_class: (batch, seq)  [[ 6  3  6 10 10 10 10 10  4 10 10  4 10  5  4 4]
                                   [ 6  6  6  4 10 10  1 10 10  2  2 10 10 0 10  5]]

        'pred_ner_list_records':
          [{ 'start': 0, 'end': 1, 'type': 'ORG', value : "B-ORG"},   ]

            pred_ner_list_records
            List<Struct<{end:Int64, predictionstring:String, start:Int64, text:String, type:String}>>

            accuracy
            Struct<{city:Float64, country:Float64, location:Float64, location_type:Float64, total_acc:Float64}>          

    """
    pred_class            = np.argmax(preds_proba, axis=-1)
    log("pred_proba: ", str(preds_proba)[:50],)
    log("labels: ",     str(labels)[:50]      )
    log("pred_class: ", str(pred_class)[:50] )

    df_val['pred_proba'] = np_3darray_into_2d(preds_proba) 
    df_val['pred_class'] = list(pred_class) ### 2D array into List of List  ## ValueError: Expected a 1D array, got an array with shape (2, 25)

    ### Need to convert into (start, end, tag) record format
    df_val['pred_ner_list'] = df_val['pred_class'].apply(lambda x : x)   
    # df_val['preds_labels'] = labels

    df_val['pred_ner_list_records'] = pd_predict_convert_ner_to_records(df_val, offset_mapping)
    return df_val



def pd_predict_convert_ner_to_records(df_val:pd.DataFrame, offset_mapping: list,
                                       col_nerlist="pred_ner_list", col_text="text")->pd.DataFrame:
    """Convert predicted classes into span records for NER.

    Args:
        df_val (pd.DataFrame): DataFrame containing the input data. It should have the following columns:
            - col_nerlist (str): Column name for the predicted classes.
            - col_text (str): Column name for the text.
        offset_mapping (list): List of offset mappings.

    Returns:
        list: List of span records for NER. Each span record is a dictionary with the following keys:
            - text (str): text.
            - ner_list (list): List of named entity records. Each named entity record is a dictionary with the following keys:
                - type (str)            : type of the named entity.
                - predictionstring (str): predicted string for the named entity.
                - start (int)           : start position of the named entity.
                - end (int)             : end position of the named entity.
                - text (str)            : text of the named entity.

    """
    # print(df_val)
    # assert df_val[[ "text", "input_ids", "offset_mapping", "pred_ner_list"  ]]
    def get_class(c):
        if c == NCLASS*2: return 'Other'
        else: return I2L[c][2:]

    def pred2span(pred_list, df_row, viz=False, test=False):
        #     example_id = example['id']
        n_tokens = len(df_row['offset_mapping'][0])
        #     print(n_tokens, len(example['offset_mapping']))
        classes = []
        all_span = []
        for i, c in enumerate(pred_list.tolist()):
            if i == n_tokens-1:
                break
            if i == 0:
                cur_span = df_row['offset_mapping'][0][i]
                classes.append(get_class(c))
            elif i > 0 and (c == pred_list[i-1] or (c-NCLASS) == pred_list[i-1]):
                cur_span[1] = df_row['offset_mapping'][0][i][1]
            else:
                all_span.append(cur_span)
                cur_span = df_row['offset_mapping'][0][i]
                classes.append(get_class(c))
        all_span.append(cur_span)

        text = df_row["text"]
        
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

        #### Generate Record format 
        row = {  "text": text, "ner_list": []}
        es = []
        for ner_type, span, predstring in zip(classes, all_span, predstrings):
            if ner_type!='Other':
              e = {
                'type' : ner_type,
                'value': predstring,
                'start': span[0],
                'end'  : span[1],
                'text' : text[span[0]:span[1]]
              }
              es.append(e)
        row["ner_list"] = es
    
        return row


    #### Convert
    pred_class = df_val[col_nerlist].values
    valid      = df_val[[col_text]]
    valid['offset_mapping'] = offset_mapping
    valid = valid.to_dict(orient="records")

    ### pred_class : tuple(start, end, string)
    predicts= [pred2span(pred_class[i], valid[i]) for i in range(len(valid))]

    return [row['ner_list'] for row in predicts]


    #pd_to_file( predicts, dirout + '/predict_ner_visualize.parquet' )
    # pred = pd.read_csv("nguyen/20240215_171305/predict.csv")
    # pred
    # pred = pred[["text", "ner_list"]]
    # eval(pred.ner_tag.iloc[0])
    # pred["ner_list"] = pred["ner_list"].apply(eval)


def np_3darray_into_2d(v3d):
    """ Required to save 3d array in parquet format


    """ 
    shape = v3d.shape
    v2d = np.empty((shape[0], shape[1]), dtype=str)

    for i in range(shape[0]):
        for j in range(shape[1]):
            vstr    = ",".join(map(str, v3d[i,j,:]))
            v2d[i,j]= vstr
    return list(v2d)




################################################################################
########## Run Inference  ######################################################
def run_infer(cfg:str=None, dirmodel="ztmp/models/gliner/small", 
                cfg_name    = "ner_gliner_predict",
                dirdata     = "ztmp/data/text.csv",
                coltext     = "text",
                dirout      = "ztmp/data/ner/predict/",
                multi_label = 0,
                threshold   = 0.5
                  ):
  """Run prediction using a pre-trained  Deberta model.

    ### Usage
      export pyner="python nlp/ner/ner_deberta.py "

      pyner run_infer --dirmodel "./ztmp/exp/20240520/235015/model_final/"  --dirdata "ztmp/data/ner/deberta"  --dirout ztmp/out/ner/deberta/

      pyner run_infer --cfg config/train.yaml     --cfg_name "ner_deberta_infer_v1"


    Output:


  Parameters:
      cfg (dict)    : Configuration dictionary (default is None).
      dirmodel (str): path of pre-trained model 
      dirdata (str) : path of input data 
      coltext (str) : Column name of text
      dirout (str)  : path of output data 


  #log(model.predict("My name is John Doe and I love my car. I bought a new car in 2020."))

  """
  cfg0 = config_load(cfg,)
  cfg0 = cfg0.get(cfg_name, None) if isinstance(cfg0, dict) else None

  ner_tags    = ["person", "city", "location", "date", "actor", ]
  if  isinstance( cfg0, dict) : 
    if "ner_tags" in cfg0: 
        ner_tags = cfg0["ner_tags"]
    log("ner_tags:", str(ner_tags)[:100] )

    dirmodel = cfg0.get("dirmodel", dirmodel)
    dirdata  = cfg0.get("dirdata",  dirdata)
    dirout   = cfg0.get("dirout",   dirout)

  multi_label = False if multi_label==0 else True

  model = AutoModelForTokenClassification.from_pretrained(dirmodel,)
  log(str(model)[:10])
  model.eval()

  flist = exp_get_filelist(dirdata)
  for ii,fi in enumerate(flist) :
     df = pd_read_file(fi)
     log(ii, fi,  df.shape)
     #df["ner_list_pred"] = df[coltext].apply(lambda x: model.predict(x, flat_ner=True, threshold=0.5, multi_label=False))
     df["ner_list_pred"] = df[coltext].apply(lambda xstr: model.predict_entities(xstr, 
                                               labels= ner_tags, threshold=threshold,
                                               multi_label=multi_label))

     pd_to_file(df, dirout + f"/df_predict_ner_{ii}.parquet", show=1)






################################################################################
########## Metrics Helper    ###################################################
def metrics_calc_callback_train(p,):
    """  
            import evaluate
            import numpy as np

            clf_metrics = evaluate.combine(["accuracy", "f1", "precision", "recall"])

            def sigmoid(x):
               return 1/(1 + np.exp(-x))

        def compute_metrics(eval_pred):

            predictions, labels = eval_pred
            predictions = sigmoid(predictions)
            predictions = (predictions > 0.5).astype(int).reshape(-1)
            return clf_metrics.compute(predictions=predictions, references=labels.astype(int).reshape(-1))
            references=labels.astype(int).reshape(-1))

    """
    global L2I, I2L

    # metric = datasets.load_metric("seqeval")
    metric = evaluate.combine(["accuracy", "f1", "precision", "recall"])
    preds, labels = p
    preds = np.argmax(preds, axis=2)

    # Remove ignored index (special tokens)
    true_preds = [
        [I2L[p] for (p, l) in zip(pred, label) if l != -100]
        for pred, label in zip(preds, labels)
    ]
    true_labels = [
        [I2L[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(preds, labels)
    ]

    results = metric.compute(predictions=true_preds, references=true_labels)
    
    #return results
    return {
        "precision": results["overall_precision"],
        "recall"   : results["overall_recall"],
        "f1"       : results["overall_f1"],
        "accuracy" : results["overall_accuracy"],
    }



def metrics_calc_full(df_val,):
    #### Error due : Need to conver the ner_list into  {start, end, tag} format
    log( metrics_ner_accuracy(df_val["ner_list"].iloc[0], df_val['pred_ner_list_records'].iloc[0]) )    
    df_val['accuracy'] = df_val.apply(lambda x: metrics_ner_accuracy(x["ner_list"], 
                                                                     x['pred_ner_list_records']),axis=1 )
    return df_val



def metrics_ner_accuracy(tags_true:list, tags_pred:list):
    """Calculate   accuracy metric for NER (NER) task.
    Args:
        tags (List[Dict]): List of dict  ground truth tags.
                            contains   'start' index, 'value', and 'type' of a tag.

        preds (List[Dict]): List of dict predicted tags.
                            contains   'start' index, 'text', and 'type' of a tag.

    Returns: Dict:   accuracy metric for each tag type

    """
    nerdata_validate_row(tags_true, cols_ref=['start', 'value', 'type'])
    nerdata_validate_row(tags_pred, cols_ref=['start', 'value', 'type'])

    ### Sort by starting indices
    tags_true = sorted(tags_true, key= lambda x: x['start'])
    tags_pred = sorted(tags_pred, key= lambda x: x['start'])

    acc = {}
    acc_count = {}
    for tag in tags_true:
        value_true = tag['value'] ## NER value 
        type_true  = tag['type']  ## NER column name

        if type_true not in acc:
            acc[type_true]       = 0
            acc_count[type_true] = 0

        acc_count[type_true] += 1

        for pred in tags_pred:
           if pred['type'] == type_true and pred['value'].strip() == value_true.strip():
              acc[type_true ]+= 1

    total_acc   = sum(acc.values()) / sum(acc_count.values())
    metric_dict = {"accuracy": {tag: v/acc_count[tag] for tag, v in acc.items() } }

    metric_dict['accuracy_total'] = total_acc
    return metric_dict








###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()









def zz_data_tokenize_split_v2(data:dict, max_length=128, model_id="microsoft/deberta-base",):
    # Tokenization
    tokenizer = DebertaTokenizer.from_pretrained(model_id)

    def preprocess_function(examples):
        output = tokenizer(examples["text"], truncation=True, padding=True, max_length= max_length)
        # output["input_ids"] = output.pop("input_ids")  # Add input_ids to  output
        return output

    # Load  dataset
    ds = Dataset.from_dict(data)

    # Encode texts
    ds = ds.map(preprocess_function, batched=True)

    # Remove labels with only a single instance
    label_counts = Counter([tuple(label) for label in ds["labels"]])
    valid_labels = [label for label, count in label_counts.items() if count > 1]
    ds           = ds.filter(lambda example: tuple(example["labels"]) in valid_labels)

    # Split dataset into training and validation sets with stratification
    text_train, text_test, labels_train, labels_test = train_test_split(
        ds["text"],
        ds["labels"],
        test_size=0.2,
        random_state=42,
        stratify=ds["labels"],
    )

    train_dataset = Dataset.from_dict(
        {   "text": text_train,
            "labels": labels_train,
            "input_ids": ds["input_ids"][: len(text_train)],
            "attention_mask": ds["attention_mask"][: len(text_train)],
        }
    )

    test_dataset = Dataset.from_dict(
        {   "text": text_test,
            "labels": labels_test,
            "input_ids": ds["input_ids"][len(text_train) :],
            "attention_mask": ds["attention_mask"][len(text_train) :],
        }
    )
    return train_dataset, test_dataset, tokenizer

