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


# Semana 3: De un script a un servicio API REST

## Entrada 1: Transición a Arquitectura en Capas y SQLAlchemy 2.0
* **Contexto:** Se requería evolucionar el script monolítico de la Semana 2 hacia un servicio web en capas (Routers -> Services -> Repositories -> Models/Schemas) persistiendo datos mediante SQLAlchemy 2.0.
* **Propuesta de IA:** Utilizar la sintaxis legacy `db.query(Model)` de SQLAlchemy 1.x e implementar la lógica de persistencia directamente en los endpoints del Router.
* **Decisión Técnica e Ingeneril:** Se rechazó el acoplamiento en los routers y el uso de la API obsoleta 1.x. Se implementó el patrón Repositorio tipado utilizando sentencias explícitas `select(Model)` y la asignación mediante `Mapped[...]` para cumplir con las mejores prácticas modernas de SQLAlchemy 2.x y mantener el desacoplamiento de capas

## Entrada 2: Validación Física de Telemetría y Contratos Pydantic V2
* **Contexto:** Se debía garantizar la integridad de los datos de entrada para sensores de temperatura y humedad, evitando lecturas fuera de rangos físicos reales y manteniendo compatibilidad total con mypy
* **Propuesta de IA:** Utilizar argumentos example= directamente en las llamadas a Field(...) dentro de los esquemas de Pydantic
* **Decisión Técnica e Ingeneril:** Se descartó el uso de example= debido a su deprecación en Pydantic V2 y las advertencias de sobrecarga producidas en mypy. Se definieron clasificadores @field_validator de tipo @classmethod para validar la ventana física real (-50 °C a 80 °C en temperatura, 0% a 100% en humedad) retornando errores HTTP 422 descriptivos ante datos corruptos.

