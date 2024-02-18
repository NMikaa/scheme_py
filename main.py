from lexer import Scheme_Lexer
from scheme_parser import Parser
from evaluator import *

scheme_code = """
(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1))))); (factorial 5) 
"""
lexer = Scheme_Lexer()
tokens = lexer.tokenize(scheme_code)

parser_object = Parser(tokens)
ast = parser_object.parse()
print(ast[0])

for expression in ast:
    # You might need to adjust, depending on your AST output
    result = evaluate(expression)
    print(result)
