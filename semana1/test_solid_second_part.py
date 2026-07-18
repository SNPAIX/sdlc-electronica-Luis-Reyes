from .solid_isp_dip import BasicSensorISP, GoodDataProcessor

# TESTS ISP
def test_isp_basic_sensor_reading():
    sensor = BasicSensorISP()
    assert sensor.read_data() == 24.5

def test_isp_interface_segregation():
    sensor = BasicSensorISP()
    # Verificamos que no heredó ni tiene el método innecesario de calibración
    assert not hasattr(sensor, 'calibrate')


# TESTS DIP
class MockAdcReader:
    """Clase simulada (Mock) de hardware de bajo nivel para inyectar al procesador."""
    def read_raw(self) -> int:
        return 1023

def test_dip_processor_calculation():
    mock_reader = MockAdcReader()
    processor = GoodDataProcessor(reader=mock_reader)
    # 1023 debe calcular exactamente 5.0V
    assert processor.get_voltage() == 5.0

def test_dip_processor_with_different_value():
    class HalfScaleMock:
        def read_raw(self) -> int:
            return 0
    processor = GoodDataProcessor(reader=HalfScaleMock())
    assert processor.get_voltage() == 0.0