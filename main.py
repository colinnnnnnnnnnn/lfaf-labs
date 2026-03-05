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
    strings = []
    i = 1
    while i < 6:
        string = grammar.generate_string()
        if string in strings:
            i -= 1
        else:
            strings.append(string)
            print(f"  {i}. {string}")
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

    # ---- Lab 2 ----
    print("\n" + "=" * 60)
    print("LAB 2")
    print("=" * 60)

    # 1. Classify the grammar based on Chomsky hierarchy
    chomsky_type = grammar.classify_chomsky()
    print(f"\n1. Chomsky classification: {chomsky_type}")

    # 2. FA to regular grammar conversion
    rg = fa.to_regular_grammar()
    print(f"\n2. FA → Regular Grammar conversion:")
    print(f"  V_N = {rg.vn}")
    print(f"  V_T = {rg.vt}")
    print(f"  Start = {rg.start_symbol}")
    print(f"  Productions:")
    for lhs, rhs_list in sorted(rg.productions.items()):
        for rhs in rhs_list:
            print(f"    {lhs} → {rhs}")

    # 3. Determine if the FA is deterministic or non-deterministic
    det = fa.is_deterministic()
    print(f"\n3. Is the FA deterministic? {'Yes (DFA)' if det else 'No (NFA)'}")

    # 4. Convert NFA to DFA
    if not det:
        dfa = fa.to_dfa()
        print(f"\n4. NFA → DFA conversion:")
        print(f"  States:        {dfa.states}")
        print(f"  Alphabet:      {dfa.alphabet}")
        print(f"  Start state:   {dfa.start_state}")
        print(f"  Accept states: {dfa.accept_states}")
        print(f"  Transitions:")
        for (state, symbol), targets in sorted(dfa.transitions.items()):
            print(f"    δ({state}, {symbol}) = {targets}")

        print(f"\n  Is the converted FA deterministic? "
              f"{'Yes (DFA)' if dfa.is_deterministic() else 'No (NFA)'}")

        # Verify DFA accepts the same strings
        print(f"\n  Verification (DFA should match NFA results):")
        for s in test_strings:
            nfa_result = fa.string_belongs_to_language(s)
            dfa_result = dfa.string_belongs_to_language(s)
            match = "✓" if nfa_result == dfa_result else "✗ MISMATCH"
            print(f"    '{s}' -> NFA={'accepted' if nfa_result else 'rejected'}, "
                  f"DFA={'accepted' if dfa_result else 'rejected'} {match}")


if __name__ == "__main__":
    main()
