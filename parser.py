from lexer import *
from AST import *
## let's define a CFG for the language
# S -> E
# E -> T '|' E | T
# T -> C F T | C
# F -> '*' | '+' | '?' | epsilon
# C -> L | '(' E ')' | '[' L DASH L ']' | epsilon
# L -> LITERAL | ESCAPED
# OR -> '|' | epsilon
# STAR -> '*' | epsilon
# PLUS -> '+' | epsilon
# QUESTION_MARK -> '?' | epsilon
# OPEN_PAREN -> '(' | epsilon
# CLOSED_PAREN -> ')' | epsilon
# OPEN_SQUARE_BRACKET -> '[' | epsilon
# CLOSED_SQUARE_BRACKET -> ']' | epsilon
# DASH -> '-' | epsilon
# LITERAL -> any character except '|' '*', '+', '?', '(', ')', '[', ']', '\\', and '-' 

class ParseRegex:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream
        self.currToken = 0

    
    def parse(self):
        ast = self.parse_E()
        if self.currToken < len(self.tokenStream):
            raise Exception("Unexpected token")
        return ast

    def parse_E(self):
        ast = self.parse_T()
        if self.match(TokenType.OR):
            left = ast
            right = self.parse_E()
            ast = OrAstNode(left, right)
        return ast

    def parse_T(self):
        ast = self.parse_C()
        if self.currToken < len(self.tokenStream):
            ttype = self.tokenStream[self.currToken].ttype
            if ttype in [TokenType.LITERAL, TokenType.OPEN_PAREN, TokenType.OPEN_SQUARE_BRACKET]:
                left = ast
                right = self.parse_T()
                ast = SeqAstNode(left, right)
        return ast

    def parse_C(self):
        if self.match(TokenType.LITERAL):
            ast = LiteralCharacterAstNode(self.tokenStream[self.currToken - 1].content)
        elif self.match(TokenType.OPEN_PAREN):
            ast = self.parse_E()
            self.expect(TokenType.CLOSED_PAREN)
        elif self.match(TokenType.OPEN_SQUARE_BRACKET):
            clas = self.parse_L()
            self.expect(TokenType.CLOSED_SQUARE_BRACKET)
            ast = SquareBracketAstNode(clas)
        else:
            ast = AstNode()
        if self.match(TokenType.STAR):
            ast = StarAstNode(ast)
        elif self.match(TokenType.PLUS):
            ast = PlusAstNode(ast)
        elif self.match(TokenType.QUESTION_MARK):
            ast = QuestionMarkAstNode(ast)
        return ast

    def parse_L(self):
        clas = set()
        que = []
        while self.currToken < len(self.tokenStream):
            ttype = self.tokenStream[self.currToken].ttype
            if ttype == TokenType.CLOSED_SQUARE_BRACKET:
                break
            elif ttype == TokenType.LITERAL:
                clas.add(self.tokenStream[self.currToken].content)
                que.append(self.tokenStream[self.currToken].content)
            elif ttype == TokenType.DASH:
                if len(clas) == 0 or self.currToken + 1 == len(self.tokenStream) or self.tokenStream[self.currToken + 1].ttype == TokenType.CLOSED_SQUARE_BRACKET:
                    clas.add('-')
                else:
                    # get last character in que
                    start = ord(que.pop())
                    end = ord(self.tokenStream[self.currToken + 1].content)
                    # print(chr(start), chr(end))
                    for i in range(start, end + 1):
                        clas.add(chr(i))
                    self.currToken += 1
            self.currToken += 1
        return clas

    def match(self, ttype):
        if self.currToken >= len(self.tokenStream):
            return False
        if self.tokenStream[self.currToken].ttype == ttype:
            self.currToken += 1
            return True
        return False

    def expect(self, ttype):
        if not self.match(ttype):
            raise Exception("Expected token", getTokenValue(ttype))
        