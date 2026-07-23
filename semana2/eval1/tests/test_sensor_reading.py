import pytest
from semana2.eval1.iot_monitoring.sensor_reading import SensorReading

def test_sensor_reading_valid_creation():
    """Valida la creación de una lectura dentro de parámetros normales."""
    reading = SensorReading(sensor_id="TEMP-01", temperature=25.0, humidity=50.0)
    assert reading.sensor_id == "TEMP-01"
    assert reading.temperature == 25.0
    assert reading.humidity == 50.0

def test_sensor_reading_invalid_temperature_raises_error():
    """Valida que lecturas fuera de rango físico (-20 a 70 °C) lancen error."""
    with pytest.raises(ValueError, match="Temperatura fuera de rango"):
        SensorReading(sensor_id="TEMP-01", temperature=85.0, humidity=50.0)

def test_sensor_reading_invalid_humidity_raises_error():
    """Valida que humedades fuera de rango (0 a 100 %) lancen error."""
    with pytest.raises(ValueError, match="Humedad fuera de rango"):
        SensorReading(sensor_id="TEMP-01", temperature=25.0, humidity=-5.0)