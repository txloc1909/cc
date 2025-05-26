from typing import List, Any
from dataclasses import dataclass, field


__all__ = [
    "Parser",
    "ParserError",
]


@dataclass
class Expr:
    pass


@dataclass
class UnaryExpr(Expr):
    op: str
    rhs: Expr


@dataclass
class Literal(Expr):
    type: str
    value: Any


@dataclass
class Statement:
    type: str
    value: Expr


@dataclass
class Function:
    type: str = "Function"
    name: str = "main"
    body: Statement = field(
        default_factory=lambda: Statement(
            type="ReturnStatement", value=Literal(value=0)
        )
    )


@dataclass
class Program:
    functions: List[Function] = field(default_factory=list)


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = [token for token in tokens if token[0] != "COMMENT"]
        self.curr = 0

    @property
    def current_token(self):
        return self.tokens[self.curr] if self.curr < len(self.tokens) else None

    # <program> ::= <function> { <function> }
    def parse_program(self):
        functions = []
        while self.current_token is not None:
            functions.append(self.parse_function())

        if not functions:
            raise ParserError("No valid top-level program found")

        return Program(functions=functions)

    # <function> ::= "int" <identifier> "(" "void" ")" "{" <statement> "}"
    def parse_function(self):
        self.expect("KEYWORD")  # Expect "int"
        _, identifier = self.expect("IDENTIFIER")  # Expect function name
        self.expect("LPAREN")  # Expect "("
        self.expect("KEYWORD")  # Expect "void"
        self.expect("RPAREN")  # Expect ")"
        self.expect("LBRACE")  # Expect "{"
        statement = self.parse_statement()  # Parse the statement
        self.expect("RBRACE")  # Expect "}"
        return Function(type="Function", name=identifier, body=statement)

    # <statement> ::= "return" <exp> ";"
    def parse_statement(self):
        self.expect("KEYWORD")  # Expect "return"
        expression = self.parse_exp()  # Parse the expression
        self.expect("SEMICOLON")  # Expect ";"
        return Statement(type="ReturnStatement", value=expression)

    # <exp> ::= <unary_op> <exp> | <int>
    def parse_exp(self):
        next_type = self.current_token[0] if self.current_token else None
        if next_type == "INTEGER_CONST":
            return self.parse_int()
        else:
            return self.parse_unary()

    # <unary_op> ::= "-" | "~" | "-"
    def parse_unary(self):
        match self.current_token:
            case ("MINUS", "-"):
                self.advance()
                return UnaryExpr(op="-", rhs=self.parse_exp())
            case ("TILDE", "~"):
                self.advance()
                return UnaryExpr(op="~", rhs=self.parse_exp())
            case ("BANG", "!"):
                self.advance()
                return UnaryExpr(op="!", rhs=self.parse_exp())
            case _:
                raise ParserError(f"Unexpected token for unary: {self.current_token}")

    # <int> ::= ? A constant token ?
    def parse_int(self):
        int_token = self.expect("INTEGER_CONST")  # Expect an integer constant
        return Literal(type="IntegerLiteral", value=int(int_token[1]))

    def advance(self):
        self.curr += 1

    def expect(self, token_type):
        token = self.current_token
        if token == (None, None) or token[0] != token_type:
            expected = token_type
            found = token[0] if token else "EOF"
            raise ParserError(f"Expected {expected} but found {found}")

        self.advance()
        return token

    @property
    def is_at_end(self):
        return self.curr >= len(self.tokens)

    @property
    def peek(self):
        return self.tokens[self.curr] if self.curr < len(self.tokens) else None
