"""Módulo de la entidad base abstracta para el modelo del dominio Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class EntidadSistema(ABC):
    """Clase base abstracta que encapsula identidad y trazabilidad temporal."""

    def __init__(self, id_entidad: str | None = None) -> None:
        """Inicializa los atributos encapsulados comunes a toda entidad del sistema.

        Args:
            id_entidad: Identificador opcional. Si no se indica, se genera uno único.
        """
        self.__id_entidad: str = (
            id_entidad.strip() if id_entidad and id_entidad.strip() else str(uuid.uuid4())[:8].upper()
        )
        self.__fecha_creacion: datetime = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self.__id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad (solo lectura)."""
        return self.__fecha_creacion

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Verifica que el estado interno de la entidad cumpla las reglas del negocio."""

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una representación legible y estructurada de la entidad."""
