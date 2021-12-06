from typing import List

from rule import Rule
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

    def is_chart_completed(self):
        return self.current_state > len(self.states) - 1

    def has_rule(self, rule: Rule) -> bool:
        for state in self.states:
            if state.rule.__eq__(rule):
                return True
        return False
