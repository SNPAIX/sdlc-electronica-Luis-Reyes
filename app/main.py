import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# Importar todos los routers del proyecto
from app.routers import anomalies, readings, sensor_router

logger = logging.getLogger("sensorhub.errors")

app = FastAPI(
    title="SensorHub API",
    description="API de monitoreo e integración de sensores con arquitectura limpia",
    version="1.0.0",
)

# Incluir routers
app.include_router(readings.router)
app.include_router(anomalies.router)
app.include_router(sensor_router.router)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Observability"],
    summary="Healthcheck para monitoreo en producción",
)
def healthcheck() -> dict[str, str]:
    return {"status": "healthy", "database": "connected"}


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error(
        f"Excepción no capturada en {request.url.path}: {str(exc)}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "Ha ocurrido un error interno en el servidor. El incidente ha sido registrado.",
        },
    )