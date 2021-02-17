"""
Generate timing results for inefficient sorting algorithms.

    :Example:

    Random Sort Trials
    N    TimeToSort
    1    0.00
    2    0.00
    3    0.00
    4    0.00
    5    0.00
    6    0.00
    7    0.01
    8    0.26
    9    2.66
    10  75.65     -- sometimes you don't get lucky
    11   6.09     -- sometimes you do get lucky!
"""

import timeit
import numpy as np
from scipy.optimize import curve_fit

from algs.table import DataTable, factorial_model

def run_permutation_sort_worst_case():
    """Generate table for permutation sort."""
    x = []
    y = []
    for n in range(10):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup=f'''
from ch02.random_sort import permutation_sort
x=list(range({n},0,-1))''', number=1)
        x.append(n)
        y.append(sort_time)

    # Coefficients are returned as first argument
    [factorial_coeffs, _] = curve_fit(factorial_model, np.array(x), np.array(y))
    print('Factorial    = {}*N!'.format(factorial_coeffs[0]))

    tbl = DataTable([8,8,8], ['N', 'TimeToSort', 'Model'], decimals=4)

    for n in range(13):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup=f'''
from ch02.random_sort import permutation_sort
x=list(range({n},0,-1))''', number=1)
        tbl.row([n, sort_time, factorial_model(n, factorial_coeffs[0])])

def run_random_sort():
    """Generate table for random sort."""
    x = []
    y = []
    for n in range(10):
        sort_time = timeit.timeit(stmt='random_sort(x)', setup=f'''
import random
from ch02.random_sort import random_sort
x=list(range({n}))
random.shuffle(x)''', number=1)
        x.append(n)
        y.append(sort_time)

    # Coefficients are returned as first argument
    [factorial_coeffs, _] = curve_fit(factorial_model, np.array(x), np.array(y))
    print('Factorial    = {}*N!'.format(factorial_coeffs[0]))

    tbl = DataTable([8,8,8], ['N', 'TimeToSort', 'Model'], decimals=4)

    for n in range(12):
        sort_time = timeit.timeit(stmt='random_sort(x)', setup=f'''
import random
from ch02.random_sort import random_sort
x=list(range({n}))
random.shuffle(x)''', number=1)
        tbl.row([n, sort_time, factorial_model(n, factorial_coeffs[0])])

#######################################################################
if __name__ == '__main__':
    print('Permutation Sort Trials (up to N=13): These can take Unusually Long.')
    run_permutation_sort_worst_case()

    print('Random Sort Trials (up to N=11): These can take Unusually Long.')
    run_random_sort()
