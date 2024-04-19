from enum import *

OP_SEQUENCE = '+-*/%()\0'

class TokenType(Enum):
    NUM    = 0  # NOTE: MUTABLE MNEMONIC
    ADD    = 1
    SUB    = 2
    MUL    = 3
    DIV    = 4
    PER    = 5
    LPA    = 6
    RPA    = 7
    END    = 8
    NOP    = 9

TOKEN_HASH = {
    'NUM'  : TokenType.NUM,
    '+'    : TokenType.ADD,
    '-'    : TokenType.SUB,
    '*'    : TokenType.MUL,
    '/'    : TokenType.DIV,
    '%'    : TokenType.PER,
    '('    : TokenType.LPA,
    ')'    : TokenType.RPA,
    '\0'   : TokenType.END,
    'NOP'  : TokenType.NOP,
}

class Token:
    def __init__(self, token_type: TokenType, src: str):
        self.token_type = token_type
        self.src        = src


class Expression:
    def __init__(self):
        pass

    def eval(self):
        pass


class NumberExpression(Expression):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def eval(self):
        return self.value


class BinaryExpression(Expression):
    def __init__(self, operation, expr1, expr2):
        super().__init__()
        self.operation = operation
        self.expr1     = expr1
        self.expr2     = expr2

    def eval(self):
        # match self.operation:
        #     case self.operation["+"]:
        #         return self.expr1.eval() + self.expr2.eval()
        #     case _:
        #         raise RuntimeError("Unknown operation")

        if self.operation == TokenType.ADD:
            return self.expr1.eval() + self.expr2.eval()
        elif self.operation == TokenType.SUB:
            return self.expr1.eval() - self.expr2.eval()
        elif self.operation == TokenType.MUL:
            return self.expr1.eval() * self.expr2.eval()
        elif self.operation == TokenType.DIV:
            return self.expr1.eval() / self.expr2.eval()
        elif self.operation == TokenType.PER:
            return self.expr1.eval() % self.expr2.eval()
        else:
            raise RuntimeError(f'Unsupported operation: {self.operation}')

class UnaryExpression(Expression):
    pass

