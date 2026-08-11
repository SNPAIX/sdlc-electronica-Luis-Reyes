# Guía de Prompting Efectivo para Desarrollo de Software (Semana 5)

**Marco de Trabajo Utilizado:** Framework **CTRF**
* **C**ontexto: Entorno técnico, arquitectura del proyecto y tecnologías utilizadas.
* **T**area: La acción específica que debe realizar el modelo.
* **R**estricciones: Lo que el modelo NO debe hacer, librerías permitidas y reglas de estilo.
* **F**ormato: Estructura de la salida esperada (ej. solo código, Markdown, docstrings).

---

## Tarea 1: Generación de Código (Detección de Anomalías)

### Prompt Pobre
> "Hazme una función en Python para detectar anomalías de temperatura de un sensor."

* **Por qué falla:** No especifica la arquitectura del proyecto, el criterio matemático para definir una anomalía, los tipos de datos ni el formato del resultado. El modelo generará código genérico difícil de integrar en la API.

### Prompt Efectivo (CTRF)
> **Contexto:** Estoy desarrollando una API RESTful con FastAPI en Python 3.11+. La arquitectura sigue un patrón en capas (`routers`, `services`, `repositories`).
> 
> **Tarea:** Escribe una función pura `detect_temperature_anomalies(readings: list[float], threshold_std: float = 3.0) -> list[dict]` que analice un historial de lecturas de temperatura.
> 
> **Restricciones:**
> 1. Utiliza únicamente la librería estándar de Python (`math` y `statistics`), sin importar `numpy` ni `pandas`.
> 2. Considera como anomalía cualquier valor que se aleje del promedio por más de `threshold_std` desviaciones estándar.
> 3. Incluye tipado estrito compatible con `mypy`.
> 
> **Formato:** Devuelve únicamente la función con docstrings en formato Google y sus correspondientes type hints, lista para colocarse en `app/services/anomaly_service.py`.

---

## Tarea 2: Refactorización de Código (Repositorio SQLAlchemy 2.x)

### Prompt Pobre
> "Optimiza este repositorio para que sea más rápido."

* **Por qué falla:** Es completamente ambiguo. La IA no sabe qué método optimizar, qué versión de SQLAlchemy se está usando ni si debe modificar el esquema o la consulta.

### Prompt Efectivo (CTRF)
> **Contexto:** Tengo un método en `app/repositories/reading_repository.py` que consulta lecturas por `sensor_id` y rango de fechas utilizando SQLAlchemy 2.x.
> 
> **Tarea:** Refactoriza la consulta para aplicar paginación eficientemente en la base de datos usando `select().where().offset().limit()`.
> 
> **Restricciones:**
> 1. No utilices la sintaxis obsoleta 1.x `session.query(...)`.
> 2. Asegura que el ordenamiento sea determinista ordenando por `created_at` de forma descendente antes de aplicar la paginación.
> 3. Retorna un objeto `Sequence[Reading]` tipado para `mypy`.
> 
> **Formato:** Proporciona el método refactorizado junto con una breve explicación de dos oraciones justificando por qué la paginación a nivel de SQL es superior a aplicar slices en Python.

---

## Tarea 3: Explicación de Código (Inyección de Dependencias en FastAPI)

### Prompt Pobre
> "Explícame qué hace Depends(get_db) en FastAPI."

* **Por qué falla:** Produce una explicación de libro de texto genérica sin conectarla con la arquitectura en capas ni el manejo del ciclo de vida de las sesiones de base de datos.

### Resultado del Prompt Pobre
```python
# La IA generó código con pandas y sin tipado estricto
import pandas as pd

def detectar_anomalia(datos):
    df = pd.DataFrame(datos)
    return df[df > 30]
```

### Prompt Efectivo (CTRF)
> **Contexto:** Estamos implementando la inversión de dependencias en nuestra API IoT con FastAPI y SQLAlchemy. En nuestros routers usamos `session: Session = Depends(get_db)`.
> 
> **Tarea:** Explica el ciclo de vida de la sesión de base de datos cuando una petición HTTP llega a un endpoint que usa `Depends(get_db)`.
> 
> **Restricciones:**
> 1. Enfócate en cómo funciona el bloque `yield` y el bloque `finally: session.close()`.
> 2. Explica qué sucede con la sesión si el servicio dentro del endpoint lanza una excepción (ej. `HTTPException 404`).
> 
> **Formato:** Explícalo en máximo 3 puntos usando listas con viñetas y formato Markdown técnico claro.

### Resultado del Prompt Efectivo (CTRF)
# La IA generó código limpio con la librería estándar y type hints
```python
import math
from typing import Any

def detect_temperature_anomalies(
    readings: list[float], threshold_std: float = 3.0
) -> list[dict[str, Any]]:
    ...
```