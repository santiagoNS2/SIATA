# leer_csv_metadata.py

import csv
from pathlib import Path


def leer_csv_geoespacial(ruta_csv: Path) -> list[dict]:
    """
    Lee el archivo CSV de metadatos geoespaciales y devuelve una lista de dicts.
    Cada dict representa una fila con las columnas:
    id_dataset, country, state, city, latitude_left, latitude_right,
    longitude_left, longitude_right
    """
    filas: list[dict] = []

    with ruta_csv.open(newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for row in lector:
            filas.append(row)

    return filas
