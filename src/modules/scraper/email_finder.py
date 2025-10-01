import re

from src.utils.http import fetch_text


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def normalize_url(url: str) -> str:
    """Asegura que la URL tenga esquema (https) para requests."""
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url


def find_email_in_website(website_url: str, timeout_s: float) -> str:
    """Busca emails en página raíz y rutas frecuentes de contacto.

    Estrategia básica (MVP): inspección por regex; no usa parser HTML para
    mantener dependencia ligera y tolerar HTML defectuoso.
    """
    base = normalize_url(website_url)
    if not base:
        return ""
    candidates = [
        base,
        base.rstrip("/") + "/contacto",
        base.rstrip("/") + "/contact",
    ]
    for url in candidates:
        html = fetch_text(url, timeout_s)
        if not html:
            continue
        matches = EMAIL_REGEX.findall(html)
        if matches:
            for email in matches:
                if not re.search(r"example\.com|\.png|\.jpg|\.jpeg|\.gif", email, re.I):
                    return email
            return matches[0]
    return ""


