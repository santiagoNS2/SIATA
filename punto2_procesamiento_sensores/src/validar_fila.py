from datetime import datetime
from typing import Tuple, Optional, Dict


def _limpiar_campo(valor) -> str:
    """
    Convierte None a cadena vacía y hace strip().
    Siempre devuelve un string.
    """
    if valor is None:
        return ""
    return str(valor).strip()


def validar_fila(row: Dict[str, str], line_number: int) -> Tuple[bool, str, Optional[datetime], Optional[float]]:
 
    sensor_id = _limpiar_campo(row.get("sensor_id"))
    timestamp_str = _limpiar_campo(row.get("timestamp"))
    valor_str = _limpiar_campo(row.get("valor"))
    unidad = _limpiar_campo(row.get("unidad"))

    # 1) Fila vacia
    if not (sensor_id or timestamp_str or valor_str or unidad):
        return False, f"Fila vacía (línea {line_number})", None, None

    # 2) Faltan campos obligatoriuos
    if not (sensor_id and timestamp_str and valor_str and unidad):
        return False, f"Campos faltantes en la fila (línea {line_number})", None, None

    # 3) Validar timestamp
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, f"Timestamp inválido: '{timestamp_str}' (línea {line_number})", None, None

    # 4) Validar valor numerico
    try:
        valor = float(valor_str)
    except ValueError:
        return False, f"Valor no numérico: '{valor_str}' (línea {line_number})", None, None

    return True, "", timestamp, valor
