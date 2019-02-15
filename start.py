#!/bin/python
from collections import namedtuple

Node = namedtuple('Node' , ['literal', 'value', 'picked'])

def main():
    solver = Solver()
    solver.add_sat_file('test.sat')
    solver.print()
    solver.simplify()
    solver.print()
    solver.simplify()
    solver.print()

class Solver(object):
    def __init__(self):
        self.clauses = []
        self.n_not_falses = {}
        self.literal_values = {}
        self.literal_clauses = {}
        self.clause_done = {}
        self.nodes = []

    def print(self):
        print('NClauses: {}, NLiterals: {}, NNodes: {}'.format(len(self.clauses), len(self.literal_values), len(self.nodes)))
        for node in self.nodes:
            print(node)

    def add_node(self, literal: int, value: bool, picked: bool):
        self.nodes.append(Node(literal, value, picked))
        self.literal_values[literal] = value

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
                clause = []
                cid = len(self.clauses)
                for c in line.split():
                    lit = float(c)
                    if lit == 0:
                        self.n_not_falses[cid] = len(clause)
                        self.clauses.append(clause)
                        break
                    self.literal_clauses.setdefault(lit, [])
                    self.literal_values[lit] = None
                    self.literal_clauses[lit].append(cid)
                    clause.append((abs(lit), lit >0))

if __name__ == "__main__":
    main()
