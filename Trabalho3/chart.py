from typing import List

from state import State


class Chart:
    def __init__(self, states: List[State] = None):
        if states is None:
            states = []
        self.states = states
        self.current_state = 0

    def enqueue_state(self, state: State):
        self.states.append(state)

    def advance_state(self):
        self.current_state = self.current_state + 1
