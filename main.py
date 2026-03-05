from grammar import Grammar
from finite_automaton import FiniteAutomaton
from visualize import draw_automaton


def main():
    # ---- Lab 1 ----
    # Variant 21 (Grammar)
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
    fa_from_grammar = grammar.to_finite_automaton()
    print(f"\nFinite Automaton (from grammar):")
    print(f"  States:        {fa_from_grammar.states}")
    print(f"  Alphabet:      {fa_from_grammar.alphabet}")
    print(f"  Start state:   {fa_from_grammar.start_state}")
    print(f"  Accept states: {fa_from_grammar.accept_states}")
    print(f"  Transitions:")
    for (state, symbol), targets in sorted(fa_from_grammar.transitions.items()):
        print(f"    δ({state}, {symbol}) = {targets}")

    # (d) Test strings against the finite automaton
    lab1_test_strings = ["ab", "aab", "aabab", "abab", "abc", "aaba", "aabda", "abcab"]
    print("\nString validation via Finite Automaton:")
    for s in lab1_test_strings:
        result = fa_from_grammar.string_belongs_to_language(s)
        print(f"  '{s}' -> {'accepted' if result else 'rejected'}")

    # ---- Lab 2 ----
    print("\n" + "=" * 60)
    print("LAB 2")
    print("=" * 60)

    # 1. Classify the grammar based on Chomsky hierarchy (Lab 1 grammar)
    chomsky_type = grammar.classify_chomsky()
    print(f"\n1. Chomsky classification of Lab 1 grammar: {chomsky_type}")

    # Variant 21 (Finite Automaton)
    # Q = {q0, q1, q2, q3}, Σ = {a, b, c}, F = {q3}
    # δ(q0,a) = q0, δ(q0,a) = q1, δ(q1,b) = q2,
    # δ(q2,c) = q3, δ(q3,c) = q3, δ(q2,a) = q2
    fa = FiniteAutomaton(
        states={"q0", "q1", "q2", "q3"},
        alphabet={"a", "b", "c"},
        transitions={
            ("q0", "a"): {"q0", "q1"},
            ("q1", "b"): {"q2"},
            ("q2", "c"): {"q3"},
            ("q3", "c"): {"q3"},
            ("q2", "a"): {"q2"},
        },
        start_state="q0",
        accept_states={"q3"},
    )

    print(f"\nVariant 21 Finite Automaton:")
    print(f"  States:        {fa.states}")
    print(f"  Alphabet:      {fa.alphabet}")
    print(f"  Start state:   {fa.start_state}")
    print(f"  Accept states: {fa.accept_states}")
    print(f"  Transitions:")
    for (state, symbol), targets in sorted(fa.transitions.items()):
        print(f"    δ({state}, {symbol}) = {targets}")

    # 2a. FA to regular grammar conversion
    rg = fa.to_regular_grammar()
    print(f"\n2a. FA → Regular Grammar conversion:")
    print(f"  V_N = {rg.vn}")
    print(f"  V_T = {rg.vt}")
    print(f"  Start = {rg.start_symbol}")
    print(f"  Productions:")
    for lhs, rhs_list in sorted(rg.productions.items()):
        for rhs in rhs_list:
            print(f"    {lhs} → {rhs}")

    # 2b. Determine if the FA is deterministic or non-deterministic
    det = fa.is_deterministic()
    print(f"\n2b. Is the FA deterministic? {'Yes (DFA)' if det else 'No (NFA)'}")

    # 2c. Convert NFA to DFA
    if not det:
        dfa = fa.to_dfa()
        print(f"\n2c. NFA → DFA conversion:")
        print(f"  States:        {dfa.states}")
        print(f"  Alphabet:      {dfa.alphabet}")
        print(f"  Start state:   {dfa.start_state}")
        print(f"  Accept states: {dfa.accept_states}")
        print(f"  Transitions:")
        for (state, symbol), targets in sorted(dfa.transitions.items()):
            print(f"    δ({state}, {symbol}) = {targets}")

        print(f"\n  Is the converted FA deterministic? "
              f"{'Yes (DFA)' if dfa.is_deterministic() else 'No (NFA)'}")

        # Verify DFA accepts the same strings as the NFA
        test_strings = ["abc", "aabc", "abaac", "abcc", "abaccc",
                        "ab", "aac", "bc", "b", "abcb"]
        print(f"\n  Verification (DFA should match NFA results):")
        for s in test_strings:
            nfa_result = fa.string_belongs_to_language(s)
            dfa_result = dfa.string_belongs_to_language(s)
            match = "✓" if nfa_result == dfa_result else "✗ MISMATCH"
            print(f"    '{s}' -> NFA={'accepted' if nfa_result else 'rejected'}, "
                  f"DFA={'accepted' if dfa_result else 'rejected'} {match}")

    # 2d. Visualize the finite automaton graphically
    print(f"\n2d. Graphical representation:")
    draw_automaton(fa, "NFA (Variant 21)", "nfa_graph")
    if not det:
        draw_automaton(dfa, "DFA (Variant 21)", "dfa_graph")


if __name__ == "__main__":
    main()
