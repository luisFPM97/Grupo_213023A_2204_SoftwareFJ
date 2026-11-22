# -*- coding: utf-8 -*-
"""
Modulo: entidad.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Clase abstracta EntidadBase: representa cualquier "cosa" que el sistema
necesita identificar y registrar (un cliente, un servicio). Aporta un id
autoincremental, el nombre y la fecha de registro, y obliga a cada hija a
implementar describir(), su propio metodo virtual.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """Clase abstracta: no se puede instanciar directamente, solo a
    traves de una subclase concreta (Cliente, Servicio, etc.)."""

    _contador_global = 0

    def __init__(self, nombre):
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre de la entidad no puede estar vacio.")
        EntidadBase._contador_global += 1
        self._id = EntidadBase._contador_global
        self._nombre = nombre.strip()
        self._fecha_registro = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe explicar, en una linea de texto,
        que es y en que estado se encuentra."""

    def __str__(self):
        return self.describir()
