Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list


def tokenize(chars: str):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


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
