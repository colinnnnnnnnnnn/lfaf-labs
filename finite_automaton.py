class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        """Check if the input string can be obtained via state transitions."""
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

    def is_deterministic(self):
        """Check if the finite automaton is deterministic (DFA) or non-deterministic (NFA)."""
        for (state, symbol), targets in self.transitions.items():
            if len(targets) > 1:
                return False
        return True

    def to_regular_grammar(self):
        """Convert the finite automaton to an equivalent regular grammar."""
        from grammar import Grammar

        vn = set(self.states)
        vt = set(self.alphabet)
        productions = {}

        for (state, symbol), targets in self.transitions.items():
            for target in targets:
                # Always add A -> aB
                productions.setdefault(state, []).append(symbol + target)
                # If target is an accept state, also add A -> a
                if target in self.accept_states:
                    productions.setdefault(state, []).append(symbol)

        return Grammar(vn, vt, productions, self.start_state)

    def to_dfa(self):
        """Convert this NFA to an equivalent DFA using the subset construction algorithm."""
        dfa_start = frozenset({self.start_state})
        dfa_states = set()
        dfa_transitions = {}
        queue = [dfa_start]
        dfa_states.add(dfa_start)

        while queue:
            current = queue.pop(0)

            for symbol in self.alphabet:
                next_state = set()
                for nfa_state in current:
                    key = (nfa_state, symbol)
                    if key in self.transitions:
                        next_state |= self.transitions[key]

                if not next_state:
                    continue

                next_frozen = frozenset(next_state)
                dfa_transitions[(current, symbol)] = {next_frozen}

                if next_frozen not in dfa_states:
                    dfa_states.add(next_frozen)
                    queue.append(next_frozen)

        # A DFA state is accepting if it contains any NFA accept state
        dfa_accept = set()
        for state in dfa_states:
            if state & self.accept_states:
                dfa_accept.add(state)

        # Rename states from frozensets to readable strings
        state_names = {}
        for state in sorted(dfa_states, key=lambda s: sorted(s)):
            name = "{" + ",".join(sorted(s for s in state)) + "}"
            state_names[state] = name

        renamed_states = {state_names[s] for s in dfa_states}
        renamed_transitions = {}
        for (state, symbol), targets in dfa_transitions.items():
            renamed_targets = {state_names[t] for t in targets}
            renamed_transitions[(state_names[state], symbol)] = renamed_targets
        renamed_accept = {state_names[s] for s in dfa_accept}
        renamed_start = state_names[dfa_start]

        return FiniteAutomaton(
            renamed_states,
            set(self.alphabet),
            renamed_transitions,
            renamed_start,
            renamed_accept,
        )
