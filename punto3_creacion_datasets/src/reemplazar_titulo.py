import json
from typing import Dict, Any


def reemplazar_titulo_en_plantilla(plantilla: Dict[str, Any], titulo: str) -> Dict[str, Any]:

    plantilla_str = json.dumps(plantilla, ensure_ascii=False)
    plantilla_str = plantilla_str.replace("TITULO_PLACEHOLDER", titulo)
    plantilla_modificada = json.loads(plantilla_str)
    return plantilla_modificada
