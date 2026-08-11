from typing import Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.anomaly_service import detect_temperature_anomalies

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


class AnomalyCheckRequest(BaseModel):
    readings: list[float] = Field(
        ...,
        description="Lista de lecturas de temperatura a analizar",
        examples=[[20.0, 20.1, 19.9, 45.0]],
    )
    threshold_std: float = Field(
        default=3.0,
        gt=0,
        description="Umbral de desviaciones estándar (debe ser mayor a 0)",
    )


class AnomalyResponse(BaseModel):
    total_readings: int
    anomalies_found: int
    anomalies: list[dict[str, Any]]


@router.post(
    "/check",
    response_model=AnomalyResponse,
    status_code=status.HTTP_200_OK,
    summary="Detectar anomalías en un conjunto de lecturas",
)
def check_anomalies(payload: AnomalyCheckRequest) -> AnomalyResponse:
    if not payload.readings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La lista de lecturas no puede estar vacía.",
        )

    detected = detect_temperature_anomalies(
        readings=payload.readings,
        threshold_std=payload.threshold_std,
    )

    return AnomalyResponse(
        total_readings=len(payload.readings),
        anomalies_found=len(detected),
        anomalies=detected,
    )