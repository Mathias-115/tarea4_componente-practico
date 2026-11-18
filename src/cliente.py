"""Módulo de gestión y validación de clientes para Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

import re
from src.entidad_base import EntidadSistema
from src.excepciones import DatoInvalidoError
from src.logger import obtener_logger

logger = obtener_logger("cliente")

PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PATRON_DOCUMENTO = re.compile(r"^\d{6,12}$")


class Cliente(EntidadSistema):
    """Representa un cliente registrado en el sistema con validación estricta."""

    def __init__(
        self,
        nombre: str,
        documento: str,
        correo: str,
        id_entidad: str | None = None,
    ) -> None:
        """Inicializa un nuevo cliente validando todos sus atributos.

        Args:
            nombre: Nombre completo del cliente (mínimo 3 caracteres).
            documento: Número de documento entre 6 y 12 dígitos numéricos.
            correo: Correo electrónico válido.
            id_entidad: Identificador opcional del cliente.
        """
        super().__init__(id_entidad=id_entidad)
        self.__nombre: str = ""
        self.__documento: str = ""
        self.__correo: str = ""

        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        logger.info("Cliente registrado exitosamente: %s (ID: %s)", self.nombre, self.id_entidad)

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(
                "El nombre del cliente debe tener al menos 3 caracteres válidos.",
                codigo_error="FJ-102",
            )
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        """Retorna el documento de identidad del cliente."""
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Valida que el documento contenga entre 6 y 12 dígitos numéricos."""
        if not isinstance(valor, str) or not PATRON_DOCUMENTO.fullmatch(valor.strip()):
            raise DatoInvalidoError(
                "El documento debe contener exclusivamente entre 6 y 12 dígitos numéricos.",
                codigo_error="FJ-103",
            )
        self.__documento = valor.strip()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato del correo electrónico mediante expresión regular."""
        if not isinstance(valor, str) or not PATRON_CORREO.fullmatch(valor.strip()):
            raise DatoInvalidoError(
                f"El correo electrónico '{valor}' no tiene un formato válido.",
                codigo_error="FJ-104",
            )
        self.__correo = valor.strip().lower()

    def validar_integridad(self) -> bool:
        """Verifica que los datos del cliente sigan siendo consistentes."""
        return (
            len(self.__nombre) >= 3
            and bool(PATRON_DOCUMENTO.fullmatch(self.__documento))
            and bool(PATRON_CORREO.fullmatch(self.__correo))
        )

    def obtener_resumen(self) -> str:
        """Retorna una cadena descriptiva con la información principal del cliente."""
        return (
            f"Cliente [{self.id_entidad}] | Nombre: {self.__nombre} | "
            f"Doc: {self.__documento} | Correo: {self.__correo}"
        )
