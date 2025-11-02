"""Configuration settings for the RAG Chatbot application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from multiple locations
# Try backend directory first, then project root
backend_dir = Path(__file__).parent.parent.parent
project_root = backend_dir.parent
load_dotenv(backend_dir / ".env")
load_dotenv(project_root / ".env")
load_dotenv()  # Also try default locations

# Base paths
# Go up from: backend/app/utils/config.py (4 levels) -> RAG_Chatbot
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Model Provider Selection (priority: GEMINI > OPENAI > LOCAL)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()  # "gemini", "openai", or "local"
USE_GEMINI = os.getenv("USE_GEMINI", "").lower() == "true" or (LLM_PROVIDER == "gemini" and GEMINI_API_KEY)
USE_OPENAI = os.getenv("USE_OPENAI", "").lower() == "true" or (LLM_PROVIDER == "openai" and OPENAI_API_KEY)

# Model settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-pro")  # Default to Gemini if not specified
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # gemini-1.5-flash, gemini-1.5-pro, gemini-pro

# Chunking settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Retrieval settings
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))

# Vector store settings
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chroma")  # "chroma" or "faiss"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