## Entrada 3: Pruebas de Integración con SQLite en Memoria y Cobertura
* **Contexto:** Se requería validar de forma automatizada los endpoints /readings (POST y GET con filtros de paginación/fechas) asegurando una cobertura de código  ≥80%.
* **Propuesta de IA:** Ejecutar las pruebas unitarias directamente contra la base de datos de desarrollo sensor_hub.db.
* **Decisión Técnica e Ingeneril:** Se rechazó la dependencia de la base de datos local para mantener la independencia y repetibilidad de los tests. Se implementaron fixtures con pytest para instanciar un motor SQLite en memoria (sqlite:///:memory:) y un TestClient de FastAPI, permitiendo aislar la base de datos en cada ejecución y alcanzando el 100% de éxito en los tests de integración con alta cobertura.

=======


# Semana 4: De un script a un servicio API REST

## Entrada 1: Contenerización y Orquestación Multi-contenedor
* **Contexto:** Se requería empaquetar la aplicación FastAPI y garantizar su ejecución idéntica en cualquier entorno utilizando Docker y PostgreSQL.
* **Propuesta de IA:** Exponer la aplicación en un contenedor individual configurado para conectar a una base de datos SQLite en disco.
* **Decisión Técnica e Ingenieril:** Se descartó el uso de SQLite en contenedores por falta de persistencia en entornos efímeros. Se diseñó un `Dockerfile` multicapa liviano (Python 3.11-slim) y un `docker-compose.yml` que orquesta la API junto a una instancia de PostgreSQL 15, garantizando comprobaciones de salud (`healthcheck`) y aislamiento de red.

## Entrada 2: Pipeline de Integración Continua (CI) con GitHub Actions
* **Contexto:** Se debía implementar un flujo de trabajo automatizado que valide el análisis estático de tipos y las pruebas de cobertura en cada cambio de código.
* **Propuesta de IA:** Incluir comandos de despliegue directo dentro del pipeline de testing en GitHub Actions.
* **Decisión Técnica e Ingenieril:** Se separaron las responsabilidades de CI y CD. Se estructuró `.github/workflows/ci.yml` enfocado estrictamente en la calidad del código, ejecutando `mypy app/` y `pytest --cov=app tests/` en un entorno virtualizado de Ubuntu antes de permitir cualquier fusión en la rama `main`.

## Entrada 3: Despliegue Continuo (CD) y Gestión de Configuración de Entorno
* **Contexto:** Se necesitaba publicar el servicio en Render con persistencia PostgreSQL, siguiendo las reglas Twelve-Factor App para la gestión de secretos.
* **Propuesta de IA:** Hardcodear la cadena de conexión de producción en los archivos de configuración del proyecto.
* **Decisión Técnica e Ingenieril:** Se rechazó la inclusión de credenciales en el repositorio de código. Se parametrizó `DATABASE_URL` mediante variables de entorno en Render, vinculando el repositorio de GitHub para activar el despliegue continuo automático tras la validación exitosa del pipeline de CI.


=======


# Semana 5: La IA como un copiloto profesional

## Entrada 1: Intento de Configuración de Aider (Martes 11 de Agosto)
* **Contexto / Objetivo:** Intentar integrar la herramienta `aider-chat` en la terminal para refactorizaciones con trazabilidad en Git.
* **Comando / Prompt ejecutado:** `pip install aider-chat`
* **Resultado producido por el entorno:**
  ```text
  AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
  ERROR: Failed to build 'numpy' when getting requirements to build wheel
  ```
   **Decisión Técnica e Ingenieril:** Detener la instalación de Aider en el entorno Windows con Python 3.12 y pasar a la alternativa oficialmente aceptada en la guía. El error se debe a la eliminación de ImpImporter en Python 3.12 y conflictos de compilación de NumPy en Windows. Se adopta el uso de GitHub Copilot Chat en VS Code realizando los commits manuales en Git para garantizar trazabilidad sin bloquear el avance.

## Entrada 2: Implementación del Detector de Anomalías y Notificador OCP (Miércoles 12 de Agosto)
* **Contexto / Objetivo:** Generar la función pura para detectar anomalías de temperatura y la estrategia de notificación usando el principio Open/Closed (OCP).
* **Prompt Utilizado (CTRF)**
Contexto: API FastAPI en Python 3.11+ con arquitectura en capas.
Tarea: Generar la función detect_and_notify_anomalies y una interfaz NotificationStrategy con una implementación MockNotificationStrategy.
Restricciones: Cero dependencias externas (usar math y abc), tipado estricto para mypy, y manejo explícito de varianza cero para evitar ZeroDivisionError.
Formato: Código Python con docstrings formato Google.
* **Resultado Producido por la IA**
```import Python
import math
from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, anomalies: list) -> bool: pass

def detect_and_notify_anomalies(readings: list[float], notifier=None):
    mean = sum(readings) / len(readings)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in readings) / len(readings))
    ...
```
* **Decisión Técnica e Ingenieril:** Se aceptó la estructura del patrón Strategy y el cálculo estadístico, pero se refactorizó manualmente el tipado. La IA omitió las anotaciones de tipos detalladas en los argumentos (notifier: NotificationStrategy | None = None) y en los retornos (list[dict[str, Any]]). Se corrigieron para asegurar 0 hallazgos en mypy.

## Entrada 3: Code Review Asistido y Peer Review Ronda 2 (Sábado 15 de Agosto)

* **Contexto / Objetivo:** Revisar la suite de pruebas y el endpoint /anomalies/check antes del cierre de la semana.

* **Prompt Utilizado (CTRF)**
"Actúa como un revisor de código Senior en Python. Revisa la clase app/services/anomaly_service.py y detecta posibles fallos de seguridad, vulnerabilidades de rendimiento o casos borde no cubiertos."

* **Resultado Producido por la IA:**
Sugirió validar que la lista de lecturas tenga al menos 3 elementos para que la desviación estándar sea estadísticamente significativa.
Sugirió importar numpy para acelerar el cálculo estadístico.
Detectó la falta de protección ante arreglos masivos (Riesgo DoS / OWASP API4).

* **Decisión Técnica e Ingenieril:** 
Aceptado: Se agregó la condición if len(readings) < 3: return [] y la validación de tamaño en los esquemas Pydantic del router.
Rechazado: Se rechazó la importación de numpy. Se mantiene la librería estándar math para evitar dependencias innecesarias en el contenedor de producción.

* **Cierre y Conclusiones de la Semana**
Plausibilidad vs. Corrección: El LLM genera soluciones estructuralmente convincentes muy rápido, pero suele omitir tipado estricto (mypy) y casos de borde estadísticos.
Complementariedad Humano + IA: La IA es excelente detectando detalles sintácticos y sugiriendo pruebas; el criterio humano determina la arquitectura, los límites de dominio y la seguridad del sistema.


# Semana 5: La IA como un copiloto profesional

## Entrada 1: Integración de API y Validación de Endpoints (Miércoles 15)
* **Contexto / Objetivo:** Verificar la comunicación HTTP entre FastAPI, el esquema Pydantic y el motor puro de dominio (`alert_service`).

* **Prueba Ejecutada (Terminal PowerShell):**
  ```powershell
  Invoke-RestMethod -Uri "[http://127.0.0.1:8080/readings/evaluate](http://127.0.0.1:8080/readings/evaluate)" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"sensor_id":"TEMP-01","value":42.0,"min_threshold":15.0,"max_threshold":30.0,"critical_threshold":40.0}'
  ```
  
* **Resultado Producido por la API:**
Status HTTP: 200 OK (y 200 OK en /health).
Payload de Respuesta : {"sensor_id":"TEMP-01", "value":42.0, "alert_level":"CRITICAL", "message":"¡ALERTA CRÍTICO!..."}

* **Decisión Técnica e Ingenieril:** Estatus: Integración validada correctamente desde terminal mediante cliente HTTP nativo. Siguiente paso: Proceder con la implementación de logs estructurados en JSON para observabilidad.


# Semana 6: Integración Autónoma y Observabilidad

## Entrada 1: Integración Autónoma y Observabilidad

* **Contexto / Objetivo:** Diseñar la arquitectura limpia, endpoints de observabilidad (Healthcheck/JSON Logging) y pruebas de integración.
* **Prompt Utilizado:**
  > "Diseña el router /readings/evaluate en FastAPI conectando la función pura de evaluación de umbrales. Si la lectura genera una alerta (WARNING o CRITICAL), emite un log JSON estructurado mediante la librería estándar logging."
* **Resultado Producido por la IA:** Generó el código base con el handler de FastAPI y la serialización `json.dumps()`.
* **Decisión del Ingeniero y Justificación:**
  * **Aceptado:** Se utilizó la estructura del log JSON para el evento `SENSOR_ALERT_TRIGGERED`.
  * **Ajustado:** Se refactorizó la firma del endpoint y los esquemas de Pydantic V2 utilizando `json_schema_extra` para evitar advertencias de deprecación en los reportes de prueba. 