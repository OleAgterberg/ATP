from Nine_Lexer import Nine_Lexer
import sys, enum

lexer = Nine_Lexer()


file = open(sys.argv[1])

text = file.read()

tokens = lexer.text_to_tokens(text)

print(tokens)
