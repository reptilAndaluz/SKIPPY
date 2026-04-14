"""
Tests para el módulo de ingesta de datos.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.config import RAW_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.data_ingestion import load_pdfs, split_documents, ingest_all


class TestLoadPdfs:
    """Tests para la carga de PDFs."""

    def test_load_pdfs_from_raw_dir(self):
        """Verifica que se cargan PDFs del directorio raw."""
        docs = load_pdfs(RAW_DIR)
        # Si hay PDFs en data/raw/, debemos obtener documentos
        pdf_files = list(RAW_DIR.glob("*.pdf"))
        if pdf_files:
            assert len(docs) > 0, "Debería cargar al menos un documento"
            # Cada documento debe tener contenido
            for doc in docs:
                assert hasattr(doc, "page_content")
                assert hasattr(doc, "metadata")
        else:
            assert len(docs) == 0

    def test_load_pdfs_empty_dir(self, tmp_path):
        """Verifica que retorna lista vacía si no hay PDFs."""
        docs = load_pdfs(tmp_path)
        assert docs == []

    def test_documents_have_metadata(self):
        """Verifica que los documentos cargados tienen metadata."""
        docs = load_pdfs(RAW_DIR)
        if docs:
            assert "source" in docs[0].metadata


class TestSplitDocuments:
    """Tests para el chunking de documentos."""

    def test_split_creates_chunks(self):
        """Verifica que el splitting genera chunks."""
        docs = load_pdfs(RAW_DIR)
        if docs:
            chunks = split_documents(docs)
            assert len(chunks) > 0
            # Debería haber más chunks que documentos originales
            assert len(chunks) >= len(docs)

    def test_chunk_size_respected(self):
        """Verifica que los chunks respetan el tamaño máximo."""
        docs = load_pdfs(RAW_DIR)
        if docs:
            chunks = split_documents(docs)
            for chunk in chunks:
                # Permitir un margen por el splitter
                assert len(chunk.page_content) <= CHUNK_SIZE * 1.5


class TestIngestAll:
    """Tests para el pipeline completo de ingesta."""

    def test_ingest_all_returns_chunks(self):
        """Verifica que ingest_all retorna chunks."""
        chunks = ingest_all()
        pdf_files = list(RAW_DIR.glob("*.pdf"))
        if pdf_files:
            assert len(chunks) > 0
        else:
            assert len(chunks) == 0
