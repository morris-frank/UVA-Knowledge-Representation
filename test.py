#!/bin/python
import sys
import start4

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
    clauses = start4.parse_dimacs_files(['./test.sat', './sudoku-rules.txt'])
    start4.solve(clauses)

def main():
    sys.setrecursionlimit(10000)
    fname = './top91.sdk.txt'

    with open(fname) as fp:
        for line in fp:
            input('{}?'.format(line))
            parse_n_run_sudoku(line)


if __name__ == "__main__":
    main()
