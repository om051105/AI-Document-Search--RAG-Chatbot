# 🧠 DocuMind AI: Industrial RAG Chatbot

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)
![Next.js](https://img.shields.io/badge/Next.js-14.0+-000000.svg)

**DocuMind AI** is an industrial-grade Retrieval-Augmented Generation (RAG) system designed to interact exclusively with private documentation. Unlike generic LLMs, this system ingests, chunks, and indexes PDF documents into a vector store to provide factual, context-aware answers with zero hallucinations.

## 🏗️ Enterprise Architecture

This project follows a strict **Microservice-Monorepo** architecture, separating concerns for scalability and maintainability.

| Layer | Technology Stack | Purpose |
|-------|------------------|---------|
| **Presentation** | Next.js 14, Tailwind CSS, Framer Motion | High-performance, reactive UI with streaming responses. |
| **API Gateway** | FastAPI (Python) | Async REST API handling file uploads and query orchestration. |
| **Orchestrator** | LangChain (LCEL) | Manages the RAG pipeline: Retriever → Prompt → LLM. |
| **Vector Engine** | ChromaDB | Local vector store for semantic search and embeddings. |
| **Intelligence** | OpenAI GPT-3.5/4o | Generative engine for synthesizing final answers. |

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **OpenAI API Key** (Required for Embeddings & Generation)

### ⚠️ Security Warning
> **NEVER** commit your `.env` file or API keys to GitHub. This repository uses `.gitignore` to prevent secret leakage.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/AI-Document-Search-RAG.git
    cd AI-Document-Search-RAG
    ```

2.  **Environment Configuration**
    Navigate to the `backend/` directory and set up your secrets.
    ```bash
    cd backend
    cp .env.example .env
    ```
    Open `.env` and add your key:
    ```ini
    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
    ```

3.  **Run the System (Windows)**
    Simply double-click the `start_app.bat` file in the root directory.

    *Alternatively, run services manually:*
    
    *Backend (Terminal 1):*
    ```bash
    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python main.py
    ```

    *Frontend (Terminal 2):*
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 🧠 System Internals

For a deep dive into the algorithms used (Recursive Character Splitting, Cosine Similarity, and Vector Embeddings), please refer to definitions in the source code comments or the accompanying `LEARNING_JOURNAL.md`.

### The RAG Pipeline
1.  **Ingestion**: PDF is uploaded via frontend -> sent to FastAPI.
2.  **Processing**: `LangChain` loaders read the file.
3.  **Chunking**: Text is split recursively (overlap: 200 tokens) to preserve semantic context.
4.  **Embedding**: Chunks are converted to vectors using `text-embedding-3-small`.
5.  **Retrieval**: User query is embedded; system finds nearest k=3 vectors.
6.  **Synthesis**: Context + Query sent to GPT-3.5 for the final answer.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose bug fixes and new features.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built for Capstone 2026 / Industrial Demonstration*