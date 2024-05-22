# -*- coding: utf-8 -*-
"""export_model_to_onnx.ipynb
Docs:

    https://colab.research.google.com/drive/17sjCf9vsO7w2nGuP28qp_q-ZTEo3Ezqn

    !pip install -q -U bitsandbytes peft accelerate  transformers==4.37.2

    !pip install datasets transformers fastembed simsimd

    !pip install transformers==4.37.2
    !pip install utilmy
    !pip install onnxruntime

    !pip install -q seqeval


"""

from datasets import load_dataset, Dataset
from datasets import Dataset, load_metric
# If issue dataset: please restart session and run cell again
from transformers import (
    AutoModelForCausalLM,
    PhiForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    GenerationConfig,
    AutoModelForSeq2SeqLM
)
from tqdm import tqdm
import torch
import time
import json
import pandas as pd
import numpy as np
from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy
from transformers import AutoModelForMultipleChoice, TrainingArguments, Trainer
from dataclasses import dataclass
from typing import Optional, Union
from seqeval.metrics import f1_score, precision_score, recall_score, classification_report

import os
from pathlib import Path
import spacy
from spacy import displacy
from pylab import cm, matplotlib





def init_googledrive(shortcut="phi2"):
    import os
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir(f"/content/drive/MyDrive/{shortcut}/")
    # ! ls .
    #! pwd
    #! ls ./traindata/
    #ls



from utilmy import date_now, date_now, pd_to_file
import os
dirout0='nguyen'
dt = "20240215_171305"
dirout= os.path.join(dirout0, dt)
# os.makedirs(dirout)
!ls $dirout/log_training//checkpoint-314

import pandas as pd

data_path = "traindata/df_10000_1521.parquet"
df_test = pd.read_parquet('traindata/df_1000.parquet')#.head(100)
df = pd.read_parquet(data_path)
df.head()

# location, address, city, country, location_type, type_exclude
import re
def preprocess_text_predict(row):
    """

    """
    text = row['answer_fmt']
    query = row['query']
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
#         location_type=\[(.*?)\],location_type_exclude=\[(.*?)\]
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

def extract_from_answer_full(row):
    dict_i4 = json.loads(row['answerfull'])['args']
    query = row['query']
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
#             address': '4700 Gilbert Ave',
#    'city': 'Chicago',
#    'country': 'United States',
#    'location_type': 'hot dog stand and viewpoint',
#    'location_type_exclude': [],
#     query = row['query']

df['entity_tag']=df.apply(preprocess_text_predict, axis=1)
df_test['entity_tag'] = df_test.apply(preprocess_text_predict, axis=1)

model_name='FacebookAI/roberta-base'
tokenizer = AutoTokenizer.from_pretrained(os.path.join(dirout,"log_training//checkpoint-314"))

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
i2l

# tokenize and add labels
def fix_beginnings(labels):
    for i in range(1,len(labels)):
        curr_lab = labels[i]
        prev_lab = labels[i-1]
        if curr_lab in range(NCLASS,NCLASS*2):
            if prev_lab != curr_lab and prev_lab != curr_lab - NCLASS:
                labels[i] = curr_lab -NCLASS
    return labels

def tokenize_and_align_labels(examples):

    o = tokenizer(examples['query'],
                  return_offsets_mapping=True,
                  return_overflowing_tokens=True)
    offset_mapping = o["offset_mapping"]
    o["labels"] = []
    for i in range(len(offset_mapping)):
        labels = [L2I['O'] for i in range(len(o['input_ids'][i]))]
        for tag in examples['entity_tag']:
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

        labels = fix_beginnings(labels)

        o["labels"].append(labels)
    o['labels'] = o['labels'][0]
    o['input_ids'] = o['input_ids'][0]
    o['attention_mask'] = o['attention_mask'][0]
    return o

dataset = Dataset.from_pandas(df)
valid = Dataset.from_pandas(df_test)
dataset = dataset.map(tokenize_and_align_labels)
valid = valid.map(tokenize_and_align_labels)

from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer

model = AutoModelForTokenClassification.from_pretrained(os.path.join(dirout,"log_training//checkpoint-314"))

from transformers import DataCollatorForTokenClassification

@dataclass
class DataCollatorForLLM:
    tokenizer: PreTrainedTokenizerBase
    padding: Union[bool, str, PaddingStrategy] = True
    max_length: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None

    def __call__(self, features):
        label_name = 'label' if 'label' in features[0].keys() else 'labels'
        labels = [feature.pop(label_name) for feature in features]
        max_length_labels = max([len(i) for i in labels])
        labels_pad = np.zeros((len(labels), max_length_labels, )) + -100
        for index in range(len(labels)):
#             print(len(labels[index]), labels[index])
            labels_pad[index, : len(labels[index])] = labels[index]

        batch_size = len(features)
        flattened_features = features
        batch = self.tokenizer.pad(
            flattened_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors='pt',
        )
        batch['labels'] = torch.from_numpy(labels_pad).long()

        return batch

metric = load_metric("seqeval")

def compute_metrics(p):
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
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

def tokenizer_query(query):
  o = tokenizer(query,
                  return_offsets_mapping=True,
                  return_overflowing_tokens=True)
  offset_mapping = o["offset_mapping"]
  o['input_ids'] = o['input_ids'][0]
  o['attention_mask'] = o['attention_mask'][0]
  return o

query_0 = df_test['query'].iloc[0]

tokenizer_query(query_0)

valid[0]

