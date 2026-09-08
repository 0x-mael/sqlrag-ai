from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import (SimpleDirectoryReader, VectorStoreIndex, StorageContext)
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Settings
import os 
from dotenv import load_dotenv
from core.db_functions import Dbconn


ollama_url = os.getenv("OLLAMA_URL")
embed_model = OllamaEmbedding(
                        model_name = "qwen3-embedding:0.6b",
                        base_url = ollama_url
)
db = Dbconn()
vector_store = PGVectorStore.from_params(database = db.dbname,
                                        host = db.dbhost, 
                                        password = db.dbpass, 
                                        port = db.dbport, 
                                        user= db.dbuser,
                                        table_name = "contrat_embeddings",
                                        embed_dim = 1024 )

storage_ctx = StorageContext.from_defaults(vector_store = vector_store)

documents = SimpleDirectoryReader('./assets/contrats/').load_data()
index = VectorStoreIndex.from_documents(documents = documents, storage_context = storage_ctx, embed_model = embed_model, show_progress=True)
queryEngine = index.as_query_engine()

if __name__=='__main__':
    response = queryEngine.query("Quels sont les clauses sur l'échéance de paiement du client CLT-006 ?")
    print(response)