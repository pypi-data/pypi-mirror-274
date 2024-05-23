```bash



############################################################################################
### Generate Prompt, query from Answers using GPT-3.5

  ### generate prompt via DSPy
     export PYTHONPATH="$(pwd)"
     python rag/query.py prompt_find_best --dirdata "./ztmp/bench/norm/"  --dataset "ag_news"  --dirout ./ztmp/exp  

          --> Add 1 prompt to PromptStorage Saved in ztmp/prompt_hist.csv
          --> Pick up manually promptid from ztmp/prompt_hist.csv


  ### Generate synthetic from specific Prompt-id (using default promptStorage path)
     python rag/query.py generator_syntheticquery --dataset "ag_news" --nfile 70 --nquery 100 --prompt_id "20240507-671"

          -->  saves queries in ztmp/bench/ag_news/query/df_synthetic_queries_{dt}.parquet

          export dirquery="ztmp/bench/ag_news/query/df_synthetic_queries_20240509_171632.parquet" 



############################################################################################
###### Benchmark Engine  ###################################################################
    export PYTHONPATH="$(pwd)"
    alias pybench=" python3 -u rag/bench.py ";
    function echo2() { echo -e "$1" >> zresults.md; }


#### Prepare parquet data to feed Engine Indexes 
   # pybench bench_v1_data_convert  --dirin "./ztmp/hf_dataset/ag_news/"    --dirout "./ztmp/bench/ag_news"


#### Create Engine Indexes for later retrieval
   dataset=="ag_news"
   dirdata="ztmp/bench"

   ### Load data from f"ztmp/bench/norm/ag_news/" 
   pybench bench_v1_create_sparse_indexes  --dirdata_root $dirdata

   pybench bench_v1_create_dense_indexes   --dirdata_root $dirdata

   pybench bench_v1_create_tantivy_indexes --dirdata_root $dirdata



#### Generate bechnmark of retrieval engine using query file.

    dirquery="ztmp/bench/ag_news/query/df_synthetic_queries_20240509_171632.parquet" 

    echo2 `date`
    echo2 "\`\`\`" ;

    echo2 "### dense run"
    pybench bench_v1_dense_run   --dirquery $dirquery  >> zresults.md

    
    echo2 "### sparse run"
    pybench bench_v1_sparse_run  --dirquery $dirquery  >> zresults.md;
    
    echo2 "### tantivy run"
    pybench bench_v1_tantivy_run --dirquery $dirquery  >> zresults.md;


    echo2 "\`\`\`"
    echo2 "---" 



#### Create Analysis report
    pybench create_error_report --dirin "ztmp/bench/"  --dataset $dataset --dirquery $dirquery 






###### kg search #################################################################################

    ### Nebula KG DB
        cd asearch
        export PYTHONPATH="$(pwd)"  ### relative import issue
        alias pykg="python3 -u rag/engine_kg.py  "

        ###############################################
        #### Create test data using Wikipedia/LlamaIndex
           pykg test_create_test_data --dirout ztmp/kg/testraw.csv
                
        ### Extract  triplets From raw text and save to csv 
           pykg  kg_model_extract --dirin myraw.csv --model_id Babelscape/rebel-large -- dirout ztmp/kg/data/kg_relation.csv
        

        ### Extract the triplet from  agnews Data --> Store in csv file  ( Need Rebel-Large to prevent empty triplet....)
           pykg  kg_model_extract --model_id Babelscape/rebel-large  --dirin ztmp/bench/norm/ag_news/test/df_*.parquet  --dirout ztmp/kg/data/agnews_kg_relation_test.csv --coltxt body --nrows 1000000 --batch_size 25 


        ###############################################
        ##### Create schema : in Nebula   DB
             pykg nebula_db_create_schema  --space_name kg_relation

        ##### insert triplets to Nebula Graph
             pykg  nebula_db_insert_triplet_file --dirin ztmp/kg/data/kg_relation.csv   --space_name kg_relation


        ##### search kg:  using LlamaIndex and nebula Graph
             pykg nebula_db_query --space_name "agnews_kg_relation" --query "What is the capital of mexico ?"


        ################################################
        # generate Query from Inverting from triplets (using LlamaIndex and GPT3.5 )
           pykg kg_generate_questions_from_triplets --dirin ztmp/kg/data/agnews_kg_relation.csv --dirout ztmp/kg/data/agnews_kg_questions.csv --batch_size 20

        # benchmark queries using Nebula Graph
           pykg kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_questions.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=1000



        ###############################################
        ## neo4j insert
            pykg neo4j_db_insert_triplet_file --dirin ztmp/kg/data/kg_relation.csv --db_name "neo4j"  --nrows -1




     #### Neo4j Install
        installation steps (https://neo4j.com/docs/operations-manual/current/installation/linux/tarball/):
                1. Download tar file from https://neo4j.com/deployment-center
                2. tar zxf neo4j-enterprise-5.19.0-unix.tar.gz
                3. mv neo4j-community-5.19.0 /opt/
                ln -s /opt/neo4j-community-5.19.0 /opt/neo4j
                4.  groupadd neo4j
                    useradd -g neo4j neo4j -s /bin/bash
                5. chown -R neo4j:adm /opt/neo4j-community-5.19.0

                Run in background:
                1. /opt/neo4j/bin/neo4j start
                2. Web UI: http://localhost:7474

        docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs neo4j:4.4.34-community

        http://localhost:7474/browser/
           neo4j / neo4j


     #### Insert / Query sample with neo4J
        export PYTHONPATH="$(pwd)"  ### relative import issue
        alias pykg=" python3 -u rag/engine_kg.py ";


        # extract triplets from dataset and store to csv
        pykg kg_model_extract --dirin "ztmp/bench/norm/ag_news/*/*.parquet", model_id="Babelscape/rebel-large", dirout="ztmp/kg/data/kg_relation.csv",
                            nrows=100000,
                            colid="id", coltxt="text"): 

        # store dataset id, text in localdb
        pykg localstorage_save_records_to_db --dirin "ztmp/bench/norm/ag_news/*/*.parquet" --table_name "agnews" --coltext "body" --colid "id"



        # create neo4j db with constraints
        pykg neo4j_create_db --db_name "neo4j"


        # store triplets along with doc_ids in neo4j db
        pykg neo4j_db_insert_triplet_file --dirin "ztmp/kg/data/kg_relation.csv" --db_name "neo4j"

        # search documents in neo4j
        pykg neo4j_search_docs --db_name "neo4j" --query "Who visited Chechnya?"




```
