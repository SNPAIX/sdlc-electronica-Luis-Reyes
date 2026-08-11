# Análisis de Seguridad OWASP API Security Top 10 — API IoT

**Proyecto:** API de Monitoreo de Sensores  
**Fecha:** Semana 5  

---

## Evaluación de Riesgos y Mitigaciones en la API

### 1. API1:2023 - Broken Object Level Authorization (BOLA)
* **Riesgo:** Un usuario autenticado podría consultar o modificar lecturas de sensores pertenecientes a otro usuario cambiando el `sensor_id` en la URL.
* **Mitigación Implementada/Recomendada:** Validar en la capa de servicio que el `sensor_id` consultado pertenezca explícitamente al `user_id` extraído del token JWT.

### 2. API4:2023 - Unrestricted Resource Consumption (Rate Limiting)
* **Riesgo:** Un cliente o bot podría enviar miles de peticiones al endpoint `/anomalies/check` o enviar arreglos con millones de lecturas, provocando denegación de servicio (DoS) por uso de CPU/Memoria.
* **Mitigación Implementada/Recomendada:** 
  1. Limitar el tamaño máximo de la lista de lecturas enviadas en el esquema de Pydantic.
  2. Implementar middleware de Rate Limiting (ej. `slowapi`) en FastAPI para limitar a máximo 60 peticiones por minuto por dirección IP.

### 3. API8:2023 - Security Misconfiguration
* **Riesgo:** Exposición de stack traces o información sensible en los errores HTTP en entorno de producción.
* **Mitigación Implementada/Recomendada:** Configurar manejadores de excepciones globales (`HTTPException`) en FastAPI para retornar mensajes de error genéricos y limpios en producción.

### 4. Riesgo Específico de Código Generado por IA (Alucinación de Dependencias)
* **Riesgo:** Copiar código sugerido por LLMs que importe paquetes obsoletos, vulnerables o maliciosos (ej. ataques de Typosquatting en PyPI).
* **Mitigación Aplicada:** Verificación estricta mediante `ruff` y mantener cero dependencias innecesarias en los módulos core (`anomaly_service.py` utiliza solo la librería estándar `math`).