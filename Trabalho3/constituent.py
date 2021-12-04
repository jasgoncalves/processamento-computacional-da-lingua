from typing import List


class Constituent:
    def __init__(self, representation: str, is_terminal: bool, words: List[str] = None):
        if words is None:
            words = []
        self.representation = representation
        self.is_terminal = is_terminal
        self.words = words
