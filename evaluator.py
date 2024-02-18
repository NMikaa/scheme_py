from utils import parse


class SchemeEnvironment(dict):
    def __init__(self, parameters=(), arguments=(), outer=None):
        self.update(zip(parameters, arguments))
        self.outer = outer

    def find(self, variable):
        return self if (variable in self) else self.outer.find(variable)


class Procedure(object):
    def __init__(self, parameters, body, env):
        self.parameters, self.body, self.env = parameters, body, env

    def __call__(self, *args):
        return evaluate(self.body, SchemeEnvironment(self.parameters, args, self.env))

def standard_environment():
    import math, operator as op
    env = SchemeEnvironment()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs, 'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'cons': lambda x, y: [x] + y,
        'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list),
        'map': map, 'max': max, 'min': min, 'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)), 'print': print,
        'round': round, 'symbol?': lambda x: isinstance(x, str),
    })
    return env


global_env = standard_environment()


def evaluate(expression, env=global_env):
    # print(f"Evaluating: {expression}")  # Debug print
    if isinstance(expression, str):
        return env.find(expression)[expression]
    elif not isinstance(expression, list):
        return expression

    expr_type = expression[0]
    expr_handlers = {
        'quote': lambda exp: exp[1],
        'if': lambda exp: create_lambda(exp[1], exp[2], env),
        'define': lambda exp: define_variable(exp[1], exp[2], env),
        'set!': lambda exp: update_variable(exp[1], exp[2], env),
        'lambda': lambda exp: create_lambda(exp[1], exp[2], env),
    }
    if expr_type in expr_handlers:
        return expr_handlers[expr_type](expression)
    else:
        procedure = evaluate(expression[0], env)
        arguments = [evaluate(arg, env) for arg in expression[1:]]
        return procedure(*arguments)


def define_variable(variable, expression, env):
    env[variable] = evaluate(expression, env)


def update_variable(variable, expression, env):
    env.find(variable)[variable] = evaluate(expression, env)


def create_lambda(parameters, body, env):
    return Procedure(parameters, body, env)


if __name__ == '__main__':
    test_code1 = '''(define circle-area (lambda (r) (* pi (* r r)))) (circle-area (+ 5 5))'''
    print(evaluate(parse(test_code1), global_env))


