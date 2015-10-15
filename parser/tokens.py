# This file defines all the tokens used by the JSON parser.
from enum import Enum

from parser import EqualityMixin


class InvalidTokenFormatError:
    PARAM_NAME = None
    EXPECTED_TYPE = None

    def __init__(self, param_name, expected_type):
        self.PARAM_NAME = param_name
        self.EXPECTED_TYPE = expected_type


class TokenType(Enum):
    EOF = 1

    TRUE = 2
    FALSE = 3

    COLON = 4
    COMMA = 5

    START_OBJECT = 6
    END_OBJECT = 7

    START_ARRAY = 8
    END_ARRAY = 9

    NULL = 10
    NUMBER = 11
    STRING = 12

    OTHER = 13


class Token(EqualityMixin):

    def __init__(self, token_type, token_value, token_position):
        try:
            if not isinstance(token_type, TokenType):
                raise InvalidTokenFormatError('token_type', 'parser.tokens.TokenType')
            self.token_type = token_type

            if not isinstance(token_value, basestring):
                raise InvalidTokenFormatError('token_type', 'str')
            self.token_value = token_value

            if not isinstance(token_position, (int, long)):
                raise InvalidTokenFormatError('token_position', 'int')
            self.token_position = token_position
        except InvalidTokenFormatError as err:
            raise TypeError('"{}" must be of type "{}"!', err.PARAM_NAME, err.EXPECTED_TYPE)

    def __eq__(self, obj):
        return (
            self.token_type == token.token_type
            and self.token_value == token.token_value
            and self.token_position == token.token_position
        )
