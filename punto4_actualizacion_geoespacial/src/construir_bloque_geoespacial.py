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

    # Dataverse espera una "bounding box": oeste, este, norte, sur
    south = min(lat_left, lat_right)
    north = max(lat_left, lat_right)
    west = min(lon_left, lon_right)
    east = max(lon_left, lon_right)

    geospatial_block = {
        "fields": [
            {
                # Cobertura geográfica (país, departamento, ciudad)
                "typeName": "geographicCoverage",
                "typeClass": "compound",
                "multiple": True,
                "value": [
                    {
                        "country": {
                            "typeName": "country",
                            "typeClass": "controlledVocabulary",
                            "multiple": False,
                            "value": country
                        },
                        "state": {
                            "typeName": "state",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": state
                        },
                        "city": {
                            "typeName": "city",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": city
                        }
                        # Si quieres, podrías agregar "otherGeographicCoverage"
                    }
                ]
            },
            {
                # Nivel de detalle geográfico (texto libre)
                "typeName": "geographicUnit",
                "typeClass": "primitive",
                "multiple": False,
                "value": "Municipio"
            },
            {
                # Bounding box geográfica
                "typeName": "geographicBoundingBox",
                "typeClass": "compound",
                "multiple": False,
                "value": [
                    {
                        "westLongitude": {
                            "typeName": "westLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": west
                        },
                        "eastLongitude": {
                            "typeName": "eastLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": east
                        },
                        "northLongitude": {
                            "typeName": "northLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": north
                        },
                        "southLongitude": {
                            "typeName": "southLongitude",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": south
                        }
                    }
                ]
            }
        ]
    }

    return geospatial_block