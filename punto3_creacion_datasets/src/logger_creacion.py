import logging
import os
from typing import Final


def configurar_logger_creacion() -> logging.Logger:
 
    base_dir = os.path.dirname(__file__)
    logs_dir = os.path.abspath(os.path.join(base_dir, "..", "salida", "logs"))
    os.makedirs(logs_dir, exist_ok=True)

    log_path: Final[str] = os.path.join(logs_dir, "creacion_datasets.log")

    logger = logging.getLogger("creacion_datasets")
    logger.setLevel(logging.INFO)

    # Evitar agregar múltiples handlers si se llama varias veces
    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
