import re

__all__ = [
    "lex",
]


TOKEN_PATTERNS = [
    # token_type, regex
    ("KEYWORD", r"\b(?:int|void|return)\b"),  # Just these keywords, for now
    ("IDENTIFIER", r"[a-zA-Z_]\w*\b"),
    ("INTEGER_CONST", r"[0-9]+\b"),
    # two-char tokens before one-char tokens, longest match first
    ("AMP_AMP", r"&&"),
    ("MINUS_MINUS", r"--"),
    ("PLUS_PLUS", r"\+\+"),
    ("EQUAL_EQUAL", r"=="),
    ("LESS_EQUAL", r"<="),
    ("GREATER_EQUAL", r">="),
    ("PIPE_PIPE", r"\|\|"),
    ("BANG_EQUAL", r"!="),
    # one-char tokens
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"{"),
    ("RBRACE", r"}"),
    ("SEMICOLON", r";"),
    ("MINUS", r"-"),
    ("PLUS", r"\+"),
    ("EQUAL", r"="),
    ("LESS", r"<"),
    ("GREATER", r">"),
    ("AMP", r"&"),
    ("PIPE", r"\|"),
    ("TILDE", r"~"),
    ("BANG", r"!"),
    # misc
    ("COMMENT", r"//.*?$|/\*.*?\*/"),
    ("WHITESPACE", r"\s+"),
]

TOKEN_REGEX = "|".join(
    f"(?P<{token_type}>{pattern})" for token_type, pattern in TOKEN_PATTERNS
)
COMPILED_REGEX = re.compile(TOKEN_REGEX, re.MULTILINE | re.DOTALL)


def lex(source):
    tokens = []
    while source:
        if not (source := source.lstrip()):
            break

        match = COMPILED_REGEX.match(source)
        if match:
            token_type = match.lastgroup
            lexeme = match.group()
            if token_type != "WHITESPACE":
                tokens.append((token_type, lexeme))
            source = source[len(lexeme) :]
        else:
            raise ValueError(f"Unexpected token at: {source[0]}")

    return tokens
