"""
SKIPPY — Agente RAG.
Conecta el retriever, el prompt y el LLM en una cadena RAG.
"""

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import LLM_MODEL, OLLAMA_BASE_URL, NUM_THREADS
from src.prompts import build_prompt_template
from src.vector_store import get_retriever


def get_llm():
    """
    Crea una instancia del LLM usando Ollama.

    Returns:
        ChatOllama configurado con el modelo y threads optimizados.
    """
    return ChatOllama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        num_thread=NUM_THREADS,
        temperature=0.1,  # Baja temperatura para respuestas más precisas
    )


def _format_docs(docs):
    """Formatea los documentos recuperados como texto plano."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    """
    Construye la cadena RAG completa:
    pregunta → retriever → prompt con contexto → LLM → respuesta.

    Returns:
        Cadena ejecutable de LangChain.
    """
    retriever = get_retriever()
    prompt = build_prompt_template()
    llm = get_llm()
    parser = StrOutputParser()

    rag_chain = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | parser
    )

    return rag_chain


def query(question):
    """
    Ejecuta una consulta contra la cadena RAG.

    Args:
        question: Pregunta del usuario en texto plano.

    Returns:
        Respuesta generada por el LLM basada en los documentos.
    """
    chain = build_rag_chain()
    response = chain.invoke(question)
    return response
