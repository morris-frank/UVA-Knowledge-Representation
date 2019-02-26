#!/bin/python
from glob import glob
from tqdm import tqdm


def convert_line(line):
    sudoku= ''
    for c in line:
        if c != '_':
            if c.isdigit():
                sudoku += c
            else:
                sudoku += '.' * (ord(c) - 96)
    assert(len(sudoku) == 81)
    return sudoku


def convert_file(fn):
    sudokus = []
    with open(fn) as f:
        for line in f:
            sudokus.append(convert_line(line))
    with open(fn + '.txt', 'w') as f:
        f.write('\n'.join(sudokus))


if __name__ == '__main__':
    for fn in tqdm(glob('./simon_sudokus/*simon')):
        convert_file(fn)
