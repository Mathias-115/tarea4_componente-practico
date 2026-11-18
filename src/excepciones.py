"""Módulo de excepciones personalizadas para el Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""


class ErrorSistemaFJ(Exception):
    """Excepción base de la jerarquía de errores del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "FJ-000") -> None:
        """Inicializa la excepción con un mensaje descriptivo y código de error.

        Args:
            mensaje: Descripción detallada del fallo ocurrido.
            codigo_error: Identificador único del tipo de error en el sistema.
        """
        self.codigo_error = codigo_error
        self.mensaje = mensaje
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con las reglas de validación."""

    def __init__(self, mensaje: str, codigo_error: str = "FJ-101") -> None:
        """Inicializa la excepción para datos inválidos."""
        super().__init__(mensaje, codigo_error)


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta utilizar un servicio que no está disponible."""

    def __init__(self, mensaje: str, codigo_error: str = "FJ-201") -> None:
        """Inicializa la excepción para servicios no disponibles."""
        super().__init__(mensaje, codigo_error)


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva incumple reglas de negocio o consistencia."""

    def __init__(self, mensaje: str, codigo_error: str = "FJ-301") -> None:
        """Inicializa la excepción para reservas inválidas."""
        super().__init__(mensaje, codigo_error)


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta ejecutar una acción prohibida por el estado actual."""

    def __init__(self, mensaje: str, codigo_error: str = "FJ-401") -> None:
        """Inicializa la excepción para operaciones no permitidas."""
        super().__init__(mensaje, codigo_error)
