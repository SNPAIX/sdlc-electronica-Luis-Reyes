from .hola_sensor import Sensor
def test_sensor_read():
    sensor = Sensor()
    assert sensor.read() == 23.5