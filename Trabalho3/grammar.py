from typing import List

import chardet
import pandas as pd

from Trabalho3.constituent import Constituent
from rule import Rule

COLUMNS = ["lhs", "sep", "param0", "param1", "param2"]


def read_grammar(path: str) -> pd.DataFrame:
    with open(path, 'rb') as f:
        enc = chardet.detect(f.read())
    return pd.read_csv(path, sep='\t', names=COLUMNS, encoding=enc['encoding'])


class Grammar:
    def __init__(self, grammar_path: str, terminals: List[str], non_terminals: List[str], rules: List[Rule] = None, lexical_rules: List[Constituent] = None):
        self.non_terminals = non_terminals
        self.terminals = terminals
        if rules is None:
            rules = []
        if lexical_rules is None:
            lexical_rules = []
        self.dataframe = read_grammar(grammar_path)
        self.rules = rules
        self.lexical_rules = lexical_rules

    def get_lexical_rule_by_constituent(self, representation: str) -> Constituent:
        for const in self.lexical_rules:
            if const.representation.__eq__(representation):
                return const

    def create_lexical_grammar(self):
        for representation in self.terminals:
            curr_const = Constituent(representation, True)
            self.lexical_rules.append(curr_const)

        for index, row in self.dataframe.iterrows():
            if row.lhs in self.terminals:
                self.get_lexical_rule_by_constituent(row.lhs).words.append(row.param0)

    def generate_syntactic_grammar(self):
        for index, row in self.dataframe.iterrows():
            if row.lhs not in self.terminals:
                lhs_const = Constituent(row.lhs, row.lhs in self.terminals)
                rhs_const = []
                for param in COLUMNS[2:]:
                    if not pd.isna(row[param]):
                        is_terminal_curr = row[param] in self.terminals
                        if is_terminal_curr:
                            curr_const = self.get_lexical_rule_by_constituent(row[param])
                        else:
                            curr_const = Constituent(row[param], row[param] in self.terminals)
                        rhs_const.append(curr_const)

                self.rules.append(Rule(lhs_const, rhs_const))
