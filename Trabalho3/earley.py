import copy
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
        self.sentence = sentence.lower().split(" ")
        self.grammar = grammar
        self.charts = [Chart() for _ in self.sentence]
        self.charts.append(Chart())

    def parse(self):
        self.create_initial_state()

        for index in range(0, len(self.sentence)):
            for state in self.charts[index].states:
                if not state.is_complete():
                    if not state.next_constituent().is_terminal:
                        self.predictor(state, index, grammar)
                    else:
                        self.scanner(state, index)
                else:
                    self.completer(state, index)

        print("abc")

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
        next_chart = self.charts[index + 1]
        next_constituent = state.next_constituent()
        if self.sentence[index] in next_constituent.words:
            word_constituent = Constituent(self.sentence[index], True)
            new_rule = Rule(next_constituent, [word_constituent], 1)
            new_state = State(new_rule, (index, index + 1))
            if not next_chart.has_rule(new_rule):
                next_chart.enqueue_state(new_state)

    def completer(self, state: State, index: int):
        prev_chart = self.charts[state.position[0]]
        curr_chart = self.charts[index]
        final_constituent = state.final_constituent()
        for old_state in prev_chart.states:
            if old_state.is_awaiting_constituent(final_constituent):
                old_rule = old_state.rule
                new_rule = Rule(old_rule.left_hs, old_rule.right_hs, old_rule.current_state + 1)
                new_backpointer = copy.deepcopy(old_state.backpointer)
                new_backpointer.append(state)
                new_state = State(new_rule, (old_state.position[0], index), new_backpointer)
                curr_chart.enqueue_state(new_state)


if __name__ == "__main__":
    grammar = Grammar(GRAMMAR_PATH, TERMINALS, NON_TERMINALS)
    grammar.create_lexical_grammar()
    grammar.generate_syntactic_grammar()
    earley = Earley("A infalibilidade papal é um dogma", grammar)
    earley.parse()
