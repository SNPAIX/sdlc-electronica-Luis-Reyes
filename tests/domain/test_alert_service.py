from app.domain.services.alert_service import AlertLevel, evaluate_sensor_reading


def test_evaluate_reading_ok() -> None:
    """Debe retornar OK si la lectura está dentro del rango normal."""
    status, message = evaluate_sensor_reading(
        value=22.0, min_threshold=15.0, max_threshold=30.0, critical_threshold=40.0
    )
    assert status == AlertLevel.OK
    assert "Lectura dentro del rango normal" in message


def test_evaluate_reading_warning_lower() -> None:
    """Debe retornar WARNING si la lectura está por debajo del umbral mínimo."""
    status, message = evaluate_sensor_reading(
        value=10.0, min_threshold=15.0, max_threshold=30.0, critical_threshold=40.0
    )
    assert status == AlertLevel.WARNING
    assert "por debajo del umbral mínimo" in message


def test_evaluate_reading_warning_upper() -> None:
    """Debe retornar WARNING si supera el máximo pero no el crítico."""
    status, message = evaluate_sensor_reading(
        value=35.0, min_threshold=15.0, max_threshold=30.0, critical_threshold=40.0
    )
    assert status == AlertLevel.WARNING
    assert "supera el umbral máximo" in message


def test_evaluate_reading_critical() -> None:
    """Debe retornar CRITICAL si la lectura alcanza o supera el umbral crítico."""
    status, message = evaluate_sensor_reading(
        value=42.0, min_threshold=15.0, max_threshold=30.0, critical_threshold=40.0
    )
    assert status == AlertLevel.CRITICAL
    assert "CRÍTICO" in message