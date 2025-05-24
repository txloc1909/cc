import argparse
import os
import sys

from .lexer import lex
from .parser import Parser, ParserError
from .codegen import codegen, emit_assembly


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Input source file")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--lex",
        action="store_true",
        help="Only perform lexing",
    )
    group.add_argument(
        "--parse",
        action="store_true",
        help="Only perform parsing",
    )
    group.add_argument(
        "--codegen",
        action="store_true",
        help="Only perform generating assembly",
    )
    group.add_argument(
        "-S",
        action="store_true",
        help="Emit assembly file",
    )

    args = parser.parse_args()

    assert os.path.exists(args.input_file)
    with open(args.input_file, "r") as f:
        source = f.read()

    if args.lex:
        try:
            tokens = lex(source)
        except ValueError:
            sys.exit(1)
    elif args.parse:
        try:
            tokens = lex(source)
        except ValueError:
            sys.exit(1)

        try:
            program = Parser(tokens).parse_program()  # noqa: F841
        except ParserError:
            sys.exit(1)

    elif args.codegen:
        program = Parser(lex(source)).parse_program()
        print(codegen(program))
    elif args.S:
        exe_name, ext = os.path.splitext(os.path.basename(args.input_file))
        assert ext == ".c"
        program = Parser(lex(source)).parse_program()
        emit_assembly(program, f"{exe_name}.s")
    else:
        print("No option")
