import json
from typing import Dict, Any


def reemplazar_titulo_en_plantilla(plantilla: Dict[str, Any], titulo: str) -> Dict[str, Any]:
    """
    Toma la plantilla de metadatos y devuelve una nueva copia donde
    todas las apariciones de 'TÍTULO_PLACEHOLDER' han sido reemplazadas
    por el título especificado.
    """
    plantilla_str = json.dumps(plantilla, ensure_ascii=False)
    plantilla_str = plantilla_str.replace("TITULO_PLACEHOLDER", titulo)
    plantilla_modificada = json.loads(plantilla_str)
    return plantilla_modificada
