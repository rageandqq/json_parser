# This file defines all the tokens used by the JSON parser.
from enum import Enum

class InvalidTokenFormatError:
    PARAM_NAME = None
    EXPECTED_TYPE = None

    def __init__(self, param_name, expected_type):
        self.PARAM_NAME = param_name
        self.EXPECTED_TYPE = expected_type

class TokenType(Enum):
    EOF = 1

    true = 2
    false = 3

    colon = 4
    comma = 5

    start_object = 6
    end_object = 7

    start_array = 8
    end_array = 9

    null = 10
    number = 11
    string = 12

    other = 13

class Token:

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
