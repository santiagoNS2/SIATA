# construir_bloque_geoespacial.py

def _field_single_primitive(type_name: str, value):
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "primitive",
        "value": value,
    }


def _field_single_vocab(type_name: str, value: str):
    # Para evitar problemas de vocabularios controlados raros,
    # lo dejamos como "primitive" en vez de "controlledVocabulary".
    return {
        "typeName": type_name,
        "multiple": False,
        "typeClass": "primitive",
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

    # Coords como floats
    lat_left = float(row["latitude_left"])
    lat_right = float(row["latitude_right"])
    lon_left = float(row["longitude_left"])
    lon_right = float(row["longitude_right"])

    # Bounding box: oeste, este, sur, norte
    south = min(lat_left, lat_right)
    north = max(lat_left, lat_right)
    west = min(lon_left, lon_right)
    east = max(lon_left, lon_right)

    geospatial_block = {
        "fields": [
            {
                # Cobertura geográfica básica
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
                # Unidad geográfica (texto libre)
                "typeName": "geographicUnit",
                "typeClass": "compound",
                "multiple": True,
                "value": [
                    {
                        "geographicUnit": _field_single_primitive(
                            "geographicUnit", "City"
                        )
                    }
                ],
            },
            {
                # Bounding box: OESTE / ESTE / NORTE / SUR
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
                        # ¡Ojo! Aquí estaba el error:
                        # Debe ser northLatitude / southLatitude
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
        ]
    }

    return geospatial_block
