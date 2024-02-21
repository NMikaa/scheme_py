from utils import *
import math, operator as op



def create_lambda(args, body, env):
    def lambda_fn(*new_args):
        if len(new_args) != len(args):
            print("Error: Lambda function arguments size error")
            return AssertionError
        new_env = SchemeEnvironment(args, new_args, env)
        return evaluate(body, new_env)

    return lambda_fn

def define_variable(variable, expression, env):
    env[variable] = evaluate(expression, env)

def update_variable(variable, expression, env):
    env.find(variable)[variable] = evaluate(expression, env)
def scheme_append(*args):
    result = []
    for arg in args:
        result.extend(arg)
    return result
def standard_environment():
    env = SchemeEnvironment()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs, 'append': scheme_append,
        'apply': lambda proc, args: proc(*args),
        'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'cons': lambda x, y: [x] + y,
        'list': lambda *x: list(x), 'list?': lambda x: isinstance(x, list),
        'map': lambda func, lst: list(map(func, lst)), 'max': max, 'min': min, 'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)), 'print': print,
        'round': round, 'symbol?': lambda x: isinstance(x, str),
    })
    return env


global_env = standard_environment()


def evaluate(expression, env=global_env):
    # print("Evaluating:", expression)
    # String literals
    # print("Evaluating:", expression)
    if isinstance(expression, str):
        return env.find(expression)[expression]
    # Non-list expressions
    elif not isinstance(expression, list):
        return expression

    # List expressions
    op = expression[0]
    if op == 'quote':
        return expression[1]
    elif op == 'if':
        (_, test, conseq, alt) = expression
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)
    elif op == 'define':
        (_, var, exp) = expression
        if isinstance(var, list):  # Handling function definitions
            func_name = var[0]
            func_args = var[1:]
            func_body = exp
            env[func_name] = create_lambda(func_args, func_body, env)
        else:
            env[var] = evaluate(exp, env)
    elif op == 'set!':
        (_, var, exp) = expression
        env.find(var)[var] = evaluate(exp, env)
    elif op == 'lambda':
        (_, params, body) = expression
        return create_lambda(params, body, env)
    else:  # Procedure call
        proc = evaluate(op, env)
        args = [evaluate(arg, env) for arg in expression[1:]]
        return proc(*args)




if __name__ == '__main__':
    list_of_tests = [
                    '''(define (remove num l) (if (= (car l) num) (cdr l) (cons (car l) (remove num (cdr l)))))''',
                     "(define (permute ll) (if (null? ll) '(()) (apply append (map (lambda (x1) (map (lambda (y1) (cons x1 y1)) (permute (remove x1 ll)))) ll))))",
                     "(define (helper t) (apply append (map (lambda (x1) (map (lambda (y1) (cons x1 y1)) (permute (remove x1 t)))) t)))",
                     "(helper '(1))",
                      "(permute '(1))"
                   ]
    env = standard_environment()
    for test in list_of_tests:
        print(evaluate(parse(test), env))
