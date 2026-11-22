# -*- coding: utf-8 -*-
"""
Modulo: excepciones.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Jerarquia de excepciones personalizadas del sistema. Todas heredan de
ErrorSoftwareFJ para que el resto del codigo pueda capturar "cualquier
error propio del negocio" con un solo except, sin atrapar por accidente
errores de programacion (TypeError, IndexError, etc. que no se esperan).
"""


class ErrorSoftwareFJ(Exception):
    """Excepcion base de todo el sistema Software FJ."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente invalidos: nombre vacio, documento repetido,
    correo o telefono con formato incorrecto, etc."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Parametros de un servicio invalidos, incompletos o fuera de rango
    (tarifa negativa, capacidad o stock invalidos, nivel de experto
    desconocido, etc.)."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado existe pero no esta disponible para
    reservarse en este momento."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no cumple las condiciones minimas para crearse
    (parametros incoherentes con el servicio solicitado)."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se intenta una operacion que el estado actual del objeto no
    permite, por ejemplo cancelar una reserva que ya fue procesada."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El calculo de un costo arrojo un resultado invalido: no numerico,
    negativo o con parametros (descuento, impuesto) fuera de rango."""
