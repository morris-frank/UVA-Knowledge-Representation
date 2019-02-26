#!/bin/bash

NTHREADS=24

python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/block.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/simple.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/intersect.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/set.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/extreme.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 sudokus/simon/recursive.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/block_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/simple_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/intersect_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/set_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/extreme_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S1 -x sudokus/simon/recursive_x.simon.txt

python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/block.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/simple.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/intersect.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/set.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/extreme.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 sudokus/simon/recursive.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/block_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/simple_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/intersect_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/set_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/extreme_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S2 -x sudokus/simon/recursive_x.simon.txt

python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/block.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/simple.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/intersect.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/set.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/extreme.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 sudokus/simon/recursive.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/block_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/simple_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/intersect_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/set_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/extreme_x.simon.txt
python3 ./sudoku.py -p$NTHREADS -S3 -x sudokus/simon/recursive_x.simon.txt
