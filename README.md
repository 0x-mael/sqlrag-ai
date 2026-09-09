<!-- author : ABISSI Kotchikpa Ismael -->
<!-- date : September 2026 -->

# SQLRAG-AI

**SQLRAG-AI** is an agentic system designed to query large database using **Natural Langage SQL(NLSQL)** and Vector Store with embeddings to ground enterprise informations and help support. Built on **LlamaIndex**, local LLMs via **Ollama**, **MLflow** tracing, and an interactive **Gradio** web interface, it retrieves relevant contrat fields from a client's document and pesonal informations on the database with least-privileges to answer questions on status, invoices etc...

---

## Features

- **Local & Privacy-Friendly**: Runs on local open-weights models served through Ollama.

---

## Project Architecture

```text

```

---

## Tech Stack



---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with your model:
  ```bash
  ollama run llama3.1:8b
  ```

### 2. Installation

Clone the repository and set up a virtual environment:


```

### 3. Configuration

Configure your `.env` file in the root directory:

```env
OLLAMA_API_URL=http://localhost:11434
MODEL_NAME=gemma4:latest
MODEL_SMALL = llama3.1:8b
```

### 4. Running the Application

Launch the Gradio web interface:

```bash
```

To monitor traces and execution graphs in MLflow:

```bash
mlflow ui
```

The Gradio interface will be accessible at `http://127.0.0.1:7860` and the MLflow dashboard at `http://127.0.0.1:5000`.

---

## Example Queries



---

## Author

**ABISSI Kotchikpa Ismael**  
*September 2026*
