import json
from Lexer import Lexer
from Parser import Parser

def main():
    print("--- Formal Languages & Finite Automata ---")
    print("--- Lab 6: Parser & Abstract Syntax Tree ---\n")

    test_source_code = """
    let x = 10;
    let y = 20.5;
    
    let result = sin(x) + cos(y) * 3.14;
    
    if (result == 0) {
        print("Trigonometry is amazing!");
    } else {
        print("Math goes wrong here:");
        print(result);
    }
    """

    print("Source Code to Parse:")
    print("-" * 40)
    print(test_source_code)
    print("-" * 40)

    print("\nStarting Lexical Analysis using Regex...")
    lexer = Lexer(test_source_code)
    tokens = lexer.tokenize()
    print(f"Generated {len(tokens)} tokens.")

    print("\nStarting Parsing Process...")
    parser = Parser(tokens)
    
    try:
        ast = parser.parse_program()
        print("Parsing completed successfully!\n")
        
        print("Generated Abstract Syntax Tree (String Representation):")
        print("-" * 40)
        print(str(ast))
        print("-" * 40)
        
        print("\nGenerated Abstract Syntax Tree (JSON Representation):")
        print("-" * 40)
        print(json.dumps(ast.to_dict(), indent=2))
        print("-" * 40)
        
    except Exception as e:
        print(f"\nParsing Failed: {e}")

if __name__ == "__main__":
    main()
