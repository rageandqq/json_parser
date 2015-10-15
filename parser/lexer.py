import re

from tokens import Token
from tokens import TokenType


class Lexer:

    json_string = None
    peeked_token = None
    position = None

    def __init__(self, json_string):
        self.json_string = json_string
        self.position = 0

    def _action_and_advance(self, func):
        token = func()
        self.position += 1
        self.peeked_token = None
        return token

    def _advance_to_non_whitespace(self):
        while (self.position < len(self.json_string)
                and self.json_string[self.position: self.position+1].isspace()):
            self.position += 1

    def _try_parse_number(self):
        raise NotImplementedError

    # Read until next unescaped double quote
    def _try_parse_string(self):
        raise NotImplementedError

    def _try_parse_value(self, token):
        if self.json_string[self.position:].startswith(token.token_value):
            self.position += len(token.token_value)
            return token
        raise ParsingException(
            'Invalid token at position {}. Expected "{}".'.format(
                self.position,
                token.token_value,
            )
        )

    def next(self):
        peeked_token = self.peeked_token
        if peeked_token:
            self.position += len(peeked_token)
            self.peeked_token = None
            return peeked_token

        self._advance_to_non_whitespace()

        if self.position >= len(self.json_string):
            return Token(TokenType.EOF, '', self.position)

        token_action_mapper = {
            't': lambda: self._try_parse_value(Token(TokenType.TRUE, 'true', self.position)),
            'f': lambda: self._try_parse_value(Token(TokenType.FALSE, 'false', self.position)),
            'n': lambda: self._try_parse_value(Token(TokenType.NULL, 'null', self.position)),
            '"': lambda: self._try_parse_string(),
            '{': lambda: Token(TokenType.START_OBJECT, '{', self.position),
            '}': lambda: Token(TokenType.END_OBJECT, '}', self.position),
            '[': lambda: Token(TokenType.START_ARRAY, '[', self.position),
            ']': lambda: Token(TokenType.END_ARRAY, ']', self.position),
            ':': lambda: Token(TokenType.COLON, ':', self.position),
            ',': lambda: Token(TokenType.COMMA, ',', self.position),
        }

        token_action = token_action_mapper.get(self.json_string[self.position], self._try_parse_number)
        return self._action_and_advance(token_action)

    def peek(self):
        if not self.peeked_token:
            self.peeked_token = self.next()
        return self.peeked_token


class ParsingException(Exception):
    pass
