import chromadb
import uuid
from sentence_transformers import SentenceTransformer

# ---------------- EMBEDDING MODEL ----------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    return embedding_model.encode([text])[0].tolist()


# ---------------- CHROMA CLIENT ----------------
chroma_client = chromadb.PersistentClient(path="chroma_db")


# =========================================================
# 🧠 COLLECTION 1: CHAT MEMORY
# =========================================================
chat_collection = chroma_client.get_or_create_collection(
    name="chat_memory"
)


def add_memory(user: str, session_id: str, role: str, content: str):
    doc_id = str(uuid.uuid4())

    chat_collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embed_text(content)],
        metadatas=[{
            "user": user,
            "session_id": session_id,
            "role": role
        }]
    )


def retrieve_memory(query: str, session_id: str, top_k: int = 5):
    results = chat_collection.query(
        query_embeddings=[embed_text(query)],
        n_results=top_k,
        where={"session_id": session_id}
    )

    docs = results.get("documents", [])
    flattened = []
    for sublist in docs:
        flattened.extend(sublist)

    return flattened



# =========================================================
# 📄 COLLECTION 2: UPLOADED DOCUMENTS
# =========================================================
document_collection = chroma_client.get_or_create_collection(
    name="uploaded_documents"
)


def add_uploaded_document(user: str, session_id: str, filename: str, content: str):
    doc_id = str(uuid.uuid4())

    document_collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embed_text(content)],
        metadatas=[{
            "user": user,
            "session_id": session_id,
            "filename": filename
        }]
    )

    return doc_id


def search_documents(query: str, session_id: str, top_k: int = 3):
    results = document_collection.query(
        query_embeddings=[embed_text(query)],
        n_results=top_k,
        where={"session_id": session_id}
    )

    docs = results.get("documents", [])
    flattened = []
    for sublist in docs:
        flattened.extend(sublist)

    return flattened



def get_all_documents(session_id: str):
    results = document_collection.get(
        where={"session_id": session_id}
    )

    if results and results.get("documents"):
        return results["documents"]

    return []

# =========================================================
# 📚 COLLECTION 3: CA BOOKS
# =========================================================
ca_collection = chroma_client.get_or_create_collection(
    name="ca_books"
)

def add_ca_book(content: str, source: str):
    doc_id = str(uuid.uuid4())

    ca_collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embed_text(content)],
        metadatas=[{
            "source": source,
            "type": "ca_book"
        }]
    )

def search_ca_books(query: str, top_k: int = 3):
    results = ca_collection.query(
        query_embeddings=[embed_text(query)],
        n_results=top_k,
        include=["documents", "distances"]
    )

    docs = results.get("documents", [])
    distances = results.get("distances", [])

    flattened_docs = []
    flattened_distances = []

    # 🔹 Flatten results
    for dlist, dist_list in zip(docs, distances):
        flattened_docs.extend(dlist)
        flattened_distances.extend(dist_list)

    filtered_docs = []

    print("\n===== DISTANCE DEBUG =====")

    for i, (doc, dist) in enumerate(zip(flattened_docs, flattened_distances)):
        print(f"\nChunk {i+1}")
        print(f"Distance: {dist}")
        print(f"Text: {doc[:120]}...")

        #APPLY FILTER HERE
        if dist < 1.2:
            filtered_docs.append(doc)

    print("=================================\n")

    return filtered_docs   # return filtered, not all
# =========================================================
# 📄 COLLECTION 4: TXT KNOWLEDGE
# =========================================================
txt_collection = chroma_client.get_or_create_collection(
    name="txt_knowledge"
)

def add_txt_knowledge(content: str, source: str):
    doc_id = str(uuid.uuid4())

    txt_collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embed_text(content)],
        metadatas=[{
            "source": source,
            "type": "txt"
        }]
    )

def search_txt_knowledge(query: str, top_k: int = 3):
    results = txt_collection.query(
        query_embeddings=[embed_text(query)],
        n_results=top_k,
        include=["documents", "distances"]
    )

    docs = results.get("documents", [])
    distances = results.get("distances", [])

    flattened_docs = []
    flattened_distances = []

    for dlist, dist_list in zip(docs, distances):
        flattened_docs.extend(dlist)
        flattened_distances.extend(dist_list)

    filtered_docs = []

    print("\n===== TXT DEBUG =====")

    for doc, dist in zip(flattened_docs, flattened_distances):
        print(f"Distance: {dist}")

        if dist < 1.2:   # you can keep same logic
            filtered_docs.append(doc)

    print("=====================\n")

    return filtered_docs