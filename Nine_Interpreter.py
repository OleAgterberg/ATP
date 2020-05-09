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
fname = sys.argv[1]
file = open(fname)
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
program, line = parser.parse(instructions)

if not program:
    print('Could not parse code at line %d' % line, end =' -> ')
    [print(i.value, end='') for i in tokens[line-1]]
    exit(-1)

# The current state with varaibles of the program
state = {}


# new_line :: Dict(str, int) -> Dict(str, int)
def new_line(state : Dict[str, int]) -> Dict[str, int]:
    if 'line_number' in state.keys():
        state['line_number'] += 1
    else:
        state['line_number'] = 1
    return state

# new_instruction :: Dict(str, int) -> Dict(str, int)
def new_instruction(state : Dict[str, int]) -> Dict[str, int]:
    if 'instruction_number' in state.keys():
        state['instruction_number'] += 1
    else:
        state['instruction_number'] = 1
    return state


# execute_program :: (Program -> Dict[str, int]) -> (Program -> Dict[str, int])
# Program = List[Line]
# line = List[AST]
def execute_program(program : List[List[AST]], state : Dict[str, int]) -> Tuple[ Union[List[List[AST]], None], Dict[str, int] ]:
    if program == []:
        return [], state
    line, *tail = program
    line, state = execute_line(line, state)
    state = new_line(state) #add line number for error correction
    if line == None:
        return None, state
    if 'instruction_number' in state.keys():
        del state['instruction_number'] #delete instruction number for new line
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

# Function execute a line.
# When the program gets a ""end"" command it returns None with the current program state
# Other wise it returns the line for the next round with the current program state
# execute_line :: (Line -> Dict[str, int]) -> (Line, Dict[str, int])
def execute_line(line : List[AST], state : Dict[str, int]) -> Tuple[ Union[List[AST], None], Dict[str, int] ]:
    if line == []:
        return [], state
    head, *tail = line
    result, state = head.getValue(state)
    state = new_instruction(state)
    if result == None:
        return None, state
    #print(state)
    if 'end' in state.keys():    	  # End program, return None
        #print('end')
        return None, state
    if 'run_once' in state.keys():     # execute line but don't return the run_once instruction
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
        return line, state # return the line and don't exectur the instruction

    if 'print' in state.keys():        # print value
        #print('print')
        print(state['print'], end='')
        del state['print']
    tail, state = execute_line(tail, state)
    line = [head] + tail if tail != None else None
    return line, state


try:
    # while program, execute program
    while program and len(program) > 0:
        program, state = execute_program(program, state)
        if not program and 'end' not in state.keys():
            raise Exception('')
        else:
            del state['line_number']
except Exception as e:
    print("\nError at line %d" % state['line_number'])
    print("On instruction %d" % state['instruction_number'])
    print('\nEnd of program\nProgram values: ')
    for key in state.keys():
        print(' ', key, ' = ', state[key])
except KeyboardInterrupt:
    print('\n\nKeyboardInterrupt!')
    print('Program values: ')
    for key in state.keys():
        print(' ', key, ' = ', state[key])



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
