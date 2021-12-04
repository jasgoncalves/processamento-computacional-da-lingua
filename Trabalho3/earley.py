import os
from typing import List

import chardet
import pandas as pd
from pandas import isna

from rule import Rule
from grammar import Grammar
from constituent import Constituent

PROJECT_PATH = os.path.dirname("Trabalho3")
GRAMMAR_PATH = os.path.join(PROJECT_PATH, "grammar.txt")
COLUMNS = ["lhs", "sep", "param0", "param1", "param2"]
NON_TERMINALS = ["S", "NP", "VP", "PP"]
TERMINALS = ["Art", "Noun", "Prep", "Verb", "Adj"]


def read_grammar(path: str) -> pd.DataFrame:
    with open(path, 'rb') as f:
        enc = chardet.detect(f.read())
    return pd.read_csv(path, sep='\t', names=COLUMNS, encoding=enc['encoding'])


def get_constituent(consts: List[Constituent], representation: str) -> Constituent:
    for const in consts:
        if const.representation.__eq__(representation):
            return const


def create_lexical_grammar(grammar_df: pd.DataFrame) -> List[Constituent]:
    term_constituents = []
    for representation in TERMINALS:
        curr_const = Constituent(representation, True)
        term_constituents.append(curr_const)

    for index, row in grammar_df.iterrows():
        if row.lhs in TERMINALS:
            get_constituent(term_constituents, row.lhs).words.append(row.param0)

    return term_constituents


def create_syntactic_grammar(grammar_df: pd.DataFrame, lexical_grammar: List[Constituent]) -> Grammar:
    curr_grammar = Grammar()
    for index, row in grammar_df.iterrows():
        if row.lhs not in TERMINALS:
            lhs_const = Constituent(row.lhs, row.lhs in TERMINALS)
            rhs_const = []
            for param in COLUMNS[2:]:
                if not isna(row[param]):
                    is_terminal_curr = row[param] in TERMINALS
                    if is_terminal_curr:
                        curr_const = get_constituent(lexical_grammar, row[param])
                    else:
                        curr_const = Constituent(row[param], row[param] in TERMINALS)
                    rhs_const.append(curr_const)

            current_rule = Rule(lhs_const, rhs_const)
            curr_grammar.add_rule(current_rule)

    return curr_grammar


if __name__ == "__main__":
    df_grammar = read_grammar(GRAMMAR_PATH)
    lexical_grammar = create_lexical_grammar(df_grammar)
    syntactic_grammar = create_syntactic_grammar(df_grammar, lexical_grammar)