torch.cuda.device_count()

i2l

def predict(query):
  device = 'cpu'
  if torch.cuda.device_count():
    device='cuda'
  o = tokenizer_query(query)
  input_ids = torch.tensor(o['input_ids']).long().reshape([ 1, -1]).to(device)
  model.eval()
  with torch.no_grad():
    output = model(
        input_ids
    ).logits
  # print(output)
  output = torch.argmax(output, -1)
  o['query'] = query
  return output, o

def get_class(c):
    if c == NCLASS*2: return 'Other'
    else: return i2l[c][2:]

def pred2span(pred, example, viz=False, test=False):
    n_tokens = len(example['input_ids'])
    classes = []
    all_span = []
    for i, c in enumerate(pred.tolist()):
        if i == n_tokens-1:
            break
        if i == 0:
            cur_span = list(example['offset_mapping'][0][i])
            classes.append(get_class(c))
        elif i > 0 and (c == pred[i-1] or (c-NCLASS) == pred[i-1]):
            cur_span[1] = example['offset_mapping'][0][i][1]
        else:
            all_span.append(cur_span)
            cur_span = list(example['offset_mapping'][0][i])
            classes.append(get_class(c))
    all_span.append(cur_span)

    text = example['query']
    predstrings = []
    for span in all_span:
        span_start = span[0]
        span_end = span[1]
        before = text[:span_start]
        token_start = len(before.split())
        if len(before) == 0: token_start = 0
        elif before[-1] != ' ': token_start -= 1
        num_tkns = len(text[span_start:span_end+1].split())
        tkns = [str(x) for x in range(token_start, token_start+num_tkns)]
        predstring = ' '.join(tkns)
        predstrings.append(predstring)

    row = {
        'query': text,
        'entity_tag': []
    }
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
    row['entity_tag'] = es


    return row

pred, sample = predict(df_test['query'].iloc[4])
pred2span(pred[0], sample)





def export_onnx(model, tokenizer, query_0, dirout):

    device = 'cpu'
    if torch.cuda.device_count():
    device='cuda'
    o = tokenizer_query(query_0)
    x = torch.tensor(o['input_ids']).long().reshape([ 1, -1]).to(device)

    class WrapModel(torch.nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m
        def forward(self, x):
            output = self.m(  x).logits
            return torch.argmax(output, -1)

    model_export = WrapModel(model)
    torch_out = model_export(x)

    # Export the model
    torch.onnx.export(model_export,               # model being run
                    x,                         # model input (or a tuple for multiple inputs)
                    os.path.join(dirout, 'model.onnx'),   # where to save the model (can be a file or file-like object)
                    export_params=True,        # store the trained parameter weights inside the model file
                    opset_version=15,          # the ONNX version to export the model to
                    do_constant_folding=True,  # whether to execute constant folding for optimization
                    input_names = ['input'],   # the model's input names
                    output_names = ['output'], # the model's output names
                    dynamic_axes={'input' : {0 : 'batch_size', 1:'seq_len'},    # variable length axes
                                    'output' : {0 : 'batch_size', 1:'seq_len'}})


    import onnxruntime
    ort_session = onnxruntime.InferenceSession(os.path.join(dirout, 'model.onnx'), 
                    providers=["CPUExecutionProvider"])

    def to_numpy(tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    # compute ONNX Runtime output prediction
    ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}
    ort_outs = ort_session.run(None, ort_inputs)

    # compare ONNX Runtime and PyTorch results
    np.testing.assert_allclose(to_numpy(torch_out), ort_outs[0], rtol=1e-03, atol=1e-05)
    print("Exported model has been tested with ONNXRuntime, and the result looks good!")
    ort_outs[0]

from tqdm import tqdm


predicts = []
for index, row in tqdm(df_test.iterrows()):
  query = row.query
  o = tokenizer_query(query)
  o['query'] = query
  x = torch.tensor(o['input_ids']).long().reshape([ 1, -1])
  ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}
  ort_outs = ort_session.run(None, ort_inputs)
  pred = ort_outs[0] # bs, seq_length
  value_pre_dict = pred2span(pred[0], o)
  predicts.append(value_pre_dict['entity_tag'])

df_test['predict_raw_tag'] = predicts



df_test

predicts[0]

def acc_metric(tags, preds):
  tags = sorted(tags, key=lambda x:x['start'])
  preds = sorted(preds, key=lambda x:x['start'])
  acc = {}
  acc_count = {}
  for tag in tags:
    value = tag['value']
    tag_type = tag['type']
    if tag_type not in acc:
      acc[tag_type] = 0
      acc_count[tag_type] = 0
    acc_count[tag_type] += 1
    for p in preds:
      if p['type'] == tag_type and p['text'].strip() == value.strip():

        acc[tag_type]+= 1
  total_acc = sum(acc.values()) / sum(acc_count.values())
  acc = {
      k: v/acc_count[k] for k, v in acc.items()
  }
  acc['total_acc'] = total_acc
  return acc

# acc_metric(df_test.entity_tag.iloc[0], predicts[0])
df_test['acc'] = df_test.apply(
    lambda x: acc_metric(
        x['entity_tag'],
        x['predict_raw_tag']
    ),
    axis=1
)

df_test[(df_test['acc'].apply(lambda x:x['total_acc']<=0.8)) & (df_test['acc'].apply(lambda x:x['total_acc']>=0.6))][['predict_raw_tag', 'entity_tag', 'acc']].sample(1).to_dict()

df_test

