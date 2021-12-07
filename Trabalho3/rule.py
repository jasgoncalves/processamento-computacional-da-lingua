from __future__ import annotations

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

    def is_awaiting_constituent(self, const: Constituent):
        return

    def __eq__(self, other: Rule):
        right_hs_eq = True
        for index, const in enumerate(self.right_hs):
            right_hs_eq = right_hs_eq and (const.__eq__(other.right_hs[index]))

        return self.left_hs.__eq__(other.left_hs) and right_hs_eq and self.current_state == other.current_state
