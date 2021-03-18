"""Challenge problems for ch02."""

import timeit
import math

from algs.table import DataTable
from algs.modeling import quadratic_model, log_model, numpy_error

def log_log_model(n, a):
    """Formula for A*Log_2(N) with single coefficient."""
    if numpy_error:
        logn = math.log(n)/math.log(2)
        return a*logn
    else:
        import numpy as np
        logn = np.log(n)/np.log(2)
        return a*logn

def factorial_model(n, a):
    """Formula for A*N! with single coefficient."""
    if numpy_error:
        return a*math.factorial(n)
    else:
        from scipy.special import factorial
        return a*factorial(n)

def log_log_table(max_k=55, output=True, decimals=3):
    """
    Generate Log(Log(N)) table and model up to (but not including) 2**max_k.
    Model is defined based on first 30 values.
    """
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

    if numpy_error:
        log_log_coeff = [0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit

        [log_log_coeff, _] = curve_fit(log_log_model, np.array(xvals), np.array(yvals))
        if output:
            print('Log Log N  = {:.12f}*log2((log2(N))'.format(log_log_coeff[0]))

    tbl = DataTable([30, 10, 10], ['N', 'NumSqrt', 'Model'], decimals=decimals, output=output)
    tbl.format('NumSqrt', 'd')
    trials = [2**k for k in range(5,max_k)]
    for n in trials:
        num_sqrts = 0
        tmp = n
        while tmp >= 2:
            num_sqrts += 1
            tmp = tmp ** 0.5

        tbl.row([n, num_sqrts, log_log_model(n, log_log_coeff[0])])

    return tbl

def max_sort(A):
    """Evaluate the space complexity of this sorting algorithm."""
    result = []
    while len(A) > 1:
        index_max = max(range(len(A)), key=A.__getitem__)
        result.insert(0, A[index_max])
        A = A[:index_max] + A[index_max+1:]
    return A + result

def run_max_sort_worst_case(max_k=14, output=True, decimals=4):
    """Generate table for max sort up to (but not including 2**max_k)."""
    xvals = []
    yvals = []
    for n in [2 ** k for k in range(5, 12)]:
        sort_time = timeit.timeit(stmt='max_sort(x)', setup='''
from ch02.challenge import max_sort
import random
x=list(range({},0,-1))
random.shuffle(x)'''.format(n), number=10)
        xvals.append(n)
        yvals.append(sort_time)

    if numpy_error:
        quadratic_coeff = [0, 0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [quadratic_coeff, _] = curve_fit(quadratic_model, np.array(xvals), np.array(yvals))
        if output:
            print('Quadratic N  = {:.12f}*N*N + {:.12f}*N'.format(quadratic_coeff[0], quadratic_coeff[1]))

    tbl = DataTable([8,8,8], ['N', 'MaxSort', 'Model'], output=output, decimals=decimals)

    for n in [2 ** k for k in range(5, max_k)]:
        sort_time = timeit.timeit(stmt='max_sort(x)', setup='''
from ch02.challenge import max_sort
import random
x=list(range({},0,-1))
random.shuffle(x)'''.format(n), number=10)
        tbl.row([n, sort_time, quadratic_model(n, quadratic_coeff[0], quadratic_coeff[1])])

    return tbl

def run_permutation_sort(max_n=12, output=True, decimals=4):
    """Generate table for permutation sort up to (but not including) max_n."""
    xvals = []
    yvals = []
    for n in range(1,6):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup='''
from ch02.random_sort import permutation_sort
x=list(range({},0,-1))'''.format(n), number=10)
        xvals.append(n)
        yvals.append(sort_time)

    if numpy_error:
        factorial_coeff = [0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [factorial_coeff, _] = curve_fit(factorial_model, np.array(xvals), np.array(yvals))
        if output:
            print('Factorial N  = {:.12f}*N! '.format(factorial_coeff[0]))
            print('Estimated time to sort 20 values is {:,.2f} years'.format(
                  factorial_model(20, factorial_coeff[0])/(60*60*24*365)))

    tbl = DataTable([8,8,8], ['N', 'PermutationSort', 'Model'],
                    output=output, decimals=decimals)

    for n in range(max_n):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup='''
from ch02.random_sort import permutation_sort
x=list(range({},0,-1))'''.format(n), number=10)
        tbl.row([n, sort_time, factorial_model(n, factorial_coeff[0])])

    return tbl

def performance_bas(max_k=22, output=True, decimals=3):
    """
    Generate performance tables for binary array search up to (but not including)
    2**max_k.
    """
    # Train on five values...
    trials = [2**k for k in range(5,12)]
    xvals = []
    yvals = []
    num = 50000
    for n in trials:
        search_time = timeit.timeit(stmt='binary_array_search(x, random.randint(0,{}*4))'.format(n),
                                    setup='''
import random
from ch02.bas import binary_array_search        
x=sorted(random.sample(range({0}*4), {0}))'''.format(n), number=num)
        xvals.append(n)
        yvals.append(search_time)

    if numpy_error:
        log_coeff = [0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [log_coeff, _] = curve_fit(log_model, np.array(xvals), np.array(yvals))
        if output:
            print('Log N   = {:.12f}*log2(N)'.format(log_coeff[0]))

    tbl = DataTable([15, 10, 10], ['N', 'T(N)', 'Model'], output=output, decimals=decimals)
    trials = [2**k for k in range(5,max_k)]
    for n in trials:
        search_time = timeit.timeit(stmt='binary_array_search(x, random.randint(0,{}*2))'.format(n),
                                    setup='''
import random
from ch02.bas import binary_array_search        
x=sorted(random.sample(range({0}*4), {0}))'''.format(n), number=num)

        tbl.row([n, search_time, log_model(n, log_coeff[0])])

    return tbl

#######################################################################
if __name__ == '__main__':
    print('log log results')
    log_log_table()
    run_permutation_sort()
    print()

    run_max_sort_worst_case()
    print()
