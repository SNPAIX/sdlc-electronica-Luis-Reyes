# ADR 0002: Observabilidad Mediante Structured JSON Logging

* **Estatus:** Aceptado
* **Fecha:** 15 Agosto 2026

## Contexto
En un entorno distribuido de sensores IoT, los logs en texto plano dificultan la búsqueda, filtrado y agregación automática de eventos críticos en herramientas de monitoreo (Datadog, CloudWatch, Grafana).

## Decisión
Implementar un esquema de **Structured JSON Logging** para todos los eventos de alerta de nivel `WARNING` y `CRITICAL` disparados por el servicio de dominio.

## Consecuencias
* **Positivas:** Permite parseo automático de atributos clave (`sensor_id`, `reading_value`, `alert_level`).
* **Negativas:** Formato menos legible a simple vista para humanos sin herramientas de formateo de logs.