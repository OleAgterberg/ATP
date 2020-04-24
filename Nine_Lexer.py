from typing import List, Union

#    '\-?[0-9]+'     : 'INTEGER',
#    '[a-zA-Z0-9]+'  : 'IDENTIFIER',

'''
https://esolangs.org/wiki/Nine
Instruction       Action
#VAR.VAL	      VAR = VAL ("_" is replaced with a space)
#VAR+<value>	  VAR += <value>
#VAR-<value>	  VAR -= <value>
#VAR.*            VAR = user-input
$VAR$	          Call a variable
>TEXT	          Print Text
>TEXT*	          Print Text without \n
>$VAR$	          Print Variable
>$VAR$*	          Print Variable without \n
!	              One line down
end	              End program
(A|B)	          if A != B, one line down
(A%B)	          if A % B != 0, one line down
;	              Begin of a comment, have to be at the start of a line
~INSTRUCTION      Run a command once (Then ignored in main-loop)

Lexer is not perfect becease,
the tokens in the instructions are not separated with a space or something.

'''

class Nine_Lexer(object):
    def __init__(self):
        self.token_dict = {
            '#'         : 'VARIABLE',
            '.'         : 'ASSIGN',
            '+'         : 'ADD',
            '-'         : 'MIN',
            '.*'        : 'INPUT',
            '$'  	    : 'CALL',
            '>'         : 'PRINT',
            '*'         : 'PRINT_WO_NL',          #Without new line
            '!'         : 'LINE_DOWN',
            'end'       : 'END',
            '('         : 'LPAREN',
            ')'         : 'RPAREN',
            '|'         : 'NOT_EQUAL',          #Changed! A|B -> A != B
            '%'         : 'NOT_MOD',          #Changed! A%B -> A % B != 0
            ';'         : 'COMMENT',
            '~'         : 'RUN_ONCE',
        }

    # returns the identifier.
    # instruction_to_identifier :: [Char] -> [Char]
    def instruction_to_identifier(self, instruction: str) -> str:
        if instruction == []:
            return ''
        head, *tail = instruction
        if head in ['.', '+', '-', ' ', '$']:
            return ''
        if head == '_':
            head = ' '
        return head + self.instruction_to_identifier(tail)

    # instruction_to_interger :: [Char] -> [Char]
    def instruction_to_interger(self, instruction: str) -> str:
        if instruction == []:
            return ''
        head, *tail = instruction
        if head.isdigit():
            return head + self.instruction_to_interger(tail)
        else: #error??
            return ''

    # returns tokens of instructions
    # instruction_to_tokens :: [Char] -> [String]
    def instruction_to_tokens(self, instruction : str) -> List[str]:
        if instruction == 'end':
            return [self.token_dict[instruction]]
        if instruction == [] or instruction == '':
            return []
        head, *tail = instruction
        # separated if statement becease * is used as input as print wo nl
        if head == '.' and tail[0] == '*':
            return [self.token_dict[head], 'INPUT']
        # if head char is a token add token
        # else add interger or identifier
        if head in self.token_dict.keys():
            return [self.token_dict[head]] + self.instruction_to_tokens(tail)
        elif head.isdigit():
            interger = self.instruction_to_interger(instruction)
            return [interger] + self.instruction_to_tokens(instruction[len(interger):])
        else:
            identifier = self.instruction_to_identifier(instruction)
            return [identifier] + self.instruction_to_tokens(instruction[len(identifier):])

    # returns tokens of a line
    # line_to_token :: [Char] -> [String]
    def line_to_tokens(self, line : str) -> Union[List[str], int]:
        if line == []:
            return []
        end = line.find(' ')
        # if multiple instructions in line
        if end != -1:
            instruction, tail = line[:end], line[end + 1:]
            return self.instruction_to_tokens(instruction) + self.line_to_tokens(tail)
        # just one instruction on line
        return self.instruction_to_tokens(line) # last instruction of line

    # returns tokens in a text file
    def text_to_tokens(self, text : str) -> List[str]:
        end = text.find('\n')
        if end != -1:
            line, tail = text[:end], text[end + 1:]
            #print('tail = ', tail)
            if len(line) == 0 or line[0] == ';':  # commentsymbol or empty ignore line
                return self.text_to_tokens(tail)
            else:
                return self.line_to_tokens(line) + self.text_to_tokens(tail) #['LINE_DOWN'] + self.text_to_tokens(tail)
        return self.line_to_tokens(text) #last line of text
