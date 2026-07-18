from enum import Enum, auto

class State(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class TrafficLightFSM:
    def __init__(self) -> None:
        self.current_state: State = State.RED
        self.cycle_count: int = 0

    def transition(self) -> None:
        """Controla el flujo de transiciones de la FSM."""
        if self.current_state == State.RED:
            self.current_state = State.GREEN
        elif self.current_state == State.GREEN:
            self.current_state = State.YELLOW
        elif self.current_state == State.YELLOW:
            self.current_state = State.RED
            self.cycle_count += 1