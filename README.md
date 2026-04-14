# S.K.I.P.P.Y.

### Semantic Knowledge Indexing & Processing Pipeline Yielder

Sistema de **RAG** (Retrieval-Augmented Generation) optimizado para procesadores con gráficos integrados. Permite ingestar documentos PDF, vectorizarlos localmente con **ChromaDB**, y consultarlos mediante un LLM ligero a través de una interfaz de terminal.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|---|---|
| **Framework RAG** | LangChain |
| **LLM** | Ollama — `llama3.2:1b` |
| **Embeddings** | Ollama — `nomic-embed-text` |
| **Vector Store** | ChromaDB (persistencia local) |
| **Lectura de PDFs** | PyPDF |

---

## 📋 Requisitos Previos

1. **Python 3.10+** instalado en tu sistema.
2. **Ollama** instalado ([instrucciones](https://ollama.com/download)).
3. Descargar los modelos necesarios:
   ```bash
   ollama pull llama3.2:1b
   ollama pull nomic-embed-text
   ```

---

## ⚡ Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd SKIPPY

# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

### 1. Ingestar documentos

Coloca tus archivos PDF en la carpeta `data/raw/` y ejecuta:

```bash
source .venv/bin/activate
python -m src.main --ingest
```

Esto leerá los PDFs, los dividirá en fragmentos de 512 tokens y generará los embeddings en `data/chroma_db/`.

### 2. Chat interactivo

```bash
source .venv/bin/activate
python -m src.main
```

Escribe tus preguntas en el prompt `[SKIPPY] >>>`. El sistema buscará en los documentos ingestados y generará respuestas basadas exclusivamente en ellos.

- Escribe `salir` o `exit` para terminar.

---

## 📁 Estructura del Proyecto

```
SKIPPY/
├── data/
│   ├── raw/              # PDFs a ingestar
│   └── chroma_db/        # Vectores persistidos (auto-generado)
├── src/
│   ├── config.py          # Configuración central (rutas, modelos, parámetros)
│   ├── data_ingestion.py  # Carga de PDFs y chunking
│   ├── vector_store.py    # Gestión de ChromaDB y embeddings
│   ├── prompts.py         # System prompt del RAG
│   ├── agent.py           # Cadena RAG (retriever → LLM → respuesta)
│   └── main.py            # CLI (--ingest | chat)
├── tests/
│   ├── test_ingestion.py  # Tests de ingesta y chunking
│   └── test_agent.py      # Tests del agente RAG
├── requirements.txt       # Dependencias con versiones fijadas
├── .env                   # Variables de entorno (no versionado)
├── .env.example           # Ejemplo de configuración
└── .gitignore
```

---

## 🧪 Tests

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

---

## ⚙️ Configuración

Las variables principales se encuentran en `src/config.py`:

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `LLM_MODEL` | `llama3.2:1b` | Modelo de lenguaje |
| `EMBED_MODEL` | `nomic-embed-text` | Modelo de embeddings |
| `CHUNK_SIZE` | `512` | Tamaño de fragmentos (tokens) |
| `CHUNK_OVERLAP` | `50` | Solapamiento entre fragmentos |
| `NUM_THREADS` | `CPU / 2` | Hilos para procesamiento |

---

## 📝 Notas

- Los directorios `data/` y `.venv/` están en el `.gitignore` por cuestiones de rendimiento y privacidad.
- Asegúrate de que `ollama serve` esté corriendo antes de usar el sistema.
- El sistema está optimizado para hardware con recursos limitados (gráficos integrados).

---

## 🗺️ Hoja de Ruta (Roadmap)

- [x] **Fase 1** — Configuración del Entorno
- [x] **Fase 2** — Ingesta y Vectorización
- [x] **Fase 3** — Motor de Consulta (RAG)
- [x] **Fase 4** — Interfaz CLI y Optimización
