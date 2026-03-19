# Lexer and Scanner. Lexical Analysis.

### Course: Formal Languages & Finite Automata
### Author: Poiata Calin

----

## Theory

Lexical analysis is one of the first stages of language processing in a compiler or interpreter. A lexer (also called scanner or tokenizer) reads a stream of characters and groups them into meaningful units.

A **lexeme** is the exact text fragment extracted from the input (for example, `sin`, `3.14`, `+`). A **token** is the categorized representation of that lexeme (for example, `FUNCTION`, `NUMBER`, `PLUS`) and may also store metadata such as numeric value and source position.

The output of lexical analysis is a token stream, which is then consumed by later phases (usually parsing and semantic analysis).


## Objectives

* Understand how lexical analysis works.
* Implement a lexer/scanner/tokenizer in Python.
* Go beyond a minimal calculator by supporting integers, floats, and trigonometric functions (`sin`, `cos`).
* Demonstrate the lexer on realistic input and show the produced token stream.


## Implementation Description

### Token Model

The implementation defines a `TokenType` enum and a `Token` dataclass.

Token categories:

* Single-character tokens: `PLUS`, `MINUS`, `STAR`, `SLASH`, `CARET`, `LPAREN`, `RPAREN`, `COMMA`, `ASSIGN`
* Value-bearing tokens: `NUMBER`, `IDENTIFIER`, `FUNCTION`
* End marker: `EOF`

Each token stores:

* `type`
* `lexeme`
* `line`
* `column`
* optional `value` (`int`, `float`, `str`, or `None`)


### Lexer Class

The `Lexer` scans the input from left to right while maintaining:

* current index in the source
* current line
* current column

Core behavior:

* Skips spaces, tabs, carriage returns, and newlines.
* Ignores comments that start with `#` and continue to end-of-line.
* Emits tokens for operators and separators.
* Parses numbers as:
  * integer (`90`, `2`)
  * float (`3.14`, `0.5`)
* Parses names (`result`, `value_1`, `radius`):
  * classified as `FUNCTION` if lexeme is `sin` or `cos`
  * otherwise classified as `IDENTIFIER`
* Raises `LexerError` for invalid characters or malformed numeric literals.
* Appends an explicit `EOF` token at the end.


### Number Scanning Details

Number scanning supports:

* integer form: one or more digits
* float form: digits `.` digits
* leading-dot floats like `.5`

Malformed literals (for example `12.`) trigger a clear lexical error.


### Runner / Demonstration

The `main.py` file demonstrates the lexer in two modes:

* **Default demo mode** (no arguments): tokenizes a multiline sample containing assignments, identifiers, integers, floats, `sin`, `cos`, arithmetic operators, and a comment line.
* **CLI mode** (with arguments): tokenizes the provided custom expression.

The output is printed in a table with token type, lexeme, parsed value, and source position (`line:column`).


## Source Files

* `lexer.py` - token definitions, `LexerError`, and `Lexer` implementation.
* `main.py` - demo and command-line runner.
* `README.md` - short project guide and usage instructions.


## Program Output (Sample Run)

Command used:

```bash
python3 main.py
```

Observed output:

```text
Input:
result = sin(90) + cos(0) - 3.14 * radius^2 + value_1 / 2
# This line is a comment and will be ignored by the lexer
next_value = sin(0.5) + cos(1)

Tokens:
TYPE         LEXEME     VALUE      POS
-------------------------------------------
IDENTIFIER   result     result     1:1
ASSIGN       =                     1:8
FUNCTION     sin        sin        1:10
LPAREN       (                     1:13
NUMBER       90         90         1:14
RPAREN       )                     1:16
PLUS         +                     1:18
FUNCTION     cos        cos        1:20
LPAREN       (                     1:23
NUMBER       0          0          1:24
RPAREN       )                     1:25
MINUS        -                     1:27
NUMBER       3.14       3.14       1:29
STAR         *                     1:34
IDENTIFIER   radius     radius     1:36
CARET        ^                     1:42
NUMBER       2          2          1:43
PLUS         +                     1:45
IDENTIFIER   value_1    value_1    1:47
SLASH        /                     1:55
NUMBER       2          2          1:57
IDENTIFIER   next_value next_value 3:1
ASSIGN       =                     3:12
FUNCTION     sin        sin        3:14
LPAREN       (                     3:17
NUMBER       0.5        0.5        3:18
RPAREN       )                     3:21
PLUS         +                     3:23
FUNCTION     cos        cos        3:25
LPAREN       (                     3:28
NUMBER       1          1          3:29
RPAREN       )                     3:30
EOF                                3:31
```


## Conclusions

The implemented scanner successfully performs lexical analysis for a small expression language that is more complex than a basic calculator. It correctly recognizes integers, floating-point numbers, identifiers, arithmetic symbols, assignment, and trigonometric functions (`sin`, `cos`), while also tracking source positions and ignoring comments.

This confirms the main objective of the lab: transforming raw character input into a structured stream of tokens suitable for the next compiler/interpreter phase.