import random
from typing import List
from semana2.eval1.iot_monitoring.sensor_reading import SensorReading

class SensorSimulator:
    """Genera lecturas estocásticas para una red de sensores utilizando distribución gaussiana."""
    def __init__(
        self,
        num_sensors: int = 10,
        mean_temp: float = 25.0,
        std_temp: float = 4.0,
        mean_hum: float = 55.0,
        std_hum: float = 8.0
    ) -> None:
        self.sensor_ids = [f"SENSOR-{i+1:02d}" for i in range(num_sensors)]
        self.mean_temp = mean_temp
        self.std_temp = std_temp
        self.mean_hum = mean_hum
        self.std_hum = std_hum

    def generate_cycle_readings(self) -> List[SensorReading]:
        readings: List[SensorReading] = []
        for s_id in self.sensor_ids:
            # Muestreo gaussiano truncado a límites físicos válidos
            temp = round(max(-15.0, min(65.0, random.gauss(self.mean_temp, self.std_temp))), 2)
            hum = round(max(5.0, min(95.0, random.gauss(self.mean_hum, self.std_hum))), 2)
            readings.append(SensorReading(sensor_id=s_id, temperature=temp, humidity=hum))
        return readings