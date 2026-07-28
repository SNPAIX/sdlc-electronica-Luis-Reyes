from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SensorReadingBase(BaseModel):
    sensor_id: str = Field(..., description="Identificador único del sensor")
    temperature: float = Field(..., description="Temperatura ambiental en °C")
    humidity: float = Field(..., description="Humedad relativa en %")

    @field_validator("temperature")
    @classmethod
    def validate_temperature_limits(cls, v: float) -> float:
        if not (-50.0 <= v <= 80.0):
            raise ValueError("La temperatura está fuera de los límites físicos reales (-50 °C a 80 °C)")
        return v

    @field_validator("humidity")
    @classmethod
    def validate_humidity_limits(cls, v: float) -> float:
        if not (0.0 <= v <= 100.0):
            raise ValueError("La humedad debe estar entre 0% y 100%")
        return v


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReadingResponse(SensorReadingBase):
    id: int
    timestamp: datetime
    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)