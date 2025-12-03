# actualizar_metadata_geoespacial.py
import requests
from config import BASE_URL, API_TOKEN

def actualizar_metadata_geoespacial(dataset_id: int, bloque_geoespacial: dict, replace: bool = True):
    """
    Actualiza el bloque de metadatos geoespaciales de un dataset en Dataverse.

    Usa el endpoint:
      PUT /api/datasets/editMetadata/{id}?replace=true

    Parámetros
    ----------
    dataset_id : int
        ID interno del dataset en Dataverse (ej: 13).
    bloque_geoespacial : dict
        Diccionario con la estructura del bloque 'geospatial' (clave 'fields').
    replace : bool
        True => reemplaza el bloque existente.
        False => intenta solo agregar.
    """

    # Endpoint por ID interno (no usa :persistentId)
    url = f"{BASE_URL}/api/datasets/editMetadata/{dataset_id}"
    params = {
        "replace": "true" if replace else "false"
    }

    # Para editMetadata la documentación indica que el JSON puede contener
    # solo los metadatos a editar, organizados por metadataBlocks.
    payload = {
        "metadataBlocks": {
            "geospatial": bloque_geoespacial
        }
    }

    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        resp = requests.put(
            url,
            params=params,
            headers=headers,
            json=payload,
            timeout=30
        )
    except requests.RequestException as e:
        return False, f"Error de red al actualizar metadata: {e}"

    if resp.status_code != 200:
        # Devolvemos el cuerpo tal cual para que lo veas en el reporte
        return False, f"Error {resp.status_code}: {resp.text}"

    # Si todo salió bien, tratamos de extraer versión/estado de la respuesta
    try:
        data = resp.json().get("data", {})
        version = data.get("versionNumber", "desconocida")
        estado = data.get("versionState", "desconocido")
        return True, f"OK (versión {version}, estado {estado})"
    except ValueError:
        # No hay JSON pero el status fue 200, igual lo damos por bueno
        return True, "OK (respuesta sin JSON)"
