# ADR 0001: Adopción de Arquitectura en Capas para la API IoT

* **Estatus:** Aceptado
* **Fecha:** 2026-08-10
* **Autores:** Equipo de Desarrollo (SDLC)

---

## Contexto

El sistema de monitoreo requiere procesar lecturas de sensores, almacenar datos históricos y servir endpoints HTTP para clientes externos. Inicialmente, colocar lógica de base de datos directamente en las rutas de FastAPI dificulta el mantenimiento, la reutilización de código y la creación de pruebas unitarias aisladas sin tocar la base de datos.

---

## Decisión

Adoptar una **Arquitectura en Capas** estructurada de la siguiente manera:

1. **Routers (`app/routers/`):** Manejan las peticiones HTTP, validación de entrada/salida mediante esquemas Pydantic y códigos de respuesta.
2. **Services (`app/services/`):** Contienen las reglas de negocio, cálculos (detección de anomalías) y orquestación.
3. **Repositories (`app/repositories/`):** Gestionan el acceso a la base de datos mediante ORM (SQLAlchemy 2.x).
4. **Models & Schemas (`app/models/`, `app/schemas/`):** Definen las entidades de persistencia y los DTOs de comunicación.

---

## Consecuencias

### Positivas
* **Testabilidad:** Permite probar la capa de servicio con mocks sin necesidad de levantar la base de datos.
* **Mantenibilidad:** Separación clara de responsabilidades; los cambios en la BD no afectan a las rutas HTTP.

### Negativas
* **Indirección:** Mayor cantidad de archivos y clases para operaciones CRUD simples.


---

## Notas de Lectura: Martin Fowler — MonolithFirst y Microservicios

### Discusión Arquitectónica: ¿Cuándo NO usar microservicios?

Basado en las lecturas de Martin Fowler (*Microservices* y *MonolithFirst*), la arquitectura de microservicios **NO** debe utilizarse en los siguientes escenarios:

1. **Sistemas Nuevos o Dominio No Entendido (Greenfield Projects):** Intentar diseñar microservicios antes de comprender los límites del dominio (*Bounded Contexts*) conduce a microservicios acoplados y refactorizaciones complejas entre red.
2. **Equipos Pequeños:** Gestionar despliegues independientes, monitoreo distribuido y redes para un equipo pequeño consume más tiempo que aportar valor al producto.
3. **Complejidad Distribuida Innecesaria:** Si la aplicación no requiere escalar componentes de forma independiente ni tiene cuellos de botella aislados, un monolito modular como nuestra API en FastAPI con arquitectura en capas ofrece menor latencia, transacciones simples en base de datos y facilidad de depuración.

> **Conclusión:** Adoptamos el principio *MonolithFirst*. Nuestro sistema nace como un monolito bien estructurado en capas. Si en el futuro un módulo (ej. el procesamiento masivo de sensores) requiere escalado independiente, se extraerá como servicio individual.