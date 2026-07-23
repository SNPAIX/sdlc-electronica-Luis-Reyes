import os
import pytest
from semana2.eval1.iot_monitoring.sensor_simulator import SensorSimulator
from semana2.eval1.iot_monitoring.anomaly_detector import AnomalyDetector
from semana2.eval1.iot_monitoring.alert_manager import AlertManager, FileNotificationStrategy
from semana2.eval1.iot_monitoring.warehouse_monitor import WarehouseMonitorSystem

def test_full_warehouse_simulation_600_readings(tmp_path):
    """
    Prueba de integración (Extensión de Distinción):
    Simula 10 sensores durante 60 ciclos (600 lecturas) con distribución gaussiana.
    Verifica que la telemetría y las alertas procesadas se registren adecuadamente.
    """
    log_file = tmp_path / "test_alerts.log"
    
    # 1. Configurar componentes
    simulator = SensorSimulator(num_sensors=10, mean_temp=25.0, std_temp=5.0, mean_hum=60.0, std_hum=10.0)
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    file_strategy = FileNotificationStrategy(log_filepath=str(log_file))
    alert_manager = AlertManager(strategy=file_strategy)
    
    monitor = WarehouseMonitorSystem(simulator=simulator, detector=detector, alert_manager=alert_manager)
    
    # 2. Ejecutar 60 ciclos de simulación (10 sensores x 60 ciclos = 600 lecturas)
    total_readings, total_anomalies = monitor.run_simulation_cycles(cycles=60)
    
    # 3. Verificaciones
    assert total_readings == 600
    assert total_anomalies >= 0
    
    # Si hubo anomalías, comprobar que el archivo de log se generó y no está vacío
    if total_anomalies > 0:
        assert os.path.exists(log_file)
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == total_anomalies