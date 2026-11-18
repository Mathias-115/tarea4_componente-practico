"""Script principal de ejecución y simulación del sistema Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

from src.cliente import Cliente
from src.excepciones import (
    DatoInvalidoError,
    ErrorSistemaFJ,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from src.logger import obtener_logger
from src.reserva import Reserva
from src.servicios import ReservaSala

logger = obtener_logger("main")


def procesar_reserva_con_encadenamiento(
    cliente: Cliente,
    servicio: ReservaSala,
    horas: float,
) -> Reserva:
    """Intenta instanciar una reserva propagando errores de disponibilidad encadenados.

    Args:
        cliente: Cliente validado.
        servicio: Servicio solicitado.
        horas: Cantidad de horas requeridas.

    Returns:
        Instancia de ``Reserva`` creada.

    Raises:
        ReservaInvalidaError: Cuando el servicio no está disponible o falla la validación.
    """
    try:
        return Reserva(cliente=cliente, servicio=servicio, horas=horas)
    except ServicioNoDisponibleError as err_disponibilidad:
        raise ReservaInvalidaError(
            f"No fue posible procesar la reserva para '{cliente.nombre}' "
            f"debido a indisponibilidad del servicio.",
            codigo_error="FJ-305",
        ) from err_disponibilidad


def ejecutar_simulacion() -> None:
    """Ejecuta las 5 operaciones base simuladas del sistema Software FJ."""
    logger.info("=== INICIO DE SIMULACIÓN SOFTWARE FJ (FASE 4) ===")

    cliente_valido: Cliente | None = None
    sala_disponible: ReservaSala | None = None
    sala_mantenimiento: ReservaSala | None = None

    # --------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de cliente
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 1: Registro válido de cliente ---")
    try:
        cliente_valido = Cliente(
            nombre="Jennifer Perdomo",
            documento="1075289431",
            correo="yenniferperdomo276@gmail.com",
        )
    except ErrorSistemaFJ as err:
        logger.error("Fallo inesperado en Operación 1: %s", err)
    else:
        print("Resultado:", cliente_valido.obtener_resumen())
    finally:
        logger.info("Finalizada Operación 1.")

    # --------------------------------------------------------------------------
    # OPERACIÓN 2: Registro inválido de cliente (capturado sin detener ejecución)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 2: Registro inválido de cliente ---")
    try:
        Cliente(
            nombre="Al",
            documento="123",
            correo="correo_invalido_sin_arroba",
        )
    except DatoInvalidoError as err:
        logger.warning("Excepción controlada en Operación 2: %s", err)
        print(f"Error esperado capturado correctamente -> {err}")
    else:
        print("Error: Se registró un cliente con datos inválidos.")
    finally:
        logger.info("Finalizada Operación 2 (el sistema continúa operando).")

    # --------------------------------------------------------------------------
    # OPERACIÓN 3: Creación de dos servicios ReservaSala (disponible y no disponible)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 3: Creación de servicios ReservaSala ---")
    try:
        sala_disponible = ReservaSala(
            nombre_servicio="Sala Ejecutiva Norte",
            tarifa_base_hora=80000.0,
            capacidad=20,
            disponible=True,
        )
        sala_mantenimiento = ReservaSala(
            nombre_servicio="Auditorio Innovación (Mantenimiento)",
            tarifa_base_hora=150000.0,
            capacidad=60,
            disponible=False,
        )
    except ErrorSistemaFJ as err:
        logger.error("Error al crear servicios en Operación 3: %s", err)
    else:
        print("Servicio 1:", sala_disponible.obtener_resumen())
        print("Servicio 2:", sala_mantenimiento.obtener_resumen())
    finally:
        logger.info("Finalizada Operación 3.")

    # --------------------------------------------------------------------------
    # OPERACIÓN 4: Reserva exitosa con cálculo de descuento
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 4: Reserva exitosa con cálculo de descuento ---")
    try:
        if cliente_valido is None or sala_disponible is None:
            raise ReservaInvalidaError("Faltan entidades base para la Operación 4.")

        reserva_exitosa = Reserva(
            cliente=cliente_valido,
            servicio=sala_disponible,
            horas=5,
        )
        total = reserva_exitosa.confirmar_reserva(descuento=15.0)
    except ErrorSistemaFJ as err:
        logger.error("Error en Operación 4: %s", err)
    else:
        print(f"Reserva confirmada. Total a pagar (incl. IVA 19%): ${total:,.2f}")
        print("Detalle:", reserva_exitosa.obtener_resumen())
    finally:
        logger.info("Finalizada Operación 4.")

    # --------------------------------------------------------------------------
    # OPERACIÓN 5: Intento de reserva sobre servicio no disponible (encadenamiento)
    # --------------------------------------------------------------------------
    print("\n--- OPERACIÓN 5: Reserva sobre servicio no disponible (encadenamiento) ---")
    try:
        if cliente_valido is None or sala_mantenimiento is None:
            raise ReservaInvalidaError("Faltan entidades base para la Operación 5.")

        procesar_reserva_con_encadenamiento(
            cliente=cliente_valido,
            servicio=sala_mantenimiento,
            horas=3,
        )
    except ReservaInvalidaError as err:
        logger.error(
            "Excepción encadenada en Operación 5: %s | Causa original: %s",
            err,
            err.__cause__,
        )
        print(f"Error capturado -> {err}")
        print(f"Causa raíz encadenada (__cause__) -> {err.__cause__}")
    else:
        print("Error: Se permitió reservar una sala no disponible.")
    finally:
        logger.info("Finalizada Operación 5.")

    # ==========================================================================
    # TODO - INTEGRANTE 5: Agregar operaciones simuladas 6 a 10+
    # Instrucciones para el Integrante 5:
    # - Operación 6: Instanciar y reservar `AlquilerEquipo` (Integrante 2).
    # - Operación 7: Instanciar y reservar `AsesoriaEspecializada` (Integrante 3).
    # - Operación 8: Probar cancelación de reserva con `cancelar_reserva(motivo)` (Integrante 4).
    # - Operación 9: Probar intento de cancelar una reserva ya cancelada (OperacionNoPermitidaError).
    # - Operación 10: Generar un reporte consolidado en consola con el historial de reservas.
    # ==========================================================================

    logger.info("=== FIN DE SIMULACIÓN SOFTWARE FJ ===")


if __name__ == "__main__":
    ejecutar_simulacion()
