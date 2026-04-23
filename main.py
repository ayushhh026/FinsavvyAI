from fastapi import FastAPI, Depends, HTTPException, Form, Request,Body
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from auth import create_access_token, verify_token, oauth2_scheme
from pydantic import BaseModel
from typing import List
import os
import sqlite3
import hashlib
from groq import Groq
import uuid
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import Form, File, UploadFile
import fitz
import pytesseract
from PIL import Image
import io
from memory import search_ca_books
from memory import search_txt_knowledge
from memory import (
    add_memory,
    retrieve_memory,
    add_uploaded_document,
    search_documents
)


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

load_dotenv()  # this will read .env file

client = Groq(api_key=os.getenv("GROK_API"))


app = FastAPI()
oauth = OAuth()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_ID"), session_cookie="finsavvy_session",)
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

oauth.register(
    name="linkedin",
    client_id=os.getenv("LINKEDIN_CLIENT_ID"),
    client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
    access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
    authorize_url="https://www.linkedin.com/oauth/v2/authorization",
    api_base_url="https://api.linkedin.com/v2/",
    client_kwargs={"scope": "r_liteprofile r_emailaddress"},
)

# Static files & templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    session_id TEXT,
    sender TEXT,
    message TEXT
);
''')
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    username TEXT,
    title TEXT
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS uploaded_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    session_id TEXT,
    filename TEXT,
    upload_index INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

def generate_chat_title(messages: list[str]) -> str:
    prompt = (
        "Generate a short 3 to 6 word title for this conversation.\n"
        "Do NOT use quotes.\n"
        "Do NOT include punctuation.\n\n"
        "Conversation:\n"
        + "\n".join(messages[:4])
    )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=20,
        temperature=0.3
    )

    return completion.choices[0].message.content.strip()


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register")
def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
        conn.commit()
        return templates.TemplateResponse("login.html", {"request": request, "message": "Registered successfully! Please login."})
    except sqlite3.IntegrityError:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Username already exists!"})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user and user[0] == hash_password(password):

        session_id = str(uuid.uuid4())

        #  INSERT SESSION INTO DB
        cursor.execute(
            "INSERT INTO sessions (session_id, username, title) VALUES (?, ?, ?)",
            (session_id, username, "New Conversation")
        )
        conn.commit()

        return RedirectResponse(
            url=f"/chat?username={username}&session_id={session_id}",
            status_code=303
        )

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": "Invalid credentials!"}
    )




# ---------- Models ----------
# class ChatMessage(BaseModel):
#     message: str = Form(...)
#     file: UploadFile = File(None)


# ---------- Routes ----------
@app.get("/auth/{provider}")
async def auth_login(request: Request, provider: str):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail="Provider not supported")

    redirect_uri = request.url_for("auth_callback", provider=provider)
    print(str(redirect_uri))
    return await client.authorize_redirect(request, redirect_uri)


@app.get("/auth/{provider}/callback")
async def auth_callback(request: Request, provider: str):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail="Provider not supported")

    token = await client.authorize_access_token(request)

    username = None
    email = None

    if provider == "google":
        user_info = token.get("userinfo")
        username = user_info.get("name")
        email = user_info.get("email")

    elif provider == "github":
    #  Ensure token is valid
        if not token:
            raise HTTPException(status_code=400, detail="GitHub authentication failed")

        resp = await client.get("user", token=token)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch GitHub profile")

        profile = resp.json()
        username = profile.get("login")
        if not username:
            raise HTTPException(status_code=400, detail="GitHub login failed: username missing")

    #  Fetch email safely
        email_resp = await client.get("user/emails", token=token)
        if email_resp.status_code == 200:
            emails = email_resp.json()
            email = next((e["email"] for e in emails if e.get("primary")), None)
        else:
            email = None

        if not email:
            email = f"{username}@github.oauth"

    elif provider == "linkedin":
        resp = await client.get(
            "me?projection=(id,localizedFirstName,localizedLastName)", token=token
        )
        profile = resp.json()
        email_resp = await client.get(
            "emailAddress?q=members&projection=(elements*(handle~))", token=token
        )
        email_data = email_resp.json()
        email = email_data["elements"][0]["handle~"]["emailAddress"]
        username = f"{profile.get('localizedFirstName')} {profile.get('localizedLastName')}"

    # fallback if email is missing
    if not email:
        email = f"{username}@{provider}.oauth"

    # Store in DB
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, "oauth"),
        )
        conn.commit()

    session_id = str(uuid.uuid4())
    cursor.execute(
    "INSERT INTO sessions (session_id, username, title) VALUES (?, ?, ?)",
    (session_id, username, "New Conversation")
    )
    conn.commit()
    return RedirectResponse(
        url=f"/chat?username={username}&session_id={session_id}", status_code=303
    )
@app.get("/",response_class=HTMLResponse)
async def Home_page(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    session_id = request.query_params.get("session_id")
    username = request.query_params.get("username") 
    if not username:
        return RedirectResponse(url="/")

    if not session_id:
        session_id = str(uuid.uuid4())

        cursor.execute(
            "INSERT INTO sessions (session_id, username, title) VALUES (?, ?, ?)",
            (session_id, username, "New Conversation")
        )
        conn.commit()

    # Fetch chat history for this session
    cursor.execute(
        "SELECT sender, message FROM messages WHERE session_id=? ORDER BY id ASC",
        (session_id,)
    )
    history = cursor.fetchall()

    print("Chat history for session", session_id, ":", history)

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_history": history,
            "session_id": session_id,
            "username": username
        }
    )

@app.post("/chat")
async def chat_api(
    request: Request,
    message: str = Form(""),
    language: str = Form("English"),
    files: List[UploadFile] = File([])
):
    username = request.query_params.get("username", "guest")
    session_id = request.query_params.get("session_id")
    print("Selected language:", language)
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID missing")

    uploaded_documents_text = []
    uploaded_filenames = []

    # ---------------- FILE PROCESSING ----------------
    if files:
        for file in files:
            contents = await file.read()
            extracted_text = ""

            if file.content_type == "application/pdf":
                pdf = fitz.open(stream=contents, filetype="pdf")
                for page in pdf:
                    extracted_text += page.get_text()

            elif file.content_type.startswith("image/"):
                image = Image.open(io.BytesIO(contents))
                extracted_text += pytesseract.image_to_string(image)

            if extracted_text.strip():
                chunks = chunk_text(extracted_text)

                for chunk in chunks:
                    add_uploaded_document(
                        username,
                        session_id,
                        file.filename,
                        chunk
                    )

                uploaded_documents_text.append(extracted_text)
                uploaded_filenames.append(file.filename)

    # ---------------- MESSAGE PROCESSING ----------------
    user_message = (message or "").strip()

    if not user_message and not uploaded_documents_text:
        return JSONResponse({"reply": "Please type a message or upload a document."})

    # Build display message properly
    display_message = user_message

    if uploaded_filenames:
        file_list = ", ".join(uploaded_filenames)
        if user_message:
            display_message += f"\n\n📎 Uploaded: {file_list}"
        else:
            display_message = f"📎 Uploaded: {file_list}"

    # Save to DB
    cursor.execute(
        "INSERT INTO messages (username, session_id, sender, message) VALUES (?, ?, ?, ?)",
        (username, session_id, "user", display_message)
    )
    conn.commit()

    if user_message:
        add_memory(username, session_id, "user", user_message)

    # If only upload without text
    if uploaded_documents_text and not user_message:
        bot_message = f"📄 Documents uploaded successfully: {file_list}\nWhat would you like me to do with them?"

        cursor.execute(
            "INSERT INTO messages (username, session_id, sender, message) VALUES (?, ?, ?, ?)",
            (username, session_id, "bot", bot_message)
        )
        conn.commit()

        add_memory(username, session_id, "bot", bot_message)

        return JSONResponse({"reply": bot_message})

    # ---------------- CONTEXT BUILDING ----------------
    context_parts = []
    source_used = []

    print("User message:", user_message)

    if user_message:

        # 🔹 1. SEARCH USER DOCUMENTS
        doc_results = search_documents(user_message, session_id)

        print("\n===== DEBUG: RETRIEVED DOCS =====")
        for i, doc in enumerate(doc_results):
            print(f"\nChunk {i+1}:\n{doc[:200]}...")
        print("=================================\n")

        # 🔹 2. SEARCH CA BOOKS (NEW)
        ca_results = search_ca_books(user_message)

        print("\n===== DEBUG: CA BOOKS =====")
        for i, doc in enumerate(ca_results):
            print(f"\nCA Chunk {i+1}:\n{doc[:200]}...")
        print("=================================\n")

        # 🔹 3. DOCUMENT CONTEXT
        if doc_results:
            context_parts.append(
                "DOCUMENT CONTEXT:\n" + "\n\n".join(doc_results[:2])
            )
            source_used.append("User Document")

        # 🔹 4. CA KNOWLEDGE (IMPORTANT)
        if ca_results:
            context_parts.append(
                "CA KNOWLEDGE:\n" + "\n\n".join(ca_results[:2])
            )
            source_used.append("CA Notes")

        # 🔹 5. CHAT MEMORY
        chat_memory = retrieve_memory(user_message, session_id)
        if chat_memory:
            context_parts.append(
                "CHAT HISTORY:\n" + "\n".join(chat_memory[:5])
            )
        # 🔹 TXT KNOWLEDGE
        txt_results = search_txt_knowledge(user_message)

        print("\n===== DEBUG: TXT RESULTS =====")
        for i, doc in enumerate(txt_results):
            print(f"\nTXT Chunk {i+1}:\n{doc[:200]}...")
        print("=================================\n")

        if txt_results:
            context_parts.append(
                "TXT KNOWLEDGE:\n" + "\n\n".join(txt_results[:3])
            )
            source_used.append("Data Ingestion Txt")
    context = "\n\n".join(context_parts)
    source_used = list(set(source_used))

   # ---------------- AI CALL ----------------
    system_prompt = f"""
        You are FinSavvy, a professional Chartered Accountant AI assistant.
        The user has selected language: {language}

        You MUST reply entirely in {language}.
        Do not mix languages unless necessary for technical terms.

        ----------------------------------------
        🔹 CONTEXT TYPES
        You may receive:
        1. DOCUMENT CONTEXT (user uploaded files)
        2. CA KNOWLEDGE (preloaded tax/finance knowledge)
        3. CHAT HISTORY (previous conversation)

        ----------------------------------------

        🔹 RESPONSE RULES

        1. If DOCUMENT CONTEXT is provided:
        - Use it to extract exact values, numbers, and user-specific data.
        - Do NOT invent or assume missing values.

        2. If CA KNOWLEDGE is provided:
        - Use it to explain financial concepts, tax rules, and meanings.

        3. If BOTH DOCUMENT CONTEXT and CA KNOWLEDGE are present:
        - Combine them intelligently:
        • Use DOCUMENT for facts/data
        • Use CA KNOWLEDGE for explanation
        - Do NOT ignore either if both are relevant.

        4. If the answer is NOT clearly present in the document:
        - Say exactly:
        "The document does not contain that information."

        5. If NO DOCUMENT CONTEXT is provided:
        - Use CA KNOWLEDGE if available.
        - Otherwise, answer using general knowledge.

        ----------------------------------------

        🔹 DOCUMENT HANDLING

        6. If multiple documents exist:
        - Use only the most relevant content.
        - Do not mix unrelated documents.

        7. If user says:
        - "Show full document"
        - "What is written in it"
        - "Read the document"
        → Return complete document text without summarizing.

        8. If user refers to:
        - "first document"
        - "earlier file"
        - "that image"
        → Use chat memory to identify correct reference.

        ----------------------------------------

        🔹 BEHAVIOR RULES

        9. Be professional, structured, and precise.
        10. Never hallucinate financial, legal, or tax data.
        11. If no relevant context exists:
        - Answer to the best of your knowledge.
        - If unsure, clearly say you are not certain.

        ----------------------------------------

        🔹 RESPONSE FORMAT (IMPORTANT)

        When applicable:
        - Start with a clear answer
        - Then provide explanation
        - Keep responses clean and structured

        ----------------------------------------

        Your goal:
        Provide accurate, context-aware, document-grounded financial assistance by intelligently combining document data and financial knowledge.
        """


    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Context:\n{context}"},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_completion_tokens=1024,
    )

    bot_reply = completion.choices[0].message.content
    if source_used:
        bot_reply += "\n\nSource: " + ", ".join(source_used)
    else:
        bot_reply += "\n\nSource: General Knowledge"

    # Save bot reply
    cursor.execute(
        "INSERT INTO messages (username, session_id, sender, message) VALUES (?, ?, ?, ?)",
        (username, session_id, "bot", bot_reply)
    )
    conn.commit()

    add_memory(username, session_id, "bot", bot_reply)

    return JSONResponse({"reply": bot_reply})

@app.get("/sessions")
async def get_sessions(username: str):
    cursor.execute(
        """
        SELECT session_id, title
        FROM sessions
        WHERE username=?
        ORDER BY rowid DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()

    return {
        "sessions": [
            {
                "id": session_id,
                "title": title
            }
            for session_id, title in rows
        ]
    }




@app.post("/rename_session")
async def rename_session(data: dict = Body(...)):
    session_id = data.get("session_id")
    title = data.get("title")

    cursor.execute(
        "UPDATE sessions SET title=? WHERE session_id=?",
        (title, session_id)
    )
    conn.commit()

    return {"status": "success"}

@app.post("/delete_session")
async def delete_session(data: dict = Body(...)):
    session_id = data.get("session_id")

    cursor.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
    cursor.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
    conn.commit()

    return {"status": "deleted"}


@app.get("/logout")
async def logout():
    return RedirectResponse(url="/")



# to run the code
# uvicorn main:app --host localhost --port 8000
# HARD REFRESH == CTRL + SHIFT + R FOR UI