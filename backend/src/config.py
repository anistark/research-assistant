"""
Configuration settings for the Research Assistant API
"""
import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "") # Optional

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
