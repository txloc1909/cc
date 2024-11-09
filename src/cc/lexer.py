import re

__all__ = ["lex", ]


TOKEN_PATTERNS = [
    # token_type, regex
    ("KEYWORD", r"\b(?:int|void|return)\b"),  # Just these keywords, for now
    ("IDENTIFIER", r"[a-zA-Z_]\w*\b"),
    ("INTEGER_CONST", r"[0-9]+\b"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"{"),
    ("RBRACE", r"}"),
    ("SEMICOLON", r";"),
    ("COMMENT", r"//.*?$|/\*.*?\*/"),
]

TOKEN_REGEX = [
    (token_type, re.compile(pattern, re.DOTALL | re.MULTILINE)) 
    for token_type, pattern in TOKEN_PATTERNS
]


def lex(source):
    tokens = []
    while source:
        if not (source := source.lstrip()):
            break

        for token_type, regex in TOKEN_REGEX:
            match = regex.match(source)
            if match:
                matched_text = match.group(0)
                tokens.append((token_type, matched_text))
                source = source[len(matched_text):]
                break
        else:
            raise ValueError(f"Unexpected token at: {source[:20]}")

    return tokens

