from regex_lexer import *
from regex_ast import *

class RegexParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        expression = self._parse_expression()
        if self.index < len(self.tokens):
            raise SyntaxError("Unexpected extra tokens found.")
        return expression

    def _parse_expression(self):
        node = self._parse_term()
        if self._accept(TokenType.OR):
            return UnionNode(node, self._parse_expression())
        return node

    def _parse_term(self):
        node = self._parse_core()
        if self._has_more_tokens():
            next_type = self.tokens[self.index].ttype
            if next_type in [TokenType.LITERAL, TokenType.OPEN_PAREN, TokenType.OPEN_BRACKET]:
                return SequenceNode(node, self._parse_term())
        return node

    def _parse_core(self):
        node = None
        if self._accept(TokenType.LITERAL):
            node = LiteralCharacterNode(self.tokens[self.index - 1].content)
        elif self._accept(TokenType.OPEN_PAREN):
            node = self._parse_expression()
            self._expect(TokenType.CLOSE_PAREN)
        elif self._accept(TokenType.OPEN_BRACKET):
            char_set = self._parse_set()
            self._expect(TokenType.CLOSE_BRACKET)
            node = CharSetNode(char_set)
        else:
            raise SyntaxError("Invalid character in regex")

        if self._accept(TokenType.STAR):
            return StarNode(node)
        elif self._accept(TokenType.PLUS):
            return PlusNode(node)
        elif self._accept(TokenType.QUESTION_MARK):
            return OptionalNode(node)

        return node

    def _parse_set(self):
        result = set()
        buffer = []

        while self._has_more_tokens():
            t = self.tokens[self.index].ttype
            if t == TokenType.CLOSE_BRACKET:
                break
            elif t == TokenType.LITERAL:
                result.add(self.tokens[self.index].content)
                buffer.append(self.tokens[self.index].content)
            elif t == TokenType.DASH:
                if not buffer or self.index + 1 >= len(self.tokens):
                    result.add('-')
                else:
                    range_start = ord(buffer.pop())
                    range_end = ord(self.tokens[self.index + 1].content)
                    for c in range(range_start, range_end + 1):
                        result.add(chr(c))
                    self.index += 1
            self.index += 1
        return result

    def _accept(self, expected_type):
        if self._has_more_tokens() and self.tokens[self.index].ttype == expected_type:
            self.index += 1
            return True
        return False

    def _expect(self, expected_type):
        if not self._accept(expected_type):
            raise SyntaxError(f"Expected token of type {expected_type}")

    def _has_more_tokens(self):
        return self.index < len(self.tokens)
