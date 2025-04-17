class DFAMinimizer:
    def __init__(self, dfa_dict):
        self.states = list(dfa_dict.keys())
        self.start_state = dfa_dict['startingState']
        self.states.remove('startingState')
        self.alphabet = list(set([k for d in dfa_dict.values() for k in d if k != 'isTerminatingState']))
        self.alphabet.remove(dfa_dict['startingState'])
        self.accept_states = set([s for s in self.states if dfa_dict[s]['isTerminatingState']])
        self.reject_states = set(self.states) - self.accept_states
        self.groups = [self.accept_states, self.reject_states]
        self.partition = self._partition(dfa_dict)
        self.old_dfa_dict = dfa_dict
        

    def _partition(self, dfa_dict):
        # Initialize partition with the accepting and rejecting states
        partition = [self.accept_states.copy(), self.reject_states.copy()]
        #[[acc],[rej]]

       
        
        # Keep refining the partition until it no longer changes
        while True:
           #[ [1,2,3],[4,5,6]]
            groupToIdx = {}
            for i, group in enumerate(partition):
                for state in group:
                    groupToIdx[state] = i

            new_partition = []
            next_states = {}

            #next_states[2]={'a':0,'b':0,'c':'stuck'}
            for group in partition: 
                if len(group) == 0:
                    continue      
                
                for state in group:
                    next_states[state] = {}
                    # state:2
                    # sy : 'a'
                    # 3
                    for symbol in self.alphabet:
                        if symbol in dfa_dict[state]:
                            next_states[state][symbol] = groupToIdx[dfa_dict[state][symbol]]
                        else:
                            next_states[state][symbol] = 'stuck'
            # for they have the same next states, they are in the same group
            for group in partition:
                if len(group) == 0:
                    continue
                if len(group) == 1:
                    new_partition.append(group)
                    continue
                #next_states[2]={'a':0,'b':0,'c':'stuck'}
                #next_states[3]={'a':0,'b':0,'c':'stuck'}
                #sameNextStates[{'a':0,'b':0,'c':'stuck'}] -> [2,3]
                sameNextStates = {}
                for state in group:
                    sameNextStates[tuple(next_states[state].items())] = []
                for state in group:
                    sameNextStates[tuple(next_states[state].items())].append(state)
                for sameNextState in sameNextStates.values():
                    new_partition.append(set(sameNextState))
                
            if new_partition == partition:
                break
            else:
                partition = new_partition
        return partition



    
    def to_dict(self):
        maNewStateNames = {}
        for state in self.states:
            for i, group in enumerate(self.partition):
                if state in group:
                    maNewStateNames[state] = i
                    break
        dfa_dict = {
            "startingState": str(maNewStateNames[self.start_state])
        }
        
        for state in self.states:
            dfa_dict[str(maNewStateNames[state])] = {
                "isTerminatingState": state in self.accept_states
            }
            for symbol in self.alphabet:
                if symbol in self.old_dfa_dict[state]:
                    dfa_dict[str(maNewStateNames[state])][symbol] = str(maNewStateNames[self.old_dfa_dict[state][symbol]])
        
        return dfa_dict