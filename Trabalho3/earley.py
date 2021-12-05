import os

from constituent import Constituent
from rule import Rule
from state import State
from chart import Chart
from grammar import Grammar


PROJECT_PATH = os.path.dirname("Trabalho3")
GRAMMAR_PATH = os.path.join(PROJECT_PATH, "grammar.txt")
NON_TERMINALS = ["S", "NP", "VP", "PP"]
TERMINALS = ["Art", "Noun", "Prep", "Verb", "Adj"]


class Earley:
    def __init__(self, sentence: str, grammar: Grammar):
        self.sentence = sentence.split(" ")
        self.grammar = grammar
        self.charts = []
        self.charts.append(Chart())

    def parse(self):
        self.create_initial_state()

    def create_initial_state(self):
        initial_rule = Rule(Constituent("ROOT", True), [Constituent("S", False)])
        initial_state = State(initial_rule, (0, 0))
        self.charts[0].enqueue_state(initial_state)


if __name__ == "__main__":
    grammar = Grammar(GRAMMAR_PATH, TERMINALS, NON_TERMINALS)
    grammar.create_lexical_grammar()
    grammar.generate_syntactic_grammar()
    earley = Earley("A infalibilidade papal é um dogma", grammar)
    earley.parse()
