```markdown
# Sprint 1 Planning - Monitoreo IoT Bodega Industrial

## 1. Sprint Goal
Implementar el núcleo funcional del sistema IoT (Ingesta validada, Detección dinámica de anomalías y Alertas multicanal) cubriendo las Historias US-01, US-02, US-03, US-04 y US-05 bajo la metodología TDD estricta y con cobertura de pruebas ≥ 80%.

## 2. Historias Seleccionadas (Sprint Backlog)
- **US-01:** Ingesta y Validación de Lecturas (`SensorReading`) - 3 pts
- **US-02:** Detección Dinámica de Anomalías (`AnomalyDetector`) - 5 pts
- **US-03:** Despacho Multicanal de Alertas (`AlertManager`) - 5 pts
- **US-04:** Simulación Gaussiana de Red (`SensorSimulator`) - 8 pts
- **US-05:** Configuración Dinámica de Umbrales - 2 pts
**Total Story Points:** 23 pts.

## 3. Desglose de Tareas (Estimación ≤ 4 horas por tarea)
1. **Tarea 1.1 (TDD Red):** Crear test unitario para la clase `SensorReading` validando atributos y rangos (-20 a 70 °C). *(1.5 h)*
2. **Tarea 1.2 (TDD Green/Refactor):** Implementar la dataclass `SensorReading` con validaciones en `__post_init__`. *(1 h)*
3. **Tarea 2.1 (TDD Red):** Crear tests unitarios para `AnomalyDetector` probando umbrales de temperatura (>35 °C) y humedad (>80 %). *(2 h)*
4. **Tarea 2.2 (TDD Green/Refactor):** Implementar `AnomalyDetector` con inyección de dependencias para los umbrales. *(1.5 h)*
5. **Tarea 3.1 (TDD Red):** Crear tests para `AlertManager` usando mocks para las estrategias `ConsoleAlertStrategy` y `FileAlertStrategy`. *(2 h)*
6. **Tarea 3.2 (TDD Green/Refactor):** Implementar patrón Strategy para `AlertManager`. *(2 h)*
7. **Tarea 4.1 (TDD Red & Green):** Crear e implementar `SensorSimulator` con distribución gaussiana y prueba de integración de 10 sensores x 60 ciclos. *(3 h)*