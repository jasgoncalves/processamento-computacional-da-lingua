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
        self.charts = [Chart() for _ in self.sentence]

    def parse(self):
        self.create_initial_state()

        for index, value in enumerate(self.sentence):
            for state in self.charts[index].states:
                if not state.is_complete():
                    if not state.next_constituent().is_terminal:
                        self.predictor(state, index, grammar)
                    else:
                        self.scanner(state, index)
                else:
                    self.completer(state, index)

    def create_initial_state(self):
        initial_rule = Rule(Constituent("ROOT", True), [Constituent("S", False)])
        initial_state = State(initial_rule, (0, 0))
        self.charts[0].enqueue_state(initial_state)

    def predictor(self, state: State, index: int, grammar: Grammar):
        chart = self.charts[index]
        next_constituent = state.next_constituent()
        rules = grammar.get_syntactic_rules_by_constituent(next_constituent)
        for rule in rules:
            if not chart.has_rule(rule):
                new_state = State(rule, (index, index))
                chart.enqueue_state(new_state)

    def scanner(self, state: State, index: int):
        pass

    def completer(self, state: State, index: int):
        pass


if __name__ == "__main__":
    grammar = Grammar(GRAMMAR_PATH, TERMINALS, NON_TERMINALS)
    grammar.create_lexical_grammar()
    grammar.generate_syntactic_grammar()
    earley = Earley("A infalibilidade papal é um dogma", grammar)
    earley.parse()
