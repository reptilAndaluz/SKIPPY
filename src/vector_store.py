"""
SKIPPY — Módulo del Vector Store.
Gestiona ChromaDB para persistencia local de embeddings.
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from src.config import (
    EMBED_MODEL,
    OLLAMA_BASE_URL,
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
)


def get_embeddings():
    """
    Crea una instancia del modelo de embeddings usando Ollama.

    Returns:
        OllamaEmbeddings configurado con nomic-embed-text.
    """
    return OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )


def create_vector_store(chunks):
    """
    Crea un vector store en ChromaDB a partir de los chunks proporcionados.
    Los embeddings se persisten en disco en data/chroma_db/.

    Args:
        chunks: Lista de Document chunks a vectorizar.

    Returns:
        Instancia de Chroma con los vectores almacenados.
    """
    print(f"\n🧮 Generando embeddings para {len(chunks)} fragmentos...")
    print(f"   Modelo: {EMBED_MODEL}")
    print(f"   Persistencia: {CHROMA_DIR}")

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"✅ Vector store creado con {len(chunks)} vectores en ChromaDB")
    return vector_store


def load_vector_store():
    """
    Carga un vector store existente desde disco.

    Returns:
        Instancia de Chroma con los vectores previamente almacenados.
    """
    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    # Verificar que hay datos
    count = vector_store._collection.count()
    if count == 0:
        print("⚠️  El vector store está vacío. Ejecuta --ingest primero.")
    else:
        print(f"📦 Vector store cargado: {count} vectores disponibles")

    return vector_store


def get_retriever(k=3):
    """
    Retorna un retriever configurado para búsqueda por similitud.

    Args:
        k: Número de documentos similares a recuperar (default: 3).

    Returns:
        Retriever de LangChain listo para usar en la cadena RAG.
    """
    vector_store = load_vector_store()
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
