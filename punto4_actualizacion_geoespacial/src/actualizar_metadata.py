# actualizar_metadata.py
import json
import requests
from config import BASE_URL, API_TOKEN


def actualizar_metadata_geoespacial(
    persistent_id: str,
    bloque_geoespacial: dict,
    replace: bool = True,
) -> tuple[bool, str | dict]:
    """
    Actualiza el bloque de metadatos geoespaciales de un dataset en Dataverse.

    Usa el endpoint oficial:
      PUT {BASE_URL}/datasets/:persistentId/editMetadata
        ?persistentId=doi:...&replace=true|false
    """

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
            timeout=15,
        )
    except requests.RequestException as e:
        return False, f"Error de red al actualizar metadata: {e}"

    # DEBUG opcional: descomenta si necesitas ver qué se envía y qué responde el server
    # print("URL:", resp.request.url)
    # print("PAYLOAD:", resp.request.body)
    # print("STATUS:", resp.status_code, "BODY:", resp.text)

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
