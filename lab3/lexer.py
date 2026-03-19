from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Single-character symbols
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    CARET = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    ASSIGN = auto()

    # Literals and names
    NUMBER = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    value: int | float | str | None = None


class LexerError(ValueError):
    pass


class Lexer:
    """A small scanner that tokenizes arithmetic-like input with sin/cos support."""

    _SINGLE_CHAR_TOKENS: dict[str, TokenType] = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "^": TokenType.CARET,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ",": TokenType.COMMA,
        "=": TokenType.ASSIGN,
    }

    _FUNCTIONS = {"sin", "cos"}

    def __init__(self, source: str) -> None:
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while not self._is_at_end():
            token = self._scan_token()
            if token is not None:
                tokens.append(token)
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _scan_token(self) -> Token | None:
        ch = self._peek()

        if ch in " \t\r":
            self._advance()
            return None

        if ch == "\n":
            self._advance()
            self.line += 1
            self.column = 1
            return None

        # Python-style comments are ignored until end-of-line.
        if ch == "#":
            while not self._is_at_end() and self._peek() != "\n":
                self._advance()
            return None

        if ch in self._SINGLE_CHAR_TOKENS:
            start_line, start_col = self.line, self.column
            lexeme = self._advance()
            return Token(self._SINGLE_CHAR_TOKENS[lexeme], lexeme, start_line, start_col)

        if ch.isdigit() or (ch == "." and self._peek_next().isdigit()):
            return self._number()

        if ch.isalpha() or ch == "_":
            return self._identifier_or_function()

        raise LexerError(f"Unexpected character {ch!r} at line {self.line}, column {self.column}")

    def _number(self) -> Token:
        start = self.index
        start_line, start_col = self.line, self.column

        while self._peek().isdigit():
            self._advance()

        is_float = False
        if self._peek() == ".":
            is_float = True
            self._advance()
            if not self._peek().isdigit():
                raise LexerError(
                    f"Malformed float literal at line {start_line}, column {start_col}"
                )
            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[start : self.index]
        value: int | float = float(lexeme) if is_float else int(lexeme)
        return Token(TokenType.NUMBER, lexeme, start_line, start_col, value)

    def _identifier_or_function(self) -> Token:
        start = self.index
        start_line, start_col = self.line, self.column

        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        lexeme = self.source[start : self.index]
        if lexeme in self._FUNCTIONS:
            return Token(TokenType.FUNCTION, lexeme, start_line, start_col, lexeme)
        return Token(TokenType.IDENTIFIER, lexeme, start_line, start_col, lexeme)

    def _advance(self) -> str:
        ch = self.source[self.index]
        self.index += 1
        self.column += 1
        return ch

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.index]

    def _peek_next(self) -> str:
        next_index = self.index + 1
        if next_index >= self.length:
            return "\0"
        return self.source[next_index]

    def _is_at_end(self) -> bool:
        return self.index >= self.length
