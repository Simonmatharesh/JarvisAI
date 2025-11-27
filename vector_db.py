# vector_db.py
import chromadb
import uuid
from sentence_transformers import SentenceTransformer

# Local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma client
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("dataset_summaries")

def get_embedding(text):
    return model.encode(text).tolist()  # converts to list for Chroma

def add_text(text, text_id=None, metadata=None):
    text_id = text_id or str(uuid.uuid4())
    collection.add(
        ids=[text_id],
        documents=[text],
        metadatas=[metadata or {}],
        embeddings=[get_embedding(text)]
    )

def query_text(query, top_k=3):
    emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[emb],
        n_results=top_k
    )
    return results['documents'][0] if results['documents'] else []
