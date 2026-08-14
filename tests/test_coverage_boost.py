from typing import Any
from fastapi.testclient import TestClient
from app.main import app
from app.services.anomaly_service import (
    LogNotificationStrategy,
    detect_and_notify_anomalies,
)

# Cliente estándar
client = TestClient(app)

# Cliente configurado para capturar excepciones 500 sin relanzarlas en pytest
client_no_raise = TestClient(app, raise_server_exceptions=False)


# -------------------------------------------------------------------
# 1. Cobertura para app/main.py (Global Exception Handler)
# -------------------------------------------------------------------
def test_global_exception_handler(monkeypatch: Any) -> None:
    """Fuerza una excepción inesperada para cubrir el manejador global de errores."""

    def mock_raise(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("Error interno simulado para pruebas de cobertura")

    monkeypatch.setattr(
        "app.routers.readings.evaluate_sensor_reading", mock_raise
    )

    payload = {
        "sensor_id": "TEST-ERR",
        "value": 25.0,
        "min_threshold": 10.0,
        "max_threshold": 30.0,
        "critical_threshold": 40.0,
    }
    
    # Usamos client_no_raise para que FastAPI capture la excepción con HTTP 500
    response = client_no_raise.post("/readings/evaluate", json=payload)

    assert response.status_code == 500
    assert response.json()["error"] == "InternalServerError"


# -------------------------------------------------------------------
# 2. Cobertura para app/routers/anomalies.py (Endpoint HTTP)
# -------------------------------------------------------------------
def test_anomalies_check_endpoint_success() -> None:
    """Prueba el endpoint /anomalies/check enviando lecturas con una anomalía."""
    payload = {
        "readings": [20.0, 20.0, 20.0, 20.0, 20.0, 100.0],
        "threshold_std": 1.5,
    }
    response = client.post("/anomalies/check", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["total_readings"] == 6
    assert data["anomalies_found"] == 1


def test_anomalies_check_endpoint_empty_list() -> None:
    """Prueba error 400 cuando la lista de lecturas está vacía."""
    payload = {"readings": [], "threshold_std": 2.0}
    response = client.post("/anomalies/check", json=payload)
    assert response.status_code == 400


# -------------------------------------------------------------------
# 3. Cobertura para app/services/anomaly_service.py (LogNotificationStrategy)
# -------------------------------------------------------------------
def test_log_notification_strategy_execution() -> None:
    """Ejecuta la estrategia concreta de logs para cubrir las líneas faltantes."""
    log_strategy = LogNotificationStrategy()

    # Caso 1: Notificación sin anomalías
    assert log_strategy.notify([]) is False

    # Caso 2: Notificación con anomalías
    anomalies = [{"index": 0, "value": 100.0, "z_score": 4.0, "is_anomaly": True}]
    assert log_strategy.notify(anomalies) is True

    # Caso 3: Integración directa en el servicio con threshold adecuado
    results = detect_and_notify_anomalies(
        [20.0, 20.0, 20.0, 20.0, 20.0, 100.0],
        notifier=log_strategy,
        threshold_std=1.5,
    )
    assert len(results) == 1