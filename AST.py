from abc import ABC, abstractmethod

class AstNode(ABC):
    @abstractmethod
    def __init__(self):
        pass

class OrAstNode(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
class SeqAstNode(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class StarAstNode(AstNode):
    def __init__(self, left):
        self.left = left
        
class PlusAstNode(AstNode):
    def __init__(self, left):
        self.left = left
        
class QuestionMarkAstNode(AstNode):
    def __init__(self, left):
        self.left = left
        
class LiteralCharacterAstNode(AstNode):
    def __init__(self, char):
        self.char = char
        
class SquareBracketAstNode(AstNode):
    def __init__(self, clas):
        self.clas = clas
        
def print_ast(node, indent=0):
    if isinstance(node, OrAstNode):
        print(' ' * indent + 'OR')
        print_ast(node.left, indent + 2)
        print_ast(node.right, indent + 2)
    elif isinstance(node, SeqAstNode):
        print(' ' * indent + 'SEQ')
        print_ast(node.left, indent + 2)
        print_ast(node.right, indent + 2)
    elif isinstance(node, StarAstNode):
        print(' ' * indent + 'STAR')
        print_ast(node.left, indent + 2)
    elif isinstance(node, PlusAstNode):
        print(' ' * indent + 'PLUS')
        print_ast(node.left, indent + 2)
    elif isinstance(node, QuestionMarkAstNode):
        print(' ' * indent + 'QUESTION_MARK')
        print_ast(node.left, indent + 2)
    elif isinstance(node, LiteralCharacterAstNode):
        print(' ' * indent + 'LITERAL: ' + node.char)
    elif isinstance(node, SquareBracketAstNode):
        print(' ' * indent + 'SQUARE_BRACKET')
        for char in node.clas:
            if isinstance(char, tuple):
                print(' ' * (indent + 2) + 'RANGE: {}-{}'.format(char[0], char[1]))
            else:
                print(' ' * (indent + 2) + 'CHARACTER: {}'.format(char))
    else:
        raise ValueError('Invalid AST node type')