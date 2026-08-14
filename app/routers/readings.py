import json
import logging
from fastapi import APIRouter, status

from app.domain.services.alert_service import AlertLevel, evaluate_sensor_reading
from app.schemas.reading import ReadingCreate, ReadingResponse

# Configuración básica del logger
logger = logging.getLogger("sensorhub.alerts")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

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

    # Observabilidad: Si hay alerta (WARNING o CRITICAL), emitir Log JSON
    if alert_level != AlertLevel.OK:
        log_event = {
            "event": "SENSOR_ALERT_TRIGGERED",
            "sensor_id": payload.sensor_id,
            "reading_value": payload.value,
            "alert_level": alert_level.value,
            "details": message,
        }
        # Imprime un JSON de una sola línea en la terminal
        logger.warning(json.dumps(log_event))

    return ReadingResponse(
        sensor_id=payload.sensor_id,
        value=payload.value,
        alert_level=alert_level,
        message=message,
    )