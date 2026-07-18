import abc

# ==============================================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# ==============================================================================
# MAL: La clase lee del hardware Y ADEMÁS formatea/imprime (dos razones para cambiar).
class BadSensorSRP:
    def read_voltage(self) -> float:
        return 3.3
    def format_to_string(self) -> str:
        return f"Sensor Value: {self.read_voltage()}V"

# BIEN: Separamos la lectura del formateo de datos.
class GoodSensorSRP:
    def read_voltage(self) -> float:
        return 3.3

class TelemetryFormatter:
    def format(self, voltage: float) -> str:
        return f"Sensor Value: {voltage}V"


# ==============================================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# ==============================================================================
# MAL: Si agregamos un nuevo tipo de sensor, hay que modificar esta clase (rompe OCP).
class BadFilterOCP:
    def filter_data(self, raw_value: float, sensor_type: str) -> float:
        if sensor_type == "ADC":
            return raw_value * 0.1
        elif sensor_type == "I2C":
            return raw_value + 1.0
        return raw_value

# BIEN: Abierto a la extensión mediante abstracción, cerrado a la modificación.
class SensorDataProcessor(abc.ABC):
    @abc.abstractmethod
    def process(self, value: float) -> float:
        pass

class ADCProcessor(SensorDataProcessor):
    def process(self, value: float) -> float:
        return value * 0.1

class I2CProcessor(SensorDataProcessor):
    def process(self, value: float) -> float:
        return value + 1.0


# ==============================================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ==============================================================================
# MAL: La subclase altera radicalmente el comportamiento esperado (lanza excepción inesperada).
class BasicSensor:
    def get_reading(self) -> float:
        return 12.5

class BrokenSubclassSensor(BasicSensor):
    def get_reading(self) -> float:
        raise RuntimeError("Hardware desconectado de forma crítica")  # Rompe el contrato base abruptamente

# BIEN: Las subclases pueden sustituirse sin romper la lógica del sistema.
class CompliantSensor(BasicSensor):
    def get_reading(self) -> float:
        # Extiende o modifica de forma segura respetando el tipo de retorno contratado
        return 15.0