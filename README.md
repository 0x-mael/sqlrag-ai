<!-- author : ABISSI Kotchikpa Ismael -->
<!-- date : September 2026 -->

# SQLRAG-AI

SQLRAG-AI is an agentic AI assistant designed to query structured enterprise data (PostgreSQL relational tables) and unstructured legal documents (client contracts) using a unified conversational interface.

Built with **LlamaIndex**, local models served through **Ollama**, **MLflow** tracing, and a **Gradio** web interface, the system leverages a ReAct agent equipped with two specialized query engines:
1. **SQLQueryEngine**: Translates natural language questions into PostgreSQL queries (Text-to-SQL) to inspect clients, invoices, payment status, and technical incidents.
2. **ContratsVectorEngine**: Searches and retrieves contractual clauses, SLA commitments, penalties, and payment terms stored in PostgreSQL via the `pgvector` extension.

---

## Features

- **Hybrid Data Retrieval**: Combines relational SQL querying (Text-to-SQL) and vector search over contract documents.
- **ReAct Agent Reasoning**: Dynamically chooses the appropriate engine depending on the query (relational, contractual, or hybrid questions requiring both).
- **Tool Tracing and Event Streaming**: Real-time event streaming and interactive dropdowns for tool calls in Gradio.
- **Observability**: Complete trace monitoring and execution logging with MLflow.
- **Data Seeding**: Automated generators for relational database records and markdown contract documents.

---

## Tech Stack

- **Framework**: LlamaIndex (ReActAgent, NLSQLTableQueryEngine, PGVectorStore)
- **LLM & Embeddings Provider**: Ollama
- **Database**: PostgreSQL with pgvector extension
- **Database Access**: SQLAlchemy, psycopg2
- **UI**: Gradio
- **Observability**: MLflow
- **Data Generation**: Faker

---

## Project Architecture

```text
sqlrag/
├── app/
│   ├── core/
│   │   ├── agent.py               # ReAct agent definition and tool binding
│   │   ├── QueryEngineSQL.py      # Text-to-SQL query engine
│   │   └── VectorEngine.py        # Vector search engine on contracts (PostgreSQL / PGVector)
│   ├── db/
│   │   ├── contrat_seeder.py      # Contract generator and file builder
│   │   ├── db_functions.py        # Database connection helper
│   │   └── db_seeder.py           # Relational data seeder (clients, factures, incidents)
│   ├── ui/
│   │   └── interface.py           # Gradio web interface entrypoint
│   └── utils/
│       └── chat_handler.py        # Async event stream handler for Gradio
├── assets/
│   ├── contrats/                  # Generated contract markdown files
│   └── templates/                 # Contract document templates
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL instance with `pgvector` extension support
- [Ollama](https://ollama.com/) running locally or accessible via a remote endpoint with your chosen LLM and embedding model.

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/0x-mael/sqlrag-ai.git
cd sqlrag-ai
python -m venv myenv
source myenv/bin/activate  # On Windows: .\myenv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory (based on `.env.example`):

```env
# Database configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=entreprise_db
DB_HOST=localhost
DB_PORT=5432

# Model configuration
OLLAMA_URL=http://localhost:11434
MODEL_NAME=mistral-small3.1:latest
EMBED_MODEL=qwen3-embedding:0.6b
```

### 4. Database Initialization & Seeding

1. Generate relational tables and dummy data:
   ```bash
   python -m app.db.db_seeder
   ```

2. Generate client contracts:
   ```bash
   python -m app.db.contrat_seeder
   ```

3. Ingest and vectorize contracts into PostgreSQL:
   ```bash
   python -c "from app.core.VectorEngine import VectorQueryEngine; VectorQueryEngine().ingest_documents()"
   ```

### 5. Running the Application

Launch the Gradio web interface:

```bash
python -m app.ui.interface
```

The Gradio interface will be accessible at `http://127.0.0.1:7860`.

To inspect MLflow execution traces and latency:

```bash
mlflow ui
```

The MLflow dashboard will be accessible at `http://127.0.0.1:5000`.

---

## Example Queries

- **Relational / SQL Queries**:
  - "Combien de clients avons-nous ?"
  - "Quelles sont les factures en retard du client CLT-006 ?"
  - "Le client CLT-002 a-t-il des incidents techniques non résolus ?"

- **Contractual / Vector Queries**:
  - "Quelles sont les pénalités SLA prévues pour le client CLT-006 ?"
  - "Quel est le délai de préavis de résiliation du client CLT-003 ?"

- **Hybrid Queries**:
  - "Quelle est la plus grosse dette du client CLT-010 et quelle est l'action immédiate à mener selon son contrat ?"

---

## Author

**ABISSI Kotchikpa Ismael**  
*September 2026*
