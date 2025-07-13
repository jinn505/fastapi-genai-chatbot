# 🧠 GenAI Document Chatbot using LangChain, Groq, and Qdrant

A robust, production-ready Conversational AI chatbot built with **LangChain**, **Groq’s LLaMA 3.1**, **Qdrant**, and **FastAPI**. The application enables users to upload `.pdf` and `.txt` documents and query them conversationally with context-aware responses powered by Retrieval-Augmented Generation (RAG).

---

## Features

- **Document Upload & Ingestion**
  - Supports `.pdf` and `.txt` formats
  - Automatically parsed and embedded using HuggingFace embeddings
  - Stored in Qdrant for fast vector similarity search

- **RAG Pipeline**
  - Combines semantic search with Groq's ultra-fast LLM (LLaMA 3.1 8B)
  - Ensures grounded, contextually relevant answers from uploaded documents

- **Conversational Memory**
  - Maintains session history using LangChain’s memory wrapper
  - Enables natural, flowing multi-turn conversations

- **Custom Prompt Engineering**
  - Standalone question rephrasing
  - Customized QA prompt to adapt to available context or fall back on general knowledge

- **Modular Architecture**
  - Organized, scalable structure with clear separation of concerns

---

## Tech Stack

| Layer              | Technology                          |
|-------------------|--------------------------------------|
| API Backend        | FastAPI                             |
| Language Model     | Groq LLaMA 3.1 (8B - Instant)        |
| Embeddings         | HuggingFace `all-MiniLM-L6-v2`       |
| Vector Store       | Qdrant                              |
| Orchestration      | LangChain                           |
| Auth (Optional)    | JWT + SQLite                        |
| Deployment         | Uvicorn / Docker-ready              |

---

## Project Structure

```
app/
├── chains/             # RAG pipeline and memory chain
├── models/             # LLM and embedding setup
├── retriever/          # Qdrant wrapper
├── db_jwt/             # JWT authentication (modular)
├── docs/               # Uploaded PDF and text files
├── main.py             # FastAPI app entry point
.env                    # Environment variables
requirements.txt
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/genai-chatbot.git
cd genai-chatbot
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Start the API Server

```bash
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### `POST /upload_pdf`

- Accepts a `.pdf` or `.txt` file
- Saves to `app/docs/`
- Parses content and indexes it into Qdrant

**Request:**
```bash
curl -X POST "http://localhost:8000/upload_pdf" \
  -F "file=@example.pdf"
```

---

### `POST /chat`

- Accepts a user query and optional chat history
- Returns a response based on relevant document context

**Request:**
```json
{
  "question": "Summarize chapter 1",
  "chat_history": []
}
```

---

## 🔍 Example Query Flow

1. User uploads `sample.txt`
2. System parses and stores embeddings in Qdrant
3. User sends a question like:
   > "What did the author say about climate change?"
4. Bot:
   - Rephrases question into standalone form
   - Performs semantic search
   - Answers using retrieved context and Groq LLM

---

## Future Improvements

- [ ] Frontend interface using Streamlit or React
- [ ] Docker containerization for full-stack deployment
- [ ] Fine-tuned domain-specific embedding models
- [ ] Admin interface for managing uploaded files

---
## 🙌 Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [Groq](https://console.groq.com)
- [Qdrant](https://qdrant.tech)
- [FastAPI](https://fastapi.tiangolo.com)
