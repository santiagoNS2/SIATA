import csv
import os
from typing import Tuple, Dict, List, Any

from validar_fila import validar_fila


def procesar_csv(ruta_csv: str) -> Tuple[Dict[str, Any], List[dict]]:
    """
    Lee el CSV, separa filas válidas y con error,
    agrupa por sensor y prepara datos para estadísticas.

    Retorna:
        datos_por_sensor: diccionario con la info agrupada por sensor_id.
        errores: lista de filas con errores, incluyendo la descripción del error.
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    errores: List[dict] = []
    datos_por_sensor: Dict[str, Any] = {}

    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        columnas_esperadas = ["sensor_id", "timestamp", "valor", "unidad"]
        if reader.fieldnames is None:
            raise ValueError("El archivo CSV no tiene encabezados.")

        for col in columnas_esperadas:
            if col not in reader.fieldnames:
                raise ValueError(f"Falta la columna requerida: {col}")

        for line_number, row in enumerate(reader, start=2):
            es_valida, mensaje_error, timestamp, valor = validar_fila(row, line_number)

            if not es_valida:
                fila_error = row.copy()
                fila_error["error"] = mensaje_error
                errores.append(fila_error)
                continue

            sensor_id = row["sensor_id"].strip()
            unidad = row["unidad"].strip()

            if sensor_id not in datos_por_sensor:
                datos_por_sensor[sensor_id] = {
                    "unidad": unidad,
                    "registros": []
                }

            datos_por_sensor[sensor_id]["registros"].append({
                "timestamp": timestamp,
                "valor": valor,
                "unidad": unidad
            })

    return datos_por_sensor, errores
