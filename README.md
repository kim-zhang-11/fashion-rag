# FashionRAG

## A **Streamlit**-Based Local Knowledge Base Upload & **RAG** Q&A Project
Perfect for getting started with local knowledge base Q&A and RAG retrieval-augmented generation
- Upload `txt` files on the web interface, automatically split and write to Chroma vector database
- Ask questions in chat format on the web interface, get retrieval-augmented answers based on knowledge base content (RAG)
- Support session history viewing and streaming chain-of-thought output
- Tech Stack: Python / Streamlit / LangChain / Chroma / Embeddings / Qwen ChatModel

---

## ✨ Features Overview

### 1) Knowledge Base Update Service (Upload)
- Upload files via Streamlit page with basic format display
- Automatically read text content
- Split content based on configuration (RecursiveCharacterTextSplitter)
- Write to Chroma vector database (local persistence)
- Use **MD5 deduplication**: prevent duplicate content from being indexed

### 2) Smart Customer Service (RAG Chat)
- Streamlit Chat UI
- Display message history (session_state)
- LangChain chain calling: `Retrieval -> Prompt -> LLM -> Output`
- Support **streaming output**
- Support **message history file storage** (FileChatMessageHistory)

---


## 🧩 Project Structure

```text
FashionRAG/
├─ app_upload.py              # Knowledge base upload service (Streamlit) - Entry point
├─ app_chat.py                # Smart Q&A service (Streamlit) - Entry point
├─ requirements.txt           # Project dependencies (environment setup)
├─ assets/                    # Location for README demo images and sample text materials
├─ chat_history/              # Chat history storage directory
├─ chroma_db/                 # Chroma vector database (local persistence)
├─ md5.text                   # MD5 deduplication records
└─ src/                       # Source code package
    ├─ config.py              # Model, path, chunk and other parameter configuration
    ├─ chatbot/               # Chatbot module
    │  ├─ rag.py              # RAG chain assembly
    │  └─ history.py          # Session history storage
    └─ knowledge_base/        # Knowledge base module
       ├─ base.py             # Knowledge base processing: read, split, write, deduplicate
       └─ vector_store.py     # Vector database retrieval wrapper (persistence)
```
---
## ✅ Environment Setup

### 1) Install Dependencies
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- Run in terminal, recommended to use virtual environment and Tsinghua mirror source for acceleration
---

## ⚙️ Configuration Guide

- Core configuration is in `src/config.py`, manually modify model configuration, chunk size, etc. as needed
- Default embedder: text-embedding-v4 and Qwen3-max
- Note: DashScope/Qwen related API Keys (e.g., DASHSCOPE_API_KEY) need to be configured in environment variables first
---

## 🚀 Quick Start
### 1) Start Knowledge Base Upload Service
```bash
streamlit run app_upload.py
```
- After opening the page, upload .txt files to write to the local vector database.

### 2) Start Smart Customer Service (RAG Chat)
```bash
streamlit run app_chat.py
```
- After entering a question, it will first retrieve from the knowledge base, then synthesize the answer with the retrieved content
---

## 🛠 FAQ

### Q1: After uploading files, chat Q&A still shows "no relevant data found"?
#### Possible Causes:
- Upload service and Q&A service use different vector database persistence directories
- `collection_name` configuration is inconsistent
- Files not properly written to local data directory after upload

### Q2: After uploading files, answers are slow or not outputting correctly?
#### Possible Causes:
- Text splitting or retrieval parameters not set appropriately, adjust chunk size and retrieval k value...
- Model interface or network request is responding slowly
- Local vector database not properly initialized

### Q3: How to handle path or configuration errors when running the project?
#### Recommended checks:
- Verify model configuration and path configuration in `src/config.py` are correct
- Check if local data directories exist
- Verify API Keys are configured in environment variables

---
## ✨ Optimization Directions (Optional)
- Add deep reranking to improve retrieval quality, such as EGE rerank module provided in langchain framework
- Optimize Streamlit page interaction and display, Streamlit has rich built-in features for UI customization
- Support more file types (multimodal) such as PDF / Markdown / Word, easily achievable by adding langchain plugins
- Chain-of-Thought -> Tree-of-Thought ?
- Single Model -> Multi-Model ? For example, multi-layer inference architecture like Doubao, multi-model hybrid output?
- Chroma -> FAISS ? Lightweight Chroma is suitable for personal reproduction, while FAISS's efficient retrieval is suitable for enterprise scenarios
- Pending...
- In summary, this is a foundational yet highly extensible RAG project:
  - Personal use → Enterprise-grade RAG → Feature plugins → Agent → AI Products
