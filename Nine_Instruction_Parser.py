from typing import List, Callable
from Token import Token
from Instruction import Instruction

class Nine_Instruction_Parser(object):
    def __init__(self):
        pass

    # makes from a list of tokens a list of instructions
    # parse :: [[Token]] -> [[Instruction]]
    def parse(self, tokens : List[List[Token]]) -> List[List[Instruction]]:
        if tokens == []:
            return []
        head, *tail = tokens
        ends = self.combine_instructions(self.combine_until_end_instruction, head)
        begins = self.parse_begin_instructions(ends)
        return [self.parse_to_instruction(begins)] + self.parse(tail)

    # Makes from a list of token lists a list of instructions
    # parse_to_instruction :: [[Token]] ->  [Instruction]
    def parse_to_instruction(self, tokens : List[List[Token]]) -> List[Instruction]:
        if tokens == []:
            return []
        head, *tail = tokens
        return [Instruction(head)] + self.parse_to_instruction(tail)

    # return a list instructions (an instruction is a list of tokens)
    # parse_begin_instructions :: [[Token]] -> [Token]
    def parse_begin_instructions(self, tokens : List[List[Token]]) -> List[Token]:
        if tokens == []:
            return []
        head, *tail = tokens
        head += self.parse_begin_instruction(tail)
        head_count = self.parse_begin_instruction_count(tail)
        tail = tokens[head_count + 1:]
        return [head] + self.parse_begin_instructions(tail)

    # Combines lists if list does not begins with a "Begin token".
    # returns the combined list if the next list is beginning with a "Begin token"
    # parse_begin_instructionst :: [[Token]] -> [Token]
    def parse_begin_instruction(self, tokens : List[List[Token]]) -> List[Token]:
        if tokens == []:
            return []
        head, *tail = tokens
        begin_tokens = ['VARIABLE', 'PRINT', 'RUN_ONCE', 'LINE_DOWN', 'END', 'LPAREN', 'DEBUG']
        if head[0].name not in begin_tokens:
            return head + self.parse_begin_instruction(tail)
        else:
            return []

    # Returns a count of how many lists are sequentially not beginning with a "begin token"
    # if list does not begins with a starting token.
    # parse_begin_instructionst :: [[Token]] -> int
    def parse_begin_instruction_count(self, tokens : List[List[Token]]) -> int:
        if tokens == []:
            return 0
        head, *tail = tokens
        begin_tokens = ['VARIABLE', 'PRINT', 'RUN_ONCE', 'LINE_DOWN', 'END', 'LPAREN', 'DEBUG']
        if head[0].name not in begin_tokens:
            return 1 + self.parse_begin_instruction_count(tail)
        else:
            return 0

    # returns a list of lists with tokens,
    # every list off tokens will end with a "end token"
    # combine_instructions :: ([Token] -> [Token]) -> [Token] -> [[Token]]
    def combine_instructions(self, f : Callable[[List[Token]], List[Token]], tokens : List[Token]) -> List[List[Token]]:
        if tokens == []:
            return []
        head = f(tokens) #self.combine_until_end_instruction(tokens)
        tail = tokens[len(head):]
        return [head] + self.combine_instructions(f, tail)

    # returns one list of tokens of a input list of tokens
    # return list will end on a "end token"
    # combine_until_end_instruction :: [Token] -> [Token]
    def combine_until_end_instruction(self, tokens : List[Token]) -> List[Token]:
        if tokens == []:
            return []
        last_token = ['CALL', 'INTERGER', 'IDENTIFIER', 'INPUT', 'PRINT_WO_NL', 'RPAREN', 'LINE_DOWN', 'END', 'DEGUB']
        head, *tail = tokens
        if head.name in last_token:
            return [head]
        else:
            return [head] + self.combine_until_end_instruction(tail)



'''
variable        : CALL IDENTIFIER CALL
                / INTERGER
                / IDENTIFIER
                / INPUT

define_variable : VARIABLE IDENTIFIER ASSIGN variable

modify_variable : VARIABLE IDENTIFIER ADD variable
                / VARIABLE IDENTIFIER MIN variable

print           : PRINT variable
                / PRINT variable PRINT_WO_NL

line_down       : LINE_DOWN

program_end     : END

if_statement    : LPAREN variable NOT_EQUAL variable RPAREN
                / LPAREN variable NOT_MOD variable RPAREN

run_once        : RUN_ONCE define_variable
                / RUN_ONCE modify_variable
                / RUN_ONCE print

'''
