# construir_bloque_geoespacial.py

def _field_single_primitive(type_name: str, value):
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "primitive",
        "value": value,
    }


def _field_single_vocab(type_name: str, value: str):
    # country es vocabulario controlado en Dataverse
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "controlledVocabulary",
        "value": value,
    }


def construir_bloque_geoespacial(row: dict) -> dict:
    """
    Construye el bloque 'geospatial' para Dataverse a partir de una fila del CSV.

    Espera columnas:
      - country
      - state
      - city
      - latitude_left
      - latitude_right
      - longitude_left
      - longitude_right
    """

    country = (row.get("country") or "").strip()
    state = (row.get("state") or "").strip()
    city = (row.get("city") or "").strip()

    # Coordenadas como floats
    lat_left = float(row["latitude_left"])
    lat_right = float(row["latitude_right"])
    lon_left = float(row["longitude_left"])
    lon_right = float(row["longitude_right"])

    # Bounding box: sur/norte, oeste/este
    south = min(lat_left, lat_right)
    north = max(lat_left, lat_right)
    west = min(lon_left, lon_right)
    east = max(lon_left, lon_right)

    geospatial_block = {
        # displayName es opcional, pero no molesta
        "displayName": "Geospatial Metadata",
        "fields": [
            {
                # Cobertura geográfica (país, estado, ciudad)
                "typeName": "geographicCoverage",
                "typeClass": "compound",
                "multiple": True,
                "value": [
                    {
                        "country": _field_single_vocab("country", country),
                        "state": _field_single_primitive("state", state),
                        "city": _field_single_primitive("city", city),
                    }
                ],
            },
            {
                # Bounding box; OJO: value debe ser una LISTA de un objeto
                "typeName": "geographicBoundingBox",
                "typeClass": "compound",
                "multiple": False,
                "value": [
                    {
                        "westLongitude": {
                            "typeName": "westLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": west,
                        },
                        "eastLongitude": {
                            "typeName": "eastLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": east,
                        },
                        "northLatitude": {
                            "typeName": "northLatitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": north,
                        },
                        "southLatitude": {
                            "typeName": "southLatitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": south,
                        },
                    }
                ],
            },
        ],
    }

    return geospatial_block
