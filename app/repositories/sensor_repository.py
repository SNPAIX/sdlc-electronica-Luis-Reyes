from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sensor_model import SensorReadingModel
from app.schemas.sensor_schema import SensorReadingCreate

class SensorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, reading_data: SensorReadingCreate) -> SensorReadingModel:
        db_reading = SensorReadingModel(
            sensor_id=reading_data.sensor_id,
            temperature=reading_data.temperature,
            humidity=reading_data.humidity
        )
        self.db.add(db_reading)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[SensorReadingModel]:
        stmt = select(SensorReadingModel).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()