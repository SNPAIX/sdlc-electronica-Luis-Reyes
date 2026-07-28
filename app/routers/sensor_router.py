from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.sensor_repository import SensorRepository
from app.services.sensor_service import SensorService
from app.schemas.sensor_schema import SensorReadingCreate, SensorReadingResponse

# ¡Asegúrate de que aquí diga 'router' en singular!
router = APIRouter(
    prefix="/readings",
    tags=["Sensor Readings"]
)

def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    repository = SensorRepository(db)
    return SensorService(repository)

@router.post(
    "/",
    response_model=SensorReadingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingresar nueva lectura de telemetría"
)
def create_reading(
    reading: SensorReadingCreate,
    service: SensorService = Depends(get_sensor_service)
) -> SensorReadingResponse:
    return service.process_reading(reading)

@router.get(
    "/",
    response_model=List[SensorReadingResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar histórico de lecturas con paginación"
)
def list_readings(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(20, ge=1, le=100, description="Límite por página (máximo 100)"),
    service: SensorService = Depends(get_sensor_service)
) -> List[SensorReadingResponse]:
    return service.get_readings(skip=skip, limit=limit)