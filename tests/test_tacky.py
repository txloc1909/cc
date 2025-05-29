from cc.lexer import lex
from cc.parser import Parser
from cc.tacky import gen_tacky, emit_tacky
from cc.tacky import Program, FuncDef, ReturnInst, UnaryInst, Constant, Variable


def test_simple_program():
    to_tacky = lambda src: gen_tacky(Parser(lex(src)).parse_program())  # noqa: E731

    src = "int main(void) { return 42; }"
    assert to_tacky(src) == Program(
        function_def=FuncDef(
            identifier="main",
            instructions=[
                ReturnInst(value=Constant(value=42)),
            ],
        )
    )


def test_unary():
    to_tacky = lambda src: emit_tacky(Parser(lex(src)).parse_exp())[0]  # noqa: E731

    assert to_tacky("-42") == [
        UnaryInst(
            op="NEGATE", src=Constant(value=42), dst=Variable(identifier="tmp.1")
        ),
    ]

    assert to_tacky("-~42") == [
        UnaryInst(
            op="COMPLEMENT",
            src=Constant(value=42),
            dst=Variable(identifier="tmp.2"),
        ),
        UnaryInst(
            op="NEGATE",
            src=Variable(identifier="tmp.2"),
            dst=Variable(identifier="tmp.3"),
        ),
    ]
