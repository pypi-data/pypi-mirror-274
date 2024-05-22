"""
    #### Install
        # NEbula installation
        Option 0 for machines with Docker: `curl -fsSL nebula-up.siwei.io/install.sh | bash`
        Option 1 for Desktop: NebulaGraph Docker Extension https://hub.docker.com/extensions/weygu/nebulagraph-dd-ext


    #### USAGE:
        alias pykg="python3 -u engine_kg.py  "

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






   ### Docs
      Good Recipes for KG building
       https://faircookbook.elixir-europe.org/content/recipes/interoperability/nlp2kg/creating-knowledge-graph-from-text.html

   ### TODO :
      We want to fetch some documents ID, related to the triplet of the initial Question.

        Current with LllamaIndex :
             Natural Query --> NebulaGraph Cypher query --> Response in triplet --> Converted back in Natural questions (hallucination)


        ----> Use KG as Document Retriever (instead)
        What we to do (ie integrate with other engine)
             Natural Query --> NebulaGraph Cypher query --> Response in triplet 
                    --> Add the document related to triplets. ????

               (triplet:  (Person, president, Country) ) ---> List of Doc_id per triplet. (list)

                Check in Nebula to find doc_id related to triplet

                    Or we do external storage (ie parquet or sqlmy, duckdb like sqlite).


         A) Goal attache doc_id to the edge A --> B : when can we can retrieve doc_id for the RAG part (as retriever)

         B) You are saying:   we need just to retrieve the triplets directly from the KG query.

             Open discussion, dont worry:  Be good or bad, --> to find something reasonable.

           --> difference is
                  A) we have dense text (ie full sentences)  to feed the LLM.
                  B) we have only the relation  A do B) : "sparse info"  for the LLM.

                  LLnm is better at transforming Dense text.

            My end goal is 
              Use LLM with this prompt
                     you are a writer.

                     Reply to the question
                          { my question }

                     Using ONLY the context below
                          { context from RAG}     
                                Doc_id --> Dense text all concatenated.

                                Graph -->  Sparse ()

           Did not have time to google search/phind how other people are doing....

           How LlamaIndex does ???
               Query to feed the LLM: ???

                  List of Triplets, (by keywords)  --> Graph Schema and the records as below

                  In the LLM prompt

                     { queestion}

                     {graph Schema} : All the relations and node type defintion.

                     {List of triples}

                   --> enough for LLm to repply...


            I think from my experience:
               graph DB can be used in both ways:
                   1) Only triplets and provide the grpah triple to LLM.

                   2) Dense Doc_id retriever and provide the doc_id + text to LLM.
                         Search Engine can be useful.

                    Investigate quickly and propose  a  simple plan
                       1)
                       2)
                       3)

                    will create different milestone     


             Issues is the database
                Nebulagraph looks incomplete, lack of funcitionnalities

                Neo4J : old DB but full of funcitonnalities + community support for the bugs/workaround
                         (ie slower)

                 Need to check 
                 You can ask phind to convert stuff...


                 Just double check if Neo4J can accept docid to the edge...

                 List of edges --> docid    simple merge ( --> re-rank by frequency --> take top-10 docis)















                       




   ### Insert agnews, create some test queries

       "what is the capital of mexico ?"

        Method 1:
            ---> Go by the triple extractor,  ---> get some triplet --> query directly the triple


        def kg_query_...


        Method 2:
            ---> Extract keyword :
                    capital, mexico






    #### Goal to small proptopye of KG retrieval

    A) Indexer :  Extract Triplet (A, relation, B) from raw text --> store in database/NebulaGraph
                Alot of connected keyword. : normalize keywords, extra triplets


    B) query  :
        query --> extract keyword from query --> search in KG datas using keyword and relation around keyword
                --> hybrid with emebdding  -->

    ####
    Groq Engine : Cloud service Host llama3, 
        very fast very cheap,  500 token/seconds,  Alternative to GPT 3.5  (cheaper/faster)

        



    ######################################################################################################
    #### Entity Extractor :

    https://github.com/zjunlp/DeepKE

    https://github.com/thunlp/OpenNRE

    https://github.com/zjunlp/KnowLM

    https://maartengr.github.io/BERTopic/getting_started/representation/representation.html#maximalmarginalrelevance

    
    
    1)
    Llamax -- use LLM + Prompt

    2) BERt like model to extract.(faster/cheaper) 
    https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa

    pre-trained model.  --> with huggingFae directlyt.
        https://huggingface.co/Babelscape/mrebel-large


    3) ... NER extraction...


    
    Llama Index --> Nebula Graph




    without LLM, one way:
    https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa


    ####Groq is cheap/Fast for Llama3 Enitry extraction
        https://towardsdatascience.com/relation-extraction-with-llama3-models-f8bc41858b9e



    #### Questions Pairs
        https://huggingface.co/datasets/databricks/databricks-dolly-15k



    REBEL model

    https://huggingface.co/Babelscape/mrebel-large




    Building  KG graph index is  trickier part....

    https://github.com/wenqiglantz/llamaindex_nebulagraph_phillies/tree/main

    https://towardsdatascience.com/12-rag-pain-points-and-proposed-solutions-43709939a28c



    hacked  coedium engine to access by CLI (ie auto generate  docstring)


"""

