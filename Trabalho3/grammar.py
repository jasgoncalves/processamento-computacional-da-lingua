from typing import List

from rule import Rule


class Grammar:
    def __init__(self, rules: List[Rule] = None):
        if rules is None:
            rules = []
        self.rules = rules

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
