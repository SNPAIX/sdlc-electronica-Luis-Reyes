from fastapi import FastAPI
from app.db import Base, engine
from app.routers.sensor_router import router as sensor_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub IoT API",
    description="API para monitoreo de telemetría e inyección de datos de sensores",
    version="1.0.0"
)

app.include_router(sensor_router)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "SensorHub IoT API"}