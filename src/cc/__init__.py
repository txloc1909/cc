import sys
from functools import partial

def _main(args):
    print("Hello world")


main = partial(_main, sys.argv)
