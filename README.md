# FinSavvy AI 🧾

<div align="center">

```
███████╗██╗███╗   ██╗███████╗ █████╗ ██╗   ██╗██╗   ██╗██╗   ██╗     █████╗ ██╗
██╔════╝██║████╗  ██║██╔════╝██╔══██╗██║   ██║██║   ██║╚██╗ ██╔╝    ██╔══██╗██║
█████╗  ██║██╔██╗ ██║███████╗███████║██║   ██║██║   ██║ ╚████╔╝     ███████║██║
██╔══╝  ██║██║╚██╗██║╚════██║██╔══██║╚██╗ ██╔╝╚██╗ ██╔╝  ╚██╔╝      ██╔══██║██║
██║     ██║██║ ╚████║███████║██║  ██║ ╚████╔╝  ╚████╔╝    ██║       ██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝    ╚═══╝     ╚═╝       ╚═╝  ╚═╝╚═╝
```

### Your Personal AI Chartered Accountant — Built from the Ground Up

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6B35?style=for-the-badge)](https://www.trychroma.com)
[![Groq](https://img.shields.io/badge/Groq-LLM_Engine-F55036?style=for-the-badge)](https://groq.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Status](https://img.shields.io/badge/Status-Active-22C55E?style=for-the-badge)](.)

<br/>

> **RAG from Scratch · Document Intelligence · Voice AI · Multilingual · OAuth 2.0**

</div>

---

## What is FinSavvy AI?

FinSavvy AI is a full-stack AI financial assistant that behaves like a **Chartered Accountant** — answering complex tax, investment, and finance queries with **cited, source-grounded responses**.

Unlike plug-and-play LLM wrappers, this system is engineered from first principles:

- ✅ **Custom RAG pipeline** — chunking, embedding, retrieval, and prompt engineering written manually, zero LangChain dependency
- ✅ **Multi-modal input** — text, voice, PDFs, scanned images via OCR
- ✅ **Source attribution** — every answer cites the exact document it pulled from
- ✅ **Persistent memory** — conversation context preserved across sessions
- ✅ **Secure auth** — Google, GitHub, and LinkedIn OAuth integration

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                          │
│               Text  ·  Voice  ·  PDF Upload  ·  Image            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INPUT PROCESSING                            │
│          STT (Speech-to-Text)  ·  OCR  ·  PDF Parser            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐    ┌───────────────────────┐
│   TEXT CHUNKING     │    │   KNOWLEDGE INGESTION  │
│  Custom chunk logic │    │  CA Books · User Docs  │
└──────────┬──────────┘    └───────────┬────────────┘
           │                           │
           └────────────┬──────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EMBEDDING GENERATION                          │
│                  Semantic vector encoding                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VECTOR SEARCH — ChromaDB                      │
│              Similarity Retrieval · Relevance Filter             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CONTEXT BUILDING                            │
│             Multi-source fusion · Prompt engineering             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GROQ LLM INFERENCE                           │
│                  Response + Source Attribution                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Feature Breakdown

### 🧠 Custom RAG — No Abstractions
The retrieval pipeline is built entirely from scratch. Manual chunking strategies, embedding management, retrieval ranking, and context injection — every layer is visible, controllable, and optimizable.

```
No LangChain. No LlamaIndex. Just clean, auditable Python.
```

**Live retrieval in action** — terminal output showing real-time vector distance scores and threshold-based filtering during a query:

![Multilingual Chat — Hindi](https://github.com/user-attachments/assets/7ccdb9bc-195d-4f5d-a4f2-57b79a3b22d2)

### 📄 Document Intelligence
Upload a PDF, image, or scanned document. The system extracts text (via PyMuPDF + Tesseract OCR), chunks it, embeds it, and immediately makes it queryable. Your uploaded documents become part of the knowledge base.

### 🎤 Voice AI
Full speech-to-text and text-to-speech pipeline — ask financial questions by voice, receive spoken answers. Designed for accessibility and a natural conversational flow.

### 🔍 Semantic Search
Queries are matched by **meaning**, not keywords. "How much tax do I pay on crypto profits?" retrieves the right sections even if the word "tax" doesn't appear verbatim in the source.

### 📚 Multi-Source Knowledge
| Source | Type | Use Case |
|---|---|---|
| CA Reference Books | PDF | Formal tax & accounting rules |
| TXT Knowledge Base | Plain text | FAQ-style financial Q&A |
| User Documents | PDF / Image | Personal document queries |

### 💬 Session-Based Memory
Each conversation retains history. AI-generated titles label your sessions. Multiple simultaneous conversations supported.

### 🌍 Multilingual
Switch languages mid-conversation. Designed for India's linguistically diverse user base.

![RAG Terminal — Distance Scores & Threshold Filtering](https://github.com/user-attachments/assets/0b6e6eec-0e37-41af-9244-87849a07f433)


### 🔐 Authentication
| Method | Provider |
|---|---|
| OAuth 2.0 | Google, GitHub, LinkedIn |
| Manual | Email + Password |

---

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **Backend** | FastAPI | REST API, routing, session management |
| **Frontend** | HTML / CSS / JS | UI, voice controls, file upload |
| **LLM** | Groq API | Fast inference (LLaMA-based) |
| **Vector DB** | ChromaDB | Embedding storage + semantic retrieval |
| **Database** | SQLite | Users, sessions, chat history |
| **OCR** | Tesseract | Scanned document text extraction |
| **PDF Parser** | PyMuPDF | Structured PDF text extraction |
| **Auth** | Authlib | OAuth 2.0 integration |

---

## Project Structure

```
FinSavvy-AI/
│
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── auth.py              # OAuth + session auth logic
│   ├── database.py          # SQLite models + CRUD
│   ├── rag/
│   │   ├── chunker.py       # Custom text chunking
│   │   ├── embedder.py      # Embedding generation
│   │   ├── retriever.py     # ChromaDB vector search
│   │   └── prompt.py        # Context injection + prompt builder
│   └── utils/
│       ├── ocr.py           # Tesseract OCR pipeline
│       ├── pdf_parser.py    # PyMuPDF extraction
│       └── voice.py         # STT / TTS handlers
│
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Styling
│   └── script.js            # API calls, voice, file upload
│
├── data/
│   ├── ca_books/            # CA reference documents
│   └── knowledge_base/      # TXT knowledge files
│
├── screenshots/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Tesseract OCR installed on your system
- A [Groq API key](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/ayushhh026/FinSavvy-AI.git
cd FinSavvy-AI
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_groq_api_key

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# GitHub OAuth
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=

SECRET_KEY=your_random_secret_key
```

### 5. Run the server
```bash
uvicorn backend.main:app --host localhost --port 8000 --reload
```

### 6. Open in browser
```
http://localhost:8000
```

> **Tip:** If the UI doesn't reflect changes after an update, force-refresh with `Ctrl + Shift + R`

---

## Screenshots

| Chat Interface | Document Upload | Voice Mode |
|---|---|---|
| ![UI 1](https://github.com/user-attachments/assets/cfb50b27-5b5e-4206-b281-406cd5a02ab1) | ![UI 2](https://github.com/user-attachments/assets/bf4a2af9-c4ca-46a5-8fcb-aa6a69d99936) | ![UI 3](https://github.com/user-attachments/assets/e6493a85-cfc0-4585-8e54-6b2e4a40210a) |

| Multilingual Support (Hindi) | RAG Terminal — Live Distance Scores |
|---|---|
| ![RAG Terminal](https://github.com/user-attachments/assets/0b6e6eec-0e37-41af-9244-87849a07f433 | ![Hindi Chat](https://github.com/user-attachments/assets/7ccdb9bc-195d-4f5d-a4f2-57b79a3b22d2) |

---

## Why Build RAG from Scratch?

Most demos use LangChain or LlamaIndex as black-box wrappers. The problem: you can't control, debug, or optimize what you can't see.

FinSavvy AI's RAG pipeline is entirely custom-built, which means:

- **Transparent** — every retrieval decision is traceable
- **Optimizable** — chunk size, similarity threshold, context window all tunable
- **Interview-defensible** — I can explain exactly how every piece works

This is the engineering difference between a project and a system.

---

## Roadmap

- [ ] Financial analytics dashboard (spending trends, tax estimation)
- [ ] AWS deployment (EC2 + Elastic Beanstalk)
- [ ] SageMaker integration for fine-tuned financial models
- [ ] Mobile app (React Native)
- [ ] Agentic workflows (auto-filing, document generation)
- [ ] Support for regional Indian languages (Hindi, Marathi, Tamil)

---

## License

[MIT License](LICENSE) — free to use, modify, and distribute with attribution.

---

## Author

**Ayush Shetty**  
AI & Data Science Engineering Student

[![GitHub](https://img.shields.io/badge/GitHub-ayushhh026-181717?style=flat-square&logo=github)](https://github.com/ayushhh026)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ayush_Shetty-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ayush-shetty-830a03281/)

---

<div align="center">

**⭐ Star this repo if it helped you — it keeps the project alive.**

*Built with curiosity, zero shortcuts, and a lot of ☕*

</div>

---

> **Disclaimer:** FinSavvy AI is an educational project. It does not constitute professional financial or tax advice. Always consult a qualified CA for legal financial decisions.
