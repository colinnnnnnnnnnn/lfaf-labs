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
