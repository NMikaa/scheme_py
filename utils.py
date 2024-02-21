Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list


class SchemeEnvironment(dict):
    def __init__(self, parameters=(), arguments=(), outer=None):
        self.update(zip(parameters, arguments))
        self.outer = outer

    def find(self, variable):
        if variable in self:
            return self
        elif self.outer is not None:
            return self.outer.find(variable)
        else:
            raise KeyError(f"Variable '{variable}' not found in environment")


def tokenize(chars: str):
    # Replace newlines with spaces and tokenize the input
    chars = chars.replace('\n', ' ').replace('(', ' ( ').replace(')', ' ) ').split()

    tokens = []

    in_string = False
    current_string = ""

    for ch in chars:
        if ch.startswith('"'):
            in_string = True
            current_string = ch
        elif in_string:
            current_string += " " + ch
            if ch.endswith('"'):
                tokens.append(current_string)
                in_string = False
        else:
            tokens.append(ch)

    return tokens


def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF while reading")
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == "'":
        return ['quote', read_from_tokens(tokens)]
    else:
        return atom(token)


def atom(token: str):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def parse(code: str):
    return read_from_tokens(tokenize(code))


def scheme_append(*args):
    result = []
    for arg in args:
        result.extend(arg)
    return result


def add(*args):
    return sum(args)


def subtract(*args):
    if len(args) == 0:
        raise TypeError("Expected at least one argument")
    if len(args) == 1:
        return -args[0]
    return args[0] - sum(args[1:])


def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


def divide(*args):
    if len(args) == 0:
        raise TypeError("Expected at least one argument")
    if len(args) == 1:
        return 1 / args[0]
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result


def remainder(a, b):
    return a % b


