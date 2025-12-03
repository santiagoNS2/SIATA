import json
import os
from typing import Dict, Any


def cargar_plantilla_dataset() -> Dict[str, Any]:
   
    base_dir = os.path.dirname(__file__)
    ruta_plantilla = os.path.abspath(
        os.path.join(base_dir, "..", "data", "plantilla_dataset.json")
    )

    with open(ruta_plantilla, "r", encoding="utf-8") as f:
        plantilla = json.load(f)

    return plantilla
