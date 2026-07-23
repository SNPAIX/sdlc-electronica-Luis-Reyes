from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not (-20.0 <= self.temperature <= 70.0):
            raise ValueError(f"Temperatura fuera de rango operativo (-20 a 70 °C): {self.temperature}")
        if not (0.0 <= self.humidity <= 100.0):
            raise ValueError(f"Humedad fuera de rango operativo (0 a 100 %): {self.humidity}")