from enum import Enum


class AlertLevel(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


def evaluate_sensor_reading(
    value: float,
    min_threshold: float,
    max_threshold: float,
    critical_threshold: float,
) -> tuple[AlertLevel, str]:
    """Evalúa el valor de una lectura respecto a sus umbrales operacionales.

    Args:
        value: Valor numérico leído por el sensor.
        min_threshold: Umbral inferior tolerable.
        max_threshold: Umbral superior tolerable.
        critical_threshold: Umbral máximo crítico de operación.

    Returns:
        Tupla con el nivel de alerta (AlertLevel) y un mensaje descriptivo.
    """
    if value >= critical_threshold:
        return (
            AlertLevel.CRITICAL,
            f"¡ALERTA CRÍTICO! Lectura de {value} ha alcanzado el límite crítico ({critical_threshold}).",
        )

    if value > max_threshold:
        return (
            AlertLevel.WARNING,
            f"Advertencia: Lectura de {value} supera el umbral máximo ({max_threshold}).",
        )

    if value < min_threshold:
        return (
            AlertLevel.WARNING,
            f"Advertencia: Lectura de {value} está por debajo del umbral mínimo ({min_threshold}).",
        )

    return AlertLevel.OK, f"Lectura de {value} dentro del rango normal."