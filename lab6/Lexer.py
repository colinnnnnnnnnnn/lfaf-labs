from enum import Enum
import re

class TokenType(Enum):
    LET = r'\blet\b'
    PRINT = r'\bprint\b'
    SIN = r'\bsin\b'
    COS = r'\bcos\b'
    IF = r'\bif\b'
    ELSE = r'\belse\b'
    FLOAT = r'\d+\.\d+'
    INTEGER = r'\d+'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'"[^"]*"'
    EQUALS = r'=='
    ASSIGN = r'='
    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    SEMICOLON = r';'
    COMMA = r','
    WHITESPACE = r'[ \t\n\r]+'
    ILLEGAL = r'.'

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        # Combine all regexes into a single master regex
        parts = []
        for token_type in TokenType:
            parts.append(f'(?P<{token_type.name}>{token_type.value})')
        self.master_regex = re.compile('|'.join(parts))

    def tokenize(self):
        tokens = []
        for match in self.master_regex.finditer(self.source_code):
            type_name = match.lastgroup
            value = match.group(type_name)
            if type_name == 'WHITESPACE':
                continue
            if type_name == 'STRING':
                value = value[1:-1] # Remove quotes
            tokens.append(Token(type_name, value))
        tokens.append(Token('EOF', ''))
        return tokens
