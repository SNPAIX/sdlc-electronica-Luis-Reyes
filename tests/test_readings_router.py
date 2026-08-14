from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck_endpoint() -> None:
    """Verifica que el endpoint /health responda 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}


def test_evaluate_reading_endpoint_critical() -> None:
    """Verifica la evaluación de lectura vía HTTP retornando CRITICAL."""
    payload = {
        "sensor_id": "TEMP-TEST-01",
        "value": 45.0,
        "min_threshold": 15.0,
        "max_threshold": 30.0,
        "critical_threshold": 40.0,
    }
    response = client.post("/readings/evaluate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == "TEMP-TEST-01"
    assert data["alert_level"] == "CRITICAL"