import pytest

from cc.lexer import lex


def test_empty_src():
    assert lex("") == []


def test_invalid_char():
    with pytest.raises(ValueError, match="Unexpected token at:"):
        lex("@")


def test_single_char():
    src = "(){};~"
    assert lex(src) == [
        ("LPAREN", "("),
        ("RPAREN", ")"),
        ("LBRACE", "{"),
        ("RBRACE", "}"),
        ("SEMICOLON", ";"),
        ("TILDE", "~"),
    ]


def test_one_or_two_chars():
    src = "! != = == < <= > >= & && | || + ++ - --"
    assert lex(src) == [
        ("BANG", "!"),
        ("BANG_EQUAL", "!="),
        ("EQUAL", "="),
        ("EQUAL_EQUAL", "=="),
        ("LESS", "<"),
        ("LESS_EQUAL", "<="),
        ("GREATER", ">"),
        ("GREATER_EQUAL", ">="),
        ("AMP", "&"),
        ("AMP_AMP", "&&"),
        ("PIPE", "|"),
        ("PIPE_PIPE", "||"),
        ("PLUS", "+"),
        ("PLUS_PLUS", "++"),
        ("MINUS", "-"),
        ("MINUS_MINUS", "--"),
    ]


def test_keywords():
    src = "int void return"  # TODO add more
    assert lex(src) == [
        ("KEYWORD", "int"),
        ("KEYWORD", "void"),
        ("KEYWORD", "return"),
    ]


def test_comments():
    src = """
// this is a comment
void // commend after keyword
/* multiline
comment */
"""

    assert lex(src) == [
        ("COMMENT", "// this is a comment"),
        ("KEYWORD", "void"),
        ("COMMENT", "// commend after keyword"),
        ("COMMENT", "/* multiline\ncomment */"),
    ]
