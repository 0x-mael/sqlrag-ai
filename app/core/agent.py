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
    vector_engine_tool = QueryEngineTool.from_defaults(
        query_engine=vector_engine.load_query_engine(),
        name="ContratsVectorEngine",
        description=(
            "À utiliser pour rechercher des informations textuelles et juridiques dans les CONTRATS clients (documents non structurés). "
            "Contient : les clauses contractuelles, niveaux de service garantis (SLA, disponibilité %, pénalités, GTR en heures), "
            "modalités de paiement convenues, conditions de suspension et clauses de résiliation. "
            "RÈGLE CRITIQUE D'ENTRÉE : Votre question transmise à cet outil DOIT OBLIGATOIREMENT mentionner explicitement l'identifiant du client au format 'CLT-XXX' "
            "(ex: 'Quelles sont les clauses de résiliation dans le contrat du client CLT-006 ?')."
        )
    )

    sql_engine_tool = QueryEngineTool.from_defaults(
        query_engine=sql_engine.query_engine,
        name="SQLQueryEngine",
        description=(
            "À utiliser pour interroger les données chiffrées, tabulaires et l'état en temps réel dans la BASE DE DONNÉES relationnelle (tables SQL). "
            "Contient : liste des clients, factures réelles (montants HT, statut 'PAYEE'/'EN_RETARD'/'EN_ATTENTE', jours de retard réels), "
            "et historique des incidents techniques (tickets, sévérité 'CRITIQUE'/'MAJEURE', état résolu ou non). "
            "Entrée : une question précise en langage naturel nécessitant un calcul, un comptage ou un état de fait (ex: 'Quelle est la dette totale du client CLT-006 ?')."
        )
    )

    llm = Ollama(model=model_name, base_url=ollama_url, temperature=0.1, request_timeout=300.0)

    agent = ReActAgent(
        llm=llm,
        tools=[vector_engine_tool, sql_engine_tool],
        system_prompt="""Tu es un assistant expert en gestion commerciale et juridique pour les comptes clients de l'entreprise.

Tu as accès à deux sources de données complémentaires :
1. `SQLQueryEngine` : Base relationnelle contenant les chiffres et faits réels (clients existants, factures, montants impayés, jours de retard, tickets d'incidents).
2. `ContratsVectorEngine` : Bibliothèque des contrats clients contenant les règles juridiques (clauses SLA, pénalités prévues, délais légaux de paiement, conditions de suspension/résiliation).

RÈGLES D'UTILISATION DES OUTILS :
- Pour les faits, montants, listes et décomptes -> Utilise `SQLQueryEngine`.
- Pour les termes juridiques, pénalités prévues et règles contractuelles -> Utilise `ContratsVectorEngine`.
- LORS DE L'APPEL À `ContratsVectorEngine` : Inclus TOUJOURS l'identifiant exact du client au format 'CLT-XXX' dans ta question (ex: 'CLT-006', 'CLT-010') afin de cibler le document juridique correspondant à ce client spécifique.
- Pour les questions hybrides (ex: "Quelle est la dette du client X et quelle action mener ?") -> Utilise d'abord `SQLQueryEngine` pour obtenir la situation chiffrée (retard, montants), puis `ContratsVectorEngine` en mentionnant le client CLT-XXX pour trouver la clause contractuelle applicable à cette situation.

CONSIGNES STRICTES :
- Ne devine jamais. Si une information n'est pas trouvée via les outils, indique-le clairement sans inventer.
- Formate tes réponses de manière claire, synthétique et professionnelle pour les équipes commerciales."""
    )
    
    return agent



