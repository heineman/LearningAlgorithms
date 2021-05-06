"""
Challenge Exercises for Chapter 5.
"""

import timeit

from algs.table import DataTable, ExerciseNum, caption
from algs.modeling import n_log_n_model, quadratic_model, numpy_error
from ch01.book import Order

numRecursiveImproved = [0]

def num_swaps(A):
    """Given an array of integers from 0 to N-1, return number of swaps to sort."""
    N = len(A)
    seen = [False] * N

    ct = 0
    for i in range(N):
        if not seen[i]:
            idx = i
            num = 0
            while not seen[idx]:
                num += 1
                seen[idx] = True
                idx = A[idx]

            ct += (num - 1)       # number of swaps is one less than size

    return ct

def num_swaps_hashable(A):
    """Given an array of distinct strings, return minimum number of swaps."""
    N = len(A)
    seen = {}
    final = {}
    original = list(A)

    # Selection sort and remember locations
    for i in range(N-1):
        min_index = i
        for j in range(i+1, N):
            if A[j] < A[min_index]:
                min_index = j

        final[A[min_index]] = i
        A[i],A[min_index] = A[min_index],A[i]
    final[A[N-1]] = N-1    # TRICKY can't forget this one

    ct = 0
    for i in range(N):
        if not original[i] in seen:
            idx = i
            num = 0
            while original[idx] not in seen:
                num += 1
                seen[original[idx]] = True
                idx = final[original[idx]]    # move to where final location will be

            ct += (num - 1)       # number of swaps is one less than size

    return ct

def slice_merge_sort(A):
    """Merge Sort where merge uses Python slice."""
    aux = [None] * len(A)

    def rsort(lo, hi):
        if hi <= lo:
            return

        mid = (lo+hi) // 2
        rsort(lo, mid)
        rsort(mid+1, hi)
        merge(lo, mid, hi)

    def merge(lo, mid, hi):
        # copy results of sorted sub-problems into auxiliary storage
        aux[lo:hi+1] = A[lo:hi+1]

        i = lo       # starting index into left sorted sub-array
        j = mid+1    # starting index into right sorted sub-array

        for k in range(lo, hi+1):
            if i > mid:
                A[k:hi+1] = aux[j:j+hi+1-k]
                return
            if j > hi:
                A[k:hi+1] = aux[i:i+hi+1-k]
                return
            if aux[j] < aux[i]:
                A[k] = aux[j]
                j += 1
            else:
                A[k] = aux[i]
                i += 1

    rsort(0, len(A)-1)

def recursive_two(A):
    """Return two largest values in A, using recursive approach."""

    def rtwo(lo, hi):
        # Base case: 1 or two values
        if lo == hi: return (A[lo], None)
        if lo+1 == hi:
            if A[lo] < A[hi]:
                return (A[hi], A[lo])
            return (A[lo], A[hi])

        mid = (lo+hi) // 2
        L = rtwo(lo, mid)
        R = rtwo(mid+1, hi)

        # Recursive case: Find largest of the possible four values. Note
        # That L[1] can never be None since that would have been handled
        # By the special case above where lo+1 == hi
        if L[0] < R[0]:
            if R[1] is None:
                return (R[0], L[0])
            return (R[0], R[1]) if L[0] < R[1] else (R[0], L[0])
        return (L[0], L[1]) if R[0] < L[1] else (L[0], R[0])

    return rtwo(0, len(A)-1)

