#!/bin/python
import numpy as np
from matplotlib import pyplot as plt
from glob import glob

givens = []
for fn in glob('./simon_sudokus/block.simon*txt'):
    with open(fn) as f:
        for line in f:
            givens.append(81 - line.count('.'))
givens = np.array(givens)
print('min: {}, max: {}, mean: {}, var: {}'.format(givens.min(), givens.max(), givens.mean(), givens.std()))

fig = plt.figure()
plt.hist(givens)
plt.show()