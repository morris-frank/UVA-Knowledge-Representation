#!/bin/python
import sys
import SAT


def main():
    SAT.VERBOSE = False
    fname = './damnhard.sdk.txt'

    with open(fname) as fp:
        for line in fp:
            SAT.run_sudoku(line)


if __name__ == "__main__":
    main()
