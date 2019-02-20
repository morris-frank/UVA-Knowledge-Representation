#!/bin/python

from SAT import solve_files
from typing import List
from itertools import repeat
from colorama import Back
from argparse import ArgumentParser
from tqdm import tqdm


def print_sudoku(trues: List[int]):
    def print_lit(lit):
        cmap = [Back.BLACK, Back.WHITE, Back.BLUE, Back.GREEN, Back.RED, Back.YELLOW, Back.MAGENTA, Back.CYAN,
                Back.LIGHTMAGENTA_EX, Back.LIGHTBLUE_EX]
        if not lit:
            return Back.LIGHTBLACK_EX + '   ' + cmap[0]
        else:
            return ' '.join([cmap[lit], str(lit), cmap[0]])
    scr = [list(repeat(None, 9)) for _ in range(1, 10)]
    for true in trues:
        if true < 0:
            continue
        _px = list(map(int, list(str(true))))
        scr[_px[0]-1][_px[1]-1] = _px[2]
    viz = ''
    for y, line in enumerate(scr, start=1):
        for x, i in enumerate(line, start=1):
            viz += print_lit(i) + (x % 3 == 0) * ' '
        viz += '\n' + (y % 3 == 0) * '\n'
    print(viz)


def sudoku2dimacs(line: str) -> List[int]:
    literals = []
    for i, c in enumerate(line):
        if c == '\n':
            continue
        if c != '.':
            column = int(i % 9 + 1)
            row = int(i / 9) + 1
            literals.append(int('{}{}{}'.format(column, row, c)))
    return literals


def export_sudoku_line(sudoku: str, fname='./.sudoku-tmp.cnf'):
    open(fname, 'w').close()
    with open(fname, 'a') as fp:
        literals = sudoku2dimacs(sudoku)
        for literal in literals:
            fp.write('{} 0\n'.format(literal))
    return literals


def solve_sudoku_file(fname: str, verbose: bool = False, solver: int = 1, tmp_file='./.sudoku-tmp.cnf',
                      rule_file='./sudoku-rules.txt'):
    _tqdm = tqdm if not verbose else lambda x: x
    with open(fname) as f:
        data = f.readlines()
    for line in _tqdm(data):
        literals = export_sudoku_line(line)
        if verbose:
            print_sudoku(literals)
        solution = solve_files([tmp_file, rule_file], verbose=verbose, solver=solver)
        if verbose:
            if solution:
                print_sudoku(solution)
            print('='*29 + '\n\n')


def parse_args():
    parser = ArgumentParser(description="Sudoku Solver.")
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1, 2, 3], default=1,
                        required=True)
    parser.add_argument('filename', help='The text file to parse from.', type=str)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    solve_sudoku_file(args.filename, verbose=args.verbose, solver=args.solver)


if __name__ == '__main__':
    main()
