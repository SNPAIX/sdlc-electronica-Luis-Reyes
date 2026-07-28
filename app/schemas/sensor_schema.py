from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class SensorReadingBase(BaseModel):
    sensor_id: str = Field(..., example="TEMP-01", description="Identificador único del sensor")
    temperature: float = Field(..., ge=-20.0, le=70.0, example=25.5, description="Temperatura en °C (-20 a 70)")
    humidity: float = Field(..., ge=0.0, le=100.0, example=55.0, description="Humedad relativa en % (0 a 100)")

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingResponse(SensorReadingBase):
    id: int
    timestamp: datetime
    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)