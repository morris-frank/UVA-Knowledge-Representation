#!/bin/python

import sys
from argparse import ArgumentParser
from typing import List, Dict

def parse_dimacs_line(line: str) -> tuple:
    return tuple([literal for literal in map(int, line.split()) if literal != 0])

def parse_dimacs_file(fname: str) -> List[tuple]:
    clauses = []
    with open(fname) as fp:
        for line in fp:
            if line.startswith('p') or line.startswith('c'):
                continue
            clauses.append(parse_dimacs_line(line))
    return clauses

def atoms_from_clauses(clauses):
    atoms = set()
    for clause in clauses:
        for literal in map(abs, clause):
            atoms.append(literal)
    return atoms

def clause_satisfied(clause, trues):
    for literal in clause:
        if literal in trues:
            return True
    return False

def satisfied(clauses, trues):
    return all([clause_satisfied(clause, trues) for clause in clauses])

def unsatisfied(clauses, trues):
    for clause in clauses:
        if all([(-literal in trues) for literal in clause]):
            return True
    return False

def unit_propagation(clauses, trues):
    for clause in clauses:
        unknown_literals = [l for l in clause if l not in trues and -l not in trues]
        if len(unknown_literals) == 1:
            if all([-l in trues for l in clause if l != unknown_literals[0]]):
                return unknown_literals[0]
    return None

def solve(clauses, atoms, trues=[]):
    def remove(sym,l): # non-destructive removal of literal
        x = sym.index(l)
        return sym[0:x] + sym[x+1:]
    if satisfied(clauses, trues):
        return trues

    if unsatisfied(clauses, trues):
        print('Unsatisfied')
        return False

    new_true = unit_propagation(clauses, trues)
    if new_true:
        return solve(clauses, remove(atoms, abs(new_true)), trues + [new_true])
    split = atoms.pop()
    split, atoms = atoms[0], atoms[1:]
    print('split with {}'.format(split))
    return solve(clauses, atoms, trues + [split]) or solve(clauses, atoms, trues + [-split])

def parse_args():
    parser = ArgumentParser(description="General SAT solver (World record as of 2021)")
    # parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1,2,3], default=1, required=True)
    parser.add_argument('filename', help='The text file to parse from.')
    args = parser.parse_args()
    return args

def main():
    # args = parse_args()
    # clauses = parse_dimacs_file(args.filename)
    clauses = parse_dimacs_file('./sudoku-rules.txt') + parse_dimacs_file('./test.sat')
    atoms = atoms_from_clauses(clauses)
    print(solve(clauses, atoms))

if __name__ == "__main__":
    main()
