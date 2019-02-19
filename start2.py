#!/bin/python
import sys
from argparse import ArgumentParser
from collections import deque

encode_literal = lambda lid, sign: lid << 1 | sign
decode_literal = lambda literal: (literal >> 1, literal & 1)

class Solver(object):
    def __init__(self):
        self.clauses = []
        self.literals = {}
        self.links = []
        self.max_lid = 0

    def add_dimacs_line(self, line: str):
        clause = []
        for literal in map(int, line.split()):
            if literal == 0:
                continue
            lid  = abs(literal)
            sign = 1 if literal < 0 else 0
            literal = encode_literal(lid, sign)
            self.literals.setdefault(lid, None)
            self.max_lid = max(self.max_lid, lid)
            clause.append(literal)
        self.clauses.append(tuple(clause))

    def add_dimacs_file(self, fname: str):
        with open(fname) as fp:
            for line in fp:
                if line.startswith('p') or line.startswith('c'):
                    continue
                self.add_dimacs_line(line)

    def add_clause_links(self):
        self.links = [deque() for _ in range(2 * self.max_lid + 1)]
        for clause in self.clauses:
            self.links[clause[0]].append(clause)

    def no_contradictions(self, literal: int) -> bool:
        print('Length links for {}: {}'.format(literal, len(self.links[literal])))
        while self.links[literal]:
            clause = self.links[literal][0] #Take next clause
            found_something = False
            for _literal in clause:
                _lid, _sign = decode_literal(_literal)
                # Check if the the other literal doesnt have a value or if its signed value is false
                if self.literals[_lid] is None or self.literals[_lid] == _sign ^ 1:
                    del self.links[literal][0]
                    self.links[_lid].append(clause)
                    found_something = True
                    break
            if not found_something:
                print('Found a contridction in clause: {}'.format(clause))
                return False
        return True

    def _solve(self, lid_iter):
        lid = next(lid_iter)
        print('Calling _solve with {}'.format(lid))
        if lid == len(self.literals):
            print('AM finished. Was solveable, duh')
            yield self.literals
        for sign in (0, 1):
            self.literals[lid] = sign
            literal = encode_literal(lid, sign)
            if self.no_contradictions(literal):
                for a in self._solve(lid_iter):
                    yield a
                # yield self._solve(lid + 1)
        self.literals[lid] = None

    def solve(self):
        self.add_clause_links()
        print(list(self._solve(iter(self.literals.keys()))))


def parse_args():
    parser = ArgumentParser(description="General SAT solver")
    # parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1,2,3], default=1, required=True)
    parser.add_argument('filename', help='The text file to parse from.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    solver = Solver()
    solver.add_dimacs_file(args.filename)
    print(sorted(solver.literals.keys()))
    solver.solve()

if __name__ == "__main__":
    main()
