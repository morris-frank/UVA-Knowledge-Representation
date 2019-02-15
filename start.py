#!/bin/python
from itertools import chain
from collections import namedtuple, OrderedDict
from typing import List


LitWrap = namedtuple('LitWrap', ['literal', 'sign'])
Node = namedtuple('Node', ['id', 'picked'])


def main():
    solver = Solver()
    solver.add_sat_file('test.sat')
    solver.print()
    # solver.solve()


class BacktrackException(Exception):
    pass


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class Literal(Bunch):
    def __init__(self, id: int, value=None):
        super().__init__(id=id, value=value)
        self.clauses = []

    def update(self, value):
        self.value = value

        # check for contridiction
        for clause in self.clauses:
            clause._number_not_falses = None
            if clause.value == False:
                raise BacktrackException

class Clause(Bunch):
    def __init__(self):
        super().__init__(literals=[], _number_not_falses=None, _value=None)

    def add(self, literal: Literal, sign: bool):
        self.literals.append(LitWrap(literal=literal, sign=sign))

    def is_tautology(self):
        counts = {}
        for litwrap in self.literals:
            if counts.setdefault(litwrap.literal.id, sign) != sign:
                return True
        return False

    @property
    def value(self):
        if _value != None:
            return _value
        values = [not(litwrap.literal.value ^ litwrap.sign) for litwrap in self.literals]
        if any(values):
            return True
        if not any(values):
            return False
        return None

    @property
    def number_not_falses(self):
        if self._number_not_falses == None:
                self._number_not_falses = sum([literal.literal.value != False for literal in self.literals])
        return self._number_not_falses


class Solver(object):
    def __init__(self):
        self.clauses = []
        self.literals = {}
        self.log = []
        self.pivot = None

    def print(self):
        print('NClauses: {}, NLiterals: {}'.format(len(self.clauses), len(self.literals)))

    def next_pivot(self):
        for id, literal in self.literals.items():
            if id <= self.pivot or literal.value != None:
                continue
            self.pivot = id

    def reverse_changes_until(self, id):
        it = reversed(self.log)
        while:
            self.literals[node.id].update(None)
            if node.literal == id:
                self.log.pop()
                break
            next(it)
            self.log.pop()

    def find_last_pivot(self):
        for node in reversed(self.log):
            if not node.picked:
                continue
            return node.id

    def backtrack(self):
        pivot = self.literals[self.pivot]
        if pivot.value == False:
            self.reverse_changes_until(pivot.id)
            pivot.update(True)
            self.log.append(Node(id=pivot.id, picked=True))
            self.simplify()
        elif pivot.id > 1 # Pivot was true:
            self.reverse_changes_until(pivot.id)
            self.pivot = self.find_last_pivot()
            self.backtrack()
        else:
            print('EMPTY')
            exit(0)

    def check_done(self):
        if all([clause.value for clause in self.clauses]):
            print('Le finish')
            exit(0)

    def split(self):
        self.next_pivot()
        self.literals[self.pivot].update(False)
        self.log.append(Node(id=self.pivot, picked=True))
        self.simplify()

    def simplify(self):
        try:
            simplified = False
            while not simplified:
                simplified = self._simplify()
            self.check_done()
            self.split()
        except BacktrackException:
            self.backtrack()

    def fix_tautologies(self):
        for clause in self.clauses:
            if clause.is_tautology():
                clause._value = True

    def _simplify(self):
        for clause in self.clauses:
            if clause.number_not_falses != 1:
                continue

            # We got a uni clause
            for litwrap in clause.literals:
                if litwrap.literal.value == None:
                    litwrap.literal.update(litwrap.sign)
                    self.log.append(Node(id=litwrap.literal.id, picked=False))
                    return True
        return False

    def solve(self):
        self.fix_tautologies()
        self.simplify()

    def add_sat_file(self, fname):
        _literals = {}
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

                    _literals.setdefault(literal, Literal(literal))
                    _literals[literal].clauses.append(clause)
                    clause.add(literal=_literals[literal], sign=sign)
        self.literals = OrderedDict(sorted(chain(self.literals.items(), _literals.items()), key=lambda x: x[0]))

if __name__ == "__main__":
    main()