if "import":
    import os, time, traceback, warnings, logging, sys, sqlite3
    from collections import Counter

    warnings.filterwarnings("ignore")

    import json, warnings, spacy, pandas as pd

    ### KG
    from nebula3.Config import Config
    from nebula3.gclient.net import ConnectionPool
    from nebula3.common import *
    from neo4j import GraphDatabase

    # NLP
    from transformers import (pipeline)
    import spacy

    nlp = spacy.load("en_core_web_sm")

    ############################################
    from rag.query import llm_get_answer

    from utils.utils_base import torch_getdevice, pd_append

    ## Uncomment this section for llamaindex llm call logs
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    import llama_index.core

    llama_index.core.set_global_handler("simple")

    ############################################
    from utilmy import pd_read_file, os_makedirs, pd_to_file
    from utilmy import log


################################################################################
def test_create_test_data(dirout="./ztmp/testdata/myraw.csv"):
    """
    usage: pythpn3 -u enging_kg test_create_test_data --dirout myraw.csv
    """
    from llama_index.readers.wikipedia import WikipediaReader
    loader = WikipediaReader()
    documents = loader.load_data(
        pages=["Guardians of  Galaxy Vol. 3"], auto_suggest=False
    )
    text_list = documents[0].text.split("\n")
    # remove short lines
    text_list = [text for text in text_list if len(text) > 20]
    text_df = pd.DataFrame(text_list, columns=["text"], dtype=str)
    pd_to_file(text_df, dirout, show=1)


def test0():
    triplet_extractor = pipeline('translation_xx_to_yy', model='Babelscape/mrebel-base',
                                 tokenizer='Babelscape/mrebel-base')

    # We need to use  tokenizer manually since we need special tokens.
    msg = " Red Hot Chili Peppers were formed in Los Angeles by Kiedis, Flea"
    extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(msg,
                                                                                 src_lang="en", return_tensors=True,
                                                                                 return_text=False)[0][
                                                                   "translation_token_ids"]])  # change __en__ for  language of  source.
    print(extracted_text[0])


################################################################################
class TripletExtractorModel:
    def __init__(self, model_id='Babelscape/rebel-large', model_type="mrebel"):
        """Initializes  TripletExtractorModel with  specified model_id and model_type.
         Args:
            model_id (str):  ID of  model to be used. Default is 'Babelscape/rebel-large'.
            model_type (str):  type of  model. Default is "mrebel".

        """
        self.model_id = model_id
        self.model_type = model_type

        if model_type == "mrebel":
            s_time = time.time()
            device = torch_getdevice()
            self.pipeline = pipeline('text2text-generation', model=model_id,
                                     tokenizer=model_id, device=device)
            log(f"Model loaded in {time.time() - s_time:.2f} seconds")
        else:
            raise ValueError(f"Invalid model type: {model_type}")

    def extract_triplets(self, text) -> list:
        """Extracts triplets from  given text.

        Args:
            text (str):  text from which to extract triplets.

        Returns:
            list: A list of dictionaries representing  extracted triplets. 
            Each dictionary contains  keys 'head', 'type', and 'tail', representing  subject, predicate, and object of  triplet.

        """
        triplets = []
        relation, subject, relation, object_ = '', '', '', ''
        text = text.strip()
        current = 'x'
        for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
            if token == "<triplet>":
                current = 't'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                    relation = ''
                subject = ''
            elif token == "<subj>":
                current = 's'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                object_ = ''
            elif token == "<obj>":
                current = 'o'
                relation = ''
            else:
                if current == 't':
                    subject += ' ' + token
                elif current == 's':
                    object_ += ' ' + token
                elif current == 'o':
                    relation += ' ' + token
        if subject != '' and relation != '' and object_ != '':
            triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
        return triplets

    def extract(self, text_list: list) -> list:
        """Extracts information from a list of texts and returns a list of extracted triplets.
        
         Args:
            text_list (list): A list of texts for which information needs to be extracted.
        
        Returns:
            list: A list of extracted triplets containing  head, type, and tail of each triplet.
        """

        result = []
        from datasets import Dataset
        data = {
            'id': list(range(len(text_list))),
            'text': text_list
        }
        dataset = Dataset.from_dict(data)
        # print(dataset)
        extracted_text = self.pipeline.tokenizer.batch_decode([x["generated_token_ids"] for x in self.pipeline(
            dataset["text"],
            return_tensors=True, return_text=False)])
        # print(f"extracted_text: {extracted_text}")
        result = [[] for _ in range(len(extracted_text))]
        for i, text in enumerate(extracted_text):
            triplet = self.extract_triplets(text)
            result[i].extend(triplet)
        return result


