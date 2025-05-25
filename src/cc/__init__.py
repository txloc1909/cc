import argparse
import os
import sys
import subprocess

from .lexer import lex
from .parser import Parser, ParserError
from .codegen import codegen


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

    try:
        tokens = lex(source)
    except ValueError:
        sys.exit(1)

    if args.lex:
        return

    try:
        program = Parser(tokens).parse_program()
    except ParserError:
        sys.exit(1)

    if args.parse:
        return

    code = codegen(program)
    if args.codegen:
        print(code)
        return

    base_dir = os.path.dirname(args.input_file)
    exe_name, ext = os.path.splitext(os.path.basename(args.input_file))
    assert ext == ".c"
    output_asm = f"{base_dir}/{exe_name}.s"
    output_exe = f"{base_dir}/{exe_name}"
    with open(output_asm, "w") as f:
        f.write(code)

    if args.S:
        return

    args = ["gcc", output_asm, "-o", output_exe]
    subprocess.run(args, capture_output=True, check=False, text=True)
    assert os.path.exists(output_asm)
    assert os.path.exists(output_exe)
    os.remove(output_asm)  # clean up
    return
