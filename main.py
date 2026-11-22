# -*- coding: utf-8 -*-
"""
Programa principal: main.py
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas: manejo de excepciones
Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
Empresa: Software FJ

Ejecucion:  python main.py

Simula mas de 10 operaciones completas sobre el sistema (registros de
clientes validos e invalidos, creacion correcta e incorrecta de
servicios, y reservas exitosas y fallidas), demostrando que el programa
sigue funcionando sin interrumpirse aunque se presenten errores graves.
No se usa ninguna base de datos: todo vive en listas en memoria y el
unico archivo que se escribe es el log de eventos y errores
(logs/software_fj.log).
"""

from gestor import GestorFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from logger_fj import obtener_logger

logger = obtener_logger()


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def main():
    gestor = GestorFJ()
    logger.info("=== Inicio de la simulacion del sistema Software FJ ===")

    # ------------------------------------------------------------------
    titulo("Operacion 1: registrar un cliente valido")
    ana = gestor.registrar_cliente("Ana Torres", "1020304050", "ana.torres@correo.com", "3101234567")

    titulo("Operacion 2: registrar un cliente invalido (documento muy corto)")
    gestor.registrar_cliente("Pedro Lopez", "123", "pedro@correo.com", "3111111111")

    titulo("Operacion 3: registrar un segundo cliente valido")
    carlos = gestor.registrar_cliente("Carlos Ruiz", "1030405060", "carlos.ruiz@correo.com", "3122223333")

    titulo("Operacion 4: registrar un cliente con documento duplicado")
    gestor.registrar_cliente("Carlos Ruiz (duplicado)", "1030405060", "otro@correo.com", "3000000000")

    titulo("Operacion 5: registrar un cliente invalido (correo mal formado)")
    gestor.registrar_cliente("Laura Gil", "1040506070", "laura-correo-invalido", "3133334444")

    # ------------------------------------------------------------------
    titulo("Operacion 6: crear un servicio valido (Reserva de sala)")
    sala_a = gestor.registrar_servicio(ReservaSala, "Sala A - Juntas", 50000, capacidad=10)

    titulo("Operacion 7: crear un servicio valido (Alquiler de equipo)")
    videobeam = gestor.registrar_servicio(AlquilerEquipo, "Videobeam Epson", 30000, stock=3)

    titulo("Operacion 8: crear un servicio valido (Asesoria especializada)")
    asesoria = gestor.registrar_servicio(
        AsesoriaEspecializada, "Asesoria en ciberseguridad", 80000, nivel_experto="senior"
    )

    titulo("Operacion 9: crear un servicio invalido (tarifa negativa)")
    gestor.registrar_servicio(ReservaSala, "Sala Fantasma", -10000, capacidad=5)

    titulo("Operacion 10: crear un servicio invalido (nivel de experto desconocido)")
    gestor.registrar_servicio(
        AsesoriaEspecializada, "Asesoria en IA", 90000, nivel_experto="maestro-jedi"
    )

    # ------------------------------------------------------------------
    titulo("Operacion 11: reserva exitosa de principio a fin (Ana - Sala A, 3 horas)")
    reserva_1 = gestor.crear_reserva(ana, sala_a, cantidad=3, descuento=0, incluir_impuesto=True)
    gestor.confirmar_y_procesar(reserva_1)

    titulo("Operacion 12: reserva fallida por capacidad excedida (Carlos - Sala A, 50 personas)")
    gestor.crear_reserva(carlos, sala_a, cantidad=50)

    titulo("Operacion 13: servicio marcado como no disponible y reserva fallida")
    videobeam.marcar_no_disponible()
    gestor.crear_reserva(carlos, videobeam, cantidad=2)

    titulo("Operacion 14: reserva exitosa con descuento e impuesto (Carlos - Asesoria, 5 horas)")
    reserva_2 = gestor.crear_reserva(carlos, asesoria, cantidad=5, descuento=10, incluir_impuesto=True)
    gestor.confirmar_y_procesar(reserva_2)

    titulo("Operacion 15: intento de cancelar una reserva ya procesada (operacion no permitida)")
    gestor.cancelar_reserva(reserva_2, motivo="El cliente cambio de opinion")

    titulo("Operacion 16: creacion y cancelacion normal de una reserva pendiente")
    videobeam.marcar_disponible()
    reserva_3 = gestor.crear_reserva(ana, videobeam, cantidad=2)
    gestor.cancelar_reserva(reserva_3, motivo="El cliente ya no necesita el equipo")

    # ------------------------------------------------------------------
    titulo("Reporte final del sistema")
    print(gestor.generar_reporte())

    logger.info("=== Fin de la simulacion del sistema Software FJ ===")
    print("\nSimulacion finalizada. Revise logs/software_fj.log para el detalle "
          "de eventos y errores registrados durante la ejecucion.")


if __name__ == "__main__":
    # Ultima red de seguridad: si ocurriera un error no previsto por el
    # resto del sistema, se registra en el log y el programa termina de
    # forma controlada en lugar de mostrar un traceback crudo al usuario.
    try:
        main()
    except Exception as error_critico:
        logger.critical("Error critico no controlado en main(): %s", error_critico, exc_info=True)
        print(f"\n[ERROR CRITICO] El sistema encontro un problema inesperado: {error_critico}")
        print("El detalle completo quedo registrado en logs/software_fj.log.")
