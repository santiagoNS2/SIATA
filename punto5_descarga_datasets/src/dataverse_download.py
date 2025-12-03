# dataverse_download.py
from pathlib import Path
import requests
from typing import List, Dict
from config import BASE_URL, API_TOKEN


def obtener_archivos_dataset(persistent_id: str) -> List[Dict]:
    """
    Obtiene la lista de archivos de un dataset dado su persistentId (DOI).

    Usa el endpoint:
      GET /api/datasets/:persistentId?persistentId=doi:...
    """
    url = f"{BASE_URL}/datasets/:persistentId"
    params = {
        "persistentId": persistent_id
    }
    headers = {
        "X-Dataverse-key": API_TOKEN
    }

    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()

    data = resp.json()["data"]
    files = data["latestVersion"]["files"]
    return files


def descargar_archivo(file_id: int, destino: Path) -> None:
    """
    Descarga un archivo individual usando su ID interno.

    Usa el endpoint:
      GET /api/access/datafile/{file_id}
    """
    url = f"{BASE_URL}/access/datafile/{file_id}"
    headers = {
        "X-Dataverse-key": API_TOKEN
    }

    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def descargar_dataset_completo(persistent_id: str, carpeta_salida: Path) -> None:
    """
    Descarga todos los archivos de un dataset (última versión) a una carpeta local.

    - Crea una subcarpeta por dataset.
    - Usa el nombre de archivo que tenga en Dataverse.
    """
    print(f"[{persistent_id}] Obteniendo lista de archivos...")
    archivos = obtener_archivos_dataset(persistent_id)

    if not archivos:
        print(f"[{persistent_id}] No se encontraron archivos en el dataset.")
        return

    for file_info in archivos:
        data_file = file_info.get("dataFile", {})
        file_id = data_file.get("id")
        file_name = data_file.get("filename", f"file_{file_id}")

        destino = carpeta_salida / file_name
        print(f"[{persistent_id}] Descargando archivo {file_name} (id={file_id})...")
        descargar_archivo(file_id, destino)

    print(f"[{persistent_id}] Descarga completa en: {carpeta_salida}")
