from Nine_Lexer import Nine_Lexer
from Nine_Instruction_Parser import Nine_Instruction_Parser
from Nine_Parser import Nine_Parser
from AST import AST
import sys, enum
from typing import List, Union, Tuple, Dict

lexer = Nine_Lexer()
instruction_parser = Nine_Instruction_Parser()
parser = Nine_Parser()

# open file
file = open(sys.argv[1])
text = file.read()

# Difference between the tokens and instructions:
# A line can have mulitple Tokens
# A line can also have multiple instructions.
# An instruction consists almost always of mulitple tokens.


# text to list with lists of tokens :: String -> [[Token]]
tokens = lexer.text_to_tokens(text)

# list with lists of tokens to a list with lists of instructions :: [[Token]] -> [[Instruction]]
# An Instruction is a list of Tokens: Instruction = [Token]
instructions = instruction_parser.parse(tokens)

# Convert the list with lists of instructions to a list with list of ASTs
# Every list in the list is a line in the code.
# Every AST is a Instruction on the line.
# With the function AST.getValue() the Instruction will be executed.
# parse :: [[Instruction]] -> [[AST]]
program = parser.parse(instructions)

# The current state with varaibles of the program
state = {}

# execute_program :: (Program -> Dict[str, int]) -> (Program -> Dict[str, int])
def execute_program(program : List[List[AST]], state : Dict[str, int]) -> Tuple[ Union[List[List[AST]], None], Dict[str, int] ]:
    if program == []:
        return [], state
    line, *tail = program
    line, state = execute_line(line, state)
    if line == None:
        return None, state
    if 'line_down' in state.keys():
        del state['line_down']
        # skip next line, but keep it for next loop
        new_tail, state = execute_program(tail[1:], state)
        tail = [tail[0]] + new_tail
    else:
        tail, state = execute_program(tail, state)
    if tail == None:
        return None, state
    program = [line] + tail
    return program, state

# execute_line :: (Line -> Dict[str, int]) -> (Line, Dict[str, int])
def execute_line(line : List[AST], state : Dict[str, int]) -> Tuple[ Union[List[AST], None], Dict[str, int] ]:
    if line == []:
        return [], state
    head, *tail = line
    result, state = head.getValue(state)
    #print(state)
    if 'end' in state.keys():    	  # End program, return None
        #print('end')
        return None, state
    if 'run_once' in state.keys():     # execute line but don't this instruction
        #print('run_once')
        del state['run_once']
        tail, state = execute_line(tail, state)
        # run_once so don't return this instruction
        return tail, state
    if 'line_down' in state.keys():    # skip all next instructions on line but return all instructions
        #print('line_down')
        return line, state
    if 'if' in state.keys():           # A%B == 0 or A==B -> if statment if true skip next instructions on the line
        #print('if')
        del state['if']
        '''
        if len(tail) > 0:
            new_tail, state = execute_line(tail[1:], state)
            return ([head] + [tail[0]] + new_tail, state)
        '''
        return line, state # needs to be a instruction after a if statement

    if 'print' in state.keys():        # print value
        #print('print')
        print(state['print'], end='')
        del state['print']
    tail, state = execute_line(tail, state)
    line = [head] + tail if tail != None else None
    return line, state


# while program, execute program
while program and len(program) > 0:
    program, state = execute_program(program, state)


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
