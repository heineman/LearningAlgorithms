"""
Challenge Exercises for Chapter 2.
"""

import timeit
import math

from algs.table import DataTable, ExerciseNum, caption
from algs.modeling import quadratic_model, log_model, numpy_error

def fragment_1(N):
    """Fragment-1 for exercise."""
    ct = 0
    for _ in range(100):
        for _ in range(N):
            for _ in range(10000):
                ct += 1
    return ct

def fragment_2(N):
    """Fragment-2 for exercise."""
    ct = 0
    for _ in range(N):
        for _ in range(N):
            for _ in range(100):
                ct += 1
    return ct

def fragment_3(N):
    """Fragment-3 for exercise."""
    ct = 0
    for _ in range(0,N,2):
        for _ in range(0,N,2):
            ct += 1
    return ct

def fragment_4(N):
    """Fragment-4 for exercise."""
    ct = 0
    while N > 1:
        ct += 1
        N = N // 2
    return ct

def fragment_5(N):
    """Fragment-5 for exercise."""
    ct = 0
    for _ in range(2,N,3):
        for _ in range(3,N,2):
            ct += 1
    return ct

def f4(N):
    """Fragment for exercise."""
    ct = 1
    while N >= 2:
        ct = ct + 1
        N = N ** 0.5
    return ct

def fragment_counting(max_k=10, output=True):
    """Generate table for counts of fragments up to (but including) 2**max_k."""
    trials = [2**k for k in range(5,max_k)]
    tbl = DataTable([8,15,8,8,8,8],['N', 'F1', 'F2', 'F3', 'F4', 'F5'], output=output)
    for i in range(1,6):
        tbl.format('F{}'.format(i), 'd')
    for N in trials:
        tbl.row([N, fragment_1(N), fragment_2(N), fragment_3(N), fragment_4(N), fragment_5(N)])
    return tbl

def another_fragment_counting(max_k=20, output=True):
    """Generate table for counts of fragments up to (but including) 2**max_k."""
    if numpy_error:
        a = 0,0
    else:
        import numpy as np
        from scipy.optimize import curve_fit

        def log_log_model(n, a):
            """Formula for A*Log_2(Log_2(N)) with single coefficient."""
            logn = np.log2(n)
            return a*np.log2(logn)

        # Train Model
        trials = [2**k for k in range(5,15)]
        nvals = []
        yvals = []
        for N in trials:
            nvals.append(N)
            yvals.append(f4(N))

        [a, _] = curve_fit(log_log_model, np.array(nvals), np.array(yvals))
        if output:
            print('LOG_LOG_MODEL = {}*log(log(N))'.format(a))

    trials = [2**k for k in range(5, max_k)]
    tbl = DataTable([8,8,8],['N', 'F4', 'Model'], output=output)
    tbl.format('F4', 'd')
    for N in trials:
        tbl.row([N, f4(N), a[0]*math.log2(math.log2(N))])
    return tbl

def factorial_model(n, a):
    """Formula for A*N! with single coefficient."""
    if numpy_error:
        return a*math.factorial(n)
    from scipy.special import factorial
    return a*factorial(n)

def max_sort(A):
    """Evaluate the space complexity of this sorting algorithm."""
    result = []
    while len(A) > 1:
        index_max = max(range(len(A)), key=A.__getitem__)
        result.insert(0, A[index_max])
        A = list(A[:index_max]) + list(A[index_max+1:])
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
    chapter = 2
    with ExerciseNum(1) as exercise_number:
        fragment_counting()
        print(caption(chapter, exercise_number),
              'Fragment Evaluation')

    with ExerciseNum(2) as exercise_number:
        another_fragment_counting()
        print(caption(chapter, exercise_number),
              'Second Fragment Evaluation')
        print()

    with ExerciseNum(3) as exercise_number:
        run_permutation_sort()
        print(caption(chapter, exercise_number),
              'Permutation Sort Exercise')
        print()

    with ExerciseNum(4) as exercise_number:
        performance_bas()
        print(caption(chapter, exercise_number),
              'Binary Array Search Evidence')
        print()

    with ExerciseNum(5) as exercise_number:
        run_max_sort_worst_case()
        print(caption(chapter, exercise_number),
              'Max sort')
        print()
