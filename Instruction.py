from Token import Token
from typing import List, Union

class Instruction(object):
    def __init__(self, tokens : List[Token]) -> None:
        self.tokens = tokens

    def __str__(self) -> str:
        str_tokens = "".join([str(token) for token in self.tokens])
        return 'Instruction [%s]' % str_tokens
