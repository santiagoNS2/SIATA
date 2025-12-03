# actualizar_metadata_geoespacial.py
import json
import requests
from config import BASE_URL, API_TOKEN

def actualizar_metadata_geoespacial(dataset_id: int, bloque_geoespacial: dict, replace: bool = True):
    """
    Actualiza el bloque de metadatos geoespaciales de un dataset en Dataverse.

    - Usa el endpoint nativo: /api/datasets/editMetadata/{id}
    - Envía un JSON en formato 'datasetVersion' con el bloque 'geospatial'.

    Parámetros:
    -----------
    dataset_id : int
        ID interno del dataset en Dataverse (ej: 13).
    bloque_geoespacial : dict
        Diccionario con la estructura del bloque 'geospatial' (clave 'fields').
    replace : bool
        Si es True, reemplaza el bloque existente. Si es False, solo agrega.
    """

    url = f"{BASE_URL}/api/datasets/editMetadata/{dataset_id}"
    params = {
        "replace": "true" if replace else "false"
    }

    payload = {
        "datasetVersion": {
            "metadataBlocks": {
                "geospatial": bloque_geoespacial
            }
        }
    }

    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        resp = requests.put(url, params=params,
                            headers=headers,
                            data=json.dumps(payload))
    except requests.RequestException as e:
        return False, f"Error de red al actualizar metadata: {e}"

    if resp.status_code != 200:
        # Devuelvo texto del servidor para que lo veas en el reporte
        return False, f"Error {resp.status_code}: {resp.text}"

    # Si todo salió bien, Dataverse responde con info de la versión
    try:
        data = resp.json().get("data", {})
    except ValueError:
        # No hay JSON válido, pero el status fue 200 → igual lo damos por OK
        return True, {"version": "desconocida", "estado": "desconocido"}

    version = data.get("versionNumber", "desconocida")
    estado = data.get("versionState", "desconocido")

    return True, {"version": version, "estado": estado}
