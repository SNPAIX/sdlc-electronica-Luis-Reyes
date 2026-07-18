import abc
from typing import Protocol

# ==============================================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# ==============================================================================
# MAL: Forzamos a un sensor simple que solo lee datos a implementar calibración (innecesaria).
class BadSensorInterface(abc.ABC):
    @abc.abstractmethod
    def read_data(self) -> float:
        pass
    @abc.abstractmethod
    def calibrate(self) -> None:
        pass

class SimpleTemperatureSensor(BadSensorInterface):
    def read_data(self) -> float:
        return 24.5
    def calibrate(self) -> None:
        # Violación de ISP: No se puede calibrar este hardware de bajo costo.
        raise NotImplementedError("Este sensor no soporta calibracion")

# BIEN: Interfaces delgadas y segregadas. El cliente solo implementa lo que necesita.
class Readable(abc.ABC):
    @abc.abstractmethod
    def read_data(self) -> float:
        pass

class Calibratable(abc.ABC):
    @abc.abstractmethod
    def calibrate(self) -> None:
        pass

class BasicSensorISP(Readable):
    def read_data(self) -> float:
        return 24.5


# ==============================================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# ==============================================================================
# MAL: La clase de alto nivel depende directamente de la clase de bajo nivel concreta (Hardcoded).
class HardcodedAdcReader:
    def read_raw(self) -> int:
        return 512

class BadDataProcessor:
    def __init__(self) -> None:
        self.reader = HardcodedAdcReader()  # Acoplamiento rígido
    def get_voltage(self) -> float:
        return (self.reader.read_raw() * 5.0) / 1023.0

# BIEN: Ambos dependen de abstracciones mediante un Protocol (inyección de dependencias).
class ReaderProtocol(Protocol):
    def read_raw(self) -> int:
        ...

class GoodDataProcessor:
    def __init__(self, reader: ReaderProtocol) -> None:
        self.reader = reader  # Inyección de dependencia

    def get_voltage(self) -> float:
        return (self.reader.read_raw() * 5.0) / 1023.0