from collections import defaultdict
from regex_ast import *

class NFAGraph:
    def __init__(self, start, end, transitions):
        self.entry = start
        self.terminal = end
        self.transition_map = transitions

    _state_id_map = {}
    _id_counter = 0

    def _get_numeric_id(self, state):
        if state not in self._state_id_map:
            self._state_id_map[state] = self._id_counter
            self._id_counter += 1
        return str(self._state_id_map[state])

    def to_dict(self):
        nfa_dict = {'startingState': self._get_numeric_id(self.entry)}

        for current_state, paths in self.transition_map.items():
            formatted_transitions = {}
            for symbol, destinations in paths.items():
                key = 'epsilon' if symbol == '' else symbol
                formatted_transitions[key] = [self._get_numeric_id(dest) for dest in destinations]

            nfa_dict[self._get_numeric_id(current_state)] = {
                "isTerminatingState": self._get_numeric_id(current_state) == self._get_numeric_id(self.terminal),
                **formatted_transitions
            }

        return nfa_dict


class ThompsonBuilder:
    def __init__(self, root_node):
        self.root = root_node

    def construct_nfa(self):
        entry, final, transition_map = self._construct_from_node(self.root)
        return NFAGraph(entry, final, transition_map)

    def _construct_from_node(self, node):
        if isinstance(node, LiteralCharacterNode):
            start, end = object(), object()
            return start, end, {
                start: {node.char: {end}},
                end: {'': set()}
            }

        elif isinstance(node, StarNode):
            sub_start, sub_end, sub_map = self._construct_from_node(node.left)
            entry, exit = object(), object()
            sub_map[sub_end] = {'': {sub_start, exit}}
            return entry, exit, {
                entry: {'': {sub_start, exit}},
                **sub_map,
                exit: {'': set()}
            }

        elif isinstance(node, PlusNode):
            sub_start, sub_end, sub_map = self._construct_from_node(node.left)
            entry, exit = object(), object()
            sub_map[sub_end] = {'': {sub_start, exit}}
            return entry, exit, {
                entry: {'': {sub_start}},
                **sub_map,
                exit: {'': set()}
            }

        elif isinstance(node, OptionalNode):
            sub_start, sub_end, sub_map = self._construct_from_node(node.left)
            entry, exit = object(), object()
            return entry, exit, {
                entry: {'': {sub_start, exit}},
                **sub_map,
                sub_end: {'': {exit}},
                exit: {'': set()}
            }

        elif isinstance(node, SequenceNode):
            left_start, left_end, left_map = self._construct_from_node(node.left)
            right_start, right_end, right_map = self._construct_from_node(node.right)
            left_map[left_end] = {'': {right_start}}
            return left_start, right_end, {**left_map, **right_map}

        elif isinstance(node, UnionNode):
            left_start, left_end, left_map = self._construct_from_node(node.left)
            right_start, right_end, right_map = self._construct_from_node(node.right)
            entry, exit = object(), object()
            return entry, exit, {
                entry: {'': {left_start, right_start}},
                **left_map,
                **right_map,
                left_end: {'': {exit}},
                right_end: {'': {exit}},
                exit: {'': set()}
            }

        elif isinstance(node, CharSetNode):
            start, end = object(), object()
            return start, end, {
                start: {char: {end} for char in node.chars},
                end: {'': set()}
            }

        else:
            raise ValueError("Unsupported AST node for NFA generation.")
