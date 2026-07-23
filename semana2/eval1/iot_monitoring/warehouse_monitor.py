from typing import Tuple
from semana2.eval1.iot_monitoring.sensor_simulator import SensorSimulator
from semana2.eval1.iot_monitoring.anomaly_detector import AnomalyDetector
from semana2.eval1.iot_monitoring.alert_manager import AlertManager

class WarehouseMonitorSystem:
    """Orquestador principal (Patrón Fachada) para el sistema de monitoreo IoT."""
    def __init__(
        self,
        simulator: SensorSimulator,
        detector: AnomalyDetector,
        alert_manager: AlertManager
    ) -> None:
        self.simulator = simulator
        self.detector = detector
        self.alert_manager = alert_manager

    def run_simulation_cycles(self, cycles: int = 60) -> Tuple[int, int]:
        total_readings = 0
        total_anomalies = 0

        for _ in range(cycles):
            cycle_readings = self.simulator.generate_cycle_readings()
            for reading in cycle_readings:
                total_readings += 1
                anomaly = self.detector.evaluate(reading)
                if anomaly:
                    total_anomalies += 1
                    self.alert_manager.dispatch(anomaly)

        return total_readings, total_anomalies