#!/bin/python

import os
from typing import List
from itertools import repeat
from colorama import Back
from argparse import ArgumentParser
import tempfile
from multiprocessing import Pool
from functools import partial


from SAT import solve_files
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
        if true > 0:
            scr[int(true/100)-1][int(true%100/10)-1] = int(true%10)
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


def solve_sudoku_line(sudoku: str, verbose: bool = False, solver: int = 1, rule_file='./sudoku-rules.txt',
                      log_file='sudoku.py.log'):
    fd, temp_file = tempfile.mkstemp(prefix='tmp-sudoku')
    literals = sudoku2dimacs(sudoku)
    with os.fdopen(fd, 'w') as fp:
        for literal in literals:
            fp.write('{} 0\n'.format(literal))

        if verbose:
            print_sudoku(literals)

    solution = solve_files([temp_file, rule_file], verbose=verbose, solver=solver, log_file=log_file)
    if verbose:
        if solution:
            print_sudoku(solution)
        print('=' * 29 + '\n\n')
    os.remove(temp_file)


def solve_sudoku_file(fname: str, verbose: bool = False, solver: int = 1, processes=1):
    if not os.path.exists('log'):
        os.mkdir('log')
    _solve_line = partial(solve_sudoku_line, verbose=verbose, solver=solver,
                          log_file='log/' + os.path.basename(fname) + '.log')
    with open(fname) as f:
        sudokus = f.readlines()
    pool = Pool(processes=processes)
    _tqdm = tqdm if not verbose else lambda x,total : x
    for _ in _tqdm(pool.imap_unordered(_solve_line, sudokus), total=len(sudokus)):
        pass


def parse_args():
    parser = ArgumentParser(description="Sudoku Solver.")
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1, 2, 3], default=1,
                        required=True)
    parser.add_argument('filename', help='The text file to parse from.', type=str)
    parser.add_argument('-p', dest='processes', help='Number of processes to start.', type=int, default=4)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    solve_sudoku_file(args.filename, verbose=args.verbose, solver=args.solver, processes=args.processes)


if __name__ == '__main__':
    main()
