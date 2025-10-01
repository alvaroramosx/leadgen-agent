import json
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
    HAS_YAML = True
except Exception:
    HAS_YAML = False


DEFAULT_CONFIG_PATHS = [
    Path("config.yaml"),
    Path("config.yml"),
    Path("config.json"),
]


def load_config_file(path: str | None = None) -> Dict[str, Any]:
    """Carga config desde YAML/JSON.

    Orden de búsqueda por defecto: config.yaml → config.yml → config.json.
    """
    candidates = [Path(path)] if path else DEFAULT_CONFIG_PATHS
    # Si el usuario especifica un archivo YAML explícitamente pero no hay PyYAML,
    # salimos con un mensaje claro en lugar de ignorarlo silenciosamente.
    if path:
        p = Path(path)
        if p.suffix.lower() in {".yaml", ".yml"} and not HAS_YAML:
            raise SystemExit(
                "Se indicó un archivo YAML en --config pero PyYAML no está instalado. "
                "Instala PyYAML (pip install PyYAML) o usa un archivo JSON (config.json)."
            )
    for p in candidates:
        if p and p.exists() and p.is_file():
            if p.suffix.lower() in {".yaml", ".yml"} and HAS_YAML:
                with p.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    if not isinstance(data, dict):
                        raise ValueError("El archivo YAML debe contener un objeto (mapping)")
                    return data  # type: ignore
            elif p.suffix.lower() == ".json":
                with p.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("El archivo JSON debe contener un objeto (mapping)")
                    return data  # type: ignore
    return {}


def merge_overrides(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Mezcla config base con overrides, ignorando valores None.

    Los valores "vacíos" intencionados (p.ej. cadena vacía) se respetan.
    """
    result = dict(base)
    for k, v in overrides.items():
        if v is None:
            continue
        result[k] = v
    return result


