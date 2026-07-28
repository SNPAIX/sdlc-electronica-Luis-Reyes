from datetime import datetime
from typing import List, Optional
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor_schema import SensorReadingCreate, SensorReadingResponse

class SensorService:
    def __init__(self, repository: SensorRepository) -> None:
        self.repository = repository

    def process_reading(self, reading_data: SensorReadingCreate) -> SensorReadingResponse:
        db_item = self.repository.create(reading_data)
        
        reasons = []
        if db_item.temperature > 35.0:
            reasons.append("Temperatura crítica (>35°C)")
        if db_item.humidity > 80.0:
            reasons.append("Humedad crítica (>80%)")
            
        return SensorReadingResponse(
            id=db_item.id,
            sensor_id=db_item.sensor_id,
            temperature=db_item.temperature,
            humidity=db_item.humidity,
            timestamp=db_item.timestamp,
            is_anomaly=len(reasons) > 0,
            anomaly_reason=" | ".join(reasons) if reasons else None
        )

    def get_readings(
        self, 
        skip: int = 0, 
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[SensorReadingResponse]:
        items = self.repository.get_all(skip=skip, limit=limit, start_date=start_date, end_date=end_date)
        
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