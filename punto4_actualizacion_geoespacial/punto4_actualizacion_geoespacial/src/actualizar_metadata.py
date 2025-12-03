# actualizar_metadata.py
import json
import requests
from config import BASE_URL, API_TOKEN


def actualizar_metadata_geoespacial(
    persistent_id: str,
    bloque_geoespacial: dict,
    replace: bool = True,
) -> tuple[bool, dict | str]:
    """
    Actualiza el bloque de metadatos geoespaciales de un dataset en Dataverse.

    Usa el endpoint:
        PUT /api/datasets/:persistentId/editMetadata?persistentId=$PID&replace=true

    El cuerpo debe tener la forma:
    {
        "metadataBlocks": {
            "geospatial": { ...bloque_geoespacial... }
        }
    }

    Parámetros
    ----------
    persistent_id : str
        DOI/hdl del dataset, por ejemplo: "doi:10.5072/FK2/EREVDH".
    bloque_geoespacial : dict
        Diccionario con la estructura del bloque 'geospatial' ya listo.
    replace : bool
        Si es True, reemplaza el bloque existente; si es False, solo agrega.
    """

    payload = {
        "metadataBlocks": {
            "geospatial": bloque_geoespacial
        }
    }

    # OJO: BASE_URL ya incluye /api/v1
    url = f"{BASE_URL}/datasets/:persistentId/editMetadata"
    params = {
        "persistentId": persistent_id,
        "replace": "true" if replace else "false",
    }

    headers = {
        "X-Dataverse-key": API_TOKEN,
        "Content-Type": "application/json",
    }

    # Debug para ver qué estamos mandando
    payload_str = json.dumps(payload, ensure_ascii=False)
    print(">>> DEBUG payload local (antes del PUT):")
    print(payload_str)
    print(f"URL: {url}")
    print(f"PARAMS: {params}")

    try:
        resp = requests.put(
            url,
            params=params,
            headers=headers,
            data=payload_str,
            timeout=30,
        )
    except requests.RequestException as e:
        return False, f"Error de red al actualizar metadata: {e}"

    print(f"STATUS: {resp.status_code} BODY: {resp.text}")

    if resp.status_code != 200:
        # Lo devolvemos tal cual para el reporte
        return False, f"Error {resp.status_code}: {resp.text}"

    try:
        data = resp.json().get("data", {})
    except ValueError:
        # No devolvió JSON pero fue 200 → lo damos por OK
        return True, {"version": "desconocida", "estado": "desconocido"}

    version = data.get("versionNumber", "desconocida")
    estado = data.get("versionState", "desconocido")

    return True, {"version": version, "estado": estado}
