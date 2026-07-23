import pytest
from semana2.eval1.iot_monitoring.anomaly_detector import Anomaly, AnomalyType
from semana2.eval1.iot_monitoring.alert_manager import (
    AlertManager,
    NotificationStrategy,
    ConsoleNotificationStrategy,
)

class MockNotificationStrategy(NotificationStrategy):
    """Estrategia de prueba para capturar las alertas enviadas."""
    def __init__(self):
        self.sent_alerts = []

    def notify(self, anomaly: Anomaly) -> None:
        self.sent_alerts.append(anomaly)

def test_alert_manager_dispatches_to_strategy():
    """Verifica que AlertManager notifique a traves de la estrategia configurada."""
    mock_strategy = MockNotificationStrategy()
    manager = AlertManager(strategy=mock_strategy)
    
    anomaly = Anomaly(
        sensor_id="TEMP-99",
        anomaly_type=AnomalyType.CRITICAL_TEMPERATURE,
        value=42.0,
        threshold=35.0
    )
    
    manager.dispatch(anomaly)
    
    assert len(mock_strategy.sent_alerts) == 1
    assert mock_strategy.sent_alerts[0].sensor_id == "TEMP-99"

def test_alert_manager_switch_strategy_at_runtime():
    """Verifica que se pueda cambiar de estrategia en tiempo de ejecucion."""
    strat1 = MockNotificationStrategy()
    strat2 = MockNotificationStrategy()
    
    manager = AlertManager(strategy=strat1)
    anomaly = Anomaly("HUM-01", AnomalyType.CRITICAL_HUMIDITY, 90.0, 80.0)
    
    manager.dispatch(anomaly)
    assert len(strat1.sent_alerts) == 1
    assert len(strat2.sent_alerts) == 0

    # Cambio dinamico de estrategia
    manager.set_strategy(strat2)
    manager.dispatch(anomaly)
    assert len(strat1.sent_alerts) == 1
    assert len(strat2.sent_alerts) == 1