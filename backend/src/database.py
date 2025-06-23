"""
Database connection and operations for ChromaDB
"""
import chromadb
from chromadb.config import Settings
from .config import CHROMA_DB_PATH

def get_chroma_client():
    """Get ChromaDB client"""
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_collection():
    """Get or create the research papers collection"""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="research_papers",
        metadata={"hnsw:space": "cosine"}
    )

collection = get_collection()