class SpacyTripletExtractorModel:

    def __init__(self, model_id='Babelscape/rebel-large'):
        self.model_id = model_id
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("rebel", after="senter", config={
            'device': -1,  # Number of the GPU, -1 if want to use CPU
            'model_name': model_id}  # Model used, will default to 'Babelscape/rebel-large' if not given
                          )

    def post_process(self, extracted_triplets):
        post_processed = []
        for triplet in extracted_triplets:
            p_triplet = {}
            p_triplet['head'] = triplet['head_span'].lemma_  # span => lemmatized str
            p_triplet['tail'] = triplet['tail_span'].lemma_  # span => lemmatized str
            p_triplet['type'] = triplet['relation']  # already str
            post_processed.append(p_triplet)
        return post_processed

    def extract(self, text_list: list) -> list:
        result = []
        docs = self.nlp.pipe(text_list)
        for doc in docs:
            for value, rel_dict in doc._.rel.items():
                result.append(rel_dict)

        result = self.post_process(result)
        return result


def kg_model_extract(dirin="myraw.csv", model_id="Babelscape/rebel-large", dirout="ztmp/data/kg_relation.csv",
                     nrows=100000,
                     colid="id", coltxt="text"):
    """
    usage: pykg kg_model_extract --dirin myraw.csv --model_id Babelscape/rebel-large -- dirout data/kg_relation.csv
    Processed docs/Time taken:
    10/5.56 seconds
    20/9.66 seconds
    30/14.06 seconds
    """
    dfraw = pd_read_file(dirin)
    assert coltxt in dfraw.columns
    # pick nrows rows from df
    doc_ids = dfraw[colid].values.tolist()
    dfraw = dfraw[:nrows]
    txt_list = dfraw[coltxt].values.tolist()
    extractor = TripletExtractorModel(model_id=model_id, model_type="mrebel")
    # extractor = SpacyTripletExtractorModel(model_id=model_id)
    extracted_triplets = extractor.extract(txt_list)

    # log(f"len(extracted_triplets): {len(extracted_triplets)}")
    result = zip(doc_ids, extracted_triplets)
    kg_relation_save(result, dirout=dirout)


def kg_relation_save(doc_id_triplets, dirout="data/kg_relation.csv"):
    if os.path.exists(dirout):
        df = pd_read_file(dirout)
        df = df[['doc_id', 'head', 'type', 'tail', "info_json"]]
    else:
        df = pd.DataFrame(columns=['doc_id', 'head', 'type', 'tail', "info_json"])

    row_list = []
    for doc_id, triplets in doc_id_triplets:
        for triplet in triplets:
            row_list.append([doc_id, triplet["head"], triplet["type"], triplet["tail"], triplet.get("info_json", {})])

    df = pd_append(df, row_list)
    df = df.drop_duplicates(subset=['doc_id', 'head', 'type', 'tail'], keep='first')
    pd_to_file(df, dirout, show=1, index=False)


######################################################################################################
#######  DB Nebula Graph #############################################################################
def test_nebula_db_insert_triplet_file():
    """ A function to test if data is inserted into KKG DB

    """
    # check if data is inserted
    space_name = "test_kg_relation"
    client = nebula_db_get_client()
    nebula_db_create_schema(client=client, space_name=space_name)
    time.sleep(10)

    resp = client.execute(f"USE {space_name};")
    nebula_db_insert_triplet_file(dirin="data/kg_relation.csv", space_name=space_name, nrows=10)
    time.sleep(10)

    resp_json = client.execute_json(f"MATCH (s)-[e]->(o) RETURN count(e) as count;")
    json_obj = json.loads(resp_json)
    # {'errors': [{'code': 0}], 'results': [{'spaceName': 'test_kg_relation', 'data': [{'meta': [None], 'row': [10]}], 'columns': ['count'], 'errors': {'code': 0}, 'latencyInUs': 4081}]}
    assert json_obj["results"][0]["data"][0]["row"][0] == 10
    # drop space
    resp = client.execute(f"DROP SPACE {space_name};")


def nebula_db_get_client(engine_name="nebula"):
    config = Config()
    connection_pool = ConnectionPool()
    assert connection_pool.init([('127.0.0.1', 9669)], config)
    # get session from  pool
    client = connection_pool.get_session('root', 'nebula')
    assert client is not None
    return client


def nebula_db_create_schema(client=None, space_name="kg_relation"):
    if client is None:
        client = nebula_db_get_client()
    resp = client.execute(
        f"CREATE SPACE {space_name}(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);"
        f"USE {space_name};"
        "CREATE TAG entity(name string);"
        "CREATE EDGE relationship(relationship string);"
        "CREATE TAG INDEX entity_index ON entity(name(256));"
    )
    assert resp.is_succeeded(), resp.error_msg()


