from typing import Dict, Any
import requests


def crear_dataset_en_dataverse(config: Dict[str, str], metadatos: Dict[str, Any]):
 
    base_url = config["base_url"].rstrip("/")
    alias = config["dataverse_alias"]
    api_token = config["api_token"]

    url = f"{base_url}/api/dataverses/{alias}/datasets"

    headers = {
        "X-Dataverse-key": api_token,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=metadatos, timeout=30)
    return response
