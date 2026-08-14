from fastapi import APIRouter, status
from app.domain.services.alert_service import evaluate_sensor_reading
from app.schemas.reading import ReadingCreate, ReadingResponse

router = APIRouter(prefix="/readings", tags=["Readings & Alerts"])


@router.post(
    "/evaluate",
    response_model=ReadingResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluar lectura de sensor y generar nivel de alerta",
)
def process_reading(payload: ReadingCreate) -> ReadingResponse:
    alert_level, message = evaluate_sensor_reading(
        value=payload.value,
        min_threshold=payload.min_threshold,
        max_threshold=payload.max_threshold,
        critical_threshold=payload.critical_threshold,
    )

    return ReadingResponse(
        sensor_id=payload.sensor_id,
        value=payload.value,
        alert_level=alert_level,
        message=message,
    )