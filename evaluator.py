import math
import operator as op
from utils import *


class Evaluator:
    def __init__(self):
        self.global_env = self.standard_environment()

    def create_lambda(self, args, body, env):
        def lambda_fn(*new_args):
            if len(new_args) != len(args):
                print("Error: Lambda function arguments size error")
                return AssertionError
            new_env = SchemeEnvironment(args, new_args, env)
            return self.evaluate(body, new_env)

        return lambda_fn

    @staticmethod
    def standard_environment():
        env = SchemeEnvironment()
        env.update(vars(math))
        env.update({
            'remainder': remainder,
            '+': add, '-': subtract, '*': multiply, '/': divide,
            '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
            'abs': abs, 'append': scheme_append, "or": op.or_, "and": op.and_,
            'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'cons': lambda x, y: [x] + y,
            'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list),
            'map': lambda func, lst: list(map(func, lst)), 'max': max, 'min': min, 'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, (int, float)),
            'round': round, 'symbol?': lambda x: isinstance(x, str), 'equal?': lambda x, y: x == y, 'display': print,
            'length': lambda x: len(x)
        })
        return env

    def handle_define(self, expression, env):
        (_, var, exp) = expression
        if isinstance(var, list):
            func_name = var[0]
            func_args = var[1:]
            func_body = exp
            env[func_name] = self.create_lambda(func_args, func_body, env)
        else:
            env[var] = self.evaluate(exp, env)

    def handle_lambda(self, expression, env):
        (_, params, body) = expression
        return self.create_lambda(params, body, env)

    def handle_if(self, expression, env):
        condition = expression[1]
        conseq = expression[2]
        alt = expression[3] if len(expression) > 3 else None
        return self.evaluate(conseq if self.evaluate(condition, env) else alt, env)

    def handle_set(self, expression, env):
        (_, var, exp) = expression
        env.find(var)[var] = self.evaluate(exp, env)

    def handle_eval(self, expression, env):
        inner_expression = self.evaluate(expression[1], env)
        return self.evaluate(inner_expression, env)

    def handle_apply(self, expression, env):
        function = self.evaluate(expression[1], env)

        args_expr = expression[2]
        if args_expr[0] == "quote":
            args = args_expr[1]
        else:
            args = self.evaluate(args_expr, env)

        if isinstance(args, list):
            return function(*args)
        else:
            return function(args)

    @staticmethod
    def handle_bool_list_str(expression, env):
        if expression == "#t":
            return True
        elif expression == "#f":
            return False
        elif isinstance(expression, str) and not expression.startswith('"'):
            # It's a symbol, so look it up in the environment.
            return env.find(expression)[expression]
        elif isinstance(expression, str):
            # It's a string literal. Remove the quotes and return the string itself.
            return expression.strip('"')
        elif not isinstance(expression, list):
            return expression
        else:
            return None

    def evaluate(self, expression, env):
        test_bool_list_str = self.handle_bool_list_str(expression, env)
        if test_bool_list_str is not None:
            return test_bool_list_str
        operator = expression[0]
        expr_handlers = {
            "quote": lambda exp: exp[1],
            "if": lambda exp: self.handle_if(exp, env),
            "define": lambda exp: self.handle_define(exp, env),
            "lambda": lambda exp: self.handle_lambda(exp, env),
            "set!": lambda exp: self.handle_set(exp, env),
            "eval": lambda exp: self.handle_eval(exp, env),
            'apply': lambda exp: self.handle_apply(exp, env)
        }

        if operator in expr_handlers:
            return expr_handlers[operator](expression)
        else:
            proc = self.evaluate(operator, env)
            args = [self.evaluate(arg, env) for arg in expression[1:]]
            return proc(*args)

    def run_evaluator(self, test):
        parsed_test = parse(test)
        return self.evaluate(parsed_test, self.global_env)

    def repl(self):
        """A prompt-read-eval-print loop."""
        cnt = 1
        while True:
            prompt = f'#|kawa:{cnt}|#:'
            test = input(prompt)
            if test is not None:
                result = self.run_evaluator(test)
                if result:
                    print("#t")
                elif not result:
                    print("#f")
                elif result is not None:
                    print(result)
            cnt += 1
