import sys

from pars import Equ_solver

if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print("only one argument needed.")
        sys.exit(0)
    equation = Equ_solver(sys.argv[1])
    