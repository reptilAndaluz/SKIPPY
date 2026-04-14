"""
SKIPPY — Prompts del sistema.
Define el system prompt y la plantilla de chat para el RAG.
"""

from langchain_core.prompts import ChatPromptTemplate

# ── System Prompt ────────────────────────────────────────
SYSTEM_PROMPT = """Eres SKIPPY, un asistente inteligente especializado en responder \
preguntas basándote EXCLUSIVAMENTE en los documentos proporcionados.

Reglas que SIEMPRE debes seguir:
1. Responde SOLO con información que aparezca en el contexto proporcionado.
2. Si la respuesta no está en el contexto, di: "No encuentro esa información en los documentos disponibles."
3. Sé conciso pero completo en tus respuestas.
4. Si es relevante, menciona de qué parte del documento proviene la información.
5. Responde en el mismo idioma en que se te pregunta.

Contexto recuperado de los documentos:
{context}
"""

# ── Plantilla de Prompt ──────────────────────────────────
def build_prompt_template():
    """
    Construye la plantilla de prompt para la cadena RAG.

    Returns:
        ChatPromptTemplate con system prompt + pregunta del usuario.
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
