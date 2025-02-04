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
        programs = []
        while self.current_token is not None:
            programs.append(self.parse_function())

        if not programs:
            raise ParserError("No valid top-level program found")
        
        return programs

    # <function> ::= "int" <identifier> "(" "void" ")" "{" <statement> "}"
    def parse_function(self):
        self.expect("KEYWORD")                  # Expect "int"
        identifier = self.expect("IDENTIFIER")  # Expect function name
        self.expect("LPAREN")                   # Expect "("
        self.expect("KEYWORD")                  # Expect "void"
        self.expect("RPAREN")                   # Expect ")"
        self.expect("LBRACE")                   # Expect "{"
        statement = self.parse_statement()      # Parse the statement
        self.expect("RBRACE")                   # Expect "}"
        return {
            "type": "Function",
            "name": identifier[1],
            "body": statement
        }

    # <statement> ::= "return" <exp> ";"
    def parse_statement(self):
        self.expect("KEYWORD")                  # Expect "return"
        expression = self.parse_exp()           # Parse the expression
        self.expect("SEMICOLON")                # Expect ";"
        return {
            "type": "ReturnStatement",
            "value": expression
        }

    # <exp> ::= <int>
    def parse_exp(self):
        return self.parse_int()

    # <int> ::= ? A constant token ?
    def parse_int(self):
        int_token = self.expect("INTEGER_CONST")  # Expect an integer constant
        return {
            "type": "IntegerLiteral",
            "value": int(int_token[1])
        }


    def advance(self):
        self.curr += 1

    def expect(self, token_type):
        token = self.current_token
        if token is None or token[0] != token_type:
            expected = token_type
            found = token[0] if token else "EOF"
            raise ParserError(f"Expected {expected} but found {found}")

        self.advance()
        return token
