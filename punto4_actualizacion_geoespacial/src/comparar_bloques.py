# comparar_bloques.py


def hay_cambios_geoespaciales(actual: dict | None, nuevo: dict) -> bool:
    """
    Compara el bloque actual con el nuevo.
    Solo comparamos el contenido de 'fields', ignorando displayName.
    """
    if actual is None:
        return True

    campos_actual = actual.get("fields", [])
    campos_nuevo = nuevo.get("fields", [])

    return campos_actual != campos_nuevo
