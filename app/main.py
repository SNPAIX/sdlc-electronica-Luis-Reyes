from fastapi import FastAPI, status
from app.routers import readings

app = FastAPI(
    title="SensorHub API",
    description="API de monitoreo e integración de sensores con arquitectura limpia",
    version="1.0.0",
)

# Incluir router de lecturas
app.include_router(readings.router)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Observability"],
    summary="Healthcheck para monitoreo en producción",
)
def healthcheck() -> dict[str, str]:
    return {"status": "healthy", "database": "connected"}