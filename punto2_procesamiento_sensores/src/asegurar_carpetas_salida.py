import os
from typing import Tuple


def asegurar_carpetas_salida() -> Tuple[str, str]:
    """
    Crea la estructura de carpetas de salida si no existe.

    Retorna:
        carpeta_salida: ruta de la carpeta 'salida'.
        carpeta_sensores: ruta de la carpeta 'salida/sensores'.
    """
    carpeta_salida = os.path.join("..", "salida")
    carpeta_sensores = os.path.join(carpeta_salida, "sensores")

    os.makedirs(carpeta_salida, exist_ok=True)
    os.makedirs(carpeta_sensores, exist_ok=True)

    return carpeta_salida, carpeta_sensores
