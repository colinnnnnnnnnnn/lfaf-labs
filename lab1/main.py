from grammar import Grammar


def main():
    # Variant 21
    vn = {"S", "B", "C", "D"}
    vt = {"a", "b", "c"}
    productions = {
        "S": ["aB"],
        "B": ["bS", "aC", "b"],
        "C": ["bD"],
        "D": ["a", "bC", "cS"],
    }
    start_symbol = "S"

    grammar = Grammar(vn, vt, productions, start_symbol)

    # (b) Generate 5 valid strings
    print("5 valid strings generated from the grammar:")
    words = []
    i = 1
    while i < 6:
        word = grammar.generate_string()
        if word in words:
            i -= 1
        else:
            words.append(word)
            print(f"  {i}. {word}")
        i += 1

    # (c) Convert grammar to finite automaton
    fa = grammar.to_finite_automaton()
    print(f"\nFinite Automaton:")
    print(f"  States:        {fa.states}")
    print(f"  Alphabet:      {fa.alphabet}")
    print(f"  Start state:   {fa.start_state}")
    print(f"  Accept states: {fa.accept_states}")
    print(f"  Transitions:")
    for (state, symbol), targets in sorted(fa.transitions.items()):
        print(f"    δ({state}, {symbol}) = {targets}")

    # (d) Test strings against the finite automaton
    test_strings = ["ab", "aab", "aabab", "abab", "abc", "aaba", "aabda", "abcab"]
    print("\nString validation via Finite Automaton:")
    for s in test_strings:
        result = fa.string_belongs_to_language(s)
        print(f"  '{s}' -> {'accepted' if result else 'rejected'}")


if __name__ == "__main__":
    main()
