from ast_nodes import *
from lexer import Scheme_Lexer


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        ast = []
        while self.current_token is not None:
            expression = self.parse_expression()
            if expression is not None:
                ast.append(expression)
            if self.current_token is not None:
                self.next_token()
        return ast

    def parse_expression(self):
        if self.current_token[0] == 'LPAREN':
            return self.parse_list()  # Renamed and modified
        elif self.current_token[0] in ['+', '-', '*', '/']:
            return self.handle_arithmetic()
        elif self.current_token[0] in ['and', 'or']:
            return self.handle_logical_ops()
        elif self.current_token[0] in ['car', 'cdr', 'cons', 'apply', 'eval']:
            return self.handle_special_operations()
        else:
            return self.parse_atom()

    def handle_special_forms(self, elements):
        if not elements:
            return None

        first, *rest = elements
        if first == 'lambda':
            return self.handle_lambda(rest)
        elif first == 'define':
            return self.handle_define(rest)
        elif first == 'if':
            return self.handle_if(rest)
        else:
            # Default: Treat it as a function call
            return CallNode(first, rest)
    def parse_list(self):
        self.next_token()  # Skip '('
        elements = []
        while self.current_token is not None and self.current_token[0] != 'RPAREN':
            elements.append(self.parse_expression())
        if self.current_token is None:
            raise SyntaxError("Expected ')', got EOF")
        self.next_token()  # Skip ')'

        if not elements:
            return ListNode([])  # Handle empty list case

        return self.handle_special_forms(elements) or CallNode(elements[0], elements[1:])

    def parse_atom(self):
        token = self.current_token
        self.next_token()
        if token[0] == 'NUMBER':
            return NumberNode(float(token[1]))  # Consider numbers as floats
        elif token[0] == 'SYMBOL':
            return SymbolNode(token[1])
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def handle_arithmetic(self):
        operator = self.current_token[0]
        self.next_token()
        left_expr = self.parse_expression()
        right_expr = self.parse_expression()
        return ArithmeticOperatorNode(operator, left_expr, right_expr)

    def handle_special_operations(self):
        operation = self.current_token[0]
        self.next_token()
        args = []
        while self.current_token is not None and self.current_token[0] != 'RPAREN':
            args.append(self.parse_expression())
        if self.current_token is None:
            raise SyntaxError("Expected ')', got EOF")
        self.next_token()  # Skip ')'

        if operation == 'car':
            if len(args) != 1:
                raise SyntaxError("car expects one argument")
            return ListOperationNode(operation, args)
        elif operation == 'cdr':
            if len(args) != 1:
                raise SyntaxError("cdr expects one argument")
            return ListOperationNode(operation, args)
        elif operation == 'cons':
            if len(args) != 2:
                raise SyntaxError("cons expects two arguments")
            return ListOperationNode(operation, args)
        elif operation == 'apply':
            if len(args) != 2:
                raise SyntaxError("apply expects two arguments")
            return ApplyNode(args[0], args[1])
        elif operation == 'eval':
            if len(args) != 1:
                raise SyntaxError("eval expects one argument")
            return EvalNode(args[0])
        else:
            raise SyntaxError(f"Unknown operation: {operation}")

    def handle_logical_ops(self):
        operator = self.current_token[0]  # Either 'and' or 'or'
        self.next_token()
        left_expr = self.parse_expression()
        right_expr = self.parse_expression()
        return LogicalOperatorNode(operator, left_expr, right_expr)


if __name__ == "__main__":
    lexer = Scheme_Lexer()
    tokens = lexer.tokenize("(define square (lambda (x) (* x x)))")
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
    print("AST!")
