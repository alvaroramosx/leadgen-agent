import requests


USER_AGENT = "LeadgenAgent/1.0"


def fetch_json(url: str, timeout_s: float) -> dict:
    """GET simple con User-Agent y parseo JSON con raise para errores HTTP."""
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()


def fetch_text(url: str, timeout_s: float) -> str:
    """GET que devuelve texto o cadena vacía si hay fallo.

    Útil para scraping tolerante a errores (no interrumpe pipeline).
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=timeout_s)
        if not resp.ok:
            return ""
        return resp.text or ""
    except Exception:
        return ""


def fetch_json_post(url: str, body: dict, timeout_s: float, extra_headers: dict | None = None) -> dict:
    """POST JSON con User-Agent y cabeceras extra; devuelve JSON o lanza en HTTP error."""
    headers = {"User-Agent": USER_AGENT, "Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    resp = requests.post(url, json=body, headers=headers, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()


