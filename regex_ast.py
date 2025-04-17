from abc import ABC, abstractmethod

class RegexNode(ABC):
    @abstractmethod
    def __init__(self):
        pass

class UnionNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class SequenceNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class StarNode(RegexNode):
    def __init__(self, left):
        self.left = left

class PlusNode(RegexNode):
    def __init__(self, left):
        self.left = left

class OptionalNode(RegexNode):
    def __init__(self, left):
        self.left = left

class LiteralCharacterNode(RegexNode):
    def __init__(self, char):
        self.char = char

class CharSetNode(RegexNode):
    def __init__(self, chars):
        self.chars = chars

def debug_ast_structure(node, indent=0):
    pad = ' ' * indent
    if isinstance(node, UnionNode):
        print(f"{pad}ALT")
        debug_ast_structure(node.left, indent + 2)
        debug_ast_structure(node.right, indent + 2)
    elif isinstance(node, SequenceNode):
        print(f"{pad}SEQ")
        debug_ast_structure(node.left, indent + 2)
        debug_ast_structure(node.right, indent + 2)
    elif isinstance(node, StarNode):
        print(f"{pad}REPEAT (*)")
        debug_ast_structure(node.left, indent + 2)
    elif isinstance(node, PlusNode):
        print(f"{pad}REPEAT (+)")
        debug_ast_structure(node.left, indent + 2)
    elif isinstance(node, OptionalNode):
        print(f"{pad}OPTIONAL (?)")
        debug_ast_structure(node.left, indent + 2)
    elif isinstance(node, LiteralCharacterNode):
        print(f"{pad}CHARACTER: {node.char}")
    elif isinstance(node, CharSetNode):
        print(f"{pad}CHARACTER SET:")
        for item in node.chars:
            if isinstance(item, tuple):
                print(f"{pad}  RANGE: {item[0]} - {item[1]}")
            else:
                print(f"{pad}  CHAR: {item}")
    else:
        raise TypeError("Unknown AST node encountered.")
