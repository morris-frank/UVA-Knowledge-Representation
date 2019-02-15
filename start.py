#!/bin/python
from collections import namedtuple
from typing import List


LitWrap = namedtuple('LitWrap', ['literal', 'sign'])

def main():
    solver = Solver()
    solver.add_sat_file('test.sat')
    solver.print()
    solver.simplify()
    solver.print()
    solver.simplify()
    solver.print()

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class Literal(Bunch):
    def __init__(self, id: int, value=None):
        super().__init__(id=id, value=value)
        self.clauses = []

class Node(Bunch):
    def __init__(self, literal: int, value: bool, picked: bool):
        super().__init__(literal=literal, value=value, picked=picked)

class Clause(Bunch);
    def __init__(self):
        super().__init__(literals=[], _number_not_falses=None)

    def add(self, literal: Literal, sign: bool):
        self.literals.append(LitWrap(literal=literal, sign=sign))

    def value(self):
        values = [literal.literal.value for literal in self.literals]
        if any(values):
            return True
        if not any(values):
            return False
        return None

    def number_not_falses(self):
        if self._number_not_falses == None:
                self._number_not_falses = sum([literal.literal.value != False for literal in self.literals])
        return self._number_not_falses

class Solver(object):
    def __init__(self):
        self.clauses = []
        self.literals = {}

    def print(self):
        print('NClauses: {}, NLiterals: {}'.format(len(self.clauses), len(self.literals)))

    def pick_random(self):
        picked_lit = None
        for lit, val in self.literal_values.items():
            if not val:
                picked_lit = lit
        self.add_node(picked_lit, True, True)

    def solve(self):
        simplified = False
        while not simplified:
            simplified = self.simplify()

    def simplify(self):
        # Step checking for unit clauses
        unicids = [cid for (cid, n) in self.n_not_falses.items() if n == 1]
        for cid in unicids:
            for (lit, sgn) in self.clauses[cid]:
                if not self.literal_values[lit]:
                    self.add_node(lit, sgn, False)
                    return True
        return False


    def add_sat_file(self, fname):
        with open(fname) as fp:
            for line in fp:
                if line.startswith('p') or line.startswith('c'):
                    continue
                clause = Clause()
                clauseid = len(self.clauses)
                for c in line.split():
                    literal = float(c)
                    literal, sign = abs(literal), literal > 0
                    if literal == 0:
                        self.clauses.append(clause)
                        break

                    self.literals.setdefault(literal, Literal(literal))
                    self.literals[literal].clauses.append(clauseid)
                    clause.add(self.literals[literal])

if __name__ == "__main__":
    main()
