# -*- coding: utf-8 -*-
"""
Modulo: cliente.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Clase Cliente: hereda de EntidadBase y agrega los datos personales
(documento, correo, telefono) con validaciones estrictas y encapsulados
detras de propiedades de solo lectura.
"""

import re

from entidad import EntidadBase
from excepciones import ClienteInvalidoError


class Cliente(EntidadBase):
    """Representa a un cliente de Software FJ."""

    _PATRON_EMAIL = re.compile(r"^[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}$")

    def __init__(self, nombre, documento, email, telefono):
        # Si el nombre viene vacio, EntidadBase ya lanza ValueError; aqui lo
        # traducimos a nuestra excepcion propia para que todo el manejo de
        # errores del negocio use la misma jerarquia (ErrorSoftwareFJ).
        try:
            super().__init__(nombre)
        except ValueError as err:
            raise ClienteInvalidoError(str(err)) from err

        self._documento = self._validar_documento(documento)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_documento(documento):
        documento = str(documento).strip()
        if not documento.isdigit() or len(documento) < 6:
            raise ClienteInvalidoError(
                f"Documento invalido: '{documento}'. Debe tener minimo 6 digitos numericos."
            )
        return documento

    def _validar_email(self, email):
        email = str(email).strip()
        if not self._PATRON_EMAIL.match(email):
            raise ClienteInvalidoError(f"Correo electronico invalido: '{email}'.")
        return email

    @staticmethod
    def _validar_telefono(telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or len(telefono) < 7:
            raise ClienteInvalidoError(
                f"Telefono invalido: '{telefono}'. Debe tener minimo 7 digitos numericos."
            )
        return telefono

    @property
    def documento(self):
        return self._documento

    @property
    def email(self):
        return self._email

    @property
    def telefono(self):
        return self._telefono

    def describir(self):
        return (f"Cliente #{self.id}: {self.nombre} (Doc. {self.documento}, "
                f"{self.email}, Tel. {self.telefono})")
