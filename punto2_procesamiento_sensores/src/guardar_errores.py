import csv
import os
from typing import List, Dict


def guardar_errores(errores: List[Dict[str, str]], carpeta_salida: str) -> None:
    """
    Guarda las filas con errores en 'errores.csv' dentro de la carpeta de salida.
    """
    if not errores:
        return

    ruta_errores = os.path.join(carpeta_salida, "errores.csv")
    fieldnames = list(errores[0].keys())

    with open(ruta_errores, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errores)

    print(f"Se guardaron {len(errores)} filas con error en: {ruta_errores}")
