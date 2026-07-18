from .fsm_demo import TrafficLightFSM, State

def test_fsm_initial_state():
    fsm = TrafficLightFSM()
    assert fsm.current_state == State.RED
    assert fsm.cycle_count == 0

def test_fsm_transition_red_to_green():
    fsm = TrafficLightFSM()
    fsm.transition()
    assert fsm.current_state == State.GREEN

def test_fsm_full_cycle_returns_to_red():
    fsm = TrafficLightFSM()
    fsm.transition()  # -> GREEN
    fsm.transition()  # -> YELLOW
    fsm.transition()  # -> RED
    assert fsm.current_state == State.RED

def test_fsm_cycle_counting():
    fsm = TrafficLightFSM()
    # Ejecuta dos ciclos completos
    for _ in range(6):
        fsm.transition()
    assert fsm.cycle_count == 2