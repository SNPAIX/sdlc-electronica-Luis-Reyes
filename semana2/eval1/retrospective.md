# Sprint 1 Retrospective - Monitoreo IoT Bodega Industrial

**Fecha:** 22 de Julio, 2026  
**Facilitador / Rol:** LUIS KHALED REYES CASANOVA (Scrum Master & Developer)  

---

## 1. ¿Qué salió bien? (What went well?)
* **Disciplina TDD Estricta:** Se logró la separación atómica entre los commits del conjunto de pruebas (`[RED]`) y los commits de la solución funcional (`[GREEN]`) para las 4 historias desarrolladas.
* **Arquitectura Desacoplada:** La aplicación de patrones de diseño (Inyección de Dependencias en `AnomalyDetector` y Patrón Strategy en `AlertManager`) permitió aislar las reglas del negocio de los canales físicos de notificación.
* **Cobertura de Pruebas:** Se alcanzó una cobertura de código superior al 80% requerida por la *Definition of Done*.

## 2. ¿Qué se puede mejorar? (What could be improved?)
* **Manejo del Entorno Virtual:** En las primeras ejecuciones de pruebas hubo fallos leves de configuración por olvidar la activación del `.venv` en la sesión de terminal.
* **Estimación de Story Points:** La implementación del simulador gaussiano requirió más tiempo de ajuste matemático en la distribución de la desviación estándar del previsto inicialmente.

## 3. Plan de Acción Concreto (Action Item)
* **Acción:** Configurar un script de pre-commit o automatización local que valide la presencia de entornos virtuales activos y corra `ruff check` antes de permitir un commit en las siguientes semanas.