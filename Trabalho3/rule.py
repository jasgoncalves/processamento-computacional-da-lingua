from typing import List

from constituent import Constituent


class Rule:
    def __init__(self, left_hs: Constituent, right_hs: List[Constituent], current_state=0):
        self.right_hs = right_hs
        self.left_hs = left_hs
        self.current_state = current_state

    def advance_state(self):
        self.current_state = self.current_state + 1
