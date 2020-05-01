from Nine_Lexer import Nine_Lexer
from Nine_Parser import Nine_Parser
import sys, enum

lexer = Nine_Lexer()
parser = Nine_Parser()


file = open(sys.argv[1])

text = file.read()

tokens = lexer.text_to_tokens(text)

print('Tokens: ')
for token in tokens:
    print(token)

instructions = parser.parse(tokens)

print('Instructions: ')
for instruction in instructions:
    print(instruction)
