#!/bin/python

import sys
from argparse import ArgumentParser
from typing import List, Dict
import copy

ERROR    = 0
DONE     = 1
NOT_DONE = 2

def parse_dimacs_line(line):
    return {literal: None for literal in map(int, line.split()) if literal != 0}

def parse_dimacs_files(fnames):
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

def assign(clauses, trues, true):
    # print('{}'.format(true))
    # input()
    new_trues = trues.copy()
    new_trues.append(true)
    new_clauses = [clause.copy() for clause in clauses]

    for clause in new_clauses.copy():
        if true in clause: # Clause is now true
            new_clauses.remove(clause)
        else: # Literal not important anymore for clause
            clause.pop(true, None)
            clause.pop(-true, None)
    return new_clauses, new_trues

def unit_propagation(clauses, trues):
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

def first_none_variable(variables):
    for k,v in variables.items():
        if v == None:
            return k

def split(clauses, trues, val):
    print(clauses[0].keys())
    next_literal = next(iter(clauses[0].keys()))
    true = next_literal if val else -next_literal
    return assign(clauses, trues, true)


def solve(clauses, trues=[]):
    if len(clauses) == 0:
        print('We finished')
        return True

    s, clauses, trues = unit_propagation(clauses, trues)
    if s == NOT_DONE:
        return solve(clauses, trues)
    else:
        print('SPLIT')
        return solve(*split(clauses, trues, False)) or solve(*split(clauses, trues, False))


def parse_args():
    parser = ArgumentParser(description="General SAT solver (World record as of 2021)")
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1,2,3], default=1, required=True)
    parser.add_argument('filename', help='The text file to parse from.')
    args = parser.parse_args()
    return args

def main():
    clauses = parse_dimacs_files(['./sudoku-example-processed.txt'])
    solve(clauses)

if __name__ == "__main__":
    main()
