# construir_bloque_geoespacial.py

def _field_single_primitive(type_name: str, value):
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "primitive",
        "value": value,
    }


def _field_single_vocab(type_name: str, value: str):
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "controlledVocabulary",
        "value": value,
    }


def construir_bloque_geoespacial(fila: dict) -> dict:
    """
    A partir de una fila del CSV construye el bloque de metadatos "geospatial"
    en el formato que espera Dataverse.
    """
    country = fila["country"].strip()
    state = fila["state"].strip()
    city = fila["city"].strip()

    lat_left = float(fila["latitude_left"])
    lat_right = float(fila["latitude_right"])
    lon_left = float(fila["longitude_left"])
    lon_right = float(fila["longitude_right"])

    # Convención: left = west (mínimo long), right = east (máximo long)
    #             lat_left = south, lat_right = north
    return {
        "displayName": "Geospatial Metadata",
        "name": "geospatial",
        "fields": [
            _field_single_vocab("country", country),
            _field_single_primitive("state", state),
            _field_single_primitive("city", city),
            _field_single_primitive("westLongitude", lon_left),
            _field_single_primitive("eastLongitude", lon_right),
            _field_single_primitive("southLatitude", lat_left),
            _field_single_primitive("northLatitude", lat_right),
        ],
    }
