"""
SKIPPY — Configuración central del proyecto.
Rutas, modelos y parámetros de chunking.
"""

import os
from pathlib import Path

# ── Rutas ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Crear directorios si no existen
RAW_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# ── Parámetros de Chunking ───────────────────────────────
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# ── Modelos Ollama ───────────────────────────────────────
LLM_MODEL = "llama3.2:1b"
EMBED_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ── Rendimiento ─────────────────────────────────────────
NUM_THREADS = max(1, (os.cpu_count() or 2) // 2)  # Mitad de los núcleos disponibles

# ── ChromaDB ─────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "skippy_docs"
