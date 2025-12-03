# publicar_dataset.py

import requests
from config import BASE_URL, API_TOKEN


def publicar_nueva_version(dataset_id: str, tipo: str = "minor") -> tuple[bool, str | None, str | None, str]:
    """
    Llama a /api/datasets/{id}/actions/:publish?type=...
    Retorna (ok, version, estado, mensaje).
    """
    url = f"{BASE_URL}/api/datasets/{dataset_id}/actions/:publish?type={tipo}"
    headers = {"X-Dataverse-key": API_TOKEN}

    resp = requests.post(url, headers=headers, timeout=15)

    if resp.status_code not in (200, 202):
        return False, None, None, f"Error {resp.status_code}: {resp.text}"

    data = resp.json().get("data", {})

    version = None
    estado = None

    if isinstance(data, dict):
        vnum = data.get("versionNumber")
        vmin = data.get("versionMinorNumber")
        if vnum is not None and vmin is not None:
            version = f"{vnum}.{vmin}"
        estado = data.get("versionState")

    return True, version, estado, "OK"
