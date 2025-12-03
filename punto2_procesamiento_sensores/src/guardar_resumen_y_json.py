import csv
import os
import json
from typing import Dict, Any


def guardar_resumen_y_json(datos_por_sensor: Dict[str, Any],
                           carpeta_salida: str,
                           carpeta_sensores: str) -> None:

    ruta_resumen = os.path.join(carpeta_salida, "resumen_por_sensor.csv")

    with open(ruta_resumen, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["sensor_id", "promedio_valor", "min_valor", "max_valor", "num_registros"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for sensor_id, info in datos_por_sensor.items():
            registros = info["registros"]
            valores = [r["valor"] for r in registros]

            promedio = sum(valores) / len(valores)
            minimo = min(valores)
            maximo = max(valores)
            num_reg = len(valores)

            writer.writerow({
                "sensor_id": sensor_id,
                "promedio_valor": f"{promedio:.3f}",
                "min_valor": f"{minimo:.3f}",
                "max_valor": f"{maximo:.3f}",
                "num_registros": num_reg
            })

            registros_json = []
            for r in registros:
                registros_json.append({
                    "timestamp": r["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    "valor": r["valor"],
                    "unidad": r["unidad"]
                })

            contenido_json = {
                "sensor_id": sensor_id,
                "registros": registros_json
            }

            ruta_json = os.path.join(carpeta_sensores, f"{sensor_id}.json")
            with open(ruta_json, mode="w", encoding="utf-8") as jf:
                json.dump(contenido_json, jf, ensure_ascii=False, indent=2)

    print(f"Se guardó el resumen de sensores en: {ruta_resumen}")
    print(f"Se crearon archivos JSON por sensor en: {carpeta_sensores}")
