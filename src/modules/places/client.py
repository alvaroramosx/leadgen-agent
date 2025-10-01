import time
import requests

from src.utils.http import fetch_json_post


PLACES_TEXTSEARCH_V1 = "https://places.googleapis.com/v1/places:searchText"
PLACES_DETAILS_V1 = "https://places.googleapis.com/v1/places/{place_id}"


def text_search(query: str, api_key: str, page_token: str | None, timeout_s: float) -> dict:
    """Places API (New) Text Search v1: POST JSON.

    Documentación: https://developers.google.com/maps/documentation/places/web-service/search-text
    Soporta `pageToken` para paginación.
    """
    body = {
        "textQuery": query,
        "languageCode": "es",
        "regionCode": "ES",
    }
    if page_token:
        body["pageToken"] = page_token
    headers = {"X-Goog-Api-Key": api_key, "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.internationalPhoneNumber,places.websiteUri,nextPageToken"}
    return fetch_json_post(PLACES_TEXTSEARCH_V1, body, timeout_s, headers)


def details(place_id: str, api_key: str, timeout_s: float) -> dict:
    """Places Details v1: GET con FieldMask.

    Nota: Podemos evitar esta llamada si el Text Search ya devuelve campos suficientes.
    """
    url = PLACES_DETAILS_V1.format(place_id=place_id)
    headers = {"X-Goog-Api-Key": api_key, "X-Goog-FieldMask": "id,displayName,formattedAddress,internationalPhoneNumber,websiteUri"}
    return fetch_json_post(url, {}, timeout_s, headers)


def fetch_places_with_details(query: str, api_key: str, max_results: int, timeout_s: float) -> list[dict]:
    """Itera páginas de Text Search v1 y normaliza datos necesarios."""
    collected: list[dict] = []
    page_token: str | None = None
    while len(collected) < max_results:
        data = text_search(query, api_key, page_token, timeout_s)
        places = data.get("places", []) or []
        for item in places:
            if len(collected) >= max_results:
                break
            name = (item.get("displayName") or {}).get("text") or ""
            address = item.get("formattedAddress", "")
            phone = item.get("internationalPhoneNumber", "")
            website = item.get("websiteUri", "")
            collected.append({
                "name": name,
                "address": address,
                "phone": phone,
                "website": website,
            })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
        time.sleep(1.2)  # respetar pacing mínimo entre páginas
    return collected


