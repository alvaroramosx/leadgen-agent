from pathlib import Path
from typing import Dict, Any, List
import time

from src.config.loader import load_config_file, merge_overrides
from src.modules.places.client import fetch_places_with_details
from src.modules.scraper.email_finder import find_email_in_website
from src.utils.csv_export import export_to_csv
from src.utils.text import sanitize_filename


def load_inputs(
    config: str | None = None,
    sector: str | None = None,
    provincia: str | None = None,
    municipio: str | None = None,
    apiKey: str | None = None,
    max_results: int | None = None,
    timeoutMs: int | None = None,
    outputDir: str | None = None,
) -> Dict[str, Any]:
    """Carga config desde archivo y aplica overrides; valida y prepara el contexto."""
    file_cfg = load_config_file(config)
    overrides = {
        "sector": sector,
        "provincia": provincia,
        "municipio": municipio,
        "apiKey": apiKey,
        "max": max_results,
        "timeoutMs": timeoutMs,
        "outputDir": outputDir,
    }
    cfg = merge_overrides(file_cfg, {k: v for k, v in overrides.items() if v is not None and v != ""})

    sector_v = cfg.get("sector", "")
    provincia_v = cfg.get("provincia", "")
    municipio_v = cfg.get("municipio", "")
    api_key_v = cfg.get("apiKey", "")
    max_results = int(cfg.get("max", 50))
    timeout_s = max(int(cfg.get("timeoutMs", 15000)), 1000) / 1000.0
    output_dir = Path(cfg.get("outputDir", "data"))

    if not sector_v or not provincia_v or not municipio_v:
        raise SystemExit("Faltan parámetros: sector/provincia/municipio. Usa archivo de config o pasa args.")
    if not api_key_v:
        raise SystemExit("Falta API Key de Google Places. Usa --apiKey, GOOGLE_MAPS_API_KEY o config.")

    query = f"{sector_v} en {municipio_v}, {provincia_v}, España"

    return {
        "sector": sector_v,
        "provincia": provincia_v,
        "municipio": municipio_v,
        "api_key": api_key_v,
        "max_results": max_results,
        "timeout_s": timeout_s,
        "output_dir": output_dir,
        "query": query,
    }


def fetch_leads(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Busca en Places y enriquece con posibles emails."""
    print(f"Buscando: {ctx['query']}")
    places = fetch_places_with_details(ctx["query"], ctx["api_key"], ctx["max_results"], ctx["timeout_s"])
    leads: List[Dict[str, Any]] = []
    for p in places:
        website = p.get("website", "")
        email = ""
        if website:
            try:
                email = find_email_in_website(website, ctx["timeout_s"])
            except Exception:
                email = ""
        lead = {
            "name": p.get("name", ""),
            "address": p.get("address", ""),
            "phone": p.get("phone", ""),
            "website": website,
            "email": email,
            # Campos adicionales solicitados para el CSV
            "sector": ctx.get("sector", ""),
            "ubicacion": ctx.get("municipio", ""),
        }
        leads.append(lead)
        print(f"+ {lead['name']} | {website or 'sin web'} | {email or 'sin email'}")
    return leads


def export_leads(leads: List[Dict[str, Any]], ctx: Dict[str, Any]) -> Path:
    """Exporta los leads a CSV y devuelve la ruta de salida."""
    stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    out_name = f"leads_{sanitize_filename(ctx['sector'])}_{sanitize_filename(ctx['municipio'])}_{stamp}.csv"
    out_path = ctx["output_dir"] / out_name
    export_to_csv(leads, out_path)
    print(f"\nGuardado: {out_path} ({len(leads)} registros)")
    return out_path


