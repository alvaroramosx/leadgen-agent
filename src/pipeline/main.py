"""Punto de entrada CLI.

Este módulo solo parsea argumentos y delega la ejecución en `run_pipeline`.
Mantenerlo delgado simplifica pruebas y reusabilidad del pipeline desde otros módulos.
"""

import argparse
from src.pipeline.runner import run_pipeline
import os


def parse_args() -> argparse.Namespace:
    """Define argumentos y devuelve el namespace sin lógica adicional."""
    parser = argparse.ArgumentParser(description="Leadgen con Google Places → CSV (config por archivo y overrides por args)")
    parser.add_argument("--config", help="Ruta a archivo de configuración (yaml/yml/json)")
    parser.add_argument("--sector", help="Sector a buscar (p.ej. restaurantes)")
    parser.add_argument("--provincia", help="Provincia (p.ej. Madrid)")
    parser.add_argument("--municipio", help="Municipio (p.ej. Alcobendas)")
    parser.add_argument("--apiKey", help="API Key de Google Places (o GOOGLE_MAPS_API_KEY)", default=os.getenv("GOOGLE_MAPS_API_KEY"))
    parser.add_argument("--max", type=int, help="Máximo de resultados")
    parser.add_argument("--timeoutMs", type=int, help="Timeout de requests en ms")
    parser.add_argument("--outputDir", help="Directorio de salida para CSV")
    return parser.parse_args()

def main() -> None:
    """Parsea argumentos y delega todo en `run_pipeline`."""
    args = parse_args()

    run_pipeline(
        config=args.config,
        sector=args.sector,
        provincia=args.provincia,
        municipio=args.municipio,
        apiKey=args.apiKey,
        max=args.max,
        timeoutMs=args.timeoutMs,
        outputDir=args.outputDir,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("Interrumpido por el usuario")


