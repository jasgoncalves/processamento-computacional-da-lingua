from typing import List

from state import State


class Chart:
    def __init__(self, states: List[State] = None):
        if states is None:
            states = []
        self.states = states
