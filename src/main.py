"""
SKIPPY — Interfaz de línea de comandos (CLI).
Modos: --ingest para ingestar documentos, sin flags para chat interactivo.
"""

import argparse
import gc
import sys

from src.config import RAW_DIR, CHROMA_DIR


# ── Colores ANSI ─────────────────────────────────────────
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    """Muestra el banner de inicio de SKIPPY."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ███████╗██╗  ██╗██╗██████╗ ██████╗ ██╗   ██╗
 ██╔════╝██║ ██╔╝██║██╔══██╗██╔══██╗╚██╗ ██╔╝
 ███████╗█████╔╝ ██║██████╔╝██████╔╝ ╚████╔╝
 ╚════██║██╔═██╗ ██║██╔═══╝ ██╔═══╝   ╚██╔╝
 ███████║██║  ██╗██║██║     ██║        ██║
 ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝        ╚═╝
{Colors.RESET}
{Colors.DIM} Semantic Knowledge Indexing & Processing Pipeline Yielder{Colors.RESET}
{Colors.DIM} Escribe 'salir' o 'exit' para terminar.{Colors.RESET}
"""
    print(banner)


def run_ingest():
    """Ejecuta el pipeline de ingesta de documentos."""
    from src.data_ingestion import ingest_all
    from src.vector_store import create_vector_store

    chunks = ingest_all()

    if not chunks:
        print(f"\n{Colors.RED}❌ No se encontraron documentos para procesar.{Colors.RESET}")
        print(f"{Colors.YELLOW}   Coloca archivos PDF en: {RAW_DIR}{Colors.RESET}")
        sys.exit(1)

    create_vector_store(chunks)

    print(f"\n{Colors.GREEN}{'=' * 50}")
    print(f"✅ Ingesta completada exitosamente")
    print(f"   📄 {len(chunks)} fragmentos vectorizados")
    print(f"   💾 Persistidos en: {CHROMA_DIR}")
    print(f"{'=' * 50}{Colors.RESET}")


def run_chat():
    """Ejecuta el bucle de chat interactivo."""
    from src.agent import build_rag_chain

    print_banner()

    # Verificar que hay datos ingestados
    try:
        print(f"{Colors.DIM}⏳ Cargando modelo y vector store...{Colors.RESET}")
        chain = build_rag_chain()
        print(f"{Colors.GREEN}✅ Sistema listo.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error al inicializar: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}   ¿Has ejecutado primero 'python -m src.main --ingest'?{Colors.RESET}")
        sys.exit(1)

    while True:
        try:
            # Prompt del usuario
            user_input = input(
                f"\n{Colors.CYAN}{Colors.BOLD}[SKIPPY] >>> {Colors.RESET}"
            ).strip()

            # Comandos de salida
            if user_input.lower() in ("salir", "exit", "quit", "q"):
                print(f"\n{Colors.MAGENTA}👋 ¡Hasta luego!{Colors.RESET}")
                break

            # Ignorar entradas vacías
            if not user_input:
                continue

            # Procesar consulta
            print(f"\n{Colors.DIM}🔍 Buscando en los documentos...{Colors.RESET}")
            response = chain.invoke(user_input)

            # Mostrar respuesta
            print(f"\n{Colors.GREEN}{Colors.BOLD}SKIPPY:{Colors.RESET}")
            print(f"{response}")

            # Limpieza de memoria entre consultas
            gc.collect()

        except KeyboardInterrupt:
            print(f"\n\n{Colors.MAGENTA}👋 ¡Hasta luego!{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}   Intenta de nuevo o escribe 'salir'.{Colors.RESET}")


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="SKIPPY — RAG System optimizado para CPU integrada"
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingestar documentos PDF desde data/raw/ y vectorizarlos",
    )

    args = parser.parse_args()

    if args.ingest:
        run_ingest()
    else:
        run_chat()


if __name__ == "__main__":
    main()
