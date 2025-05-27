from cc.lexer import lex
from cc.parser import Parser
from cc.parser import UnaryExpr, Literal


def test_parse_int():
    parse_int = lambda src: Parser(lex(src)).parse_int()  # noqa: E731
    assert parse_int("42") == Literal(type="IntegerLiteral", value=42)


def test_parse_unary():
    parse_unary = lambda src: Parser(lex(src)).parse_unary()  # noqa: E731

    assert parse_unary("-42") == UnaryExpr(
        op="-", rhs=Literal(type="IntegerLiteral", value=42)
    )

    assert parse_unary("--42") == UnaryExpr(
        op="--", rhs=Literal(type="IntegerLiteral", value=42)
    )

    assert parse_unary("-(~42)") == UnaryExpr(
        op="-",
        rhs=UnaryExpr(op="~", rhs=Literal(type="IntegerLiteral", value=42)),
    )

    assert parse_unary("!~-42") == UnaryExpr(
        op="!",
        rhs=UnaryExpr(
            op="~", rhs=UnaryExpr(op="-", rhs=Literal(type="IntegerLiteral", value=42))
        ),
    )
