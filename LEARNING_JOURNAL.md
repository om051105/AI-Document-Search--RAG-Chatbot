# 🎓 AI RAG Chatbot - Project Learning Journal & Documentation

This document serves as your guide and learning resource. As we build this "Industrial Level" RAG (Retrieval-Augmented Generation) application, I will document everything here: **Why** we are doing it, **What** technology we are using, and the **Algorithms** behind it.

## 🏗️ Project Architecture: The Industrial Standard

For a capstone and industrial-level project, we don't just put everything in one script. We decouple the **User Interface (Frontend)** from the **Logic (Backend)**.

### 1. The Stack
- **Frontend (The Face):** `Next.js` (React framework). 
  - *Why?* It allows for a premium, fast, and SEO-friendly user interface. Companies like Netflix, TikTok, and Twitch use it. It enables the "Rich Aesthetics" we want.
- **Backend (The Brain):** `FastAPI` (Python).
  - *Why?* It is the standard for high-performance AI APIs. It integrates natively with Python's AI ecosystem (LangChain, PyTorch, etc.) and generates automatic documentation (Swagger UI).
- **Orchestration:** `LangChain`.
  - *Why?* It abstracts the complexity of connecting LLMs (Large Language Models) to data sources, managing history, and prompt engineering.
- **Vector Database (The Memory):** `ChromaDB`.
  - *Why?* It stores data not as text, but as *vectors* (numbers representing meaning), allowing us to find "conceptually similar" documents, not just keyword matches.

---

## 🧠 Core Concepts & Algorithms

### 1. What is RAG? (Retrieval-Augmented Generation)
Standard LLMs (like ChatGPT) only know what they were trained on (up to a certain cut-off date). They don't know your private PDF data.
**RAG Algorithm Flow:**
1. **Ingestion**: We load your PDF.
2. **Chunking**: We break the PDF into small pieces (e.g., 500 words). *See "Recursive Character Splitting" below.*
3. **Embedding**: We turn each chunk into a list of numbers (a vector) using an Embedding Model (e.g., OpenAI `text-embedding-3-small`).
4. **Storage**: We save these vectors in a Vector Database.
5. **Retrieval**: When a user asks a question, we turn the question into a vector and look for the nearest vectors in the database (Cosine Similarity).
6. **Generation**: We send the user's question + the found retrieved text to the LLM and say "Answer the question using this context."

### 2. Algorithmic Deep Dive: Chunking
**RecursiveCharacterTextSplitter**: usage.
- We don't just cut text every 1000 characters. That might cut a sentence in half!
- **Algorithm**: It tries to split by paragraphs `\n\n` first. If the chunk is still too big, it splits by sentences `\n`. If still too big, it splits by words ` `.
- *Why?* This preserves the *semantic meaning* of the text better than arbitrary cutting.

### 3. Algorithmic Deep Dive: Vector Similarity
**Cosine Similarity**:
- Imagine every piece of text is a point on a graph.
- "Apple" and "Banana" are close together. "Apple" and "Car" are far apart.
- When searching, we measure the angle between the "Question Vector" and "Document Vectors". Small angle = high relevance.

---

## 🛠️ Step-by-Step Implementation Log

### Step 1: Project Initialization
We are setting up a clean folder structure.
- `/backend`: Will contain all Python code, API, and AI logic.
- `/frontend`: Will contain the React website code.

### Step 2: Backend Logic Implementation
We have created `main.py` (API) and `rag.py` (Logic).
- `rag.py` uses LangChain to load PDFs, chunk them, and store embeddings in ChromaDB.
- `main.py` uses FastAPI to expose this logic to the world.

### Step 3: Frontend Implementation (The Interface)
We set up **Next.js** with **Tailwind CSS**.
- **Why Next.js?** It provides a production-ready framework for React.
- **Why Tailwind?** It allows us to style our app rapidly using utility classes (e.g., `flex`, `bg-slate-900`) without writing separate CSS files.
- **Components Used**:
  - `page.tsx`: The main user interface. It handles state (what the user sees) and effects (sending data to the backend).
  - `globals.css`: Premium dark mode styling.

### Step 4: Connecting the Dots
We created a "Full Stack" application.
1. **User** uploads a PDF on the Frontend.
2. Frontend sends it to `FastAPI` (Backend).
3. Backend runs `RAGService` to analyze the PDF.
4. User asks a question.
5. Frontend sends the question to Backend.
6. Backend searches Vector DB + asks OpenAI -> Returns Answer.

### Step 5: Getting Access to the Intelligence (API Keys)
To make our bot smart, we need to connect it to OpenAI's production servers.
1. **Get an Account**: Go to [platform.openai.com](https://platform.openai.com/signup).
2. **Generate Key**: Click on "Dashboard" -> "API Keys" -> "Create new secret key".
3. **Save It**: This key starts with `sk-...`. It is your password to the AI.
4. **Config**: We paste this into our `backend/.env` file so our Python code can read it securely.
