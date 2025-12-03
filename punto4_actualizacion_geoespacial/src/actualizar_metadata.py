# actualizar_metadata.py

import requests
from typing import Optional, Dict, Any

from config import BASE_URL, API_TOKEN


def actualizar_metadata_geoespacial(
    internal_id: str,
    persistent_id: Optional[str],
    bloque_geoespacial: Dict[str, Any],
) -> tuple[bool, str]:
    """
    Actualiza el bloque geoespacial de un dataset.

    - Si hay persistentId (dataset ya tiene DOI), usa el endpoint con :persistentId.
    - Si NO hay persistentId (dataset solo tiene ID interno), usa el endpoint por ID.

    Retorna (ok, mensaje).
    """
    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {
        "metadataBlocks": {
            "geospatial": bloque_geoespacial,
        }
    }

    # Caso 1: usar persistentId
    if persistent_id:
        url = (
            f"{BASE_URL}/api/datasets/:persistentId/editMetadata"
            f"?persistentId={persistent_id}&replace=true"
        )
    else:
        # Caso 2: usar ID interno
        url = (
            f"{BASE_URL}/api/datasets/{internal_id}/editMetadata"
            f"?replace=true"
        )

    resp = requests.put(url, headers=headers, json=payload, timeout=15)

    if resp.status_code != 200:
        return False, f"Error {resp.status_code}: {resp.text}"

    return True, "OK"
