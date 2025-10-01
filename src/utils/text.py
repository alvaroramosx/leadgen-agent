import re


def sanitize_filename(text: str) -> str:
    """Normaliza y limita nombres para uso seguro en archivos."""
    normalized = (
        text
        .encode("utf-8", "ignore")
        .decode("utf-8", "ignore")
    )
    normalized = re.sub(r"[\u0300-\u036f]", "", normalized)
    normalized = re.sub(r"[^a-zA-Z0-9-_.]", "_", normalized)
    return normalized[:80]


