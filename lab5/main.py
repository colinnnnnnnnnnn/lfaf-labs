from __future__ import annotations

import argparse
from pathlib import Path

from cnf_grammar import CFG

def _parse_set_line(content: str, expected_key: str) -> set[str]:
    key, value = content.split("=", maxsplit=1)
    if key.strip().lower() != expected_key.lower():
        raise ValueError(f"Expected '{expected_key}=...', got '{content}'")
    return {token.strip() for token in value.split(",") if token.strip()}


def load_grammar_from_file(path: str) -> CFG:
    """
    File format:
      VN=S,A,B,C,D
      VT=a,b,d
      S=S
      P:
      S->dB
      S->AC
      A->d
      A->dS
      A->aBdB
      B->a
      B->aA
      B->AC
      D->ab
      C->bC
      C->ε
    """
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f]

    lines = [line for line in raw_lines if line and not line.startswith("#")]
    if len(lines) < 4:
        raise ValueError("Grammar file is too short. Expected VN, VT, S, and productions.")

    vn = _parse_set_line(lines[0], "VN")
    vt = _parse_set_line(lines[1], "VT")

    s_key, s_value = lines[2].split("=", maxsplit=1)
    if s_key.strip().lower() != "s":
        raise ValueError("Expected start symbol line in format 'S=<nonterminal>'")
    start_symbol = s_value.strip()

    productions_start = 3
    if lines[3].lower() == "p:" or lines[3].lower() == "p":
        productions_start = 4

    rules = lines[productions_start:]
    if not rules:
        raise ValueError("No production rules found in grammar file.")

    return CFG.from_rules(vn, vt, start_symbol, rules)


def run_pipeline(grammar: CFG) -> CFG:
    print(grammar.pretty("Initial Grammar"))
    print()

    step_1 = grammar.eliminate_epsilon_productions()
    print(step_1.pretty("1) After eliminating epsilon productions"))
    print()

    step_2 = step_1.eliminate_unit_productions()
    print(step_2.pretty("2) After eliminating unit (renaming) productions"))
    print()

    step_3 = step_2.eliminate_inaccessible_symbols()
    print(step_3.pretty("3) After eliminating inaccessible symbols"))
    print()

    step_4 = step_3.eliminate_non_productive_symbols()
    print(step_4.pretty("4) After eliminating non-productive symbols"))
    print()

    step_5 = step_4.to_chomsky_normal_form()
    print(step_5.pretty("5) Chomsky Normal Form"))
    print()

    print(f"CNF validation: {step_5.is_cnf()}")
    return step_5


if __name__ == "__main__":
    default_input = Path(__file__).with_name("variant21_grammar.txt")

    parser = argparse.ArgumentParser(
        description="Normalize a CFG to Chomsky Normal Form (CNF)."
    )
    parser.add_argument(
        "--input",
        "-i",
        default=str(default_input),
        help=(
            "Path to a grammar file. "
            "Defaults to lab5/variant21_grammar.txt."
        ),
    )
    args = parser.parse_args()

    grammar = load_grammar_from_file(args.input)
    final_grammar = run_pipeline(grammar)
    if not final_grammar.is_cnf():
        raise SystemExit("Resulting grammar is not in CNF.")
