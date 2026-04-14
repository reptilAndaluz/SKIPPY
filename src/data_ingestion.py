"""
SKIPPY — Módulo de ingesta de datos.
Lee PDFs desde data/raw/ y los divide en fragmentos (chunks).
"""

import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import RAW_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_pdfs(directory=None):
    """
    Carga todos los archivos PDF del directorio indicado.

    Args:
        directory: Ruta al directorio con PDFs. Por defecto usa RAW_DIR.

    Returns:
        Lista de objetos Document con el contenido de cada página.
    """
    if directory is None:
        directory = RAW_DIR

    pdf_files = glob.glob(str(directory / "*.pdf"))

    if not pdf_files:
        print(f"⚠️  No se encontraron PDFs en {directory}")
        return []

    all_docs = []
    for pdf_path in pdf_files:
        print(f"📄 Cargando: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"   → {len(docs)} páginas extraídas")

    print(f"\n✅ Total: {len(all_docs)} páginas de {len(pdf_files)} archivo(s)")
    return all_docs


def split_documents(documents):
    """
    Divide los documentos en fragmentos más pequeños para vectorización.

    Args:
        documents: Lista de objetos Document.

    Returns:
        Lista de chunks (fragmentos) listos para vectorizar.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    print(f"🔪 Documentos divididos en {len(chunks)} fragmentos "
          f"(chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def ingest_all(directory=None):
    """
    Pipeline completo de ingesta: carga PDFs y los divide en chunks.

    Args:
        directory: Ruta opcional al directorio con PDFs.

    Returns:
        Lista de chunks listos para vectorizar.
    """
    print("=" * 50)
    print("🚀 SKIPPY — Ingesta de documentos")
    print("=" * 50)

    docs = load_pdfs(directory)
    if not docs:
        return []

    chunks = split_documents(docs)
    return chunks
