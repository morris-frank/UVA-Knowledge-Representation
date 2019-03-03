#!/bin/python3

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import json
import numpy as np
from glob import glob
from typing import List, Any, Dict
from os.path import basename
import seaborn as sns

sns.set('paper', 'whitegrid', 'tab10', font_scale=1.4)
DIFFICULTIES = ['block', 'simple', 'intersect', 'set', 'extreme', 'recursive']
SOLVERS = ['Next', 'DLIS', 'VSIDS', 'Jeroslow-Wang']


def savefig(filename):
    plt.tight_layout()
    plt.gcf().savefig('./figures/{}.pdf'.format(filename), dpi=200)
    plt.cla()


def create_padded_array(llist: List[List[Any]]) -> np.ndarray:
    w, h = max([len(x) for x in llist]), len(llist)
    arr = np.full((h,w), np.nan)
    for idx, _el in enumerate(llist):
        arr[idx, 0:len(_el)] = _el
        arr[idx, len(_el):] = _el[-1]
    return arr


def load_log_file(log_file: str) -> List[Dict[str, Any]]:
    data = []
    difficulty = basename(log_file).split('.')[0].split('_x')[0]
    cross_rules = '_x' in log_file
    number_of_rules = 11988 + cross_rules * 1296
    with open(log_file) as f:
        for line in f:
            _data = json.loads(line)
            log = np.array(_data['iter_log'])
            if log.shape[0] > 200:
                continue
            givens = _data['number_clauses'] - number_of_rules
            data.append({'nsolve': log[:,1], 'nsolution': log[:,5], 'nunit': log[:,3], 'nbacktrack': log[:,4],
                         'nassign': log[:,2], 'timings': log[:,6], 'Clues': givens, 'Difficulty': difficulty,
                         'cross': cross_rules, 'backtracks': _data['number_backtracks'],
                         'Heuristic': SOLVERS[_data['solver']-1], 'assignments': _data['assign_calls'],
                         'splits': _data['split_calls'], 'solves': _data['solve_calls']})
    return data


def load_logs() -> pd.DataFrame:
    data = []
    for log_file in glob('./log/simon/*.log'):
        data.extend(load_log_file(log_file))
    df = pd.DataFrame(data)
    df.Difficulty = df.Difficulty.astype(CategoricalDtype(categories=DIFFICULTIES, ordered=True))
    df.Heuristic = df.Heuristic.astype(CategoricalDtype(categories=SOLVERS, ordered=True))
    return df


def generate_plots(df):
    textwidth = 452./72
    golden_mean = (5**.5-1)/2
    fig = plt.figure(figsize=(textwidth, textwidth * golden_mean))
    ax = fig.add_subplot(111)

    sns.boxenplot(x='Difficulty', y='backtracks', data=df, ax=ax, outlier_prop=0.1)
    savefig('box_difficulty_backtracks_solver_all')
    for solver in SOLVERS:
        sns.boxenplot(x='Difficulty', y='backtracks', data=df[df.Heuristic==solver], ax=ax, outlier_prop=0.1)
        savefig('box_difficulty_backtracks_solver_' + str(solver))

    sns.pointplot(x='Difficulty', y='backtracks', hue='Heuristic', data=df[df.cross==True], ax=ax)
    savefig('pnt_difficulty_backtracks_solver_cross')

    sns.pointplot(x='Difficulty', y='backtracks', hue='Heuristic', data=df[df.cross==False], ax=ax)
    savefig('pnt_difficulty_backtracks_solver_nocross')

    nsolutions_b = create_padded_array(df[(df.Difficulty=='extreme') & (df.cross==True)].nsolution.to_numpy())
    nsolutions_r = create_padded_array(df[(df.Difficulty=='extreme') & (df.cross==False)].nsolution.to_numpy())
    ax.plot(range(nsolutions_b.shape[1]), nsolutions_b.mean(0), label='Cross-rules')
    ax.plot(range(nsolutions_r.shape[1]), nsolutions_r.mean(0), label='NoCross')
    plt.xlabel('Calls to Solve')
    plt.ylabel('Size Solution')
    ax.legend()
    savefig('line_nsolutions_all')

    sns.pointplot(x='Clues', y='backtracks', hue='Difficulty', data=df[df.cross==True], ax=ax)
    savefig('pnt_clues_backtracks_solver_cross')

    sns.pointplot(x='Clues', y='backtracks', hue='Difficulty', data=df[df.cross==False], ax=ax)
    savefig('pnt_clues_backtracks_solver_nocross')

def main():
    df = load_logs()
    generate_plots(df)


if __name__ == '__main__':
    main()
