from llama_index.llms.ollama import Ollama
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import Settings
from sqlalchemy import create_engine
from sqlalchemy import URL
from dotenv import load_dotenv 
import mlflow
import os


load_dotenv()

mlflow.set_experiment("SQLQueryEngine")
mlflow.llama_index.autolog()

class SQLQueryEngine :
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL")

        self.llm = Ollama(model = 'mistral-small3.1:latest',
                    base_url=self.ollama_url,
                    request_timeout = 120
                    )
        self.dbname = os.getenv("DB_NAME")
        self.dbhost = os.getenv("DB_HOST")
        self.dbuser = os.getenv("DB_USER")
        self.dbpass = os.getenv("DB_PASSWORD")
        self.dbport = os.getenv("DB_PORT")



        self.db_url = URL.create("postgresql+psycopg2",
                                username=self.dbuser,
                                password = self.dbpass,
                                host = self.dbhost, 
                                database = self.dbname
        
        )
        self.query_engine = None

        Settings.embed_model = None

    def create_query_engine(self):
        engine = create_engine(self.db_url)
        sql_db = SQLDatabase(engine, include_tables= ['clients','factures','incidents'])
        self.query_engine = NLSQLTableQueryEngine(
                            sql_database=sql_db, 
                            tables =  ['clients','factures','incidents'],
                            llm = self.llm     
        )
        return self.query_engine

    def run(self,query_str):
        query_engine = self.create_query_engine()
        response = query_engine.query(query_str)
        return response


if __name__ =="__main__":
    sql_query_eng = SQLQueryEngine()
    query_str="Quelles sont les informations du client avec le plus gros montant de facture en retard?"
    print(sql_query_eng.run(query_str))

    