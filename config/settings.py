"""
Configuration centralisée (Bloc 3 — paramètres LLM)
"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)

# Modèles OpenAI
LLM_CONFIG = {
    "research": {
        "model": os.getenv("OPENAI_RESEARCH_MODEL", "gpt-4o-mini"),
        "max_tokens": 700,
    },
    "planner": {
        "model": os.getenv("OPENAI_PLANNER_MODEL", "gpt-4o-mini"),
        "max_tokens": 2000,
    },
}


CHROMA_PATH = "chromadb_cities_openai_v1"
COLLECTION_NAME = "morocco_trip_cities_openai_v1"

# Mémoire
DEFAULT_THREAD_ID = "default_session"