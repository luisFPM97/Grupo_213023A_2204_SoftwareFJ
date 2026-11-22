# -*- coding: utf-8 -*-
"""
Modulo: logger_fj.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Configura un unico logger para todo el sistema. Cada error y cada evento
relevante (registro de cliente, creacion de servicio, cambios de estado
de una reserva, etc.) queda escrito en logs/software_fj.log, que es el
"archivo de logs" que pide el ejercicio. No se usa ninguna base de datos:
el log es un archivo de texto plano.
"""

import logging
import os

_CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
_ARCHIVO_LOG = os.path.join(_CARPETA_LOGS, "software_fj.log")

_logger = None


def obtener_logger():
    """Devuelve siempre la misma instancia de logger ya configurada
    (patron singleton simple, sin duplicar handlers en cada import)."""
    global _logger
    if _logger is not None:
        return _logger

    os.makedirs(_CARPETA_LOGS, exist_ok=True)

    logger = logging.getLogger("software_fj")
    logger.setLevel(logging.DEBUG)

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    manejador_archivo = logging.FileHandler(_ARCHIVO_LOG, mode="a", encoding="utf-8")
    manejador_archivo.setLevel(logging.DEBUG)
    manejador_archivo.setFormatter(formato)

    logger.addHandler(manejador_archivo)
    logger.propagate = False  # no duplicar en la consola raiz

    _logger = logger
    return _logger
