import pytest
from .solid_srp_ocp_lsp import (
    GoodSensorSRP, TelemetryFormatter,
    ADCProcessor, I2CProcessor,
    BasicSensor, CompliantSensor
)

# TESTS SRP
def test_srp_sensor_reading():
    sensor = GoodSensorSRP()
    assert sensor.read_voltage() == 3.3

def test_srp_formatter():
    formatter = TelemetryFormatter()
    assert formatter.format(3.3) == "Sensor Value: 3.3V"

# TESTS OCP
def test_ocp_adc_processing():
    processor = ADCProcessor()
    assert processor.process(100.0) == 10.0

def test_ocp_i2c_processing():
    processor = I2CProcessor()
    assert processor.process(100.0) == 101.0

# TESTS LSP
def test_lsp_base_class():
    sensor = BasicSensor()
    assert isinstance(sensor.get_reading(), float)

def test_lsp_subclass_substitution():
    sensors: list = [BasicSensor(), CompliantSensor()]
    # Ambos deben responder de forma segura devolviendo un flotante sin romper el bucle
    for s in sensors:
        assert isinstance(s.get_reading(), float)