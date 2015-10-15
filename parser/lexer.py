import re

from tokens import Token
from tokens import TokenType


class Lexer:

    _json_string = None
    _peeked_token = None
    _position = None

    def has_next(self):
        return self.peek().token_type != TokenType.EOF

    def next(self):
        peeked_token = self._peeked_token
        if peeked_token:
            self._position += len(peeked_token.token_value)
            self._peeked_token = None
            return peeked_token

        self._advance_to_non_whitespace()

        if self._position >= len(self._json_string):
            return Token(TokenType.EOF, '', self._position)

        token_action_mapper = {
            't': lambda: self._try_parse_value(Token(TokenType.TRUE, 'true', self._position)),
            'f': lambda: self._try_parse_value(Token(TokenType.FALSE, 'false', self._position)),
            'n': lambda: self._try_parse_value(Token(TokenType.NULL, 'null', self._position)),
            '"': lambda: self._try_parse_string(),
            '{': lambda: Token(TokenType.START_OBJECT, '{', self._position),
            '}': lambda: Token(TokenType.END_OBJECT, '}', self._position),
            '[': lambda: Token(TokenType.START_ARRAY, '[', self._position),
            ']': lambda: Token(TokenType.END_ARRAY, ']', self._position),
            ':': lambda: Token(TokenType.COLON, ':', self._position),
            ',': lambda: Token(TokenType.COMMA, ',', self._position),
        }

        token_action = token_action_mapper.get(self._json_string[self._position], self._try_parse_number)
        return self._action_and_advance(token_action)

    def peek(self):
        if not self._peeked_token:
            self._peeked_token = self.next()
        return self._peeked_token

    def reset(self):
        self._peeked_token = None
        self._position = 0

    def __init__(self, json_string):
        self._json_string = json_string
        self.reset()

    def _action_and_advance(self, func):
        token = func()
        self._position += len(token.token_value)
        self._peeked_token = None
        return token

    def _advance_to_non_whitespace(self):
        while (self._position < len(self._json_string)
                and self._json_string[self._position].isspace()):
            self._position += 1

    def _try_parse_number(self):
        raise NotImplementedError

    # Read until next unescaped double quote
    def _try_parse_string(self):
        curr_pos = self._position + 1
        found_closing_quote = False
        even_num_successive_escape_chars = True

        while curr_pos < len(self._json_string):
            curr_char = self._json_string[curr_pos]
            if curr_char == '"' and even_num_successive_escape_chars:
                found_closing_quote = True
            elif curr_char == '\\':
                even_num_successive_escape_chars = not even_num_successive_escape_chars
            else:
                even_num_successive_escape_chars = True

            curr_pos += 1

        if not found_closing_quote:
           raise ParsingException(
               'Closing \'"\' not found for string token at position {}.'.format(
                   self._position,
               ),
           )

        return Token(
            token_type=TokenType.STRING,
            token_value=self._json_string[self._position:curr_pos],
            token_position=self._position,
        )


    def _try_parse_value(self, token):
        if self._json_string[self._position:].startswith(token.token_value):
            self._position += len(token.token_value)
            return token
        raise ParsingException(
            'Invalid token at position {}. Expected "{}".'.format(
                self._position,
                token.token_value,
            ),
        )


class ParsingException(Exception):
    pass
