from leer_ruta_csv import leer_ruta_csv
from procesar_csv import procesar_csv
from asegurar_carpetas_salida import asegurar_carpetas_salida
from guardar_errores import guardar_errores
from guardar_resumen_y_json import guardar_resumen_y_json


def main() -> None:
    """
    Punto de entrada principal del programa.
    Orquesta la lectura, validación y generación de salidas.
    """
    ruta_csv = leer_ruta_csv()
    print(f"Usando archivo CSV: {ruta_csv}")

    try:
        datos_por_sensor, errores = procesar_csv(ruta_csv)
    except FileNotFoundError:
        # Aquí controlas el mensaje cuando no existe el archivo
        print(f"ERROR: No se encontró el archivo CSV en la ruta: {ruta_csv}")
        print("Verifica que el archivo exista y que la ruta sea correcta.")
        return
    except ValueError as e:
        # Aquí controlas el mensaje cuando falta una columna u otro ValueError
        print("ERROR en el formato del CSV:")
        print(f"  {e}")
        print("Revisa que el archivo tenga las columnas: sensor_id, timestamp, valor, unidad.")
        return

    carpeta_salida, carpeta_sensores = asegurar_carpetas_salida()

    guardar_errores(errores, carpeta_salida)
    guardar_resumen_y_json(datos_por_sensor, carpeta_salida, carpeta_sensores)

    print("Procesamiento finalizado.")


if __name__ == "__main__":
    main()
