# LLM Exam Project

LLM Exam Project by Group I for EK Software Development.

## Setup guide: Linear Regression vs. RAG notebook

This guide explains how to run `linear_regression_vs_rag.ipynb` on Windows.

### 1. Install the required software

- Install [Python 3.12](https://www.python.org/downloads/)
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install [Ollama for Windows](https://ollama.com/download/windows)
- In VS Code, install the **Jupyter** and **Python** extensions

### 2. Create the Python environment

Open PowerShell in the project folder and run:

```powershell
uv python install 3.12
uv sync
```

This creates the project virtual environment and installs the dependencies from `pyproject.toml`, including NumPy, pandas, scikit-learn, matplotlib, requests and ipykernel.

### 3. Pull the Ollama models

Start Ollama, then open a second terminal and run:

```powershell
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

The notebook uses `qwen3:4b` for chat responses and `nomic-embed-text` for RAG embeddings.

Keep Ollama running in the background while the notebook executes. It should be available at `http://localhost:11434`.

To confirm that Ollama is running, open a terminal and run:

```powershell
curl.exe http://localhost:11434/api/tags
```

The response should contain `qwen3:4b` and `nomic-embed-text`.

### 4. Open and run the notebook

1. Open `linear_regression_vs_rag.ipynb` in VS Code.
2. Click **Select Kernel** in the notebook toolbar.
3. Select the `.venv` environment in the project folder.
4. Choose **Run All**.

The notebook creates `rag_data/rag_collection.txt` in the project folder. Running the full notebook also produces the prediction table and MAE comparison.

### Troubleshooting

- **Connection refused or Ollama timeout:** make sure the Ollama application is running and that both models have been pulled.
- **Model not found:** run `ollama pull qwen3:4b` and `ollama pull nomic-embed-text` again.
- **Wrong kernel:** select **.venv** as the notebook kernel, rather than the system Python installation.
- **Missing package:** from the project folder, run `uv sync` again.
- **Notebook runs slowly:** the local 4B chat model can take longer on a CPU-only computer. Leave Ollama running and allow each chat call to finish.
