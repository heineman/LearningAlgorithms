"""Challenge questions for chapter 5"""
import timeit

from algs.table import DataTable
from algs.modeling import n_log_n_model, quadratic_model, numpy_error

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

        # Recursive case: Find largest of the possible four values.
        if L[0] < R[0]:
            if R[1] is None:
                return (R[0], L[0])
            return (R[0], R[1]) if L[0] < R[1] else (R[0], L[0])
        if L[1] is None:
            return (L[0], R[0])
        return (L[0], L[1]) if R[0] < L[1] else (L[0], R[0])

    return rtwo(0, len(A)-1)

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
    import numpy as np
    from scipy.optimize import curve_fit

    tbl = DataTable([8,12,12],['N', 'FiRec', 'Model'], output=output, decimals=decimals)
    tbl.format('FiRec', 'd')
    def exp_model(n, a, b):
        """Formula for A*N^B ."""
        return a*np.power(n, b)

    for n in range(3, 100):
        old = numRecursiveImproved[0]
        fib_with_lucas(n)
        model = exp_model(n, 0.28711343, 2.58031481)
        tbl.row([n, (numRecursiveImproved[0] - old), model])

    x_arr = np.array(tbl.column(tbl.labels[0]))
    y_arr = np.array(tbl.column(tbl.labels[1]))

    if output:
        [exp_coeffs, _]        = curve_fit(exp_model, x_arr, y_arr)
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

#######################################################################
if __name__ == '__main__':
    print(rediscover_heap())

    print(fib_with_lucas(12))

    print(num_swaps_hashable(['15', '21', '20', '2', '15', '24', '5', '19']))

    # Construct an array with UP-DOWN-UP structure.
    VALS = list(range(137))
    VALS.extend(list(range(300,200,-1)))
    VALS.extend(range(400,500))

    from algs.sorting import check_sorted
    slice_merge_sort(VALS)
    print('VALS should is sorted:', check_sorted(VALS))
