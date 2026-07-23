from abc import ABC, abstractmethod
from semana2.eval1.iot_monitoring.anomaly_detector import Anomaly

class NotificationStrategy(ABC):
    """Interfaz abstracta (Patron Strategy) para canales de notificacion."""
    @abstractmethod
    def notify(self, anomaly: Anomaly) -> None:
        pass

class ConsoleNotificationStrategy(NotificationStrategy):
    """Estrategia para imprimir alertas directamente en la consola."""
    def notify(self, anomaly: Anomaly) -> None:
        print(
            f"[ALERTA CONSOLA] Sensor {anomaly.sensor_id} supero limite. "
            f"Tipo: {anomaly.anomaly_type.name} | Valor: {anomaly.value} | Limite: {anomaly.threshold}"
        )

class FileNotificationStrategy(NotificationStrategy):
    """Estrategia para registrar alertas en un archivo de log."""
    def __init__(self, log_filepath: str = "alerts.log") -> None:
        self.log_filepath = log_filepath

    def notify(self, anomaly: Anomaly) -> None:
        log_message = (
            f"[LOG] Sensor={anomaly.sensor_id} | "
            f"Tipo={anomaly.anomaly_type.name} | "
            f"Valor={anomaly.value} | Umbral={anomaly.threshold}\n"
        )
        with open(self.log_filepath, "a", encoding="utf-8") as f:
            f.write(log_message)

class AlertManager:
    """Contexto que utiliza la estrategia de notificacion activa."""
    def __init__(self, strategy: NotificationStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy) -> None:
        self._strategy = strategy

    def dispatch(self, anomaly: Anomaly) -> None:
        self._strategy.notify(anomaly)