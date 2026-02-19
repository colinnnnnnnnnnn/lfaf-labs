import random


class Grammar:
    def __init__(self, vn, vt, productions, start_symbol):
        self.vn = vn            # Non-terminal symbols
        self.vt = vt            # Terminal symbols
        self.productions = productions  # dict: non-terminal -> list of right-hand sides
        self.start_symbol = start_symbol

    def generate_string(self):
        """Generate a valid string by randomly expanding productions starting from S."""
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

    def to_finite_automaton(self):
        """Convert this regular grammar to a Finite Automaton."""
        from finite_automaton import FiniteAutomaton

        states = set(self.vn) | {"X"}  # X is the accept/final state
        alphabet = set(self.vt)
        transitions = {}
        start_state = self.start_symbol
        accept_states = {"X"}

        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs in self.vt:
                    # Production like B -> b  (terminal only => transition to accept state)
                    transitions.setdefault((lhs, rhs), set()).add("X")
                elif len(rhs) == 2 and rhs[0] in self.vt and rhs[1] in self.vn:
                    # Production like S -> aB
                    transitions.setdefault((lhs, rhs[0]), set()).add(rhs[1])

        return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)
