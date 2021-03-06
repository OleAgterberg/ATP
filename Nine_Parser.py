from typing import List, Union, Tuple
from Instruction import Instruction
from Token import Token
import AST


class Nine_Parser(object):
    def __init__(self):
        pass

    # parse :: [[Instruction]] -> ([[AST_OR_NONE]] -> Interger)
    def parse(self, instructions: List[List[Instruction]]) -> Tuple[ Union[List[List[AST.AST]], None], int]:
        if instructions == []:
            return [], 1
        head, *tail = instructions
        head = self.parse_line(head)
        if head == None:
            return (None, 1)
        tail, line = self.parse(tail)
        if tail == None:
            return (None, (line + 1))
        return ([head] + tail, (line + 1))

    # parse_line :: [Instruction] -> [AST_OR_NONE]
    def parse_line(self, instructions: List[Instruction]) -> Union[List[AST.AST], None]:
        if instructions == []:
            return []
        head, *tail = instructions
        head = self.parse_to_AST(head.tokens)
        if head == None:
            return None
        tail = self.parse_line(tail)
        if tail == None:
            print(None)
            return None
        return [head] + tail

    # parse_to_AST :: [Token] -> AST_OR_NONE
    def parse_to_AST(self, tokens : List[Token]) -> Union[AST.AST, None]:
        if tokens == []:
            return []
        head, *tail = tokens
        try:
            if head.name == 'COMMENT':
                return AST.AST(f = AST.empty)

            #just ignore varaible token it's not used
            if head.name == 'VARIABLE':
                return self.parse_to_AST(tail)

            # interger: Number
            if head.name == 'INTERGER':
                interger = AST.AST(value = head.value)
                return interger

            # identifier / string
            if head.name == 'IDENTIFIER':
                if not tail or tail[0].name == 'RPAREN' or tail[0].name == 'PRINT_WO_NL':
                    identifier = AST.AST(value = head.value)
                    return identifier

            # call a vrariable
            if head.name == 'CALL' and tail[0].name == 'IDENTIFIER':
                if tail[1].name == 'CALL':
                    call = AST.AST(f = AST.call)
                    call.right = AST.AST(name = tail[0].value)
                    return call
                return None

            # input
            elif head.name == 'INPUT':
                return AST.AST(f = AST.my_input)

            # run_once
            elif head.name == 'RUN_ONCE':
                run_once = AST.AST(f = AST.run_once)
                run_once.right = self.parse_to_AST(tail)
                return run_once

            # assign
            elif head.name == 'IDENTIFIER' and tail[0].name == 'ASSIGN':
                opperator = AST.AST(f = AST.assign)
                opperator.left = AST.AST(name = head.value)
                opperator.right = self.parse_to_AST(tail[1:])
                return opperator

            # add
            elif head.name == 'IDENTIFIER' and tail[0].name == 'ADD':
                opperator = AST.AST(f = AST.add)
                opperator.left = AST.AST(f = AST.call)
                opperator.left.right = AST.AST(name = head.value)
                opperator.right = self.parse_to_AST(tail[1:])
                return opperator

            # min
            elif head.name == 'IDENTIFIER' and tail[0].name == 'MIN':
                opperator = AST.AST(f = AST.min)
                opperator.left = AST.AST(f = AST.call)
                opperator.left.right = AST.AST(name = head.value)
                opperator.right = self.parse_to_AST(tail[1:])
                return opperator

            # print
            elif head.name == "PRINT":
                func = AST.my_print_ln if not self.name_in_list(tail, 'PRINT_WO_NL') else AST.my_print
                pri = AST.AST(f = func)
                pri.right = self.parse_to_AST(tail)
                return pri

            # if statement
            elif head.name == 'LPAREN':
                if self.name_in_list(tail, 'NOT_EQUAL'):
                    left = self.list_until_name(tail, 'NOT_EQUAL')
                    func = AST.not_equal
                else:
                    left = self.list_until_name(tail, 'NOT_MOD')
                    func = AST.modus
                right = tail[ len(left)+1: ]
                sign = AST.AST(f = func)
                sign.left = self.parse_to_AST(left)
                sign.right = self.parse_to_AST(right)
                return sign

            # end
            elif head.name == 'END':
                return AST.AST(f = AST.end)

            # line down
            elif head.name == 'LINE_DOWN':
                return AST.AST(f = AST.line_down)

            # debug
            elif head.name == 'DEBUG':
                return AST.AST(f = AST.debug)

            else:
                return None
        except Exception as e:
            return None

    # returns if token with name 'name' in list of tokens
    # name_in_list :: ([Token] -> str) -> bool
    def name_in_list(self, tokens : List[Token], name : str) -> bool:
        if tokens == []:
            return False
        head, *tail = tokens
        if head.name == name:
            return True
        return self.name_in_list(tail, name)

    # list_until_name :: ([Token] -> str) -> [Token]
    def list_until_name(self, tokens : List[Token], name : str) -> List[Token]:
        if tokens == []:
            return []
        head, *tail = tokens
        if head.name == name:
            return []
        return [head] + self.list_until_name(tail, name)
