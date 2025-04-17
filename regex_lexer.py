from enum import Enum, auto

class TokenType(Enum):
    OR = auto()
    STAR = auto()
    PLUS = auto()
    QUESTION_MARK = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    DASH = auto()
    LITERAL = auto()

def classify_char(char):
    mapping = {
        '|': TokenType.OR,
        '*': TokenType.STAR,
        '+': TokenType.PLUS,
        '?': TokenType.QUESTION_MARK,
        '(': TokenType.OPEN_PAREN,
        ')': TokenType.CLOSE_PAREN,
        '[': TokenType.OPEN_BRACKET,
        ']': TokenType.CLOSE_BRACKET,
        '-': TokenType.DASH
    }
    return mapping.get(char, TokenType.LITERAL)

def stringify_token(ttype):
    for symbol, token in {
        '|': TokenType.OR,
        '*': TokenType.STAR,
        '+': TokenType.PLUS,
        '?': TokenType.QUESTION_MARK,
        '(': TokenType.OPEN_PAREN,
        ')': TokenType.CLOSE_PAREN,
        '[': TokenType.OPEN_BRACKET,
        ']': TokenType.CLOSE_BRACKET,
        '-': TokenType.DASH
    }.items():
        if token == ttype:
            return symbol
    return ttype.name

class Token:
    def __init__(self, token_type, value):
        self.ttype = token_type
        self.content = value

class Tokenizer:
    def __init__(self, regex_string):
        self.regex_string = regex_string

    def tokenize(self):
        stream = []
        for character in self.regex_string:
            stream.append(Token(classify_char(character), character))
        return stream
