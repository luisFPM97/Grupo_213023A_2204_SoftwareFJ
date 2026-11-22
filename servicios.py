# -*- coding: utf-8 -*-
"""
Modulo: servicios.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Jerarquia de servicios que ofrece Software FJ:

  Servicio (abstracta, hereda de EntidadBase)
    - ReservaSala          -> se cobra por horas, limitada por capacidad
    - AlquilerEquipo       -> se cobra por dias, limitado por stock
    - AsesoriaEspecializada -> se cobra por horas, con un factor segun
                               el nivel del experto asignado

calcular_costo_base() y validar_parametros() son metodos abstractos que
cada hija sobrescribe: ahi esta el polimorfismo. calcular_costo() (en la
clase padre) simula la sobrecarga de metodos de otros lenguajes usando
parametros opcionales: una misma llamada puede pedir el costo simple, con
descuento, con impuesto o con ambos a la vez.
"""

from abc import abstractmethod

from entidad import EntidadBase
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


class Servicio(EntidadBase):
    """Clase abstracta: representa cualquier servicio que ofrece la empresa."""

    IMPUESTO_POR_DEFECTO = 0.19
    TIPO = "Servicio generico"

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__(nombre)
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_tarifa(tarifa):
        try:
            tarifa = float(tarifa)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"La tarifa base debe ser numerica (se recibio: {tarifa!r})."
            ) from err
        if tarifa <= 0:
            raise ServicioInvalidoError("La tarifa base debe ser mayor que cero.")
        return tarifa

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def marcar_no_disponible(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    @abstractmethod
    def calcular_costo_base(self, cantidad):
        """Costo sin impuestos ni descuentos, en la unidad propia de cada
        servicio (horas, dias, etc.). Metodo virtual: cada hija lo define."""

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida que los parametros especificos de la reserva (asistentes,
        unidades, horas...) sean coherentes con este servicio en concreto."""

    def calcular_costo(self, cantidad=1, descuento=0.0, incluir_impuesto=False,
                        impuesto=None):
        """Metodo 'sobrecargado' mediante parametros opcionales. Python no
        permite dos metodos con el mismo nombre, asi que todas las variantes
        se resuelven aqui segun lo que se mande:

            calcular_costo(cantidad)                              -> costo simple
            calcular_costo(cantidad, descuento=10)                -> con descuento
            calcular_costo(cantidad, incluir_impuesto=True)       -> con impuesto
            calcular_costo(cantidad, 10, True, 0.19)              -> ambos
        """
        costo = self.calcular_costo_base(cantidad)

        if descuento:
            if not (0 <= descuento <= 100):
                raise CalculoInconsistenteError("El descuento debe estar entre 0 y 100.")
            costo -= costo * (descuento / 100)

        if incluir_impuesto:
            tasa = self.IMPUESTO_POR_DEFECTO if impuesto is None else impuesto
            if tasa < 0:
                raise CalculoInconsistenteError("La tasa de impuesto no puede ser negativa.")
            costo += costo * tasa

        if costo < 0:
            raise CalculoInconsistenteError(
                f"El costo calculado para '{self.nombre}' no puede ser negativo ({costo})."
            )
        return round(costo, 2)

    def describir(self):
        estado = "disponible" if self._disponible else "NO disponible"
        return (f"{self.TIPO} #{self.id}: {self.nombre} "
                f"(tarifa base: ${self._tarifa_base:,.2f}, {estado})")


# ---------------------------------------------------------------------
# Servicios especializados
# ---------------------------------------------------------------------
class ReservaSala(Servicio):
    """Reserva de salas de reunion. La tarifa base es por hora y esta
    limitada por la capacidad maxima de asistentes."""

    TIPO = "Reserva de sala"

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self._capacidad = self._validar_capacidad(capacidad)

    @staticmethod
    def _validar_capacidad(capacidad):
        try:
            capacidad = int(capacidad)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"La capacidad de la sala debe ser un entero (se recibio: {capacidad!r})."
            ) from err
        if capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser mayor que cero.")
        return capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, asistentes=0, **kwargs):
        try:
            asistentes = int(asistentes)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"El numero de asistentes debe ser un entero (se recibio: {asistentes!r})."
            ) from err
        if asistentes <= 0:
            raise ServicioInvalidoError("El numero de asistentes debe ser mayor que cero.")
        if asistentes > self._capacidad:
            raise ServicioInvalidoError(
                f"La sala '{self.nombre}' tiene capacidad para {self._capacidad} personas "
                f"y se solicitaron {asistentes}."
            )
        return True

    def calcular_costo_base(self, cantidad=1):
        # cantidad = numero de horas reservadas
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas reservadas deben ser mayores que cero.")
        return self.tarifa_base * cantidad


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (videobeam, portatiles, camaras, etc.). La
    tarifa base es por dia y esta limitada por el stock disponible."""

    TIPO = "Alquiler de equipo"

    def __init__(self, nombre, tarifa_base, stock, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self._stock = self._validar_stock(stock)

    @staticmethod
    def _validar_stock(stock):
        try:
            stock = int(stock)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"El stock debe ser un entero (se recibio: {stock!r})."
            ) from err
        if stock < 0:
            raise ServicioInvalidoError("El stock no puede ser negativo.")
        return stock

    @property
    def stock(self):
        return self._stock

    def validar_parametros(self, unidades=1, **kwargs):
        try:
            unidades = int(unidades)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"Las unidades solicitadas deben ser un entero (se recibio: {unidades!r})."
            ) from err
        if unidades <= 0:
            raise ServicioInvalidoError("Las unidades solicitadas deben ser mayores que cero.")
        if unidades > self._stock:
            raise ServicioInvalidoError(
                f"Solo hay {self._stock} unidades disponibles de '{self.nombre}' "
                f"y se solicitaron {unidades}."
            )
        return True

    def calcular_costo_base(self, cantidad=1):
        # cantidad = numero de dias de alquiler
        if cantidad <= 0:
            raise CalculoInconsistenteError("Los dias de alquiler deben ser mayores que cero.")
        return self.tarifa_base * cantidad


