import requests
from typing import Dict, Any, Optional

from config import BASE_URL, API_TOKEN


def _parse_dataset_info(data: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """
    Extrae info básica del dict 'data' devuelto por la API de Dataverse.
    """
    persistent_id = data.get("persistentId")
    internal_id = data.get("id")

    latest_version = data.get("latestVersion", {})
    version_number = latest_version.get("versionNumber")
    version_minor = latest_version.get("versionMinorNumber")
    version_state = latest_version.get("versionState")

    # Buscar el título en el bloque citation
    titulo = None
    citation_block = latest_version.get("metadataBlocks", {}).get("citation", {})
    for field in citation_block.get("fields", []):
        if field.get("typeName") == "title":
            titulo = field.get("value")
            break

    version_str = (
        f"{version_number}.{version_minor}"
        if version_number is not None and version_minor is not None
        else None
    )

    return {
        "id": str(internal_id) if internal_id is not None else None,
        "persistent_id": persistent_id,
        "titulo": titulo,
        "version": version_str,
        "estado": version_state,
    }


def obtener_info_dataset(dataset_identifier: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Intenta obtener información de un dataset a partir de un identificador.
    'dataset_identifier' puede ser:
      - un ID numérico interno (ej: '2')
      - un persistentId (ej: 'doi:10.5072/FK2/CBML0G')

    Estrategia:
      1) Intentar /api/datasets/{id}
      2) Si 404, intentar /api/datasets/:persistentId/?persistentId=...
      3) Si también 404, devolver None (dataset no encontrado).
    """
    headers = {"X-Dataverse-key": API_TOKEN}

    # 1) Intentar como ID interno
    url_id = f"{BASE_URL}/api/datasets/{dataset_identifier}"
    try:
        resp = requests.get(url_id, headers=headers, timeout=10)
    except requests.RequestException:
        # En caso de error de red, devolvemos None y que lo maneje el caller
        return None

    if resp.status_code == 200:
        data = resp.json().get("data", {})
        return _parse_dataset_info(data)

    if resp.status_code != 404:
        # Otro error (401, 500, etc.) => devolvemos None para que main decida
        return None

    # 2) Intentar como persistentId
    url_pid = f"{BASE_URL}/api/datasets/:persistentId/?persistentId={dataset_identifier}"
    try:
        resp = requests.get(url_pid, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if resp.status_code == 200:
        data = resp.json().get("data", {})
        return _parse_dataset_info(data)

    # 3) Si también 404 (u otro código de error), no encontramos el dataset
    return None
