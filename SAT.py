#!/bin/python

from argparse import ArgumentParser
from typing import List, Dict, NewType
from itertools import chain
import json
from time import time
import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# CONSTANTS and GLOBALS
ERROR, DONE, NOT_DONE = 0, 1, 2

# New TYPES
Clause = NewType('Clause', Dict[str, None])
Literal = NewType('Literal', str)

GLOBAL_CLAUSES = {}
GLOBAL_LITERALS = {}
GLOBAL_LITERAL_SCORES = {}


def abs_literal(literal: Literal) -> Literal:
    return literal if value_literal(literal) else literal[1:]


def neg_literal(literal: Literal) -> Literal:
    return Literal('-' + literal if value_literal(literal) else literal[1:])


def value_literal(literal: Literal) -> bool:
    return not literal.startswith('-')


def print_clauses(clauses: Dict[int, Clause]):
    for idx, clause in clauses.items():
        print('{}: ∨ '.join(clause.keys()).format(idx))


class Stats(object):
    def __init__(self, solver: int, log_file='SAT.log'):
        self.solver = solver
        self.log_file = log_file
        self.assign_calls = 0
        self.unit_calls = 0
        self.solve_calls = 0
        self.split_calls = 0
        self.number_tautologies = 0
        self.number_literals = 0
        self.number_clauses = 0
        self.number_backtracks = 0
        self.solution = None
        self.start_time = time()
        self.duration = 0
        self.iter_log = []
        self.size_solution = 0

    def update(self):
        _log = [self.split_calls, self.solve_calls, self.assign_calls, self.unit_calls, self.number_backtracks,
                self.size_solution, time() - self.start_time]
        self.iter_log.append(_log)

    def save(self):
        self.update()
        self.duration = time() - self.start_time
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(self.__dict__) + '\n')

    def report(self):
        if self.solution:
            solved = 'Solved'
            number_solution = len(self.solution)
            number_neg_solution = len([i for i in self.solution if i.startswith('-')])
        else:
            solved = 'Did not solve'
            number_solution, number_neg_solution = 0, 0

        number_pos_solution = number_solution - number_neg_solution
        print('{solved} CNF SAT with {lit} Literals and {cls} clauses in {time:.3f}s\n'
              '#Tautologies={tat}. ∥Solution∥={slt} [+{pslt}|-{nslt}], #Backtracks: {bkt}\n'
              '#Calls: [solve={slv}, split={spl}, unit={unt}, assign={asg}]\n'.format(
                solved=solved, lit=self.number_literals, cls=self.number_clauses, time=time() - self.start_time,
                tat=self.number_tautologies, slt=number_solution, pslt=number_pos_solution, nslt=number_neg_solution,
                bkt=self.number_backtracks,
                slv=self.solve_calls, spl=self.split_calls, unt=self.unit_calls, asg=self.assign_calls
                ))


def assign(clauses: Dict[int, Clause], solution: List[Literal], to_set_true: Literal, stats: Stats)\
        -> (Dict[int, Clause], List[Literal]):
    log.debug('assign: {}'.format(to_set_true))
    stats.assign_calls += 1
    new_solution = solution.copy()
    new_solution.append(to_set_true)
    new_clauses = {idx: clause.copy() for idx, clause in clauses.items()}

    for idx, clause in new_clauses.copy().items():
        if to_set_true in clause:  # Clause is now true
            del new_clauses[idx]
        else:  # Literal not important anymore for clause
            clause.pop(neg_literal(to_set_true), None)
    return new_clauses, new_solution


def split(clauses: Dict[int, Clause], stats: Stats, solver: int) -> Literal:
    global GLOBAL_LITERAL_SCORES, GLOBAL_LITERALS
    stats.split_calls += 1
    stats.update()
    next_literal = 0
    if solver == 1:
        next_literal = next(iter(next(iter(clauses.values())).keys()))
    elif solver == 2:
        max_count = 0
        next_literal = None
        for literal in GLOBAL_LITERALS:
            count = len([None for clause in clauses.values() if literal in clause])
            if count > max_count:
                next_literal = literal
                max_count = count
    elif solver == 3:
        max_score = 0
        next_literal = None
        for clause in clauses.values():
            for literal in clause:
                if next_literal == None:
                    next_literal = literal
                score = GLOBAL_LITERAL_SCORES.get(literal, 0)
                if  score > max_score:
                    next_literal = literal
                    max_score = score
    elif solver == 4:
        scores = {}
        for clause in clauses.values():
            for literal in clause:
                if value_literal(literal):
                    scores[literal] = scores.get(literal, 0) + 2**(-len(clause))
        next_literal = max(scores, key=scores.get)
    return next_literal

