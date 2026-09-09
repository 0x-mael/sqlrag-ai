from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import (SimpleDirectoryReader, VectorStoreIndex, StorageContext)
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Settings
import os 
from dotenv import load_dotenv
from pathlib import Path
from app.db.db_functions import Dbconn


BASE_DIR = Path(__file__).resolve().parent.parent.parent 


class VectorQueryEngine : 
    def __init__(self):

        self.ollama_url = os.getenv("OLLAMA_URL")
        self.model_name = os.getenv("MODEL_NAME")
        self.embed_model = os.getenv("EMBED_MODEL")
        Settings.llm = Ollama(model = self.model_name,
                            base_url = self.ollama_url)
        self.embed_model = OllamaEmbedding(
                            model_name = self.embed_model,
                            base_url = self.ollama_url
                                    )
        self.db = Dbconn()
        self.vector_engine = None
        self.setup()

    def _get_vector_store(self):
        return PGVectorStore.from_params(
            database=self.db.dbname,
            host=self.db.dbhost,
            password=self.db.dbpass,
            port=self.db.dbport,
            user=self.db.dbuser,
            table_name="contrat_embeddings",
            embed_dim=1024
        )

    def ingest_documents(self, folder_path=None):
        vector_store = self._get_vector_store()
        storage_ctx = StorageContext.from_defaults(vector_store=vector_store)
        contrats_dir = folder_path or (BASE_DIR / "assets" / "contrats")
        
        print(f"Ingest from {contrats_dir}")
        documents = SimpleDirectoryReader(str(contrats_dir)).load_data()
        index = VectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_ctx,
            embed_model=self.embed_model,
            show_progress=True
        )
        self.vector_engine = index.as_query_engine()
        return self.vector_engine

    def load_query_engine(self):
        vector_store = self._get_vector_store()
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=self.embed_model
        )
        self.vector_engine = index.as_query_engine()
        return self.vector_engine

    def setup(self):
        return self.load_query_engine()

if __name__ == '__main__':
    engine = VectorQueryEngine()

    query_engine = engine.load_query_engine()
    response = query_engine.query("Quels sont les clauses sur l'échéance de paiement du client CLT-006 ?")
    print(response)
