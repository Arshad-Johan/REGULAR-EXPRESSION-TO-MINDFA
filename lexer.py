from enum import Enum,auto
class TokenType(Enum):
  OR = auto()
  STAR = auto()
  PLUS = auto()
  QUESTION_MARK = auto()
  OPEN_PAREN = auto()
  CLOSED_PAREN = auto()
  OPEN_SQUARE_BRACKET = auto()
  CLOSED_SQUARE_BRACKET = auto()
  DASH = auto()
  LITERAL = auto()
def getTypeToken(token):
    if token == '|':
        return TokenType.OR
    elif token == '*':
        return TokenType.STAR
    elif token == '+':
        return TokenType.PLUS
    elif token == '?':
        return TokenType.QUESTION_MARK
    elif token == '(':
        return TokenType.OPEN_PAREN
    elif token == ')':
        return TokenType.CLOSED_PAREN
    elif token == '[':
        return TokenType.OPEN_SQUARE_BRACKET
    elif token == ']':
        return TokenType.CLOSED_SQUARE_BRACKET
    elif token == '-':
        return TokenType.DASH
    else:
        return TokenType.LITERAL
def getTokenValue(token):
    if token==TokenType.OR:
        return '|'
    elif token==TokenType.STAR:
        return '*'
    elif token==TokenType.PLUS:
        return '+'
    elif token==TokenType.QUESTION_MARK:
        return '?'
    elif token==TokenType.OPEN_PAREN:
        return '('
    elif token==TokenType.CLOSED_PAREN:
        return ')'
    elif token==TokenType.OPEN_SQUARE_BRACKET:
        return '['
    elif token==TokenType.CLOSED_SQUARE_BRACKET:
        return ']'
    elif token==TokenType.DASH:
        return '-'
    else:
        return token

class Token:
    ttype: TokenType
    content: str
    def __init__(self, ttype, content):
        self.ttype = ttype
        self.content = content
        
class regexLexer:
    # input: regex string
    # output: token stream
    def __init__(self, regexStr):
        self.regexStr = regexStr
    def lexer(self):
        tokenStream = []
        for i in range(len(self.regexStr)):
            token = Token(getTypeToken(self.regexStr[i]), self.regexStr[i])
            tokenStream.append(token)
        return tokenStream
    
# regexLexer = regexLexer('a|b')
# tokenStream = regexLexer.lexer()
# for token in tokenStream:
#     print(token.ttype, token.content)