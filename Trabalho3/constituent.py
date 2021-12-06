from __future__ import annotations

from typing import List


class Constituent:
    def __init__(self, representation: str, is_terminal: bool, words: List[str] = None):
        if words is None:
            words = []
        self.representation = representation
        self.is_terminal = is_terminal
        self.words = words

    def __eq__(self, other: Constituent):
        return self.representation.__eq__(other.representation) and self.is_terminal == other.is_terminal
