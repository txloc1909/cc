import platform
from typing import List, Any, NamedTuple

from .parser import Program

__all__ = [
    "codegen",
]


class Instruction(NamedTuple):
    opcode: str
    operands: List[Any]


class FunctionDefinition(NamedTuple):
    name: str
    instructions: List[Instruction]


class AsmProgram(NamedTuple):
    function_def: FunctionDefinition


def _visit_statement(stmt):
    assert stmt.type == "ReturnStatement"
    assert stmt.value.type == "IntegerLiteral"
    assert isinstance(stmt.value.value, int)
    return Instruction(opcode="RETURN", operands=[stmt.value.value, "eax"])


def _visit_function(function) -> FunctionDefinition:
    assert function.type == "Function", f"{function.type=}"
    return FunctionDefinition(
        name=function.name,
        instructions=[
            _visit_statement(function.body),
        ],
    )


def ast_to_asm(ast: Program) -> AsmProgram:
    functions = [_visit_function(f) for f in ast.functions]
    assert len(functions) == 1
    return AsmProgram(functions[0])


def _gen_instruction(inst: Instruction) -> List[str]:
    assert inst.opcode == "RETURN"
    src, dst = inst.operands
    assert isinstance(src, int), f"{src=}"
    assert dst == "eax", f"{dst=}"
    return [
        f"movl ${src}, %{dst}",
        "ret",
    ]


def _gen_function(function: FunctionDefinition) -> List[str]:
    body: List[str] = []
    for inst in function.instructions:
        body.extend(_gen_instruction(inst))

    header = [
        f"\t.globl {function.name}",
        f"\t.type {function.name}, @function",
        f"{function.name}:",
    ]

    # disable executable stack
    assert platform.system() == "Linux"
    footer = '.section .note.GNU-stack, "", @progbits\n'

    return [
        *header,
        *[f"\t{line}" for line in body],
        footer,
    ]


def _gen_asm_program(asm_program: AsmProgram) -> List[str]:
    return _gen_function(asm_program.function_def)


def codegen(program: Program) -> str:
    asm = ast_to_asm(program)
    code = _gen_asm_program(asm)
    return "\n".join(code)
