# obtener_metadata_actual.py

import requests
from config import BASE_URL, API_TOKEN


def obtener_geoespacial_actual(dataset_id: str) -> dict | None:
    """
    Devuelve el bloque de metadatos geoespaciales actual (:latest).
    Si el dataset no tiene bloque 'geospatial', devuelve None.
    """
    url = f"{BASE_URL}/api/datasets/{dataset_id}/versions/:latest/metadata/geospatial"
    headers = {"X-Dataverse-key": API_TOKEN}

    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code == 404:
        # No existe el bloque geospatial todavía
        return None

    resp.raise_for_status()
    return resp.json()["data"]
