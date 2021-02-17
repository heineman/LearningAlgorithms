"""Challenge problems for ch02."""

import timeit

import numpy as np
from scipy.optimize import curve_fit
from algs.table import quadratic_model, log_model, DataTable

def log_log_model(n, a):
    """Formula for A*Log_2(N) with single coefficient."""
    logn = np.log(n)/np.log(2)
    return a*np.log(logn)/np.log(2)

def log_log_table():
    """Generate Log(Log(N)) table and model."""
    trials = [2**k for k in range(5,30)]
    xvals = []
    yvals = []
    for n in trials:
        num_sqrts = 0
        tmp = n
        while tmp >= 2:
            num_sqrts += 1
            tmp = tmp ** 0.5

        xvals.append(n)
        yvals.append(num_sqrts)

    [log_log_coeff, _] = curve_fit(log_log_model, np.array(xvals), np.array(yvals))
    print('Log Log N  = {:.12f}*log2((log2(N))'.format(log_log_coeff[0]))

    tbl = DataTable([30, 10, 10], ['N', 'NumSqrt', 'Model'], decimals=3)
    tbl.format('NumSqrt', 'd')
    trials = [2**k for k in range(5,51)]
    for n in trials:
        num_sqrts = 0
        tmp = n
        while tmp >= 2:
            num_sqrts += 1
            tmp = tmp ** 0.5

        tbl.row([n, num_sqrts, log_log_model(n, log_log_coeff[0])])

def max_sort(A):
    """Evaluate the space complexity of this sorting algorithm."""
    result = []
    while len(A) > 1:
        index_max = max(range(len(A)), key=A.__getitem__)
        result.insert(0, A[index_max])
        A = A[:index_max] + A[index_max+1:]
    return A + result

def run_max_sort_worst_case():
    """Generate table for max sort."""
    xvals = []
    yvals = []
    for n in [2 ** k for k in range(5, 12)]:
        sort_time = timeit.timeit(stmt='max_sort(x)', setup=f'''
from ch02.challenge import max_sort
import random
x=list(range({n},0,-1))
random.shuffle(x)''', number=10)
        xvals.append(n)
        yvals.append(sort_time)

    [quadratic_coeff, _] = curve_fit(quadratic_model, np.array(xvals), np.array(yvals))
    print('Quadratic N  = {:.12f}*N*N + {:.12f}*N'.format(quadratic_coeff[0], quadratic_coeff[1]))

    tbl = DataTable([8,8,8], ['N', 'MaxSort', 'Model'], decimals=4)

    for n in [2 ** k for k in range(5, 15)]:
        sort_time = timeit.timeit(stmt='max_sort(x)', setup=f'''
from ch02.challenge import max_sort
import random
x=list(range({n},0,-1))
random.shuffle(x)''', number=10)
        tbl.row([n, sort_time, quadratic_model(n, quadratic_coeff[0], quadratic_coeff[1])])

def factorial_model(n, a):
    """Formula for A*N! with single coefficient."""
    from scipy.special import factorial
    return a*factorial(n)

def run_permutation_sort():
    """Generate table for permutation sort."""
    xvals = []
    yvals = []
    for n in range(1,6):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup=f'''
from ch02.random_sort import permutation_sort
x=list(range({n},0,-1))''', number=10)
        xvals.append(n)
        yvals.append(sort_time)

    [factorial_coeff, _] = curve_fit(factorial_model, np.array(xvals), np.array(yvals))
    print('Factorial N  = {:.12f}*N! '.format(factorial_coeff[0]))
    print('Estimated time to sort 20 values is {:,.2f} years'.format(
          factorial_model(20, factorial_coeff[0])/(60*60*24*365)))

    tbl = DataTable([8,8,8], ['N', 'PermutationSort', 'Model'], decimals=4)

    for n in range(13):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup=f'''
from ch02.random_sort import permutation_sort
x=list(range({n},0,-1))''', number=10)
        tbl.row([n, sort_time, factorial_model(n, factorial_coeff[0])])

def performance_bas():
    """Generate performance tables for binary array search."""
    # Train on five values...
    trials = [2**k for k in range(5,12)]
    xvals = []
    yvals = []
    num = 50000
    for n in trials:
        search_time = timeit.timeit(stmt=f'binary_array_search(x, random.randint(0,{n}*4))',
                                    setup=f'''
import random
from ch02.bas import binary_array_search        
x=sorted(random.sample(range({n}*4), {n}))''', number=num)
        xvals.append(n)
        yvals.append(search_time)

    [log_coeff, _] = curve_fit(log_model, np.array(xvals), np.array(yvals))
    print('Log N   = {:.12f}*log2(N)'.format(log_coeff[0]))

    tbl = DataTable([15, 10, 10], ['N', 'T(N)', 'Model'], decimals=3)
    trials = [2**k for k in range(5,22)]
    for n in trials:
        search_time = timeit.timeit(stmt=f'binary_array_search(x, random.randint(0,{n}*2))', 
                                    setup=f'''
import random
from ch02.bas import binary_array_search        
x=sorted(random.sample(range({n}*4), {n}))''', number=num)

        tbl.row([n, search_time, log_model(n, log_coeff[0])])

    return tbl

#######################################################################
if __name__ == '__main__':
    run_permutation_sort()
    print()

    run_max_sort_worst_case()
    print()

    print('log log results')
    log_log_table()
    print()
