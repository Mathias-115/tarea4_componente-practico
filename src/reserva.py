"""Módulo de gestión de reservas y ciclo de vida para Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

from src.cliente import Cliente
from src.entidad_base import EntidadSistema
from src.excepciones import DatoInvalidoError, OperacionNoPermitidaError
from src.logger import obtener_logger
from src.servicios import Servicio

logger = obtener_logger("reserva")

ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")


class Reserva(EntidadSistema):
    """Asocia un Cliente con un Servicio verificando disponibilidad y estado."""

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        horas: float,
        id_entidad: str | None = None,
    ) -> None:
        """Crea una nueva reserva en estado PENDIENTE tras verificar disponibilidad.

        Args:
            cliente: Instancia válida de ``Cliente``.
            servicio: Instancia de ``Servicio`` disponible.
            horas: Duración solicitada de la reserva (> 0).
            id_entidad: Identificador opcional de la reserva.
        """
        super().__init__(id_entidad=id_entidad)

        if not isinstance(cliente, Cliente) or not cliente.validar_integridad():
            raise DatoInvalidoError(
                "Se requiere un objeto Cliente válido para crear la reserva.",
                codigo_error="FJ-302",
            )
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError(
                "Se requiere un objeto Servicio válido para crear la reserva.",
                codigo_error="FJ-303",
            )
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError(
                "La duración de la reserva debe ser mayor a cero horas.",
                codigo_error="FJ-304",
            )

        servicio.verificar_disponibilidad()

        self.__cliente: Cliente = cliente
        self.__servicio: Servicio = servicio
        self.__horas: float = float(horas)
        self.__estado: str = "PENDIENTE"
        self.__costo_total: float = 0.0

        logger.info(
            "Reserva [%s] creada en estado %s para cliente '%s' y servicio '%s'.",
            self.id_entidad,
            self.__estado,
            self.__cliente.nombre,
            self.__servicio.nombre_servicio,
        )

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente asociado a la reserva."""
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio asociado a la reserva."""
        return self.__servicio

    @property
    def horas(self) -> float:
        """Retorna la cantidad de horas reservadas."""
        return self.__horas

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva."""
        return self.__estado

    @property
    def costo_total(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        return self.__costo_total

    def confirmar_reserva(self, descuento: float = 0.0) -> float:
        """Confirma la reserva calculando su costo total con descuento opcional.

        Args:
            descuento: Porcentaje de descuento comercial a aplicar (0 a 100).

        Returns:
            Costo total final con impuestos incluidos.
        """
        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva [{self.id_entidad}] en estado '{self.__estado}'.",
                codigo_error="FJ-402",
            )

        self.__costo_total = self.__servicio.calcular_costo(
            horas=self.__horas,
            descuento_porcentaje=descuento,
        )
        self.__estado = "CONFIRMADA"
        logger.info(
            "Reserva [%s] CONFIRMADA. Costo total: $%.2f (Descuento aplicado: %.1f%%).",
            self.id_entidad,
            self.__costo_total,
            descuento,
        )
        return self.__costo_total

    def validar_integridad(self) -> bool:
        """Valida que cliente, servicio, horas y estado sean consistentes."""
        return (
            self.__cliente.validar_integridad()
            and self.__servicio.validar_integridad()
            and self.__horas > 0
            and self.__estado in ESTADOS_VALIDOS
        )

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo de la reserva."""
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre_servicio} | "
            f"Horas: {self.__horas:.1f} | Total: ${self.__costo_total:,.2f}"
        )

    # ==========================================================================
    # TODO - INTEGRANTE 4: Implementar cancelar_reserva(self, motivo: str)
    # Instrucciones para el Integrante 4:
    # 1. Validar que `motivo` no esté vacío (mínimo 5 caracteres), lanzando DatoInvalidoError.
    # 2. Validar transiciones de estado permitidas:
    #    - No permitir cancelar una reserva ya CANCELADA (lanzar OperacionNoPermitidaError).
    #    - Si estaba CONFIRMADA, registrar posible penalización o liberación del servicio.
    # 3. Cambiar `self.__estado = "CANCELADA"`, almacenar `self.__motivo_cancelacion`
    #    y registrar el evento con `logger.warning(...)`.
    # ==========================================================================
