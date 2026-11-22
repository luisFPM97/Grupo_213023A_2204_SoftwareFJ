# -*- coding: utf-8 -*-
"""
Modulo: reserva.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Clase Reserva: integra un cliente, un servicio, la cantidad solicitada
(horas, dias o unidades, segun el servicio) y un estado que avanza asi:

    pendiente -> confirmada -> procesada
         +---> cancelada (desde pendiente o confirmada)

Aqui se concentra el manejo avanzado de excepciones que pide el
ejercicio: encadenamiento (raise ... from ...) y los tres bloques
try/except, try/except/else y try/except/finally.
"""

from datetime import datetime

from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)
from logger_fj import obtener_logger

logger = obtener_logger()


class Reserva:
    """No hereda de EntidadBase porque no es una 'entidad' de catalogo
    como Cliente o Servicio, sino la transaccion que los conecta."""

    _contador = 0
    ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "procesada"}

    def __init__(self, cliente, servicio, cantidad, descuento=0.0, incluir_impuesto=True):
        # try/except: se valida el servicio y sus parametros especificos
        # ANTES de aceptar la reserva, encadenando el error original.
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no esta disponible en este momento."
            )
        try:
            servicio.validar_parametros(asistentes=cantidad, unidades=cantidad, horas=cantidad)
        except Exception as err:
            raise ReservaInvalidaError(
                f"Los parametros de la reserva no son validos para '{servicio.nombre}'."
            ) from err

        Reserva._contador += 1
        self._id = Reserva._contador
        self._cliente = cliente
        self._servicio = servicio
        self._cantidad = cantidad
        self._descuento = descuento
        self._incluir_impuesto = incluir_impuesto
        self._estado = "pendiente"
        self._costo_total = None
        self._fecha_creacion = datetime.now()

        logger.info(
            "Reserva #%s creada: cliente=%s, servicio=%s, cantidad=%s",
            self._id, cliente.nombre, servicio.nombre, cantidad,
        )

    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self):
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError(
                f"La reserva #{self._id} no se puede confirmar porque su estado "
                f"actual es '{self._estado}'."
            )
        self._estado = "confirmada"
        logger.info("Reserva #%s confirmada.", self._id)

    def cancelar(self, motivo="No especificado"):
        if self._estado in ("cancelada", "procesada"):
            raise OperacionNoPermitidaError(
                f"La reserva #{self._id} ya esta en estado '{self._estado}' "
                f"y no puede cancelarse."
            )
        self._estado = "cancelada"
        logger.info("Reserva #%s cancelada. Motivo: %s", self._id, motivo)

    def procesar(self):
        """Calcula el costo final y cierra la reserva.

        try    -> intenta el calculo, que puede fallar con CalculoInconsistenteError.
        except -> si falla, registra el error en el log y relanza (la reserva
                  queda en 'confirmada', sin avanzar a 'procesada').
        else   -> solo se ejecuta si NO hubo excepcion: ahi se guarda el costo
                  y se cambia el estado a 'procesada'.
        finally-> se ejecuta siempre, haya habido error o no, para dejar
                  constancia de que se intento procesar la reserva.
        """
        if self._estado != "confirmada":
            raise OperacionNoPermitidaError(
                f"La reserva #{self._id} debe estar confirmada antes de procesarse "
                f"(estado actual: '{self._estado}')."
            )
        try:
            costo = self._servicio.calcular_costo(
                cantidad=self._cantidad,
                descuento=self._descuento,
                incluir_impuesto=self._incluir_impuesto,
            )
        except CalculoInconsistenteError:
            logger.error("Reserva #%s: fallo el calculo del costo.", self._id, exc_info=True)
            raise
        else:
            self._costo_total = costo
            self._estado = "procesada"
            logger.info(
                "Reserva #%s procesada con exito. Costo total: $%.2f", self._id, costo
            )
        finally:
            logger.debug(
                "Fin del intento de procesamiento de la reserva #%s (estado final: %s).",
                self._id, self._estado,
            )
        return self._costo_total

    def __str__(self):
        return (f"Reserva #{self._id} [{self._estado}] - {self._cliente.nombre} / "
                f"{self._servicio.nombre} (cant.: {self._cantidad})")
