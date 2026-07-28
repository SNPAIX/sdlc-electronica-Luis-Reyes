from fastapi import FastAPI
from app.db import engine, Base
import app.models.sensor_model  # Registrar modelos
from app.routers.sensor_router import router as sensor_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API - Monitoreo IoT",
    description="API REST para ingesta, detección de anomalías y gestión de sensores en bodega industrial.",
    version="1.0.0",
)

# Incluir el router de sensores
app.include_router(sensor_router)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Endpoint de verificación de salud de la API."""
    return {"status": "ok", "service": "SensorHub IoT API"}