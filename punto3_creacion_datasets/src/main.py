import json

from config_dataverse import obtener_config_dataverse
from logger_creacion import configurar_logger_creacion
from cargar_plantilla import cargar_plantilla_dataset
from reemplazar_titulo import reemplazar_titulo_en_plantilla
from crear_dataset_api import crear_dataset_en_dataverse


def main() -> None:
  
    config = obtener_config_dataverse()

    if not config.get("api_token"):
        print("ERROR: No hay API token configurado para Dataverse.")
        return

    logger = configurar_logger_creacion()
    plantilla = cargar_plantilla_dataset()

    num_datasets = 10

    for i in range(1, num_datasets + 1):
        titulo = f"Dataset SIATA prueba {i:02d}"
        metadatos = reemplazar_titulo_en_plantilla(plantilla, titulo)

        try:
            response = crear_dataset_en_dataverse(config, metadatos)
        except Exception as e:
            mensaje = f"ERROR al conectar con Dataverse para '{titulo}': {e}"
            print(mensaje)
            logger.error(mensaje)
            continue

        if response.status_code == 201:
            dataset_id = None
            persistent_id = None

            try:
                data_resp = response.json().get("data", {})
                dataset_id = data_resp.get("id")
                persistent_id = data_resp.get("persistentId")
            except json.JSONDecodeError:
                pass

            mensaje = (
                f"OK - Creado dataset '{titulo}' "
                f"id={dataset_id} persistentId={persistent_id}"
            )
            print(mensaje)
            logger.info(mensaje)
        else:
            mensaje = (
                f"ERROR al crear dataset '{titulo}'. "
                f"status={response.status_code} body={response.text}"
            )
            print(mensaje)
            logger.error(mensaje)

    print("Creación masiva de datasets finalizada.")


if __name__ == "__main__":
    main()
