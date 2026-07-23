# Product Backlog - Sistema de Monitoreo IoT para Bodega Industrial

## Priorización MoSCoW y Resumen de Estimación
- **Must Have (Obligatorio para Sprint 1):** US-01, US-02, US-03, US-04, US-05
- **Should Have (Deseable para Sprint 1/2):** US-06, US-07, US-08
- **Could Have (Futuro):** US-09
- **Won't Have (Fuera de alcance):** US-10

---

### US-01: Ingesta y Validación de Lecturas de Sensores (Must Have)
**Como** operador de la bodega,  
**Quiero** registrar lecturas de temperatura y humedad de los sensores cada 30 segundos,  
**Para** garantizar que la telemetría esté dentro de rangos físicamente válidos.  
**Story Points:** 3  

```gherkin
Feature: Registro de Lectura de Sensor
  Scenario: Registrar lectura válida dentro de rangos operativos
    Given un sensor con ID "TEMP-01"
    When se procesa una lectura con temperatura 25.0 °C y humedad 55.0 %
    Then la lectura debe registrarse exitosamente con marca de tiempo actual.

  Scenario: Rechazar lectura fuera de rango físico por sensor defectuoso
    Given un sensor con ID "TEMP-01"
    When se intenta procesar una lectura con temperatura 85.0 °C
    Then el sistema debe lanzar un ValueError con el mensaje "Temperatura fuera de rango operativo (-20 a 70 °C)".
```


### US-02: Detección Dinámica de Anomalías Ambientales (Must Have)
**Como** supervisor de calidad,  
**Quiero** detectar anomalías cuando la temperatura supere 35 °C o la humedad supere 80 %,  
**Para** reaccionar antes de que los productos en la bodega se dañen.  
**Story Points:** 5
```gherkin
Feature: Detección de Anomalías
  Scenario: Evaluar lectura que excede el umbral de temperatura
    Given un detector configurado con umbral de temperatura de 35.0 °C y humedad de 80.0 %
    When recibe una lectura de 36.5 °C y 50.0 % de humedad
    Then el detector debe marcar la lectura como anomalía por "CRITICAL_TEMPERATURE".

  Scenario: Evaluar lectura dentro de los parámetros normales
    Given un detector configurado con umbral de temperatura de 35.0 °C y humedad de 80.0 %
    When recibe una lectura de 22.0 °C y 45.0 % de humedad
    Then el detector debe confirmar que la lectura es normal.
```


### US-03: Despacho Multicanal de Alertas de Seguridad (Must Have)
**Como** encargado de mantenimiento,  
**Quiero** que las alertas se envíen a la consola y se registren en un archivo de log,  
**Para** mantener trazabilidad y reaccionar de inmediato.  
**Story Points:** 5
```gherkin
Feature: Gestión de Alertas
  Scenario: Emitir alerta de anomalía a archivo de registro y consola
    Given una alerta de anomalía crítica en el sensor "TEMP-05"
    When el AlertManager despacha la alerta a través del canal FileAlertStrategy
    Then la alerta debe guardarse en formato JSON dentro del archivo "alerts.log".
```


### US-03: Despacho Multicanal de Alertas de Seguridad (Must Have)
**Como** encargado de mantenimiento,  
**Quiero** que las alertas se envíen a la consola y se registren en un archivo de log,  
**Para** mantener trazabilidad y reaccionar de inmediato.  
**Story Points:** 5
```gherkin
Feature: Gestión de Alertas
  Scenario: Emitir alerta de anomalía a archivo de registro y consola
    Given una alerta de anomalía crítica en el sensor "TEMP-05"
    When el AlertManager despacha la alerta a través del canal FileAlertStrategy
    Then la alerta debe guardarse en formato JSON dentro del archivo "alerts.log".
```


### US-04 Simulación Gaussiana de Red de Sensores (Must Have / Extensión)
**Como** desarrollador de software,
**Quiero** simular 10 sensores generando datos con distribución gaussiana,
**Para** probar la estabilidad del sistema bajo carga realista.
**Story Points:** 8
```gherkin
Feature: Simulación Gaussiana
  Scenario: Generar lecturas estocásticas para 10 sensores
    Given un simulador configurado con media de 24.0 °C y desviación estándar de 2.0
    When se ejecutan 60 ciclos de simulación
    Then se deben generar 600 lecturas válidas de telemetría.
```


### US-05: Configuración Dinámica de Umbrales (Must Have)
**Como** administrador del sistema,
**Quiero** inyectar umbrales de alerta personalizados sin modificar el código fuente,
**Para** adaptar las reglas del sistema según la estación del año.
**Story Points:** 2
```gherkin
Feature: Inyección de Umbrales
  Scenario: Actualizar umbral de alerta en tiempo de ejecución
    Given un detector con umbral inicial de 35.0 °C
    When se actualiza el umbral a 30.0 °C
    Then una lectura de 31.0 °C debe ser detectada como anomalía.
```


### US-06: Persistencia de Histórico de Telemetría (Should Have)
**Como** analista de datos,
**Quiero** guardar todas las lecturas procesadas en un archivo JSON-lines,
**Para** realizar auditorías posteriores.
**Story Points:** 3
```gherkin
Feature: Persistencia JSONL
  Scenario: Guardar telemetría procesada
    Given un registrador de datos apuntando a "telemetry.jsonl"
    When procesa una lectura válida
    Then la línea debe ser agregada exitosamente al archivo de texto.
```


### US-07: Dashboard de Consola para Estado de Bodega (Should Have)
**Como** operador,
**Quiero** visualizar en tiempo real el conteo de lecturas y anomalías en la consola,
**Para** monitorear el estado general de la bodega.
**Story Points:** 3
```gherkin
Feature: Resumen en Consola
  Scenario: Mostrar estadísticas operativas
    Given 100 lecturas procesadas con 5 anomalías
    When el operador solicita el resumen
    Then la consola muestra "Total: 100 | Anomalías: 5".
```


### US-08: Notificación por Correo Electrónico Simulado (Should Have)
**Como** gerente de planta,
**Quiero** recibir un correo ante anomalías persistentes,
**Para** tomar decisiones administrativas urgentes.
**Story Points:** 5
```gherkin
Feature: Alerta Email
  Scenario: Simular envío de correo electrónico
    Given una alerta crítica no resuelta en 5 minutos
    When se activa el canal EmailAlertStrategy
    Then se registra la simulación del envío del correo al gerente.
```


### US-09: Exportación de Reportes CSV (Could Have)
**Como** auditor,
**Quiero** exportar las anomalías a un archivo CSV,
**Para** adjuntarlo a reportes mensuales.
**Story Points:** 2
```gherkin
Feature: Exportación CSV
  Scenario: Generar reporte CSV de anomalías
    Given un conjunto de anomalías registradas
    When se ejecuta la exportación
    Then se genera el archivo "anomalies_report.csv".
```


### US-10: Interfaz Web Interactiva en Tiempo Real (Won't Have)
**Como** usuario remoto,
**Quiero** ver un mapa 3D de la bodega en un navegador web,
**Para** ubicar espacialmente los sensores.
**Story Points:** 13 (Fuera de alcance para este Sprint).

```gherkin
Feature: Visualización Web 3D
  Scenario: Cargar modelo de bodega en navegador
    Given el sistema de monitoreo en ejecución
    When un usuario remoto abre la interfaz web
    Then se renderiza la representación gráfica 3D con la ubicación de los 10 sensores.
```