```

##### Dataset Schema 
mkdir -p ./ztmp/hf_data/


SCHEMA_GLOBAL_v1 = [
    ("text_id",  "int64", "global unique ID for the text"),
    ("text_id2", "int64", "text_id from original dataset"),

    ("dataset_id",  "str",   "URL of the dataset"),
    ("dataset_cat", "str",   "Category tags : english/news/"),

    ("dt", "float64", "Unix timestamps"),

    ("title", "str", " Title "),
    ("summary", "str", " Summary "),
    ("text", "str", " Core text "),
    ("info_json", "str", " Extra info in JSON string format "),


    ("cat1", "str", " Category 1 or label "),
    ("cat2", "str", " Category 2 or label "),
    ("cat3", "str", " Category 3 or label "),
    ("cat4", "str", " Category 4 or label "),
    ("cat5", "str", " Category 5 or label "),


    ("ner_list", "list", " List of triplets (str_idx_start, str_idx_end, ner_tag) "),
]






```

