from __future__ import annotations

from typing import Tuple, List

from constituent import Constituent
from rule import Rule


class State:
    def __init__(self, rule: Rule, position: Tuple[int, int], backpointer: List[State] = None):
        if backpointer is None:
            backpointer = []
        self.rule = rule
        self.position = position
        self.backpointer = backpointer

    def is_complete(self) -> bool:
        return self.rule.has_terminated()

    def next_constituent(self) -> Constituent:
        return self.rule.get_current_constituent()

    def is_awaiting_constituent(self, const: Constituent) -> bool:
        return (not self.rule.has_terminated()) and self.rule.get_current_constituent().__eq__(const)

    def final_constituent(self) -> Constituent:
        return self.rule.left_hs

    def __str__(self):
        return self.rule.__str__() + " " + self.position.__str__()
