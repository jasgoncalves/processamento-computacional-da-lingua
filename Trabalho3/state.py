from __future__ import annotations

from typing import Tuple, List

from rule import Rule


class State:
    def __init__(self, rule: Rule, position: Tuple[int, int], backpointer: List[State] = None):
        if backpointer is None:
            backpointer = []
        self.rule = rule
        self.position = position
        self.backpointer = backpointer

    def is_complete(self):
        return self.rule.has_terminated()

    def next_constituent(self):
        return self.rule.get_current_constituent()