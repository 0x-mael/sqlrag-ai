import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

class Dbconn :
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.dbhost = os.getenv("DB_HOST")
        self.dbuser = os.getenv("DB_USER")
        self.dbpass = os.getenv("DB_PASSWORD")
        self.dbport = os.getenv("DB_PORT")

        self.DB_CONFIG = {
            "dbname": self.dbname,
            "user": self.dbuser,
            "password": self.dbpass,
            "host": self.dbhost,
            "port": self.dbport,
        }
        
    def get_conn(self):
        config = self.DB_CONFIG
        conn = psycopg2.connect(**config)
        return conn


    def exec_query(self,query):
        con = self.get_conn()

        try:
            with con.cursor() as cur :
                cur.execute(query)
                result = cur.fetchall()
                
                print("Request succesfully")
                return result
            con.close()

        except Exception as e :
            print(f"An exception {e} occured when trying to execute the request {query}")
            con.close()
