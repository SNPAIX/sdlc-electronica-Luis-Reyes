import pytest
from semana2.eval1.iot_monitoring.sensor_reading import SensorReading
from semana2.eval1.iot_monitoring.anomaly_detector import AnomalyDetector, AnomalyType

def test_anomaly_detector_normal_reading():
    """Verifica que una lectura dentro de límites normales no genere anomalía."""
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="TEMP-01", temperature=25.0, humidity=50.0)
    
    anomaly = detector.evaluate(reading)
    assert anomaly is None

def test_anomaly_detector_critical_temperature():
    """Verifica la detección de anomalía por exceso de temperatura (> 35 °C)."""
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="TEMP-01", temperature=36.5, humidity=50.0)
    
    anomaly = detector.evaluate(reading)
    assert anomaly is not None
    assert anomaly.anomaly_type == AnomalyType.CRITICAL_TEMPERATURE
    assert anomaly.value == 36.5

def test_anomaly_detector_critical_humidity():
    """Verifica la detección de anomalía por exceso de humedad (> 80 %)."""
    detector = AnomalyDetector(max_temperature=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="HUM-01", temperature=22.0, humidity=85.0)
    
    anomaly = detector.evaluate(reading)
    assert anomaly is not None
    assert anomaly.anomaly_type == AnomalyType.CRITICAL_HUMIDITY
    assert anomaly.value == 85.0