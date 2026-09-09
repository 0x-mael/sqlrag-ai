from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.tools import QueryEngineTool

from llama_index.core.workflow import Context
from dotenv import load_dotenv
import os
from app.core.VectorEngine import VectorQueryEngine
from app.core.QueryEngineSQL import SQLQueryEngine
import mlflow

mlflow.set_experiment("AgentSQLRAG")
mlflow.llama_index.autolog()
load_dotenv()


def create_agent() : 
    ollama_url = os.getenv("OLLAMA_URL")
    model_name = os.getenv("MODEL_NAME")

    vector_engine = VectorQueryEngine()
    sql_engine = SQLQueryEngine()
    vector_engine_tool = QueryEngineTool.from_defaults(query_engine = vector_engine.load_query_engine(), name = "QueryEngine", description="QueryEngine Tool ,to ground on real clients contrat ")
    sql_engine_tool = QueryEngineTool.from_defaults(query_engine = sql_engine.query_engine, name = "SQLQueryEngine", description=(
        "Useful for answering questions in natural language about clients, invoices (factures), "
        "unpaid bills, debts, and technical incidents stored in the relational database. "
        "Input must be a natural language question (e.g. 'Combien avons-nous de clients ?')."
    ))
    llm = Ollama(model = model_name, base_url=ollama_url, temperature=0.1)

    agent = ReActAgent(llm = llm, tools = [vector_engine_tool, sql_engine_tool],
                        system_prompt="""Tu es un agent spécialisé en gestion commerciale et tu aides les experts commerciaux à avoir les informations nécessaires sur les clients et leur contrat.
                                        REGLES STRICTES : Tu utiliseras les outils à ta disposition pour donner des informations claires et exemptes d'hallucination. Ne réponds jamais sans les utiliser quand tu ne connais pas la réponse.
                                        Si tu n'arrives pas à trouver la réponse avec les outils à ta disposition, tu dois strictement t'en arrêter là et le préciser à l'utilisateur.
                                        
                                        """

    )
    
    return agent



