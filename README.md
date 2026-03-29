# Agentic RAG Course Planning Assistant (LOCAL USC)

A fully **Local & Agentic AI Academic Assistant** grounded in the USC Computer Science (BS) curriculum. This system provides course planning and prerequisite reasoning using a local GGUF reasoning engine and local vector search.

## 🚀 Key Features
- **Strictly Grounded**: Retrieval is performing on a curated set of **28 academic documents** (Major requirements, course descriptions, and policies).
- **Agentic Workflow**: Sequential reasoning (Intake $\rightarrow$ Retrieval $\rightarrow$ Advising $\rightarrow$ Auditing) powered by **CrewAI**.
- **Fully Local**: Runs entirely on your CPU/GPU using `LlamaCpp` for thinking and `HuggingFace` for embeddings—no API keys or cloud data leaks.
- **Citation Precision**: Every prerequisite claim includes a source URL and specific catalog section.

## 🛠️ Quick Start Guide
1. **Prerequisites**: Place your `model.gguf` in the project root folder.
2. **Setup Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   pip install llama-cpp-python sentence-transformers langchain-huggingface
   ```
3. **Build the Index**:
   ```powershell
   python ingest.py
   ```
4. **Execution**:
   - **Performance Run**: `python eval.py` (Runs the 25 required test cases).
   - **Interactive App**: `python main.py` (Chat directly with the advisor).

## 📁 Repository Structure
- `data/`: Curated source documents (28 USC policy & course files).
- `chroma_db/`: Persistent local vector store.
- `agents.py`: core logic for Agents, Tasks, and LLM orchestration.
- `ingest.py`: RAG pipeline for document ingestion and chunking.
- `writeup.md`: Detailed technical report on architecture and assessment criteria.

## ⚖️ Performance & Local Tradeoffs
This system is optimized for **Privacy and Accuracy**. Because it runs on local hardware, reasoning takes slightly longer (~15-30s per query) compared to cloud APIs, but ensures 100% data residency and zero-cost operation.
