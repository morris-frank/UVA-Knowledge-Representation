#!/bin/bash

NTHREADS=24

timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/block.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/simple.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/intersect.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/set.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/extreme.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 sudokus/simon/recursive.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/block_x.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/simple_x.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/intersect_x.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/set_x.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/extreme_x.simon.txt
timeout 1200 python3 ./sudoku.py -p$NTHREADS -S4 -x sudokus/simon/recursive_x.simon.txt
