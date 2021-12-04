import os
from grammar import Grammar


PROJECT_PATH = os.path.dirname("Trabalho3")
GRAMMAR_PATH = os.path.join(PROJECT_PATH, "grammar.txt")
NON_TERMINALS = ["S", "NP", "VP", "PP"]
TERMINALS = ["Art", "Noun", "Prep", "Verb", "Adj"]


class Early:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar


if __name__ == "__main__":
    grammar = Grammar(GRAMMAR_PATH, TERMINALS, NON_TERMINALS)
    grammar.create_lexical_grammar()
    grammar.generate_syntactic_grammar()