def nebula_db_insert_triplet(client=None, space_name="kg_relation", row=None):
    """
    Findings:
    https://docs.nebula-graph.io/2.6.1/3.ngql-guide/3.data-types/6.list/#opencypher_compatibility
    A composite data type (i.e., set, map, and list) CAN NOT be stored as properties for vertices or edges.
    It is recommended to modify the graph modeling method.  composite data type should be modeled as an adjacent edge of a vertex, rather than its property. Each adjacent edge can be dynamically added or deleted.  rank values of the adjacent edges can be used for sequencing.


    """
    resp = client.execute(f"USE {space_name};")
    assert resp.is_succeeded(), resp.error_msg()

    vertex_query = f"""INSERT VERTEX entity(name) VALUES "{row.head}":("{row.head}"), "{row.tail}":("{row.tail}")"""
    # log(vertex_query)
    resp = client.execute(vertex_query)
    assert resp.is_succeeded(), resp.error_msg()

    # edge query
    edge_query = f"""INSERT EDGE relationship(relationship) VALUES "{row.head}"->"{row.tail}":("{row.type}")"""

    # log(edge_query)
    resp = client.execute(edge_query)
    assert resp.is_succeeded(), resp.error_msg()


def nebula_db_insert_triplet_file(dirin="data/kg_relation.csv", space_name="kg_relation", nrows: int = -1):
    """

    """
    df = pd_read_file(dirin)
    nrows = len(df) if nrows < 0 else nrows

    # create nebula client
    client = nebula_db_get_client()
    assert client is not None

    log("#### create schema ")
    client.execute(f"""USE {space_name};""")

    log("#### insert ")
    for row in df[:nrows].itertuples():
        nebula_db_insert_triplet(client=client, space_name=space_name, row=row)


##############  Query DB   
def nebula_db_query(space_name="agnews_kg_relation", query="", db_type="nebula"):
    """A function to query the knowledge graph database with the specified space name and query string.

    LlamaIndex uses LLM GPt3.5
          Naturaal Query ---> KG Nebula queries.
          Required OPENAI TOKEN in env variable.
          
        Digged deeper into llama-index query calls.
        For each query it is calling llm 2 times:
        1. Extract keywords from llm query
        2. Fetch answer from db output triplets


    Issues: LLM is called every time to convert Natural Queries --> KG Nebula queries

            Find a way to generate Nebula query from llama Index.



    Args:
    - space_name (str):  name of the space in the knowledge graph database to query.
    - query (str):  query string to search in the knowledge graph.

    """
    from llama_index.core import KnowledgeGraphIndex, StorageContext
    from llama_index.graph_stores.nebula import NebulaGraphStore

    if not query:
        return

    edge_types, rel_prop_names = ["relationship"], ["relationship"]
    tags = ["entity"]

    ### Init Databse
    # expects NEBULA_USER, NEBULA_PASSWORD, NEBULA_ADDRESS in environment variables
    graph_store = NebulaGraphStore(
        space_name=space_name,
        edge_types=edge_types,
        rel_prop_names=rel_prop_names,
        tags=tags,

    )
    # create storage context
    storage_context = StorageContext.from_defaults(graph_store=graph_store, )

    # fetch KG database index
    index = KnowledgeGraphIndex.from_documents(
        [],
        storage_context=storage_context,
        max_triplets_per_chunk=2,
        space_name=space_name,
        edge_types=edge_types,
        rel_prop_names=rel_prop_names,
        tags=tags,
    )
    query_engine = index.as_query_engine()

    # llm call here. adds network overhead to each query
    ### LLM is called to generate the Natural query --> KG Query
    response = query_engine.query(query)
    return response.response





######################################################################################################
##############  NEO4J DB   ###########################################################################
def neo4j_create_db(db_name="neo4j"):
    """Creates a Neo4j database with the specified name.
    Args:
        db_name (str, optional):  name of the Neo4j database. Defaults to "neo4j".
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


    """
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "hell0neo")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        # create db
        # Note: community edition supports only single database
        # query = f"CREATE DATABASE {db_name} IF NOT EXISTS;"
        # add constraint to avoid duplicates
        # driver.execute_query(query_=query)
        query = f"CREATE CONSTRAINT FOR (n:Entity) REQUIRE n.name IS UNIQUE;"
        driver.execute_query(query_=query, database_=db_name)


