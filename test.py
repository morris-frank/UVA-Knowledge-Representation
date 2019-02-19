#!/bin/python
import sys
import SAT

def export_sudoku_line(line, fname='./test.cnt'):
    open(fname, 'w').close()
    with open(fname, 'a') as fp:
        for i,c in enumerate(line):
            if c == '\n':
                continue
            if c != '.':
                column = int(i % 9 + 1)
                row = int(i / 9) + 1
                fp.write('{}{}{} 0\n'.format(column, row, c))

def run_sudoku(line):
    export_sudoku_line(line)
    clauses = SAT.parse_dimacs_files(['./test.cnt', './sudoku-rules.txt'])
    solution = SAT.solve(clauses)
    SAT.print_solution(solution)

def main():
    SAT.VERBOSE = True
    sys.setrecursionlimit(10000)
    fname = './damnhard.sdk.txt'

    with open(fname) as fp:
        for line in fp:
            if input('{}?'.format(line)) != 'n':
                run_sudoku(line)


if __name__ == "__main__":
    main()
