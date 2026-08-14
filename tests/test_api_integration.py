from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Verifica la respuesta del endpoint de salud /health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}


def test_evaluate_reading_integration() -> None:
    """Prueba de integración de evaluación de lecturas."""
    payload = {
        "sensor_id": "TEST-SENSOR-1",
        "value": 22.5,
        "min_threshold": 15.0,
        "max_threshold": 30.0,
        "critical_threshold": 40.0,
    }
    response = client.post("/readings/evaluate", json=payload)
    assert response.status_code == 200
    assert response.json()["alert_level"] == "OK"


def test_evaluate_reading_validation_error() -> None:
    """Prueba error de validación cuando falta un campo obligatorio."""
    payload = {
        "sensor_id": "TEST-SENSOR-1"
        # Falta el campo obligatorio 'value'
    }
    response = client.post("/readings/evaluate", json=payload)
    assert response.status_code == 422  # Unprocessable Entity