# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Poiata Calin

----

## Theory

A **formal grammar** is a set of rules that describe how to form valid strings in a language. It is defined by four components: a set of non-terminal symbols (V_N), a set of terminal symbols (V_T), a set of production rules (P), and a start symbol (S). A **regular grammar** is a special case in which every production rule has at most one non-terminal on the right-hand side, and it always appears at the end (right-linear grammar). This type of grammar is equivalent in expressive power to a **finite automaton** (FA). A finite automaton is a state machine defined by states (Q), an input alphabet (Σ), a transition function (δ), a start state (q₀), and a set of accept states (F). It reads an input string one character at a time and either accepts or rejects it based on whether it ends in an accept state. The equivalence between regular grammars and finite automata means any language described by one can be recognized by the other.


## Objectives:

* Implement a class for the given grammar (Variant 21) that stores V_N, V_T, P, and S.
* Add a method to generate 5 valid strings from the language expressed by the grammar.
* Implement functionality to convert a Grammar object into a Finite Automaton object.
* Add a method to the Finite Automaton that checks whether an input string belongs to the language.


## Implementation description

### Grammar Class

The `Grammar` class stores the non-terminal symbols, terminal symbols, production rules, and start symbol. It provides a `generate_string()` method that begins from the start symbol and recursively expands non-terminals by randomly choosing among available production rules until only terminal symbols remain. The private `_expand()` helper handles the recursion: if the symbol is a terminal it returns it directly, otherwise it picks a random production and expands each character in the right-hand side.

```python
class Grammar:
    def __init__(self, vn, vt, productions, start_symbol):
        self.vn = vn
        self.vt = vt
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        result = self._expand(self.start_symbol)
        return result

    def _expand(self, symbol):
        if symbol in self.vt:
            return symbol
        if symbol not in self.productions:
            return symbol
        rhs = random.choice(self.productions[symbol])
        result = ""
        for ch in rhs:
            result += self._expand(ch)
        return result
```

### Grammar to Finite Automaton Conversion

The `to_finite_automaton()` method converts the regular grammar into a finite automaton. Each non-terminal becomes a state, plus an extra accept state `X` is introduced. For each production of the form `A → aB` (terminal followed by non-terminal), a transition δ(A, a) → B is created. For each production of the form `A → a` (terminal only), a transition δ(A, a) → X is created, since the derivation terminates. The `setdefault` method ensures that when multiple rules produce transitions on the same (state, symbol) pair (e.g., `B → bS` and `B → b` both on input `b`), all destination states are accumulated in a set, resulting in a nondeterministic finite automaton (NFA).

```python
def to_finite_automaton(self):
    from finite_automaton import FiniteAutomaton

    states = set(self.vn) | {"X"}
    alphabet = set(self.vt)
    transitions = {}
    start_state = self.start_symbol
    accept_states = {"X"}

    for lhs, rhs_list in self.productions.items():
        for rhs in rhs_list:
            if len(rhs) == 1 and rhs in self.vt:
                transitions.setdefault((lhs, rhs), set()).add("X")
            elif len(rhs) == 2 and rhs[0] in self.vt and rhs[1] in self.vn:
                transitions.setdefault((lhs, rhs[0]), set()).add(rhs[1])

    return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)
```

### Finite Automaton Class

The `FiniteAutomaton` class stores the five components of a finite automaton: states, alphabet, transitions, start state, and accept states. The `string_belongs_to_language()` method simulates the NFA by tracking a set of all currently reachable states. For each character in the input string, it computes the next set of states by following all applicable transitions. If at any point no transitions are possible, the string is rejected. If after processing all characters the current states intersect with the accept states, the string is accepted.

```python
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}
        for ch in input_string:
            next_states = set()
            for state in current_states:
                key = (state, ch)
                if key in self.transitions:
                    next_states |= self.transitions[key]
            if not next_states:
                return False
            current_states = next_states
        return bool(current_states & self.accept_states)
```

### Main Driver

The `main.py` file instantiates the grammar for Variant 21, generates 5 unique valid strings, converts the grammar to a finite automaton, prints the automaton's components, and then tests several strings for membership in the language.

```python
from grammar import Grammar

def main():
    vn = {"S", "B", "C", "D"}
    vt = {"a", "b", "c"}
    productions = {
        "S": ["aB"],
        "B": ["bS", "aC", "b"],
        "C": ["bD"],
        "D": ["a", "bC", "cS"],
    }
    grammar = Grammar(vn, vt, productions, "S")

    print("5 valid strings generated from the grammar:")
    for i in range(1, 6):
        print(f"  {i}. {grammar.generate_string()}")

    fa = grammar.to_finite_automaton()

    test_strings = ["ab", "aab", "aabab", "abab", "abc", "aaba", "aabda", "abcab"]
    for s in test_strings:
        result = fa.string_belongs_to_language(s)
        print(f"  '{s}' -> {'accepted' if result else 'rejected'}")
```


## Conclusions / Results

The program was executed successfully. Below is the output from a sample run:

```
5 valid strings generated from the grammar:
  1. aaba
  2. aabcaabbbbba
  3. abaaba
  4. abababaaba
  5. ababaabbbcab

Finite Automaton:
  States:        {'B', 'C', 'D', 'X', 'S'}
  Alphabet:      {'c', 'b', 'a'}
  Start state:   S
  Accept states: {'X'}
  Transitions:
    δ(B, a) = {'C'}
    δ(B, b) = {'X', 'S'}
    δ(C, b) = {'D'}
    δ(D, a) = {'X'}
    δ(D, b) = {'C'}
    δ(D, c) = {'S'}
    δ(S, a) = {'B'}

String validation via Finite Automaton:
  'ab' -> accepted
  'aab' -> rejected
  'aabab' -> rejected
  'abab' -> accepted
  'abc' -> rejected
  'aaba' -> accepted
  'aabda' -> rejected
  'abcab' -> rejected
```

The generated strings are all valid words in the language defined by the grammar. The finite automaton correctly accepts strings that can be derived from the grammar (e.g., `ab`, `abab`, `aaba`) and rejects those that cannot (e.g., `aab`, `abc`, `aabda`). This confirms the equivalence between the regular grammar and the constructed finite automaton.