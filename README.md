📌 Overview

FinSavvy AI is a next-generation AI-powered financial assistant designed to simulate the capabilities of a Chartered Accountant (CA).

It combines:

🧠 Custom-built Retrieval-Augmented Generation (RAG)
📄 Document Intelligence
🎤 Voice Interaction
🌍 Multilingual Support

to deliver accurate, explainable, and context-aware financial insights.

Unlike traditional chatbots, FinSavvy AI uses a multi-source RAG pipeline built from scratch to reduce hallucination and improve reliability.

🎯 Objectives
Provide accurate financial and tax-related answers
Reduce hallucination using retrieval-based AI (RAG)
Support multi-modal inputs (text, voice, documents)
Enable dynamic knowledge ingestion
Ensure transparency via source attribution
🔥 Key Features
💬 Conversational AI
Natural language financial assistant
Context-aware responses using memory
📄 Document Intelligence
Upload PDFs and images
Extract financial data using OCR
Convert unstructured data → searchable knowledge
🧠 Custom RAG (Built From Scratch)
Manual chunking
Custom retrieval functions
Multi-source knowledge integration
Manual context injection
🔍 Semantic Search
Meaning-based search (not keyword-based)
Uses embeddings for similarity matching
📚 Multi-Source Knowledge Retrieval
CA Books (domain knowledge)
TXT knowledge base
User-uploaded documents
🎤 Speech-to-Text (STT)
Voice input support
Converts speech → text
🔊 Text-to-Speech (TTS)
AI responses can be spoken back
🌍 Multilingual Support
Language switching
Multi-language interaction
🖼️ Image Upload Support
Extract text from images using OCR
🧠 Conversational Memory
Stores chat history
Improves context and continuity
🔐 Authentication System
OAuth login:
Google
GitHub
LinkedIn
Manual authentication
💬 Session-Based Chat
Multiple chat sessions
AI-generated titles
Persistent conversation storage
📊 Financial Intelligence
Structured explanations
Context-aware financial reasoning
⚙️ Tech Stack
💻 Backend
FastAPI (Python)
🎨 Frontend
HTML, CSS, JavaScript
🧠 AI / NLP
Groq API (LLM)
📚 Vector Database
ChromaDB
🗄️ Database
SQLite
📄 Document Processing
PyMuPDF (PDF parsing)
Tesseract OCR
🔐 Authentication
Authlib (OAuth)
🧠 System Architecture
User Input (Text / Voice / File)
↓
Input Processing (STT / OCR / PDF Parsing)
↓
Text Chunking
↓
Embedding Generation
↓
Vector Search (ChromaDB)
↓
Relevance Filtering (Distance Threshold)
↓
Context Building (Multi-Source)
↓
LLM Processing (Groq)
↓
Response Generation
↓
Source Attribution
↓
Final Output
🔄 Workflow
Input → Processing → Embedding → Retrieval → Filtering → LLM → Source → Output
🧩 Manual RAG Implementation

This system implements RAG without using frameworks like LangChain.

Steps:
Custom text chunking
Embedding storage in vector DB
Custom retrieval functions
Multi-source retrieval
Manual prompt/context construction
🎯 Key Innovation
Multi-source RAG (CA + TXT + User Docs)
Distance-based filtering for accuracy
Source attribution (transparency)
Multi-modal interaction
Fully manual RAG pipeline
📁 Project Structure
FinSavvy-AI/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── rag/
│   ├── utils/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
├── data/
│   ├── sample_docs/
│
├── screenshots/
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
🛠️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/finsavvy-ai.git
cd finsavvy-ai
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables

Create .env file:

GROQ_API_KEY=your_api_key
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
SECRET_KEY=your_secret
5️⃣ Run the Application
uvicorn main:app --host localhost --port 8000
6️⃣ Open in Browser
http://localhost:8000
⚠️ UI Refresh Note

If UI changes are not visible:

CTRL + SHIFT + R  (Hard Refresh)

📸 Screenshots

<img width="1900" height="912" alt="Screenshot 2026-02-19 172434" src="https://github.com/user-attachments/assets/cfb50b27-5b5e-4206-b281-406cd5a02ab1" />
<img width="1902" height="910" alt="Screenshot 2026-02-19 172512" src="https://github.com/user-attachments/assets/bf4a2af9-c4ca-46a5-8fcb-aa6a69d99936" />
<img width="1916" height="912" alt="Screenshot 2026-02-19 172649" src="https://github.com/user-attachments/assets/e6493a85-cfc0-4585-8e54-6b2e4a40210a" />
<img width="1912" height="907" alt="Screenshot 2026-02-19 174902" src="https://github.com/user-attachments/assets/4566b2cf-3734-49ea-beeb-16c50c04c5f6" />




📸 Screenshots

Add your screenshots here
