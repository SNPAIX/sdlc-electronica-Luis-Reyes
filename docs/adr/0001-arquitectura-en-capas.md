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