def run_largest_two_trials_with_recursive(mode, max_k=22, output=True, decimals=2):
    """Mode is either Order.REVERSED or Order.SHUFFLED for 2**k up to (but not including) max_k."""
    tbl = DataTable([10,15,15,10,10,15,15],
        ['N','double_two','mutable_two','largest_two','sorting_two','tournament_two','recursive_two'],
        output=output, decimals=decimals)

    if mode is Order.REVERSED:
        prepare = 'list(reversed(x))'
    if mode is Order.SHUFFLED:
        prepare = 'random.shuffle(x)'

    trials = [2**k for k in range(10,max_k)]
    num = 100
    for n in trials:
        if mode is Order.ALTERNATING:
            prepare = '''
up_down = zip(range(0,{0},2),range({0}-1,0,-2))
x=[i for i in itertools.chain(*up_down)]
'''.format(n)
        m_dt = timeit.timeit(stmt='double_two(x)', setup='''
import random
from ch01.largest_two import double_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_mt = timeit.timeit(stmt='mutable_two(x)', setup='''
import random
from ch01.largest_two import mutable_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_lt = timeit.timeit(stmt='largest_two(x)', setup='''
import random
from ch01.largest_two import largest_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        # hard-code these values since take too long to compute...
        if n > 1048576:
            m_tt = None
        else:
            m_tt = timeit.timeit(stmt='tournament_two(x)', setup='''
import random
from ch01.largest_two import tournament_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_st = timeit.timeit(stmt='sorting_two(x)', setup='''
import random
from ch01.largest_two import sorting_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_rt = timeit.timeit(stmt='recursive_two(x)', setup='''
import random
from ch05.challenge import recursive_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        # Skip runs that are going to be too expensive
        if m_tt:
            tbl.row([n, m_dt, m_mt, m_lt, m_st, m_tt, m_rt])
        else:
            tbl.row([n, m_dt, m_mt, m_lt, m_st ])

    return tbl

def fib(n):
    """Inefficient Fibonacci recurive implementation."""
    if n <= 0: return 0
    if n == 1: return 1

    return fib(n-1) + fib(n-2)

fib_profile_count = [0]
def fib_profile(n):
    """Inefficient Fibonacci recurive implementation."""
    fib_profile_count[0] += 1
    if n <= 0: return 0
    if n <= 1: return 1

    return fib_profile(n-1) + fib_profile(n-2)

def fib_with_lucas(n):
    """
    F_(x+y) = 1/2 * (F_x * L_y) + (F_y * L_x)

    Improved efficiency using Lucas numbers.
    """
    numRecursiveImproved[0] += 1
    if n == 0: return 0
    if n <= 2: return 1
    if n == 3: return 2     # Needs to be here to prevent infinite recursion

    remainder = n - n//2
    return (fib_with_lucas(n//2)*lucas_with_fib(remainder) + fib_with_lucas(remainder)*lucas_with_fib(n//2)) / 2

def lucas_with_fib(n):
    """
    Improved recursive implementation that takes advantage of identify that:

    Ln = Fn-1 + Fn+1 for n > 1
    """
    numRecursiveImproved[0] += 1
    if n == 0: return 2
    if n == 1: return 1

    return fib_with_lucas(n-1) + fib_with_lucas(n+1)

def fib_table(output=True, decimals=3):
    """Generate table showing reduced recursive invocations of fibonacci."""
    import math

    tbl = DataTable([8,12,12],['N', 'FiRec', 'Model'], output=output, decimals=decimals)
    tbl.format('FiRec', 'd')
    def exp_model(n, a, b):
        """Formula for A*N^B ."""
        return a*math.pow(n, b)

    for n in range(3, 100):
        old = numRecursiveImproved[0]
        fib_with_lucas(n)
        model = exp_model(n, 0.28711343, 2.58031481)
        tbl.row([n, (numRecursiveImproved[0] - old), model])

    if numpy_error:
        pass
    else:
        import numpy as np
        from scipy.optimize import curve_fit

        x_arr = np.array(tbl.column(tbl.labels[0]))
        y_arr = np.array(tbl.column(tbl.labels[1]))

        def np_exp_model(n, a, b):
            """Formula for A*N^B ."""
            return a*np.power(n, b)

        if output:
            [exp_coeffs, _]        = curve_fit(np_exp_model, x_arr, y_arr)
            print('A*N^B  = {:.12f}*N^{:f} '.format(exp_coeffs[0], exp_coeffs[1]))

    return tbl

def rediscover_heap(num_trials=10000000):
    """
    Given a partial heap, rediscover original input probabilistically.

    This might not work the first time, but after repeated attempts, the following
    possible starting points were found:

    [15, 12, 7, 4, 13, 8, 11, 14, 2, 1, 10, 9, 6, 9, 12, 8, 5, 14]

    [8, 2, 15, 5, 1, 14, 11, 4, 12, 12, 10, 13, 6, 9, 7, 14, 9, 8]  found in 2,380,433 tries

    [13, 14, 12, 5, 10, 6, 14, 11, 9, 1, 12, 8, 15, 9, 7, 4, 8, 2]

    [9, 10, 6, 13, 15, 8, 9, 4, 2, 1, 11, 14, 14, 12, 7, 8, 5, 12] found in 8394544 attempts.

    [5, 9, 6, 14, 10, 13, 12, 11, 15, 1, 12, 8, 14, 9, 7, 4, 8, 2] found in 3234220 attempts
       with seed 14
    """
    from ch05.heapsort import HeapSort
    from random import shuffle, seed
    A = [15, 13, 14, 12, 11, 12, 14, 8, 9, 1, 10, 8, 6, 9, 7, 4, 5, 2]
    N = len(A)
    more = 2
    seed(14)
    for i in range(num_trials):
        copy = list(A)
        shuffle(copy)
        copy1 = list(copy)
        hs = HeapSort(copy)
        one = hs.A[N//2 - more:]
        two = A[N//2 - more:]
        if one == two:
            return '{} found in {} attempts.'.format(copy1, i)

    return 'none found in {} attempts'.format(i)

def insertion_sort_bas(max_k=18, output=True, decimals=3):
    """Generate Table for Insertion Sort."""
    # Evaluate prototype execution
    x = []
    y = []
    for n in [2**k for k in range(8, 12)]:
        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(A)', setup='''
import random
from ch05.sorting import insertion_sort_bas
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=10))
        x.append(n)
        y.append(m_insert_bas)

    # Coefficients are returned as first argument
    if numpy_error:
        log_coeffs = quadratic_coeffs = [0, 0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [log_coeffs, _] = curve_fit(n_log_n_model, np.array(x), np.array(y))
        [quadratic_coeffs, _] = curve_fit(quadratic_model, np.array(x), np.array(y))

    if output:
        print('Quadratic = {}*N*N + {}*N'.format(quadratic_coeffs[0], quadratic_coeffs[1]))
        print('Log       = {:.12f}*N*log2(N)'.format(log_coeffs[0]))
        print()

    tbl = DataTable([12,10,10,10],['N','Time','Quad','Log'], output=output, decimals=decimals)
    for n,p in zip(x,y):
        tbl.row([n, p, quadratic_model(n,
                quadratic_coeffs[0], quadratic_coeffs[1]), n_log_n_model(n, log_coeffs[0])])

    for n in [2**k for k in range(12, max_k)]:
        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(A)', setup='''
import random
from ch05.sorting import insertion_sort_bas
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=10))
        tbl.row([n, m_insert_bas,
            quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
            n_log_n_model(n, log_coeffs[0])])
    return tbl

def trial_merge_sort_python_style(max_k=15, output=True, decimals=3):
    """Empirical trial for merge sort using slicing."""
    tbl = DataTable([8, 8, 8], ['N', 'merge', 'mergeSlice'], output=output, decimals=decimals)
    for n in [2**k for k in range(8, max_k)]:
        m_slice = 1000*min(timeit.repeat(stmt='slice_merge_sort(A)', setup='''
import random
from ch05.challenge import slice_merge_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=10))

        m_merge = 1000*min(timeit.repeat(stmt='merge_sort(A)', setup='''
import random
from ch05.merge import merge_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=10))

        tbl.row([n, m_merge, m_slice])
    return tbl

#######################################################################
if __name__ == '__main__':
    chapter = 5

    with ExerciseNum(1) as exercise_number:
        print('find count() in ch05.recursion')
        print(caption(chapter, exercise_number), 'Recursive count method')
        print()

    with ExerciseNum(2) as exercise_number:
        print('find num_swaps() in ch05.challenge')
        print(caption(chapter, exercise_number), 'Compute number of swaps in array with 0 .. N-1')
        print()

    with ExerciseNum(3) as exercise_number:
        from ch05.recursion import find_max_with_count
        print('how many comparisons to find max in array of size N=15:', find_max_with_count(list(range(15)))[0], 'or N-1')
        print()

    with ExerciseNum(4) as exercise_number:
        trial_merge_sort_python_style()
        print('Merge Sort with Python slice improves performance of MergeSort.')
        print()

    with ExerciseNum(5) as exercise_number:
        run_largest_two_trials_with_recursive(Order.REVERSED)
        print('find recursive_two() in ch05.challenge.')
        print()

    with ExerciseNum(6) as exercise_number:
        fib_table()
        print('find recursive_two() in ch05.challenge.')
        print()

    print('Attempting to rediscover heap. This might take unusually long time')
    print(rediscover_heap())
