"""TACKY: three-address code IR"""

from abc import ABC
from dataclasses import dataclass

from cc import parser

__all__ = [
    "gen_tacky",
]


class Value(ABC):
    pass


@dataclass
class Constant(Value):
    value: int


@dataclass
class Variable(Value):
    identifier: str


class Instruction(ABC):
    pass


@dataclass
class ReturnInst(Instruction):
    value: Value


@dataclass
class UnaryInst(Instruction):
    op: str
    src: Value
    dst: Value


@dataclass
class FuncDef:
    identifier: str
    instructions: list[Instruction]


@dataclass
class Program:
    function_def: FuncDef


_VAR_COUNTER = 0


def make_temp_var(prefix="tmp") -> str:
    global _VAR_COUNTER
    _VAR_COUNTER += 1
    return Variable(identifier=f"{prefix}.{_VAR_COUNTER}")


def convert_tacky_op(op: str) -> str:
    match op:
        case "-":
            return "NEGATE"
        case "~":
            return "COMPLEMENT"
        case "!":
            return "LOGICAL_NOT"
        case _:
            raise NotImplementedError(f"{op=}")


def emit_tacky(expr: parser.Expr) -> tuple[list[Instruction], Value]:
    match expr:
        case parser.Literal(type=type_, value=value):
            assert type_ == "IntegerLiteral", f"{type_=}"
            val = Constant(value=value)
            return [], val
        case parser.UnaryExpr(op=op, rhs=rhs):
            instrs, src = emit_tacky(rhs)
            dst = make_temp_var()
            code = [
                *instrs,
                UnaryInst(op=convert_tacky_op(op), src=src, dst=dst),
            ]
            return code, dst
        case _:
            raise NotImplementedError(f"{expr=}")


def emit_statement(stmt: parser.Statement) -> tuple[list[Instruction], Value]:
    match stmt:
        case parser.ReturnStatement(value=value):
            instrs, ret_val = emit_tacky(value)
            return [
                *instrs,
                ReturnInst(value=ret_val),
            ], ret_val
        case _:
            raise NotImplementedError(f"{stmt=}")


def gen_function(function: parser.Function) -> FuncDef:
    assert function.type == "Function", f"{function.type=}"
    assert function.name == "main", f"{function.name=}"
    assert function.body.type == "ReturnStatement", f"{function.body.type=}"

    instrs, ret_val = emit_tacky(function.body.value)
    return FuncDef(
        identifier=function.name,
        instructions=[
            *instrs,
            ReturnInst(value=ret_val),
        ],
    )


def gen_tacky(ast: parser.Program) -> Program:
    assert len(ast.functions) == 1
    return Program(
        function_def=gen_function(ast.functions[0]),
    )
