# actualizar_metadata.py
import json
import requests
from config import BASE_URL, API_TOKEN


def actualizar_metadata_geoespacial(
    persistent_id: str, bloque_geoespacial: dict, replace: bool = True
) -> tuple[bool, str | dict]:
    """
    Actualiza el bloque de metadatos geoespaciales de un dataset en Dataverse.

    Usa el endpoint oficial:
      PUT {BASE_URL}/datasets/:persistentId/editMetadata
        ?persistentId=doi:...&replace=true|false

    Parámetros:
    -----------
    persistent_id : str
        El DOI del dataset, por ejemplo: "doi:10.5072/FK2/FU2RIP".
    bloque_geoespacial : dict
        Diccionario con la estructura del bloque 'geospatial' (con 'fields').
    replace : bool
        True → reemplaza el bloque existente.
        False → agrega sin machacar lo que ya hay.
    """

    # Endpoint nativo basado en persistentId
    url = f"{BASE_URL}/datasets/:persistentId/editMetadata"

    params = {
        "persistentId": persistent_id,
        "replace": "true" if replace else "false",
    }

    payload = {
        "datasetVersion": {
            "metadataBlocks": {
                "geospatial": bloque_geoespacial,
            }
        }
    }

    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.put(
            url,
            params=params,
            headers=headers,
            data=json.dumps(payload),
            timeout=20,
        )
    except requests.RequestException as e:
        return False, f"Error de red al actualizar metadata: {e}"

    if resp.status_code != 200:
        return False, f"Error {resp.status_code}: {resp.text}"

    try:
        data = resp.json().get("data", {})
    except ValueError:
        # Status 200 pero sin JSON → lo consideramos OK
        return True, {"version": "desconocida", "estado": "desconocido"}

    version = data.get("versionNumber", "desconocida")
    estado = data.get("versionState", "desconocido")

    return True, {"version": version, "estado": estado}
