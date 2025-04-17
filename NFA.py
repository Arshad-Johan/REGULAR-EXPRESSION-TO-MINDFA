from collections import deque
from AST import *

class NFA:
    def __init__(self, starting_state,final_state, states):
        self.starting_state = starting_state
        self.final_state = final_state
        self.states = states
    dect = {}
    index = 0
    def stateToNumber(self, state):
        if state in self.dect:
            return str(self.dect[state])
        else:
            self.dect[state] = self.index
            self.index += 1
            return str(self.dect[state])
        
    
    def to_dict(self):
        nfa_dict = {}
        nfa_dict['startingState'] = self.stateToNumber(self.starting_state)
        for state_name, state in self.states.items():
            transitions = {}
            for symbol, next_states in state.items():
                if symbol == '':
                    symbol = 'epsilon'
                arr = []
                for next_state in next_states:
                    arr.append(self.stateToNumber(next_state))
                transitions[symbol] = arr
            
            nfa_dict[self.stateToNumber(state_name)] = {
                'isTerminatingState': self.stateToNumber(state_name) == self.stateToNumber(self.final_state),
                **transitions
            }
            
        return nfa_dict

class ThompsonConstruction:
    def __init__(self, ast):
        self.ast = ast

    def construct(self):
        starting_state, final_state, states = self._construct_from_ast(self.ast)
        return NFA(starting_state,final_state, states)

    def _construct_from_ast(self, node):
        if isinstance(node, LiteralCharacterAstNode):
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {node.char: {final_state}},
                final_state: {'': set()}
            }
            return starting_state, final_state, states
        
        elif isinstance(node, PlusAstNode):
            # (a|epsilon)+
            # one or more
            sub_start, sub_final, sub_states = self._construct_from_ast(node.left)
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {'': {sub_start}},
                **sub_states,
                sub_final: {'': {starting_state, final_state}},
                final_state: {'': set()}
            }
            
            return starting_state, final_state, states
        
        elif isinstance(node, QuestionMarkAstNode):
            # (a|epsilon)?
            # zero or one
            sub_start, sub_final, sub_states = self._construct_from_ast(node.left)
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {'': {sub_start, final_state}},
                **sub_states,
                sub_final: {'': {final_state}},
                final_state: {'': set()}
                
            }
            return starting_state, final_state, states

        elif isinstance(node, SeqAstNode):
            # a.b

            left_start, left_final, left_states = self._construct_from_ast(node.left)
            right_start, right_final, right_states = self._construct_from_ast(node.right)
            states = {**left_states, **right_states, left_final: {'': {right_start}}}
            starting_state = left_start
            final_state = right_final
            return starting_state, final_state, states

        elif isinstance(node, OrAstNode):
            # a|b
            left_start, left_final, left_states = self._construct_from_ast(node.left)
            right_start, right_final, right_states = self._construct_from_ast(node.right)
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {'': {left_start, right_start}},
                **left_states,
                **right_states,
                left_final: {'': {final_state}},
                right_final: {'': {final_state}},
                final_state: {'': set()},
                final_state: {'': set()}
            }
            return starting_state, final_state, states
        
        elif isinstance(node, StarAstNode):
            # (a|epsilon)*
            # zero or more
            sub_start, sub_final, sub_states = self._construct_from_ast(node.left)
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {'': {sub_start, final_state}},
                **sub_states,
                sub_final: {'': {starting_state, final_state}},
                final_state: {'': set()}
            }
            return starting_state, final_state, states
        
        elif isinstance(node, SquareBracketAstNode):
            starting_state = object()
            final_state = object()
            states = {
                starting_state: {char: {final_state} for char in node.clas},
                final_state: {'': set()}
            }
            return starting_state, final_state, states

