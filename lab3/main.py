from __future__ import annotations

import sys

from lexer import Lexer, LexerError


def print_tokens(source: str) -> None:
    print("Input:")
    print(source)
    print("\nTokens:")

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    header = f"{'TYPE':<12} {'LEXEME':<10} {'VALUE':<10} {'POS':<8}"
    print(header)
    print("-" * len(header))
    for token in tokens:
        value = "" if token.value is None else str(token.value)
        pos = f"{token.line}:{token.column}"
        print(f"{token.type.name:<12} {token.lexeme:<10} {value:<10} {pos:<8}")


def run_demo() -> None:
    sample = """
result = sin(90) + cos(0) - 3.14 * radius^2 + value_1 / 2
# This line is a comment and will be ignored by the lexer
next_value = sin(0.5) + cos(1)
""".strip()
    print_tokens(sample)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        try:
            print_tokens(input_text)
        except LexerError as exc:
            print(f"Lexer error: {exc}")
            raise SystemExit(1)
    else:
        try:
            run_demo()
        except LexerError as exc:
            print(f"Lexer error: {exc}")
            raise SystemExit(1)
