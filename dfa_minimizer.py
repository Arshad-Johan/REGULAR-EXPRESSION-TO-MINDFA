class DFAReducer:
    def __init__(self, dfa_structure):
        self.original_dfa = dfa_structure
        self.state_list = [s for s in dfa_structure if s != "startingState"]
        self.start_node = dfa_structure["startingState"]
        self.symbols = list({sym for s in self.state_list for sym in dfa_structure[s] if sym != 'isTerminatingState'})
        self.terminal_nodes = {s for s in self.state_list if dfa_structure[s]['isTerminatingState']}
        self.non_terminal_nodes = set(self.state_list) - self.terminal_nodes
        self.groupings = self._split_states()

    def _split_states(self):
        partitions = [self.terminal_nodes.copy(), self.non_terminal_nodes.copy()]
        while True:
            state_group_map = {state: idx for idx, group in enumerate(partitions) for state in group}
            new_partitions = []
            transitions = {}

            for group in partitions:
                if not group:
                    continue
                for state in group:
                    transitions[state] = {
                        symbol: state_group_map.get(self.original_dfa[state].get(symbol, None), '⊥')
                        for symbol in self.symbols
                    }

            for group in partitions:
                if len(group) <= 1:
                    new_partitions.append(group)
                    continue
                signature_map = {}
                for state in group:
                    sig = tuple(sorted(transitions[state].items()))
                    signature_map.setdefault(sig, set()).add(state)
                new_partitions.extend(signature_map.values())

            if new_partitions == partitions:
                break
            partitions = new_partitions

        return partitions

    def to_dict(self):
        renamed_states = {}
        minimized_dfa = {
            "startingState": None
        }

        for idx, group in enumerate(self.groupings):
            for state in group:
                renamed_states[state] = str(idx)

        minimized_dfa["startingState"] = renamed_states[self.start_node]

        for state in self.state_list:
            state_id = renamed_states[state]
            if state_id not in minimized_dfa:
                minimized_dfa[state_id] = {
                    "isTerminatingState": state in self.terminal_nodes
                }
            for symbol in self.symbols:
                if symbol in self.original_dfa[state]:
                    target = self.original_dfa[state][symbol]
                    minimized_dfa[state_id][symbol] = renamed_states[target]

        return minimized_dfa
