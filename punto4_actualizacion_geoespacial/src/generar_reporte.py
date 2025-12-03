# generar_reporte.py

import csv
from pathlib import Path


def guardar_reporte_actualizacion(ruta_salida: Path, filas_reporte: list[dict]) -> None:
    """
    Genera un CSV con columnas:
      id_dataset, titulo, persistent_id, cambios_aplicados,
      nueva_version, estado_final
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    campos = [
        "id_dataset",
        "titulo",
        "persistent_id",
        "cambios_aplicados",
        "nueva_version",
        "estado_final",
    ]

    with ruta_salida.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for fila in filas_reporte:
            writer.writerow(fila)
