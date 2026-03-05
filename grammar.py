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

    def classify_chomsky(self):
        """Classify the grammar based on the Chomsky hierarchy.
        Returns one of: 'Type 3 (Regular)', 'Type 2 (Context-Free)',
        'Type 1 (Context-Sensitive)', 'Type 0 (Unrestricted)'.
        """
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.productions.items():
            # For Type 2 and Type 3, the left-hand side must be a single non-terminal
            if len(lhs) != 1 or lhs not in self.vn:
                is_context_free = False
                is_regular = False

            for rhs in rhs_list:
                # Check context-sensitive: |lhs| <= |rhs| (no shrinking rules)
                if len(rhs) < len(lhs):
                    is_context_sensitive = False

                # Check regular grammar (right-linear):
                # rhs is either a single terminal, or a terminal followed by a non-terminal
                if is_regular:
                    if len(rhs) == 1:
                        if rhs not in self.vt:
                            is_regular = False
                    elif len(rhs) == 2:
                        if rhs[0] not in self.vt or rhs[1] not in self.vn:
                            is_regular = False
                    else:
                        is_regular = False

        if is_regular:
            return "Type 3 (Regular)"
        elif is_context_free:
            return "Type 2 (Context-Free)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive)"
        else:
            return "Type 0 (Unrestricted)"
