import re

class Scheme_Lexer:
    def __init__(self):
        self.token_specs = [
            ('NUMBER', r'\d+(\.\d+)?'),
            ('STRING', r'"([^"\\]|\\.)*"'),
            ('BOOLEAN', r'#[tf]'),
            ('SYMBOL', r'[^\s\(\)\d"][^\s\(\)]*'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('QUOTE', r"'"),
            ('OPERATOR', r'[+\-*/]'),
            ('LOGICAL', r'and|or'),
            ('COMMENT', r';[^\n]*'),
            ('WHITESPACE', r'\s+'),
            ('MISMATCH', r'.'),
        ]

    def tokenize(self, code):
        regex_pat = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specs)
        compiled_regex = re.compile(regex_pat)
        line_num = 1
        for mo in compiled_regex.finditer(code):
            value = mo.group()
            kind = mo.lastgroup
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind in ['WHITESPACE', 'COMMENT']:
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError()
            yield kind, value

if __name__ == '__main__':
    lexer = Scheme_Lexer()
    code = "(define sum (lambda (x y) (+ x y)))"
    tokens = list(lexer.tokenize(code))
    print(code)
    for token in tokens:
        print(token)