def unit_propagation(clauses: Dict[int, Clause], solution: List[Literal], stats: Stats)\
        -> (int, Dict[int, Clause], List[Literal]):
    stats.unit_calls += 1
    for idx,clause in clauses.items():
        if len(clause) == 1:
            return NOT_DONE, assign(clauses, solution, next(iter(clause.keys())), stats=stats)
    return DONE, (clauses, solution)


def remove_tautologies(clauses: Dict[int, Clause], stats: Stats) -> Dict[int, Clause]:
    n_tautologies = 0
    for idx, clause in clauses.copy().items():
        counts = {}
        for literal in clause:
            # If it is a tautology
            if counts.setdefault(abs_literal(literal), value_literal(literal)) != value_literal(literal):
                del clauses[idx]
                n_tautologies += 1
                break
    stats.number_tautologies += n_tautologies
    return clauses


def _solve(clauses: Dict[int, Clause], solution: List[Literal], stats: Stats, solver: int) -> List[Literal] or bool:
    global GLOBAL_CLAUSES
    stats.solve_calls += 1
    stats.size_solution = len([None for literal in solution if value_literal(literal)])

    # If no clauses left to be satisfied, then we finished
    if len(clauses) == 0:
        return solution

    # A clause is empty thus not satisfiable ⇒ current solution is incorrect
    for idx, clause in clauses.items():
        b = 1
        if len(clause) == 0:
            log.debug('Backtrack')
            stats.number_backtracks += 1
            for literal in GLOBAL_CLAUSES[idx]:
                GLOBAL_LITERAL_SCORES.setdefault(literal, 0)
                GLOBAL_LITERAL_SCORES[literal] +=  b
            return

    s, (clauses, solution) = unit_propagation(clauses, solution, stats)
    if s == NOT_DONE:
        return _solve(clauses, solution, stats, solver)
    else:
        split_literal = split(clauses, stats, solver)
        return _solve(*assign(clauses, solution, split_literal, stats=stats), stats=stats, solver=solver)\
               or _solve(*assign(clauses, solution, neg_literal(split_literal), stats=stats), stats=stats, solver=solver)


def solve(clauses: Dict[int, Clause], stats: Stats, solver: int) -> List[Literal] or bool:
    global GLOBAL_CLAUSES, GLOBAL_LITERALS
    clauses = remove_tautologies(clauses, stats=stats)
    GLOBAL_CLAUSES = {idx: clause.copy() for idx, clause in clauses.items()}
    GLOBAL_LITERALS = set(map(abs_literal, chain.from_iterable(clauses.values())))
    return _solve(clauses, [], stats=stats, solver=solver)


def parse_dimacs_line(line: str) -> Clause:
    return Clause({literal: None for literal in line.split() if literal != '0'})


def parse_dimacs_files(fnames: List[str]) -> Dict[int, Clause]:
    if type(fnames) != list:
        fnames = [fnames]
    clauses = {}
    idx = 1
    for fname in map(str, fnames):
        with open(fname) as fp:
            for line in fp:
                if line.startswith('p') or line.startswith('c'):
                    continue
                clauses[idx] = parse_dimacs_line(line)
                idx += 1
    return clauses


def count_literals(clauses: Dict[int, Clause]) -> int:
    return len(set(filter(lambda x: not x.startswith('-'), chain.from_iterable(clauses.values()))))


def solve_files(fnames: List[str], solver: int, verbose: bool = False, log_file: str = 'SAT.log')\
        -> List[Literal] or bool:
    stats = Stats(solver, log_file=log_file)
    clauses = parse_dimacs_files(fnames)
    stats.number_clauses = len(clauses)
    stats.number_literals = count_literals(clauses)
    solution = solve(clauses, solver=solver, stats=stats)
    stats.solution = solution
    if verbose:
        stats.report()
    del stats.solution
    stats.save()
    return solution


def solve_file(fname: str, solver: int, verbose: bool, log_file: str) -> List[Literal] or bool:
    return solve_files([fname], solver, verbose, log_file)


def parse_args():
    parser = ArgumentParser(description="General SAT solver (World record as of 2021)")
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-vv', dest='debug', action='store_true')
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1, 2, 3, 4], default=1,
                        required=True)
    parser.add_argument('filenames', help='The text file to parse from.', type=str, nargs='+')
    args = parser.parse_args()
    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.verbose:
        log.setLevel(logging.INFO)
    return args


def main():
    args = parse_args()
    if not os.path.exists('log'):
        os.mkdir('log')
    log_file = '_'.join([os.path.basename(f) for f in args.filenames])
    solution = solve_files(args.filenames, solver=args.solver, verbose=args.verbose,
                           log_file='log/' + log_file + '.log')
    if solution:
        print(list(filter(value_literal, solution)))


if __name__ == "__main__":
    main()
