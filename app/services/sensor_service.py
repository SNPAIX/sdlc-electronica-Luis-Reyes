from typing import List
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor_schema import SensorReadingCreate, SensorReadingResponse

class SensorService:
    def __init__(self, repository: SensorRepository) -> None:
        self.repository = repository

    def process_reading(self, reading_data: SensorReadingCreate) -> SensorReadingResponse:
        # 1. Persistir mediante el repositorio
        db_item = self.repository.create(reading_data)
        
        # 2. Regla de negocio para anomalías
        is_anomaly = False
        reasons = []
        
        if db_item.temperature > 35.0:
            is_anomaly = True
            reasons.append("Temperatura crítica (>35°C)")
        if db_item.humidity > 80.0:
            is_anomaly = True
            reasons.append("Humedad crítica (>80%)")
            
        # 3. Mapear a respuesta DTO
        return SensorReadingResponse(
            id=db_item.id,
            sensor_id=db_item.sensor_id,
            temperature=db_item.temperature,
            humidity=db_item.humidity,
            timestamp=db_item.timestamp,
            is_anomaly=is_anomaly,
            anomaly_reason=" | ".join(reasons) if reasons else None
        )

def get_readings(self, skip: int = 0, limit: int = 100) -> List[SensorReadingResponse]:
        items = self.repository.get_all(skip=skip, limit=limit)
        
        responses = []
        for item in items:
            reasons = []
            if item.temperature > 35.0:
                reasons.append("Temperatura crítica (>35°C)")
            if item.humidity > 80.0:
                reasons.append("Humedad crítica (>80%)")
                
            responses.append(
                SensorReadingResponse(
                    id=item.id,
                    sensor_id=item.sensor_id,
                    temperature=item.temperature,
                    humidity=item.humidity,
                    timestamp=item.timestamp,
                    is_anomaly=len(reasons) > 0,
                    anomaly_reason=" | ".join(reasons) if reasons else None
                )
            )
        return responses