def neo4j_db_insert_triplet_file(dirin="ztmp/kg/data/kg_relation.csv", db_name="neo4j", nrows: int = -1):
    """Inserts triplets from a CSV file into a Neo4j database.
  
       #triples: 1627, total time taken : 8.34 seconds  

       Args:
            dirin (str, optional):  path to the CSV file containing the triplets. Defaults to "ztmp/data/kg_relation.csv".
            db_name (str, optional):  name of the Neo4j database. Defaults to "neo4j".
            nrows (int, optional):  number of rows to process from the CSV file. Defaults to -1 (process all rows).

        Returns:
            None: If an exception occurs during the execution of the query.
    """
    df = pd_read_file(dirin)
    nrows = len(df) if nrows < 0 else nrows

    from neo4j import GraphDatabase

    URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
    # expects NEO4J_USERNAME and NEO4J_PASSWORD in env
    AUTH = (os.environ.get("NEO4J_USERNAME", "username"), os.environ.get("NEO4J_PASSWORD", "password"))
    s_time = time.time()
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for row in df[:nrows].itertuples():
            # pro: single query for all insertions
            # con: docids may contain duplicates
            query = f"""
                    MERGE (head:Entity {{name: "{row.head}"}})
                    ON CREATE SET head.name = "{row.head}"
                    MERGE (tail:Entity {{name: "{row.tail}"}})
                    ON CREATE SET tail.name = "{row.tail}"
                    MERGE (head)-[relation:Relationship {{name: "{row.type}"}}]->(tail)
                    ON CREATE 
                        SET 
                            relation.docids = ["{row.doc_id}"]
                    ON MATCH 
                        SET 
                            relation.docids = relation.docids + ["{row.doc_id}"]
                    """
            # pro: keeps docids unique in db
            # con: run 2 queries for 1 insertion
            # check if relation already exists
            # query = f"MATCH (n:Entity {{id: '{head}'}})-[r:RELATIONSHIP {{name: '{relation}'}}]->(m:Entity {{id: '{tail}'}}) RETURN r"
            # result, _, _ = driver.execute_query(query_=query, database_="neo4j")
            # if len(result) > 0:
            #     # print(result[0]["r"]["docids"])
            #     if docid not in result[0]["r"]["docids"]:
            #         # update relationship with new docid
            #         query = f"MATCH (n:Entity {{id: '{head}'}})-[r:RELATIONSHIP {{name: '{relation}'}}]->(m:Entity {{id: '{tail}'}}) SET r.docids = r.docids + [{docid}] RETURN r"
            #         driver.execute_query(query_=query, database_="neo4j")
            #     return
            #
            # query = f"""CREATE (e1:Entity {{id: '{head}'}}),
            # (e2:Entity {{id: '{tail}'}}),
            # (e1)-[:RELATIONSHIP {{name: '{relation}', docids: {[docid]}}}]->(e2);"""

            # print(query)
            try:
                driver.execute_query(query_=query, database_=db_name)
            except Exception as err:
                print(traceback.format_exc())
                print(query)
                return

        log(f" #triples: {nrows}, total time taken : {(time.time() - s_time):.2f} seconds")


def neo4j_search_db_by_keywords(db_name="neo4j", keywords: list = None):
    from neo4j import GraphDatabase
    query = f"""
            WITH {keywords} AS keywords
            MATCH (entity1)-[rel]-(entity2)
            WHERE any(keyword IN keywords WHERE entity1.name CONTAINS keyword OR entity2.name CONTAINS keyword OR type(rel) CONTAINS keyword)
            RETURN entity1, rel, entity2
    """
    # log(query)
    URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
    # expects NEO4J_USERNAME and NEO4J_PASSWORD in env
    AUTH = (os.environ.get("NEO4J_USERNAME", "username"), os.environ.get("NEO4J_PASSWORD", "password"))
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        s_time = time.time()
        records, summary, keys = driver.execute_query(query_=query, database_=db_name)
        log(f"#results={len(records)}, neo4j query took: {time.time() - s_time:.2f} seconds")
        return records


def neo4j_get_doc_ids_from_results(results: list, topk: int = -1) -> list:
    """
    Get the document IDs from the neo4j results.
    Args:
        results (list): A list of tuples containing the results.
        topk (int, optional):  maximum number of document IDs to return. Defaults to -1, which returns all document IDs.

    Returns:
        list: A list of document IDs.
    """
    doc_ids = []
    # log(f"len(results): {len(results)}")
    for ent1, rel, ent2 in results:
        r_docids = list(set(rel._properties["docids"]))
        doc_ids.extend(r_docids)
    docid_counter = Counter(doc_ids)
    # log(docid_counter)
    if topk == -1:
        topk = len(docid_counter)

    ### Scoring of doc_id by frequency.    
    doc_ids = [(k, v) for k, v in docid_counter.most_common(topk)]
    return doc_ids


def localdb_fetch_text_by_doc_ids(db_name="datasets.db", table_name: str = "agnews", doc_ids: list = None) -> list:
    """
    Fetches the text from a local SQLite database based on the given document IDs.

    Parameters:
        db_name (str):  name of the SQLite database file. Defaults to "datasets.db".
        table_name (str):  name of the table in the database. Defaults to "agnews".
        doc_ids (list):  list of document IDs to fetch the text for. Defaults to None.

    Returns:
        list: A list of text strings corresponding to the fetched document IDs.

    """
    conn = sqlite3.connect(f"ztmp/local/{db_name}")
    c = conn.cursor()

    doc_ids = tuple([str(docid) for docid in doc_ids])
    # log(doc_ids)
    query = f"SELECT id, text FROM {table_name} WHERE id IN {doc_ids}"
    # log(query)
    c.execute(query)
    headers = c.description
    results = c.fetchall()
    # zip headers with results
    results = [{headers[i][0]: row[i] for i in range(len(headers))} for row in results]
    # convert results to dict
    conn.close()
    return results


