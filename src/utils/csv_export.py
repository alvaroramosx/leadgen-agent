import csv
from pathlib import Path


def ensure_dir(path: Path) -> None:
    """Crea directorios intermedios si no existen."""
    path.mkdir(parents=True, exist_ok=True)


def export_to_csv(leads: list[dict], output_path: Path) -> None:
    """Escribe CSV con columnas fijas para consumo externo sencillo."""
    ensure_dir(output_path.parent)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Direccion", "Telefono", "Web", "Email", "Sector", "Ubicacion"])
        for lead in leads:
            writer.writerow([
                lead.get("name", ""),
                lead.get("address", ""),
                lead.get("phone", ""),
                lead.get("website", ""),
                lead.get("email", ""),
                lead.get("sector", ""),
                lead.get("ubicacion", ""),
            ])


