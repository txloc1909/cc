import argparse
import os
import sys

from .lexer import lex


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

        for token in tokens:
            print(token)
    elif args.parse:
        print("Parsing")
    elif args.codegen:
        print("Codegen")
    elif args.S:
        print("Emitting assembly file")
    else:
        print("No option")