def neo4j_search_docs(db_name="neo4j", query: str = ""):
    """Performs a search of (docid, doc_text) in a Neo4j database based on the given query.

    Args:
        db_name (str, optional):  name of the Neo4j database. Defaults to "neo4j".
        query (str, optional):  search query. Defaults to "".

    Returns:
        list: A list of dictionaries representing the search results. Each dictionary contains the following keys:
            - "id" (str):  ID of the document.
            - "text" (str):  text content of the document.
            - "score" (float):  score indicating the relevance of the document to the search query.

    Notes:
        query -->Keyword extraction --> Build a cypher query based on those keywords 
                --> Send the cypher query to neo4j
                ---> Get the triplets
                --> Extract the doc_id for each triplet, Score(doc_id)= Frequency of found triplet.
                --> Rank the doc by score
                --> Fetch actual text from the doc_id using SQL, Sqlite.
                    --> return results SAME Format than Qdrant, tantiviy Engine
                            Engine 
                            TODO: Official return Format as DataClass

        TODO: Need to have a global SpacyModel to prevent reload each search.
           Global Class Instance.
              global spacyModel
              spacyModel = None ### at Import level

              if spacyModel is None:
                spacyModel = SpaceyModel("en_core_web_sm")



        -  search is performed by extracting keywords from the query using the `nlp_extract_keywords_from_text` function.
        -  search is performed in the specified Neo4j database using the `neo4j_search_db_by_keywords` function.
        -  search results are processed to retrieve the document IDs and their corresponding scores using the `neo4j_get_doc_ids_from_results` function.
        -  text content of the documents is fetched from a local database using the `localdb_fetch_text_by_doc_ids` function.
        -  relevance scores are assigned to the records.
        -  records are sorted based on the relevance scores in descending order.

    Example:
        >>> neo4j_search_docs(db_name="my_database", query="search query")
        [
            {
                "id": "document1_id",
                "text": "document1_text",
                "score": 8
            },
            {
                "id": "document2_id",
                "text": "document2_text",
                "score": 6
            },
            ...
        ]
    """
    keywords = nlp_extract_keywords_from_text(query)
    results  = neo4j_search_db_by_keywords(db_name=db_name, keywords=keywords)
    doc_id_score_tuple = neo4j_get_doc_ids_from_results(results)
    # log(doc_ids)

    docid_score_map = {k: v for k, v in doc_id_score_tuple}
    doc_ids = [doc_id for doc_id, _ in doc_id_score_tuple]
    records = localdb_fetch_text_by_doc_ids(doc_ids=doc_ids)
    for record in records:
        record["score"] = docid_score_map[record["id"]]
    records = sorted(records, key=lambda x: x["score"], reverse=True)
    # log(records)
    return records




###########################################
def nlp_extract_keywords_from_text(text: str) -> list:
    """
    Extracts keywords from the given text using Natural Language Processing (NLP).
    Args:
        text (str):  input text from which keywords will be extracted.

    Returns:
        list: A list of keywords extracted from the text.


    TODO:
        Make a class for Spacy model and use it.


    """
    doc = nlp(text)
    keywords = [nc.text for nc in doc.noun_chunks]
    return keywords


class SpacyModel:
    def __init__(self, model_id="en_core_web_sm"):
        self.model_id = model_id
        self.nlp      = spacy.load(model_id)
        # self.nlp.add_pipe("rebel", after="senter", config={
        ##    'device': -1,  # Number of the GPU, -1 if want to use CPU
        #    'model_name': model_id}  # Model used, will default to 'Babelscape/rebel-large' if not given
        #                  )

    def post_process(self, extracted_triplets):
        post_processed = []
        # for triplet in extracted_triplets:
        #     p_triplet = {}
        #     p_triplet['head'] = triplet['head_span'].lemma_  # span => lemmatized str
        #     p_triplet['tail'] = triplet['tail_span'].lemma_  # span => lemmatized str
        #     p_triplet['type'] = triplet['relation']  # already str
        #     post_processed.append(p_triplet)
        return post_processed

    def extract_keywords(self, text_list: list) -> list:
        result = []
        docs = self.nlp.pipe(text_list)

        for doc in docs:
            keywords = [nc.text for nc in doc.noun_chunks]
            result.extend(keywords)
        # result = self.post_process(result)
        return result





#######  doc_id Storage  ###########################################################################
def localstorage_table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    existing_tables = [row[0] for row in cursor.fetchall()]
    return table_name in existing_tables


