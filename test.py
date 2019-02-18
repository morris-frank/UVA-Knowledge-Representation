#!/bin/python
import sys
from start2 import Solver

def parse_n_run_sudoku(line):
    open('test.sat', 'w').close()
    with open('test.sat', 'a') as fp:
        for i,c in enumerate(line):
            if c == '\n':
                continue
            if c != '.':
                column = int(i % 9 + 1)
                row = int(i / 9) + 1
                fp.write('{}{}{} 0\n'.format(column, row, c))
    solver = Solver()
    solver.add_dimacs_file('./test.sat')
    solver.add_dimacs_file('./sudoku-rules.txt')
    print('# Literals: {}, # Clauses: {}'.format(len(solver.literals), len(solver.clauses)))
    solver.solve()

def main():
    sys.setrecursionlimit(10000)
    fname = './top91.sdk.txt'

    with open(fname) as fp:
        for line in fp:
            input('{}?'.format(line))
            parse_n_run_sudoku(line)


if __name__ == "__main__":
    main()
