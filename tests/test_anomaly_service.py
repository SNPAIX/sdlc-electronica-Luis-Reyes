from app.services.anomaly_service import detect_temperature_anomalies


def test_detect_anomalies_empty_list() -> None:
    """Debe retornar una lista vacía si no hay lecturas."""
    result = detect_temperature_anomalies([])
    assert result == []


def test_detect_anomalies_no_anomalies() -> None:
    """Debe retornar lista vacía cuando todas las temperaturas son uniformes."""
    readings = [22.0, 22.5, 22.1, 22.3, 22.2]
    result = detect_temperature_anomalies(readings)
    assert result == []


def test_detect_anomalies_outlier_detected() -> None:
    """Debe identificar un valor que supere las 3 desviaciones estándar."""
    # Promedio ~20.0, std ~0.2. El valor 45.0 es una anomalía clara.
    readings = [20.0, 20.1, 19.9, 20.2, 20.0, 20.1, 19.8, 45.0]
    result = detect_temperature_anomalies(readings, threshold_std=2.5)

    assert len(result) == 1
    assert result[0]["index"] == 7
    assert result[0]["value"] == 45.0
    assert result[0]["is_anomaly"] is True


def test_detect_anomalies_insufficient_data() -> None:
    """No debe marcar anomalías si hay menos de 3 lecturas (desviación no confiable)."""
    readings = [20.0, 100.0]
    result = detect_temperature_anomalies(readings)
    assert result == []


def test_detect_anomalies_zero_variance() -> None:
    """Debe manejar varianza cero (todos los valores idénticos) sin dividir por cero."""
    readings = [25.0, 25.0, 25.0, 25.0]
    result = detect_temperature_anomalies(readings)
    assert result == []