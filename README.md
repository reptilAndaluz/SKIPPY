# Semantic Knowledge Indexing & Processing Pipeline Yielder

## S.K.I.P.P.Y

Este proyecto implementa un sistema de RAG optimizado para el procesadores con graficos integrados

## Requisitos

1. Instalar Ollama en tu sistema
2. Descargar modelos:
   - `ollama pull llama3.2:1b`
   - `ollama pull nomic-embed-text`

## Configuración

1. Crea tu entorno virtual y actívalo.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Coloca tus documentos en la carpeta `/data`.

## Notas

- El proyecto usa _LlamaIndex_ y _ChromaDB_.
- Los datos de `/data` y `/storage` están en el `.gitignore` por cuestiones de rendimiento y privacidad



## 🗺️ Hoja de Ruta (Roadmap)

El desarrollo se divide en cuatro fases principales para asegurar la estabilidad en el hardware:

### Fase 1: Configuración del Entorno (Completado)

- [x] Instalación de Ollama en el sistema.
- [x] Descarga de modelos ligeros (`llama3.2:1b` y `nomic-embed-text`).
- [x] Configuración del entorno virtual de Python y archivo `.gitignore`.

### Fase 2: Ingesta y Vectorización (Siguiente paso)

- [ ] Implementar el lector de documentos.
- [ ] Configurar el "Chunking" optimizado (512 tokens) para CPU.
- [ ] Integrar **ChromaDB** para persistencia local de vectores.
- [ ] Script de validación: Convertir un PDF en vectores y guardarlo en `/storage`.

### Fase 3: Motor de Consulta (RAG)

- [ ] Configurar el prompt dinámico (System Prompt).
- [ ] Implementar la búsqueda por similitud entre la duda del usuario y la DB.
- [ ] Conectar el contexto recuperado con el LLM para generar respuestas.

### Fase 4: Interfaz y Optimización

- [ ] Crear un bucle de chat por terminal (CLI).
- [ ] Optimizar el uso de hilos (threads) para el procesador.
- [ ] Manejo de memoria: Limpiar el contexto para evitar picos de RAM.
