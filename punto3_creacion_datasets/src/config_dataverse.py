from typing import Dict

def obtener_config_dataverse() -> Dict[str, str]:
    base_url = "https://pruebas.siata.gov.co"

    # Alias del dataverse donde estás (Root)
    dataverse_alias = "root"

    # El mismo token que ves en tu cuenta (API Token)
    api_token = "cd869adc-f556-4eb0-a80a-44250180a841"

    return {
        "base_url": base_url,
        "dataverse_alias": dataverse_alias,
        "api_token": api_token,
    }