def localstorage_create_table(conn, table_name):
    # conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR(255) PRIMARY KEY,
            text TEXT
        )
    """)

    conn.commit()
    # conn.close()


def localstorage_save_records_to_db(dirin="ztmp/bench/norm/ag_news/*/*.parquet", 
                                    db_path="./ztmp/local/datasets.db",
                                    table_name="agnews", coltext="body",
                                    colid="id"):
    record_df = pd_read_file(dirin)
    record_df = record_df[[colid, coltext]]
    print(len(record_df))
    # create mysqlite instance
    os_makedirs("ztmp/local" )

    conn = sqlite3.connect(f"{db_path}")
    if localstorage_table_exists(conn, table_name) is False:
        localstorage_create_table(conn, table_name)

    # record_df.to_sql(table_name, conn, if_exists="append", index=False)
    record_df = record_df.rename(columns={colid: "id", coltext: "text"})
    record_df["id"] = record_df["id"].astype("string")
    record_df.to_sql(table_name, conn, if_exists="append", index=False, chunksize=1000)






######################################################################################################
#######  Query generator from KG db triplet ##########################################################
def kg_generate_questions_from_triplets(dirin="ztmp/kg/data/agnews_kg_relation_test.csv",
                                        dirout="ztmp/kg/data/agnews_kg_question.csv", nrows: int = 1000,
                                        batch_size: int = 20):
    """
    Generate questions based on triplets extracted from a file and save them to a new CSV file.

    :param dirin: Input file path containing triplets, default is "ztmp/kg/data/agnews_kg_relation_gpu.csv"
    :param dirout: Output file path to save the generated questions, default is "data/agnews_kg_question.csv"
    """
    df = pd_read_file(dirin)

    df = df[["head", "type", "tail"]]
    # remove duplicates
    df = df.drop_duplicates()
    # take first nrows
    df = df[:nrows]

    result_df = pd.DataFrame(columns=["head", "type", "tail", "question"])
    for i in range(0, len(df), batch_size):
        df_subset = df[i:i + batch_size]

        ####   |head|type|tail   |head|type|tail   
        triplet_str = "\n".join([f"{'|'.join([row.head, row.type, row.tail])}" for row in df_subset.itertuples()])
        # generate question using llm
        prompt = f"For each triplet, generate a question based on the triplet(head|type|tail):\n{triplet_str}"
        # print(f"prompt: {prompt}")

        response = llm_get_answer(prompt, model="gpt-3.5-turbo", max_tokens=1000)
        questions = response.split("\n")

        # clean up : remove preceeding numerical number
        questions = [q.split(".")[1].strip() if "." in q else q for q in questions]
        if len(questions) == len(df_subset):
            df_subset["question"] = questions
            result_df = pd.concat([result_df, df_subset])

    pd_to_file(result_df, dirout, index=False)




######################################################################################################
#######  Metrics /benchmark ##########################################################
def metrics_kg_is_triplet_covered(triplet_tuple, question, answer):
    return all([k in question or k in answer for k in triplet_tuple])


def kg_benchmark_queries(dirin="ztmp/kg/data/agnews_kg_question.csv",
                         dirout="ztmp/kg/data/agnews_kg_benchmark.csv",
                         queries=1000):
    """
    Average time taken per query: 1.82 seconds
        Accuracy: 80% 

    """
    question_df = pd_read_file(dirin)
    result = []
    for row in question_df[:queries].itertuples():
        s_time = time.time()
        response = nebula_db_query(query=row.question)
        dt = time.time() - s_time

        is_correct = metrics_kg_is_triplet_covered([row.head, row.tail], row.question, response)
        result.append([row.question, response, dt, is_correct])

    df = pd.DataFrame(result, columns=["question", "response", "dt", "is_correct"])
    pd_to_file(df, dirout, index=False, show=1)
    log(f" Average time taken: {df.dt.mean():.2f} seconds")
    log(f" Percentage accuracy: {df.is_correct.mean() * 100:.2f} %")


###################################################################################################
if __name__ == "__main__":
    import fire

    fire.Fire()
    # results = neo4j_search_db_by_keywords(db_name="neo4j", keywords=["Casio Computer", 'magazine', 'United States'])
    # print(results)
    # df = pd_read_file("ztmp/bench/norm/ag_news/test/df_1.parquet")
    # print(df["id"])

#####################
# def zzz_query_using_llamaindex():
#     """
#         https://medium.com/@sauravjoshi23/building-knowledge-graphs-rebel-llamaindex-and-rebel-llamaindex-8769cf800115
#
#
#         # CREATE SPACE rebel_llamaindex(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);
#         # :sleep 10;
#         # USE rebel_llamaindex;
#         # CREATE TAG entity(name string);
#         # CREATE EDGE relationship(relationship string);
#         # CREATE TAG INDEX entity_index ON entity(name(256));
#
#     """
#
#
#     from llama_index.query_engine import KnowledgeGraphQueryEngine
#
#     from llama_index.storage.storage_context import StorageContext
#     from llama_index.graph_stores import NebulaGraphStore
#
#
#     from llama_index import SimpleDirectoryReader
#
#     reader = SimpleDirectoryReader(input_dir="../data/knowledge graphs/rebel_llamaindex/wiki/")
#     documents = reader.load_data()
#
#     kg_index = KnowledgeGraphIndex.from_documents(
#         documents,
#         storage_context=storage_context,
#         max_triplets_per_chunk=5,
#         service_context=service_context,
#         space_name=space_name,
#         edge_types=edge_types,
#         rel_prop_names=rel_prop_names,
#         tags=tags,
#         include_embeddings=True,
#     )
#
#
#
#     query_engine = KnowledgeGraphQueryEngine(
#         storage_context=storage_context,
#         service_context=service_context,
#         llm=llm,
#         verbose=True,
#     )
#

