class DeterministicAutomaton:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.label_map = {}
        self.counter = 0

    def _get_label(self, state):
        key = tuple(sorted(state))
        if key not in self.label_map:
            self.label_map[key] = str(self.counter)
            self.counter += 1
        return self.label_map[key]

    def to_serialized_dict(self):
        result = {
            "startingState": self._get_label(self.start_state)
        }

        for state in self.states:
            label = self._get_label(state)
            result[label] = {
                "isTerminatingState": state in self.accept_states
            }

            for symbol in self.alphabet:
                target_state = self.transitions[state].get(symbol)
                if target_state:
                    result[label][symbol] = self._get_label(target_state)

        return result


class NFAtoDFA:
    def __init__(self, nfa):
        self.nfa = nfa

    def _epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            current = stack.pop()
            for next_state in self.nfa.get(current, {}).get("epsilon", []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return frozenset(closure)

    def _move(self, state_set, symbol):
        result = set()
        for state in state_set:
            if symbol in self.nfa.get(state, {}):
                result.update(self.nfa[state][symbol])
        return frozenset(result)

    def convert_to_dfa(self):
        alphabet = {
            symbol
            for trans in self.nfa.values()
            for symbol in trans
            if symbol not in ["epsilon", "isTerminatingState"]
        }

        start_state = self._epsilon_closure([self.nfa["startingState"]])
        queue = [start_state]
        visited = [start_state]
        transitions = {}
        accept_states = []

        while queue:
            current = queue.pop(0)
            transitions[current] = {}

            for symbol in alphabet:
                move_res = self._move(current, symbol)
                closure_res = self._epsilon_closure(move_res)

                if not closure_res:
                    continue

                transitions[current][symbol] = closure_res

                if closure_res not in visited:
                    visited.append(closure_res)
                    queue.append(closure_res)

            if any(self.nfa.get(s, {}).get("isTerminatingState") for s in current):
                accept_states.append(current)

        return DeterministicAutomaton(
            alphabet=alphabet,
            states=visited,
            start_state=start_state,
            accept_states=accept_states,
            transitions=transitions
        )
