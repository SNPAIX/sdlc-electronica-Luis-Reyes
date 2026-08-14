from pydantic import BaseModel, Field
from app.domain.services.alert_service import AlertLevel


class ReadingCreate(BaseModel):
    sensor_id: str = Field(..., example="TEMP-SENSOR-01")
    value: float = Field(..., example=35.5, description="Valor leído por el sensor")
    min_threshold: float = Field(default=15.0, example=15.0)
    max_threshold: float = Field(default=30.0, example=30.0)
    critical_threshold: float = Field(default=40.0, example=40.0)


class ReadingResponse(BaseModel):
    sensor_id: str
    value: float
    alert_level: AlertLevel
    message: str