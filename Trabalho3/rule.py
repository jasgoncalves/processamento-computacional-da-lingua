from typing import List

from constituent import Constituent


class Rule:
    def __init__(self, left_hs: Constituent, right_hs: List[Constituent], current_state=0):
        self.right_hs = right_hs
        self.left_hs = left_hs
        self.current_state = current_state

    def advance_state(self) -> None:
        self.current_state = self.current_state + 1

    def get_current_constituent(self) -> Constituent:
        return self.right_hs[self.current_state]

    def has_terminated(self) -> bool:
        return self.current_state > len(self.right_hs) - 1
