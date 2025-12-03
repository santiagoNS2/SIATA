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


def construir_bloque_geoespacial(fila: dict) -> dict:
    country = fila["country"].strip()
    state = fila["state"].strip()
    city = fila["city"].strip()

    lat_left = float(fila["latitude_left"])
    lat_right = float(fila["latitude_right"])
    lon_left = float(fila["longitude_left"])
    lon_right = float(fila["longitude_right"])

    # Aseguramos orden correcto
    south = min(lat_left, lat_right)
    north = max(lat_left, lat_right)
    west = min(lon_left, lon_right)
    east = max(lon_left, lon_right)

    geographic_coverage_field = {
        "typeName": "geographicCoverage",
        "typeClass": "compound",
        "multiple": True,
        "value": [
            {
                "country": {
                    "typeName": "country",
                    "typeClass": "controlledVocabulary",
                    "multiple": False,
                    "value": country,
                },
                "state": {
                    "typeName": "state",
                    "typeClass": "primitive",
                    "multiple": False,
                    "value": state,
                },
                "city": {
                    "typeName": "city",
                    "typeClass": "primitive",
                    "multiple": False,
                    "value": city,
                },
            }
        ],
    }

    geographic_bounding_box_field = {
        "typeName": "geographicBoundingBox",
        "typeClass": "compound",
        "multiple": False,
        # 👇 AQUÍ ESTÁ LA DIFERENCIA: value es OBJETO, NO lista
        "value": {
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
        },
    }

    bloque_geoespacial = {
        "displayName": "Geospatial Metadata",
        "fields": [
            geographic_coverage_field,
            geographic_bounding_box_field,
        ],
    }

    return bloque_geoespacial