###################################################################################################
#####################
#     # Function to parse  generated text and extract  triplets
# def zzz_extract_triplets_typed(text):
#     triplets = []
#     relation = ''
#     text = text.strip()
#     current = 'x'
#     subject, relation, object_, object_type, subject_type = '', '', '', '', ''
#
#     for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").replace("tp_XX", "").replace("__en__",
#                                                                                                                "").split():
#         if token == "<triplet>" or token == "<relation>":
#             current = 't'
#             if relation != '':
#                 triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),
#                                  'tail': object_.strip(), 'tail_type': object_type})
#                 relation = ''
#             subject = ''
#         elif token.startswith("<") and token.endswith(">"):
#             if current == 't' or current == 'o':
#                 current = 's'
#                 if relation != '':
#                     triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),
#                                      'tail': object_.strip(), 'tail_type': object_type})
#                 object_ = ''
#                 subject_type = token[1:-1]
#             else:
#                 current = 'o'
#                 object_type = token[1:-1]
#                 relation = ''
#         else:
#             if current == 't':
#                 subject += ' ' + token
#             elif current == 's':
#                 object_ += ' ' + token
#             elif current == 'o':
#                 relation += ' ' + token
#     if subject != '' and relation != '' and object_ != '' and object_type != '' and subject_type != '':
#         triplets.append(
#             {'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(), 'tail': object_.strip(),
#              'tail_type': object_type})
#     return triplets

# def zzz_add_triplet_to_kg(head, relation, tail, docid):
#     from neo4j import GraphDatabase
#
#     URI = "neo4j://localhost:7687"
#     AUTH = ("neo4j", "hell0neo")
#     with GraphDatabase.driver(URI, auth=AUTH) as driver:
#         # check if relation already exists
#         query = f"MATCH (n:Entity {{id: '{head}'}})-[r:RELATIONSHIP {{name: '{relation}'}}]->(m:Entity {{id: '{tail}'}}) RETURN r"
#         result, _, _ = driver.execute_query(query_=query, database_="neo4j")
#         if len(result) > 0:
#             # print(result[0]["r"]["docids"])
#             if docid not in result[0]["r"]["docids"]:
#                 # update relationship with new docid
#                 query = f"MATCH (n:Entity {{id: '{head}'}})-[r:RELATIONSHIP {{name: '{relation}'}}]->(m:Entity {{id: '{tail}'}}) SET r.docids = r.docids + [{docid}] RETURN r"
#                 driver.execute_query(query_=query, database_="neo4j")
#             return
#
#         query = f"""CREATE (e1:Entity {{id: '{head}'}}),
#         (e2:Entity {{id: '{tail}'}}),
#         (e1)-[:RELATIONSHIP {{name: '{relation}', docids: {[docid]}}}]->(e2);"""
#         driver.execute_query(query_=query, database_="neo4j")

# def zzz_neo_answer_question(question):
#     """
#     Given a question,
#     this function finds keywords from the question,
#     searches a Neo4j database using those keywords,
#     retrieves the document IDs from the search results,
#     fetches the corresponding text from a local SQLite database,
#     and uses a language model to answer the question based on the retrieved text.
#
#     :param question: A string representing the question to be answered.
#     :type question: str
#
#     :return: A string representing the answer to the question.
#     :rtype: str
#     """
#     # find keywords from question
#     keywords = nlp_extract_keywords_from_text(question)
#     results = neo4j_search_db_by_keywords(db_name="neo4j", keywords=keywords)
#     doc_ids = neo4j_get_doc_ids_from_results(results)
#     texts = localdb_fetch_text_by_doc_ids(doc_ids=doc_ids)
#
#     # TODO: pick from prompt storage
#     DEFAULT_TEXT_QA_PROMPT_TMPL = (
#         "Context information is below.\n"
#         "---------------------\n"
#         "{context_str}\n"
#         "---------------------\n"
#         "Given the context information and not prior knowledge, "
#         "answer the query.\n"
#         "Query: {query_str}\n"
#         "Answer: "
#     )
#     context_str = "\n---\n".join(texts)
#     # generate prompt
#     prompt = DEFAULT_TEXT_QA_PROMPT_TMPL.format(context_str=context_str, query_str=question)
#     # print(prompt)
#     s_time = time.time()
#     response = llm_get_answer(prompt, model="gpt-3.5-turbo", max_tokens=1000)
#     log(f"llm call : {(time.time() - s_time):.2f} seconds")
#     return response