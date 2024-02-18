Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list

def tokenize(chars: str):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
def read_from_tokens(tokens: list):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str):
    try:
        return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
def parse(code: str):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(code))




if __name__ == '__main__':
    code = "(define sum (lambda (x y) (+ x y)))"
    tokens = parse(code)
    print(tokens)