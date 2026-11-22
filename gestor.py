# -*- coding: utf-8 -*-
"""
Modulo: gestor.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Clase GestorFJ: fachada que centraliza las listas de clientes, servicios
y reservas (todo en memoria, sin ninguna base de datos) y envuelve cada
operacion en manejo de excepciones. Si una operacion falla, el gestor la
registra en el log, avisa por consola y permite que el programa continue
con la siguiente operacion: es la pieza clave de la estabilidad que pide
el ejercicio.
"""

from excepciones import ErrorSoftwareFJ, ClienteInvalidoError
from cliente import Cliente
from reserva import Reserva
from logger_fj import obtener_logger

logger = obtener_logger()


class GestorFJ:
    """Orquesta clientes, servicios y reservas de Software FJ."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------
    def registrar_cliente(self, nombre, documento, email, telefono):
        try:
            if any(c.documento == str(documento).strip() for c in self._clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente registrado con el documento '{documento}'."
                )
            cliente = Cliente(nombre, documento, email, telefono)
        except ErrorSoftwareFJ as err:
            logger.error("No se pudo registrar al cliente '%s': %s", nombre, err)
            print(f"[ERROR] No se pudo registrar al cliente '{nombre}': {err}")
            return None
        else:
            self._clientes.append(cliente)
            logger.info("Cliente registrado: %s", cliente.describir())
            print(f"[OK] {cliente.describir()}")
            return cliente

    # ------------------------------------------------------------------
    # Servicios
    # ------------------------------------------------------------------
    def registrar_servicio(self, servicio_cls, *args, **kwargs):
        """Recibe la clase concreta del servicio (ReservaSala, AlquilerEquipo
        o AsesoriaEspecializada) y sus argumentos de construccion."""
        try:
            servicio = servicio_cls(*args, **kwargs)
        except ErrorSoftwareFJ as err:
            logger.error(
                "No se pudo crear el servicio de tipo %s: %s", servicio_cls.__name__, err
            )
            print(f"[ERROR] No se pudo crear el servicio {servicio_cls.__name__}: {err}")
            return None
        else:
            self._servicios.append(servicio)
            logger.info("Servicio registrado: %s", servicio.describir())
            print(f"[OK] {servicio.describir()}")
            return servicio

    # ------------------------------------------------------------------
    # Reservas
    # ------------------------------------------------------------------
    def crear_reserva(self, cliente, servicio, cantidad, descuento=0.0, incluir_impuesto=True):
        if cliente is None or servicio is None:
            logger.error("Intento de reserva con cliente o servicio nulo (operacion previa fallida).")
            print("[ERROR] No se puede crear la reserva: el cliente o el servicio no existen "
                  "(probablemente por un error en un paso anterior).")
            return None
        try:
            reserva = Reserva(cliente, servicio, cantidad, descuento, incluir_impuesto)
        except ErrorSoftwareFJ as err:
            logger.error("No se pudo crear la reserva para %s: %s", cliente.nombre, err)
            print(f"[ERROR] No se pudo crear la reserva para {cliente.nombre}: {err}")
            return None
        else:
            self._reservas.append(reserva)
            print(f"[OK] {reserva} creada.")
            return reserva

    def confirmar_y_procesar(self, reserva):
        if reserva is None:
            print("[ERROR] No hay una reserva valida para confirmar/procesar.")
            return None
        try:
            reserva.confirmar()
            costo = reserva.procesar()
        except ErrorSoftwareFJ as err:
            logger.error(
                "Fallo el flujo de confirmacion/procesamiento de la reserva #%s: %s",
                getattr(reserva, "id", "?"), err,
            )
            print(f"[ERROR] {err}")
            return None
        else:
            print(f"[OK] {reserva} -> costo total: ${costo:,.2f}")
            return costo

    def cancelar_reserva(self, reserva, motivo="No especificado"):
        if reserva is None:
            print("[ERROR] No hay una reserva valida para cancelar.")
            return False
        try:
            reserva.cancelar(motivo)
        except ErrorSoftwareFJ as err:
            logger.error("No se pudo cancelar la reserva #%s: %s", reserva.id, err)
            print(f"[ERROR] {err}")
            return False
        else:
            print(f"[OK] {reserva} cancelada. Motivo: {motivo}")
            return True

    # ------------------------------------------------------------------
    # Reportes (sin base de datos: todo se arma a partir de las listas)
    # ------------------------------------------------------------------
    def generar_reporte(self):
        lineas = [
            "REPORTE GENERAL - SOFTWARE FJ",
            "=" * 70,
            f"Clientes registrados: {len(self._clientes)}",
            f"Servicios registrados: {len(self._servicios)}",
            f"Reservas registradas: {len(self._reservas)}",
            "-" * 70,
        ]
        for r in self._reservas:
            costo = f"${r.costo_total:,.2f}" if r.costo_total is not None else "N/A"
            lineas.append(f"{str(r):<58} costo: {costo}")
        return "\n".join(lineas)

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)
