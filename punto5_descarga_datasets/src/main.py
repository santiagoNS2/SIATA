from pathlib import Path
import csv

from dataverse_download import descargar_dataset_completo


def leer_datasets_csv(ruta_csv: Path) -> list[str]:
    """
    Lee el archivo CSV con la lista de datasets a descargar.
    Espera una columna: id_dataset (persistentId).
    """
    datasets: list[str] = []

    if not ruta_csv.exists():
        print(f"[ERROR] No se encontró el archivo CSV de entrada: {ruta_csv}")
        return datasets

    print(f"[INFO] Leyendo CSV de datasets: {ruta_csv}")

    with ruta_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "id_dataset" not in reader.fieldnames:
            print(f"[ERROR] El CSV no tiene la columna 'id_dataset'. Columnas encontradas: {reader.fieldnames}")
            return datasets

        for row in reader:
            pid = (row.get("id_dataset") or "").strip()
            if pid:
                datasets.append(pid)

    print(f"[INFO] Se encontraron {len(datasets)} datasets en el CSV.")
    return datasets


def main() -> None:
    # base_dir es la carpeta padre de src (la raíz del punto 5)
    base_dir = Path(__file__).resolve().parents[1]
    ruta_csv = base_dir / "data" / "datasets_a_descargar.csv"
    carpeta_salida_base = base_dir / "salida"


    datasets = leer_datasets_csv(ruta_csv)

    if not datasets:
        print("[WARN] No se encontraron datasets en el CSV de entrada (o el archivo está vacío). No hay nada que descargar.")
        return

    for pid in datasets:
        carpeta_dataset = carpeta_salida_base / pid.replace(":", "_").replace("/", "_")
        print(f"[INFO] Descargando dataset {pid} en {carpeta_dataset} ...")
        descargar_dataset_completo(pid, carpeta_dataset)

    print("[OK] Descarga finalizada.")


if __name__ == "__main__":
    main()
