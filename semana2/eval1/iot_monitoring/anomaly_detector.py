from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from semana2.eval1.iot_monitoring.sensor_reading import SensorReading

class AnomalyType(Enum):
    CRITICAL_TEMPERATURE = auto()
    CRITICAL_HUMIDITY = auto()

@dataclass(frozen=True)
class Anomaly:
    sensor_id: str
    anomaly_type: AnomalyType
    value: float
    threshold: float

class AnomalyDetector:
    def __init__(self, max_temperature: float = 35.0, max_humidity: float = 80.0) -> None:
        self.max_temperature = max_temperature
        self.max_humidity = max_humidity

    def evaluate(self, reading: SensorReading) -> Optional[Anomaly]:
        if reading.temperature > self.max_temperature:
            return Anomaly(
                sensor_id=reading.sensor_id,
                anomaly_type=AnomalyType.CRITICAL_TEMPERATURE,
                value=reading.temperature,
                threshold=self.max_temperature
            )
        if reading.humidity > self.max_humidity:
            return Anomaly(
                sensor_id=reading.sensor_id,
                anomaly_type=AnomalyType.CRITICAL_HUMIDITY,
                value=reading.humidity,
                threshold=self.max_humidity
            )
        return None