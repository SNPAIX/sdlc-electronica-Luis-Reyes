# AI Log - Semana 1
**Estudiante:** Luis Khaled Reyes Casanova

## Entrada 1: Abstracción de Configuración UART
- **Prompt usado:** "Crea una configuración para un driver UART en Python que reemplace los structs típicos de C, usando buenas prácticas de tipado estricto."
- **Qué produjo la IA:** Sugirió usar una clase común con métodos de validación manuales.
- **Mi decisión y porqué:** Modifiqué la sugerencia para utilizar una `dataclass(frozen=True)`. La configuración de hardware de un periférico UART debe ser inmutable una vez inicializada; usar estructuras mutables expondría el código a colisiones o cambios de baudrate accidentales en tiempo de ejecución.

## Entrada 2: Diseño de la FSM de Semáforo
- **Prompt usado:** "Cómo mapear una máquina de estados (FSM) típica de microcontroladores en C a un diseño elegante orientado a objetos en Python."
- **Qué produjo la IA:** Un script con variables globales y un ciclo `while` simulando el Superloop de C.
- **Mi decisión y porqué:** Rechacé el uso de globales. Implementé una arquitectura OO usando `Enum` y encapsulando el estado dentro de una clase `TrafficLightFSM`. Esto elimina el acoplamiento rígido de C y permite instanciar múltiples FSM de forma aislada y testeable de acuerdo a los estándares del curso.

## Entrada 3: Resolución de Colisión de Librerías en Principio DIP
- **Prompt usado:** "Implementa el principio de Inversión de Dependencias (DIP) usando typing_extensions para un lector ADC."
- **Qué produjo la IA:** Un bloque utilizando `from typing import typing_extensions` y `typing_extensions.Protocol`.
- **Mi decisión y porqué:** Durante la fase de pruebas con Python 3.14.4, el intérprete arrojó un `ImportError` debido a cambios en la estructura interna de la librería estándar. Decidí refactorizar el código de inmediato para importar `Protocol` de manera directa desde `typing`, resolviendo la colisión y manteniendo el código idiomático y compatible con las versiones más modernas del entorno.



# Semana 2: Agile, TDD y Calidad Automatizada
**Estudiante:** Luis Khaled Reyes Casanova

## Entrada 1: Diseño de Pruebas TDD y Definición del Contrato para SensorReading
* **Contexto:** Se requería implementar la ingesta de telemetría de temperatura y humedad asegurando la validación estricta de rangos operativos (-20 a 70 °C para temperatura y 0 a 100% para humedad).
* **Propuesta de IA:** Iniciar con la creación de clases mutables y validadores post-procesamiento.
* **Decisión Técnica e Ingeneril:** Se rechazó la mutabilidad y se implementó una `@dataclass(frozen=True)` con validación en `__post_init__` para garantizar inmutabilidad en tiempo de ejecución. Se escribió primero la suite en `test_sensor_reading.py` registrando el commit `[RED]` antes de escribir el código de la solución (`[GREEN]`).

## Entrada 2: Elección de Patrón Strategy para AlertManager
* **Contexto:** La historia US-03 solicitaba que el sistema despachara alertas tanto a consola como a archivos de registro persistentes (`alerts.log`), manteniendo extensibilidad para futuros canales (e.g. Email o SMS).
* **Propuesta de IA:** Usar un bloque condicional `if/else` dentro del método de despacho para seleccionar el tipo de log.
* **Decisión Técnica e Ingeneril:** Se descartó el bloque `if/else` por violar el principio OCP (Open/Closed Principle) de SOLID. En su lugar, se implementó una clase abstracta base `NotificationStrategy` y se desacopló el `AlertManager` mediante Inyección de Dependencias, permitiendo cambiar las estrategias dinámicamente en tiempo de ejecución.

## Entrada 3: Simulación Gaussiana de Red de Sensores (Extensión de Distinción)
* **Contexto:** Se requería simular el comportamiento estocástico de 10 sensores de bodega durante 60 ciclos continuos para validar la estabilidad del detector de anomalías frente a volúmenes masivos de datos.
* **Propuesta de IA:** Usar `random.randint` para generar valores puramente aleatorios.
* **Decisión Técnica e Ingeneril:** Se optó por `random.gauss()` con media en 25 °C y desviación estándar de 4 °C para modelar el comportamiento térmico real de una bodega industrial, agregando truncamiento explícito para evitar lecturas físicamente imposibles.

=======


## Semana 3: De un script a un servicio API REST

### Entrada 1: Transición a Arquitectura en Capas y SQLAlchemy 2.0
* **Contexto:** Se requería evolucionar el script monolítico de la Semana 2 hacia un servicio web en capas (Routers -> Services -> Repositories -> Models/Schemas) persistiendo datos mediante SQLAlchemy 2.0.
* **Propuesta de IA:** Utilizar la sintaxis legacy `db.query(Model)` de SQLAlchemy 1.x e implementar la lógica de persistencia directamente en los endpoints del Router.
* **Decisión Técnica e Ingeneril:** Se rechazó el acoplamiento en los routers y el uso de la API obsoleta 1.x. Se implementó el patrón Repositorio tipado utilizando sentencias explícitas `select(Model)` y la asignación mediante `Mapped[...]` para cumplir con las mejores prácticas modernas de SQLAlchemy 2.x y mantener el desacoplamiento de capas

### Entrada 2: Validación Física de Telemetría y Contratos Pydantic V2
* **Contexto:** Se debía garantizar la integridad de los datos de entrada para sensores de temperatura y humedad, evitando lecturas fuera de rangos físicos reales y manteniendo compatibilidad total con mypy
* **Propuesta de IA:** Utilizar argumentos example= directamente en las llamadas a Field(...) dentro de los esquemas de Pydantic
* **Decisión Técnica e Ingeneril:** Se descartó el uso de example= debido a su deprecación en Pydantic V2 y las advertencias de sobrecarga producidas en mypy. Se definieron clasificadores @field_validator de tipo @classmethod para validar la ventana física real (-50 °C a 80 °C en temperatura, 0% a 100% en humedad) retornando errores HTTP 422 descriptivos ante datos corruptos.

### Entrada 3: Pruebas de Integración con SQLite en Memoria y Cobertura
* **Contexto:** Se requería validar de forma automatizada los endpoints /readings (POST y GET con filtros de paginación/fechas) asegurando una cobertura de código  ≥80%.
* **Propuesta de IA:** Ejecutar las pruebas unitarias directamente contra la base de datos de desarrollo sensor_hub.db.
* **Decisión Técnica e Ingeneril:** Se rechazó la dependencia de la base de datos local para mantener la independencia y repetibilidad de los tests. Se implementaron fixtures con pytest para instanciar un motor SQLite en memoria (sqlite:///:memory:) y un TestClient de FastAPI, permitiendo aislar la base de datos en cada ejecución y alcanzando el 100% de éxito en los tests de integración con alta cobertura.