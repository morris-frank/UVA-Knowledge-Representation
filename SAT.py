#!/bin/python

import sys
from argparse import ArgumentParser
from typing import List, Dict, NewType
from itertools import repeat

# CONSTANTS and GLOBALS
ERROR, DONE, NOT_DONE = 0, 1, 2
VERBOSE = False
SOLVER = 1
CALLSTATS = {'assign': 0, 'unit': 0, 'solve': 0, 'split': 0}

# New TYPES
Clause = NewType('Clause', Dict[int, bool])

def parse_dimacs_line(line: str) -> Clause:
    return {literal: None for literal in map(int, line.split()) if literal != 0}

def parse_dimacs_files(fnames: List[str]) -> List[Clause]:
    if type(fnames) != list:
        fnames = [fnames]
    clauses = []
    for fname in fnames:
        with open(fname) as fp:
            for line in fp:
                if line.startswith('p') or line.startswith('c'):
                    continue
                clauses.append(parse_dimacs_line(line))
    return clauses

def log_print(clauses: List[Clause], trues: List[int]):
    print('∥clauses∥={},∥trues∥={},#Split={},#Assign={},#Unit={},#Solve={}'.format(
        len(clauses), len(trues), CALLSTATS['split'], CALLSTATS['assign'], CALLSTATS['unit'], CALLSTATS['solve']))

def assign(clauses: List[Clause], trues: List[int], set_true: int) -> (List[Clause], List[int]):
    """
    Arguments:
        clauses {List[Clause]} -- The clauses
        trues {List[int]} -- The truefull unis
        set_true {int} -- the literal to set

    Returns:
        clauses, trues -- Copied and updated clauses and assignments
    """
    if VERBOSE:
        CALLSTATS['assign'] += 1
    new_trues = trues.copy()
    new_trues.append(set_true)
    new_clauses = [clause.copy() for clause in clauses]

    for clause in new_clauses.copy():
        if set_true in clause: # Clause is now true
            new_clauses.remove(clause)
        else: # Literal not important anymore for clause
            clause.pop(set_true, None)
            clause.pop(-set_true, None)
    return new_clauses, new_trues

def remove_tautologies(clauses: List[Clause]) -> List[Clause]:
    for clause in clauses:
        counts = {}
        for literal in clause:
            if counts.setdefault(abs(literal), literal > 0) != (literal > 0): # Is tautology
                clauses.remove(clause)
                break
    return clauses

def unit_propagation(clauses: List[Clause], trues: List[int]) -> (int, List[Clause], List[int]):
    if VERBOSE:
        CALLSTATS['unit'] += 1
    simplified = False
    status = DONE
    while not simplified:
        simplified = True
        for clause in clauses:
            if len(clause) == 1:
                simplified = False
                status = NOT_DONE
                clauses, trues = assign(clauses, trues, next(iter(clause.keys())))
                break
    return status, clauses, trues

def split(clauses: List[Clause], trues: List[int], value: bool) -> (List[Clause], List[int]):
    if VERBOSE:
        CALLSTATS['split'] += 1

    if   SOLVER == 1:
        next_literal = next(iter(clauses[0].keys()))
    elif SOLVER == 2:
        pass
    elif SOLVER == 3:
        pass

    true = next_literal if value else -next_literal
    return assign(clauses, trues, true)

def solve(clauses: List[Clause]) -> List[int]:
    clauses = remove_tautologies(clauses)
    return _solve(clauses)


def _solve(clauses: List[Clause], trues=[]) -> List[int]:
    """Solve the SAT problem described through a set of CNF clauses.

    Arguments:
        clauses {List[Clause]} -- The clauses

    Keyword Arguments:
        trues {list} -- The current assingment state (default: [])

    Returns:
        List[int] -- The final assignment state
    """
    if VERBOSE:
        CALLSTATS['solve'] += 1
        log_print(clauses, trues)

    if len(clauses) == 0:
        log_print(clauses, trues)
        if VERBOSE:
            print_solution(trues)
        return True

    s, clauses, trues = unit_propagation(clauses, trues)
    if s == NOT_DONE:
        return _solve(clauses, trues)
    else:
        return _solve(*split(clauses, trues, False)) or _solve(*split(clauses, trues, False))

def print_solution(trues: List[int]):
    scr = [list(repeat(' ', 9)) for _ in range(1,10)]
    for true in trues:
        if true < 0:
            continue
        _px = list(map(int, list(str(true))))
        scr[_px[0]-1][_px[1]-1] = str(_px[2])
    print(('\n'+'- '*17+'\n').join([' | '.join(_scr) for _scr in scr]))

def parse_args():
    global VERBOSE, SOLVER
    parser = ArgumentParser(description="General SAT solver (World record as of 2021)")
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1,2,3], default=1, required=True)
    parser.add_argument('filename', help='The text file to parse from.')
    args = parser.parse_args()
    VERBOSE = args.verbose
    SOLVER = args.solver
    return args

def main():
    args = parse_args()
    clauses = parse_dimacs_files(['./sudoku-example-processed.txt'])
    solve(clauses)

if __name__ == "__main__":
    main()
