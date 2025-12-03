import requests
from typing import Dict, Any, Optional

from config import BASE_URL, API_TOKEN


def _parse_dataset_info(
    data: Dict[str, Any],
    dataset_identifier: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    """
    Extrae info básica del dict 'data' devuelto por la API de Dataverse.
    Intenta encontrar el persistentId (DOI) en varios campos.
    """
    internal_id = data.get("id")

    latest_version = data.get("latestVersion", {})
    version_number = latest_version.get("versionNumber")
    version_minor = latest_version.get("versionMinorNumber")
    version_state = latest_version.get("versionState")

    # Intentar obtener el persistentId desde varios campos posibles
    persistent_id = (
        data.get("persistentId")
        or data.get("persistentIdentifier")
        or latest_version.get("datasetPersistentId")
        or latest_version.get("persistentId")
    )

    # Si seguimos sin persistentId y el identificador de entrada ya es un DOI,
    # lo usamos como persistentId
    if persistent_id is None and dataset_identifier and dataset_identifier.startswith("doi:"):
        persistent_id = dataset_identifier

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
      - un ID numérico interno (ej: '13')
      - un persistentId (ej: 'doi:10.5072/FK2/EREVDH')

    Estrategia:
      1) Intentar {BASE_URL}/datasets/{id}
      2) Si 404, intentar {BASE_URL}/datasets/:persistentId/?persistentId=...
      3) Si también 404, devolver None (dataset no encontrado).
    """
    headers = {"X-Dataverse-key": API_TOKEN}

    # 1) Intentar como ID interno
    url_id = f"{BASE_URL}/datasets/{dataset_identifier}"
    try:
        resp = requests.get(url_id, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if resp.status_code == 200:
        data = resp.json().get("data", {})
        return _parse_dataset_info(data, dataset_identifier)

    if resp.status_code != 404:
        # Otro error (401, 500, etc.) => devolvemos None para que main decida
        return None

    # 2) Intentar como persistentId
    url_pid = f"{BASE_URL}/datasets/:persistentId/?persistentId={dataset_identifier}"
    try:
        resp = requests.get(url_pid, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if resp.status_code == 200:
        data = resp.json().get("data", {})
        return _parse_dataset_info(data, dataset_identifier)

    # 3) Si también 404 (u otro código de error), no encontramos el dataset
    return None
