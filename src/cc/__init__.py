import argparse
import sys


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
    
    print(args.input_file)
    if args.lex:
        print("Lexing")
    elif args.parse:
        print("Parsing")
    elif args.codegen:
        print("Codegen")
    elif args.S:
        print("Emitting assembly file")
    else:
        print("No option")

