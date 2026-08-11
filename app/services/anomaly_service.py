import math
from typing import Any


def detect_temperature_anomalies(
    readings: list[float], threshold_std: float = 3.0
) -> list[dict[str, Any]]:
    """Analiza una lista de lecturas de temperatura y detecta valores atípicos.

    Args:
        readings: Lista de valores numéricos de temperatura.
        threshold_std: Umbral de desviaciones estándar para considerar anomalía.

    Returns:
        Lista de diccionarios con la información de los valores anómalos detectados.
    """
    if len(readings) < 3:
        return []

    mean = sum(readings) / len(readings)
    variance = sum((x - mean) ** 2 for x in readings) / len(readings)
    std_dev = math.sqrt(variance)

    if std_dev == 0.0:
        return []

    anomalies: list[dict[str, Any]] = []
    for index, value in enumerate(readings):
        z_score = abs(value - mean) / std_dev
        if z_score > threshold_std:
            anomalies.append(
                {
                    "index": index,
                    "value": value,
                    "z_score": round(z_score, 2),
                    "is_anomaly": True,
                }
            )

    return anomalies