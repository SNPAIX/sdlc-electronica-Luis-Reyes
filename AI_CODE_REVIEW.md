# Reporte de Code Review Asistido por IA (Semana 5)

**Objeto de Revisión:** `app/services/anomaly_service.py`  
**Herramienta de Análisis:** Asistente LLM (GitHub Copilot / Claude)  

---

## 1. Hallazgos Sugeridos por la IA

1. **Manejo de División por Cero:**
   * *Sugerencia:* La IA identificó que si todas las lecturas son idénticas (`std_dev == 0`), la fórmula del `z_score` lanzaría `ZeroDivisionError`.
   * *Veredicto:* **Aceptado.** Se incluyó el guard `if std_dev == 0.0: return []`.

2. **Diseño de Notificaciones y Principio Open/Closed (OCP):**
   * *Sugerencia:* La IA recomendó desacoplar el envío de alertas del cálculo matemático inyectando una interfaz `NotificationStrategy` para poder intercambiar canales (logs, mocks, correo) sin modificar el servicio.
   * *Veredicto:* **Aceptado.** Se implementó `NotificationStrategy`, `LogNotificationStrategy` y `MockNotificationStrategy`.

3. **Sugerencia de importación de `numpy`:**
   * *Sugerencia:* La IA recomendó usar `numpy.std()` y `numpy.mean()` para acelerar el cálculo.
   * *Veredicto:* **Rechazado.** Mantener cero dependencias externas en servicios ligeros evita sobrecargar el `requirements.txt` y posibles fallos de compilación en el entorno de despliegue.

4. **Tipado Estricto de Salida:**
   * *Sugerencia:* Especificar los tipos del diccionario de retorno (`dict[str, Any]`) y del parámetro `notifier` para cumplir con `mypy`.
   * *Veredicto:* **Aceptado.** Mantiene el repositorio alineado al criterio de 0 hallazgos en análisis estático.

---

## 2. Cobertura de Pruebas Agregadas

Se integraron **6 nuevas pruebas unitarias** en `tests/test_anomaly_service.py` que integran el pipeline de CI:
* Lista de lecturas vacía (`test_detect_anomalies_empty_list`).
* Lecturas sin anomalías (`test_detect_anomalies_no_anomalies`).
* Detección exitosa de outlier $> 2.5\sigma$ (`test_detect_anomalies_outlier_detected`).
* Protección ante conjunto de datos insuficiente $< 3$ muestras (`test_detect_anomalies_insufficient_data`).
* Protección ante varianza cero / división por cero (`test_detect_anomalies_zero_variance`).
* **Verificación de estrategia intercambiable de notificación OCP** (`test_anomaly_notification_ocp_strategy`).