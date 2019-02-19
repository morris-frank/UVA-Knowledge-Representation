#!/bin/python

import sys
from itertools import chain
from collections import namedtuple, OrderedDict
from argparse import ArgumentParser


SignedLiteral = namedtuple('SignedLiteral', ['lid', 'sign'])
Literal = namedtuple('Literal', ['value', 'clauses'])
Node = namedtuple('Node', ['id', 'picked'])

class BacktrackException(BaseException):
    pass


class Literal(object):
    def __init__(self, id: int, value=None):
        self.id = id
        self.value = value
        self.clauses = []

    def update(self, value):
        self.value = value
        # check for contridiction
        for clause in self.clauses:
            clause._number_not_falses() = None
            if clause.value() == False:
                raise BacktrackException


class Clause(Bunch):
    def __init__(self):
        super().__init__(signed_literals=[], _number_not_falses=None, _value=None)

    def add(self, literal: Literal, sign: bool):
        self.signed_literals.append(SignedLiteral(literal=literal, sign=sign))

    def is_tautology(self):
        counts = {}
        for signed_literal in self.signed_literals:
            if counts.setdefault(signed_literal.literal.id, signed_literal.sign) != signed_literal.sign:
                return True
        return False

    def value(self):
        if self._value != None:
            return self._value
        has_none = False
        for signed_literal in self.signed_literals:
            if signed_literal.literal.value == None:
                has_none = True
                continue
            value = not(signed_literal.literal.value ^ signed_literal.sign)
            if value:
                return True
        if has_none:
            return None
        else:
            return False;

    def number_not_falses(self):
        if self._number_not_falses == None:
            self._number_not_falses = 0
            for signed_literal in self.signed_literals:
                if signed_literal.literal.value == None:
                    self._number_not_falses += 1
                else:
                    self._number_not_falses += not(signed_literal.literal.value ^ signed_literal.sign)
        return self._number_not_falses


class Solver(object):
    def __init__(self):
        self.clauses = [] #
        self.literals = {} # ID -> Literals
        self.log = [] # List of lists

        self.next_call = None

    def print(self):
        print('NClauses: {}, NLiterals: {}'.format(len(self.clauses), len(self.literals)))

    def number_of_none_literals(self):
        n = 0
        for literal in self.literals.values():
            n += literal.value == None
        return n

    def check_done(self):
        if all([clause.value for clause in self.clauses]):
            print('Le finish')
            exit(0)

    def solve(self):
        self.fix_tautologies()
        self.next_call = self.simplify
        while self.next_call:
            _next_call = self.next_call
            self.next_call = None
            self.check_done()
            _next_call()


    def fix_tautologies(self):
        for clause in self.clauses:
            if clause.is_tautology():
                clause._value = True

    def reverse_last_decision(self):


    def update_literal():

    def solve(self,):
        return self.solve

    def unit_propagation(self):
        unit_clauses = [clause in self.clauses if len(clause) == 1]
        while unit_clauses:
            unit_clause = unit_clauses[0]

    def simplify(self):
        try:
            simplified = False
            while not simplified:
                simplified = self._simplify()
            self.check_done()
            self.next_call = self.split
        except BacktrackException:
            self.next_call = self.backtrack
            return

    def _simplify(self):
        for clause in self.clauses:
            if clause.number_not_falses != 1:
                continue
            # We got a uni clause
            for signed_literal in clause.signed_literals:
                if signed_literal.literal.value == None:
                    signed_literal.literal.update(signed_literal.sign)
                    self.log.append(Node(id=signed_literal.literal.id, picked=False))
                    return False
        return True

    def split(self):
        next_split = self.next_split()
        if next_split == None:
            self.next_call = self.backtrack
            return
        print('Last: {}, Next: {}, #Nones: {}'.format(self.get_split(), next_split, self.number_of_none_literals()))
        self.literals[next_split].update(False)
        self.log.append(Node(id=next_split, picked=True))
        self.next_call = self.simplify

    def next_split(self):
        last_split = self.get_split()
        for id, literal in self.literals.items():
            if (last_split != None and id <= last_split) or literal.value != None:
                continue
            return int(id)

    def backtrack(self):
        last_split_literal = self.literals[self.get_split()]
        if last_split_literal.value == False:
            print('Backtrack split {} was false'.format(last_split_literal.id))
            self.reverse_changes_until(last_split_literal.id)
            last_split_literal.update(True)
            self.next_call = self.simplify
        elif last_split_literal.id > 1: # Pivot was true:
            print('Backtrack split {} was true'.format(last_split_literal.id))
            self.reverse_changes_until(last_split_literal.id)
            self.log.pop()
            self.next_call = self.backtrack
        else:
            print('Problem unsolveable')
            exit(0)

    def get_split(self):
        for node in reversed(self.log):
            if not node.picked:
                continue
            return int(node.id)

    def reverse_changes_until(self, id: int):
        it = reversed(self.log)
        try:
            node = next(it)
            while True:
                self.literals[node.id].update(None)
                if int(node.id) == int(id):
                    break
                node = next(it)
                self.log.pop()
        except StopIteration:
            print(' '.join([str(node.id) for node in self.log]))

    def add_dimacs_line(self, line: str):
        clause = []
        for literal in map(int, line.split()):
            if literal == 0:
                continue
            lid, sign = abs(literal), literal > 0
            clause.append(SignedLiteral(lid=lid, sign=sign))
            self.literals.setdefault(lid, Literal(value=None, clauses=[]))
        self.clauses.append(tuple(clause))

    def add_dimacs_file(self, fname: str):
        with open(fname) as fp:
            for line in fp:
                if line.startswith('p') or line.startswith('c'):
                    continue
                self.add_dimacs_line(line)

def parse_args():
    parser = ArgumentParser(description="General SAT solver (World record as of 2021)")
    parser.add_argument('-S', dest='solver', help='The Solver to use.', type=int, choices=[1,2,3], default=1, required=True)
    parser.add_argument('filename', help='The text file to parse from.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    solver = Solver()
    solver.add_dimacs_file(args.filename)
    solver.solve()

if __name__ == "__main__":
    main()
