import math
from abc import ABC, abstractmethod
from typing import Any


# --- Interfaz de Notificación (Estrategia Intercambiable - OCP) ---
class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, anomalies: list[dict[str, Any]]) -> bool:
        """Envía una alerta cuando se detectan anomalías."""
        pass


class LogNotificationStrategy(NotificationStrategy):
    """Estrategia concreta 1: Notificación vía Logs."""

    def notify(self, anomalies: list[dict[str, Any]]) -> bool:
        if not anomalies:
            return False
        print(f"[ALERT LOG] Se detectaron {len(anomalies)} anomalías de temperatura.")
        return True


class MockNotificationStrategy(NotificationStrategy):
    """Estrategia concreta 2: Notificación Mock para Pruebas Unitarias."""

    def __init__(self) -> None:
        self.sent_notifications: list[list[dict[str, Any]]] = []

    def notify(self, anomalies: list[dict[str, Any]]) -> bool:
        if anomalies:
            self.sent_notifications.append(anomalies)
            return True
        return False


# --- Servicio Principal de Detección ---
def detect_temperature_anomalies(
    readings: list[float],
    threshold_std: float = 3.0,
    notifier: NotificationStrategy | None = None,
) -> list[dict[str, Any]]:
    """Calcula anomalías y opcionalmente las notifica usando una estrategia (OCP)."""
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

    if anomalies and notifier:
        notifier.notify(anomalies)

    return anomalies


# Alias para mantener retrocompatibilidad si es necesario
detect_and_notify_anomalies = detect_temperature_anomalies