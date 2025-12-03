import os
import sys


def leer_ruta_csv() -> str:
    """
    Obtiene la ruta del archivo CSV desde los argumentos de línea de comandos.
    Si no se pasa argumento, usa '../data/registro_sensores.csv' por defecto.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
       return os.path.join(os.path.dirname(__file__), "..", "data", "registro_sensores.csv")

