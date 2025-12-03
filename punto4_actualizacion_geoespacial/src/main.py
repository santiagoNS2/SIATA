from pathlib import Path

from leer_csv_metadata import leer_csv_geoespacial
from construir_bloque_geoespacial import construir_bloque_geoespacial
from obtener_info_dataset import obtener_info_dataset
from obtener_metadata_actual import obtener_geoespacial_actual
from comparar_bloques import hay_cambios_geoespaciales
from actualizar_metadata import actualizar_metadata_geoespacial
from publicar_dataset import publicar_nueva_version
from generar_reporte import guardar_reporte_actualizacion


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    ruta_csv = base_dir / "data" / "metadata_geoespacial.csv"
    ruta_reporte = base_dir / "salida" / "reporte_actualizacion_geoespacial.csv"

    filas = leer_csv_geoespacial(ruta_csv)
    reporte: list[dict] = []

    for fila in filas:
        dataset_id_csv = fila["id_dataset"].strip()

        print(f"[{dataset_id_csv}] Procesando dataset...")

        info_inicial = obtener_info_dataset(dataset_id_csv)
        if info_inicial is None:
            print(f"[{dataset_id_csv}] Dataset no encontrado en Dataverse. Se omite.")
            reporte.append(
                {
                    "id_dataset": dataset_id_csv,
                    "titulo": None,
                    "persistent_id": None,
                    "cambios_aplicados": "Dataset no encontrado",
                    "nueva_version": None,
                    "estado_final": "No encontrado",
                }
            )
            continue

        # A partir de aquí ya sabemos que el dataset existe
        internal_id = info_inicial["id"]
        persistent_id = info_inicial["persistent_id"]

        print(
            f"[{dataset_id_csv}] Encontrado dataset interno ID={internal_id}, PID={persistent_id}"
        )

        bloque_nuevo = construir_bloque_geoespacial(fila)

        # Usamos el ID interno para consultas posteriores
        bloque_actual = obtener_geoespacial_actual(internal_id)

        if not hay_cambios_geoespaciales(bloque_actual, bloque_nuevo):
            print(
                f"[{dataset_id_csv}] Sin cambios geoespaciales, no se actualiza ni publica."
            )
            reporte.append(
                {
                    "id_dataset": dataset_id_csv,
                    "titulo": info_inicial["titulo"],
                    "persistent_id": persistent_id,
                    "cambios_aplicados": "Sin cambios",
                    "nueva_version": info_inicial["version"],
                    "estado_final": info_inicial["estado"],
                }
            )
            continue

        ok_update, msg_update = actualizar_metadata_geoespacial(
        internal_id,  # ID interno (21, 22, etc.)
        persistent_id,  # Puede ser None si aún no hay DOI
        bloque_nuevo,
    )


        if not ok_update:
            print(
                f"[{dataset_id_csv}] ERROR al actualizar metadata geoespacial: {msg_update}"
            )
            reporte.append(
                {
                    "id_dataset": dataset_id_csv,
                    "titulo": info_inicial["titulo"],
                    "persistent_id": persistent_id,
                    "cambios_aplicados": f"Error al actualizar: {msg_update}",
                    "nueva_version": info_inicial["version"],
                    "estado_final": info_inicial["estado"],
                }
            )
            continue

        print(
            f"[{dataset_id_csv}] Metadata geoespacial actualizada. Publicando nueva versión..."
        )

        ok_pub, version_pub, estado_pub, msg_pub = publicar_nueva_version(
            internal_id, tipo="minor"
        )

        if not ok_pub:
            print(
                f"[{dataset_id_csv}] ERROR al publicar nueva versión: {msg_pub}"
            )
            nueva_version = info_inicial["version"]
            estado_final = info_inicial["estado"]
            cambios = "Metadata actualizada, pero error al publicar"
        else:
            nueva_version = version_pub or info_inicial["version"]
            estado_final = estado_pub or info_inicial["estado"]
            cambios = "Metadata geoespacial actualizada y versión publicada"

        reporte.append(
            {
                "id_dataset": dataset_id_csv,
                "titulo": info_inicial["titulo"],
                "persistent_id": persistent_id,
                "cambios_aplicados": cambios,
                "nueva_version": nueva_version,
                "estado_final": estado_final,
            }
        )

    guardar_reporte_actualizacion(ruta_reporte, reporte)
    print(f"\nActualización geoespacial finalizada. Reporte generado en: {ruta_reporte}")


if __name__ == "__main__":
    main()
