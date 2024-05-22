"""  Utilities to manage experiments


"""
import warnings
warnings.filterwarnings("ignore")

import os, json, pandas as pd, numpy as np, copy
from types import SimpleNamespace
from typing import List, Dict
from box import Box

from utilmy import (pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob, config_load,
                    json_save, json_load,)
from utilmy import log, log2
from utilmy import dict_merge_into




def exp_create_exp_folder(task="ner_deberta", dirout="./ztmp/exp", cc=None):
    """Create an experiment folder with a timestamped directory name and save   configuration object as a JSON file.
    Args:
        task (str, optional):   name of   task. Defaults to "ner_deberta".
        dirout (str, optional):   output directory. Defaults to "./ztmp/exp".
        cc (Box, optional):   configuration object. Defaults to None.
    """
    dt = date_now(fmt="%Y%m%d/%H%M%S")
    dirout0   = dirout
    n_train   = cc.n_train
    cc.dirout = f"{dirout0}/{dt}-{task}-{n_train}"
    os_makedirs(cc.dirout)
    json_save({"cc": cc }, f"{dirout}/exp-{task}.json")
    return cc


def exp_config_override(cc, cfg0, cfg, cfg_name:str="ner_deberta"):
    cc.cfg      = cfg
    cc.cfg_name = cfg_name    
    if isinstance(cfg0, dict):
       log(f"###### Overide by config {cfg_name} ####################") 
       cc = dict_merge_into( cc.to_dict(), copy.deepcopy(cfg0),   )
       cc = Box(cc)

    log(cc.to_dict())
    return cc



def exp_get_filelist(dirdata):
  if "*" in dirdata.split("/")[-1] or "." in dirdata.split("/")[-1]  :
      flist = glob_glob(dirdata)      
  else:   
      flist = glob_glob(dirdata + "/*.parquet")
      flist = flist + glob_glob(dirdata + "/*.csv")
  log("nFiles: ", len(flist))
  return flist



