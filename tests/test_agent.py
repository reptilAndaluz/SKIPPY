"""
Tests para el agente RAG.
Requiere Ollama corriendo con los modelos descargados.
"""

import pytest

from src.agent import get_llm, build_rag_chain, query
from src.config import LLM_MODEL


class TestGetLlm:
    """Tests para la creación del LLM."""

    def test_llm_creation(self):
        """Verifica que se crea el LLM correctamente."""
        llm = get_llm()
        assert llm is not None
        assert llm.model == LLM_MODEL


class TestRagChain:
    """Tests para la cadena RAG (requiere datos ingestados + Ollama)."""

    @pytest.mark.slow
    def test_build_rag_chain(self):
        """Verifica que se construye la cadena RAG."""
        chain = build_rag_chain()
        assert chain is not None

    @pytest.mark.slow
    def test_query_returns_response(self):
        """Verifica que una consulta devuelve respuesta."""
        response = query("¿De qué trata el documento?")
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
