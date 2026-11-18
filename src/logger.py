"""Configuración centralizada de registro de eventos (logging) para Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

import logging
import os

RUTA_DIRECTORIO_LOGS = "logs"
ARCHIVO_LOG = os.path.join(RUTA_DIRECTORIO_LOGS, "sistema_fj.log")


def configurar_logging() -> None:
    """Crea el directorio de logs y configura los manejadores de archivo y consola."""
    os.makedirs(RUTA_DIRECTORIO_LOGS, exist_ok=True)

    logger_raiz = logging.getLogger("SoftwareFJ")
    logger_raiz.setLevel(logging.DEBUG)

    if logger_raiz.handlers:
        return

    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    manejador_archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    manejador_archivo.setLevel(logging.DEBUG)
    manejador_archivo.setFormatter(formato)

    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)
    manejador_consola.setFormatter(formato)

    logger_raiz.addHandler(manejador_archivo)
    logger_raiz.addHandler(manejador_consola)


def obtener_logger(nombre_modulo: str) -> logging.Logger:
    """Devuelve un logger configurado para el módulo especificado.

    Args:
        nombre_modulo: Nombre identificador del módulo solicitante.

    Returns:
        Instancia de ``logging.Logger`` asociada al espacio de nombres SoftwareFJ.
    """
    configurar_logging()
    return logging.getLogger(f"SoftwareFJ.{nombre_modulo}")
