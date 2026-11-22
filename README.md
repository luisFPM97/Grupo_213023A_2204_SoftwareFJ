# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso: Programación (213023) — UNAD
Fase 4 — Prácticas simuladas: manejo de excepciones
Ejercicio 1 (Anexo 3 — Fase 4)

## Descripción

Sistema orientado a objetos, sin uso de bases de datos, que gestiona
clientes, servicios (reserva de salas, alquiler de equipos y asesorías
especializadas) y reservas para la empresa ficticia **Software FJ**.
Implementa abstracción, herencia, polimorfismo, encapsulación y manejo
avanzado de excepciones (excepciones personalizadas, `try/except`,
`try/except/else`, `try/except/finally` y encadenamiento de excepciones
con `raise ... from ...`), registrando cada evento y error en un archivo
de log (`logs/software_fj.log`).

## Estructura del proyecto

```
SoftwareFJ/
├── excepciones.py   # Jerarquía de excepciones personalizadas del negocio
├── entidad.py        # Clase abstracta EntidadBase (id, nombre, fecha de registro)
├── cliente.py         # Clase Cliente (hereda de EntidadBase)
├── servicios.py       # Clase abstracta Servicio + ReservaSala, AlquilerEquipo,
│                      #   AsesoriaEspecializada (herencia y polimorfismo)
├── reserva.py          # Clase Reserva (cliente + servicio + estado + manejo de excepciones)
├── gestor.py            # Fachada GestorFJ: listas en memoria + manejo robusto de errores
├── logger_fj.py          # Configuración del logger hacia logs/software_fj.log
├── main.py                # Simulación de más de 10 operaciones (válidas e inválidas)
└── logs/                   # Carpeta donde se genera el archivo de log (no versionada)
```

## Ejecución

Requiere únicamente Python 3.10+ (no usa librerías externas).

```bash
cd SoftwareFJ
python3 main.py
```

El programa simula el registro de clientes, la creación de servicios y
el ciclo completo de varias reservas (creación, confirmación,
procesamiento y cancelación), incluyendo casos válidos e inválidos, sin
detener su ejecución ante ningún error. Al finalizar, se puede revisar
`logs/software_fj.log` para ver el detalle cronológico de todos los
eventos y errores registrados durante la ejecución.

## Autores

Grupo colaborativo — Curso Programación 213023, grupo 213023A_2204.
