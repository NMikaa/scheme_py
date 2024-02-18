class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class ProgramNode(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions

class LambdaNode(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class DefineNode(ASTNode):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class SymbolNode(ASTNode):
    def __init__(self, name):
        self.name = name

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements
class CallNode(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments
class ArithmeticOperatorNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
class LogicalOperatorNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
class ListOperationNode(ASTNode):
    def __init__(self, operation, arguments):
        self.operation = operation
        self.arguments = arguments
class ApplyNode(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments
class EvalNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression