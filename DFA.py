class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transition_function):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states    
        self.transition_function = transition_function
        self.ma = {}
        self.num = 0
    def run(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            current_state = self.transition_function[current_state][symbol]
        return current_state in self.accept_states
    def get_state_number(self,state):
        if self.ma.get(state) == None:
            self.ma[state] = self.num
            self.num += 1
        return str(self.ma[state])
    def to_dict(self):
        dfa_dict = {}
        dfa_dict['startingState'] = self.get_state_number(self.start_state)
        for state in self.states:
            if state == 'frozenset()':
                continue
            dfa_dict[self.get_state_number(state)] = {
                "isTerminatingState": state in self.accept_states
            }
            for symbol in self.alphabet:
                if symbol == 'isTerminatingState':
                    continue
                if self.transition_function[state][symbol]!="frozenset()": 
                    dfa_dict[self.get_state_number(state)][symbol] = self.get_state_number(self.transition_function[state][symbol])
        return dfa_dict

class NFAtoDFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa = self.convert()

    def epsilon_closure(self, states):
        closure = set(states)
        queue = list(states)
        while queue:
            state = queue.pop()
            if state in self.nfa:
                for next_state in self.nfa[state].get("epsilon", []):
                    if next_state not in closure:
                        closure.add(next_state)
                        queue.append(next_state)
        return frozenset(closure)

    def move(self, states, symbol):
        move_states = set()
        for state in states:
            if state in self.nfa:
                # handle if isTerminatingState
                if symbol == 'isTerminatingState':
                    continue
                for next_state in self.nfa[state].get(symbol, []):
                    move_states.add(next_state)
        return frozenset(move_states)

    def convert(self):
        alphabet = set(symbol for state in self.nfa.values() for symbol in state if symbol != "epsilon")
        alphabet.discard("isTerminatingState")
        alphabet.discard(self.nfa["startingState"])
        start_state = self.epsilon_closure([self.nfa["startingState"]])
        dfa_states = [start_state]
        dfa_accept_states = []
        dfa_transition_function = {}
        queue = [start_state]

        while queue:
            current_state = queue.pop(0)
            for symbol in alphabet:
                move_states = self.move(current_state, symbol)
                closure_states = self.epsilon_closure(move_states)

                if closure_states not in dfa_states:
                    dfa_states.append(closure_states)
                    queue.append(closure_states)

                dfa_transition_function.setdefault(current_state, {})
                dfa_transition_function[current_state][symbol] = closure_states

            if any(state in self.nfa and self.nfa[state]["isTerminatingState"] for state in current_state):
                dfa_accept_states.append(current_state)

        # remove empty fozenset from dfa_transition_function
        #dfa_transition_function.pop(frozenset(), None)
        dfa_states = [str(state) for state in dfa_states]
        start_state = str(start_state)
        dfa_accept_states = [str(state) for state in dfa_accept_states]
        dfa_transition_function = {str(k): {symbol: str(v) for symbol, v in transitions.items()} for k, transitions in dfa_transition_function.items()}

        return DFA(alphabet, dfa_states, start_state, dfa_accept_states, dfa_transition_function)