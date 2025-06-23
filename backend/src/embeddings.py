"""
Embedding generation using OpenAI or sentence-transformers
"""
from typing import List
from fastapi import HTTPException
from .config import OPENAI_API_KEY

# Initialize OpenAI client
openai_client = None

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"OpenAI client initialization failed: {e}")
        print("Falling back to sentence-transformers")
        openai_client = None

def generate_embedding(text: str) -> List[float]:
    """Generate embeddings using OpenAI or fallback to sentence-transformers"""
    if openai_client:
        try:
            response = openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"OpenAI embedding failed: {e}")
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model.encode(text).tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {e}")