class AsesoriaEspecializada(Servicio):
    """Asesorias tecnicas puntuales. Se cobran por hora y el nivel del
    experto asignado ajusta la tarifa mediante un factor multiplicador."""

    TIPO = "Asesoria especializada"

    _NIVELES_VALIDOS = {"junior": 1.0, "senior": 1.3, "experto": 1.6}

    def __init__(self, nombre, tarifa_base, nivel_experto="junior", disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        self._nivel_experto = self._validar_nivel(nivel_experto)

    @classmethod
    def _validar_nivel(cls, nivel):
        nivel = str(nivel).strip().lower()
        if nivel not in cls._NIVELES_VALIDOS:
            raise ServicioInvalidoError(
                f"Nivel de experto invalido: '{nivel}'. "
                f"Opciones validas: {list(cls._NIVELES_VALIDOS)}."
            )
        return nivel

    @property
    def nivel_experto(self):
        return self._nivel_experto

    def validar_parametros(self, horas=1, **kwargs):
        try:
            horas = float(horas)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"Las horas de asesoria deben ser numericas (se recibio: {horas!r})."
            ) from err
        if horas <= 0:
            raise ServicioInvalidoError("Las horas de asesoria deben ser mayores que cero.")
        return True

    def calcular_costo_base(self, cantidad=1):
        # cantidad = horas de asesoria; el nivel del experto ajusta la tarifa
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas de asesoria deben ser mayores que cero.")
        factor = self._NIVELES_VALIDOS[self._nivel_experto]
        return self.tarifa_base * cantidad * factor

    def describir(self):
        base = super().describir()
        return f"{base} [nivel: {self._nivel_experto}]"
