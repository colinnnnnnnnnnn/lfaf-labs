# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Poiata Calin

----

## Theory
Parsing, or syntactic analysis, is a subsequent stage after lexical analysis in a typical compiler or interpreter pipeline. While lexical analysis focuses on grouping raw text characters into meaningful symbols (tokens), parsing takes those flat tokens and structures them hierarchically based on the grammatical rules of the target language. By reading the sequence of tokens, a parser verifies whether the given program is syntactically valid.

As the parser makes sense of the internal structure, it typically shapes an Abstract Syntax Tree (AST). An Abstract Syntax Tree is a rich data structure that preserves the essential relationships and meaning of the code while explicitly discarding unnecessary syntactical noise like parentheses or semicolons. The layers of the AST directly mimic the abstraction constructs forming the code—for example, root nodes representing entire programs which branch out into statements, expressions, operator nodes, and terminal literals. Producing a properly formulated AST is a critical step because it provides the operational map that semantic analyzers, optimizers, or evaluators use to actually process or run the code.

## Objectives:
1. Get familiar with parsing, what it is, and how it can be programmed.
2. Get familiar with the concept of Abstract Syntax Trees (AST).
3. In addition to what has been done in the 3rd laboratory work, fulfill the following requirements:
   - Have a `TokenType` enumeration denoting possible types of tokens utilized in lexical analysis.
   - Use regular expressions natively to identify token types during extraction.
   - Implement the necessary data structures to form an AST mapped onto the text processed in the previous lexer work.
   - Implement a functional parsing mechanism capable of extracting and storing syntactic information from the text inside the AST.

## Implementation description

This laboratory builds upon the lexical concepts explored previously by integrating a robust recursive descent parser. To conform to the updated objectives, the lexical analyzer was first refactored. Rather than maintaining manual text-pointer mechanisms, the tokens are now processed comprehensively using regular expressions.

### The Regex Lexer
The updated system employs an enumeration grouping the regular expression patterns describing everything from alphanumeric variables to explicit keywords and operands. The `Lexer` dynamically builds a master regular expression string from the enumeration and matches groups iteratively directly over the source code.

```python
class TokenType(Enum):
    LET = r'\blet\b'
    PRINT = r'\bprint\b'
    FLOAT = r'\d+\.\d+'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #...
```
This simplifies the engine tremendously. The token sequence is then submitted directly to the parser.

### The Abstract Syntax Tree (AST)

An effective parser requires destinations for the identified components. The `AST.py` file encompasses all fundamental nodes inheriting from a common base interface. I categorized nodes essentially as either Statements or Expressions. Statements typically include blocks of logic that do not return direct values (like `print` statements or `let` assignments). Conversely, Expressions compute to values (such as literals, mathematical operations, or identifiers).

Each node within the tree defines two primary features:
- A string representation method that recursively formats its children to reconstruct readable text equivalents.
- A serialization mechanic `to_dict` that dumps nested nodes into a dictionary schema easily printed as a JSON tree.

This makes debugging the syntax structure very visual and direct.

### Recursive Descent Parser

The `Parser` orchestrates the logic relying on predicting precedence. Working as a classic recursive descent model, it reads tokens left-to-right. Using tracking pointers referencing both the `current_token` and the upcoming `peek_token`, the script categorizes instructions intelligently.

For instance, when reading a statement, if the token recognizes the keyword `let`, the specific method `parse_let_statement()` takes over to expect a mandatory identifier natively mapped to an assignment.
Expressions prove slightly more complex since they inherently rely on correct mathematical precedence. The parser associates ranks (such as `LOWEST`, `SUM`, `PRODUCT`) and leverages the Pratt parsing technique to determine if loops should absorb incoming tokens into deep branches (like multiplication taking priority over addition). A typical check involves:

```python
while self.peek_token and self.peek_token.type != 'SEMICOLON' and precedence < self.peek_precedence():
    if self.peek_token.type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUALS'):
        self.advance()
        left_node = self.parse_infix_expression(left_node)
```
Ultimately, the mechanism constructs parent nodes mapping their operands iteratively. 

## Conclusions / Results

Through this laboratory work, I developed a deeper understanding of compiler front-ends, graduating from static lexical scanning to full-fledged grammatical evaluation. Rewriting the scanner using pure regular expressions minimized code footprint massively while allowing the structure to feel declarative rather than imperative.

Furthermore, integrating Pratt parsing alongside recursive statement extraction handled nested complexity elegantly. The algorithm gracefully structured conditional blocks containing print nodes, properly segregated variables, and maintained standard mathematical precedences effectively natively storing them into the crafted object-oriented AST representation. Testing the parser with operations involving logical equality tests and bundled functional calls returned exactly formatted JSON data reflecting the exact hierarchical layout.