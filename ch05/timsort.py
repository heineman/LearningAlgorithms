"""
Simplistic non-optimized, native Python implementation showing the mechanics
of TimSort.

This code is designed to show how TimSort uses Insertion Sort and Merge Sort
as its constituent building blocks. It is not the actual sorting algorithm,
because of extra complexities that optimize this base algorithm even further.

Full details on the sorting algorithm are in the actual CPython code base,
but Tim Peters has provided documentation explaining reasons behind many
of the choices in Tim Sort.

https://hg.python.org/cpython/file/tip/Objects/listsort.txt
"""
import timeit
from algs.table import DataTable

def merge(A, lo, mid, hi, aux):
    """Merge two (consecutive) runs together."""
    aux[lo:hi+1] = A[lo:hi+1]

    left = lo
    right = mid + 1
    for i in range(lo, hi+1):
        if left > mid:
            A[i] = aux[right]
            right += 1
        elif right > hi:
            A[i] = aux[left]
            left += 1
        elif aux[right] < aux[left]:
            A[i] = aux[right]
            right += 1
        else:
            A[i] = aux[left]
            left += 1

# https://hg.python.org/cpython/file/tip/Objects/listsort.txt
# Instead we pick a minrun in range(32, 65) such that N/minrun is exactly a
# power of 2, or if that isn't possible, is close to, but strictly less than,
# a power of 2.  This is easier to do than it may sound:  take the first 6
# bits of N, and add 1 if any of the remaining bits are set.  In fact, that
# rule covers every case in this section, including small N and exact powers
# of 2; merge_compute_minrun() is a deceptively simple function.

def compute_min_run(n):
    """Compute min_run to use when sorting n total values."""
    # Used to add 1 if any remaining bits are set
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(A, lo, hi):
    """Sort A[lo .. hi] using Insertion Sort."""
    for i in range(lo+1,hi+1):
        for j in range(i,lo,-1):
            if A[j-1] < A[j]:
                break
            A[j],A[j-1] = A[j-1],A[j]

def tim_sort(A):
    """Apply simplistic Tim Sort implementation on A."""
    # Small arrays are sorted using insertion sort
    N = len(A)
    if N < 64:
        insertion_sort(A,0,N-1)
        return

    # Insertion sort in strips of 'size'
    size = compute_min_run(N)
    for lo in range(0, N, size):
        insertion_sort(A, lo, min(lo+size-1, N-1))

    aux = [None]*N
    while size < N:
        # Merge all doubled ranges, taking care with last one
        for lo in range(0, N, 2*size):
            mid = min(lo + size - 1, N-1)
            hi  = min(lo + 2*size - 1, N-1)
            merge(A, lo, mid, hi, aux)

        size = 2 * size

def timing_nlogn_sorting():
    """
    Confirm N Log N performance of Merge Sort, Heap Sort and Python's built-in sort.
    """
    # Build model
    tbl = DataTable([12,10,10,10,10],['N','MergeSort', 'QuickSort', 'TimSort', 'PythonSort'])

    for n in [2**k for k in range(8, 18)]:
        t_ms = min(timeit.repeat(stmt='merge_sort(A)', setup='''
import random
from ch05.merge import merge_sort
A=list(range(int({0}*.8)))
B=list(range({0}-len(A)))
random.shuffle(B)
A.extend(B)'''.format(n), repeat=10, number=1))

        t_qs = min(timeit.repeat(stmt='quick_sort(A)', setup='''
import random
from ch05.sorting import quick_sort
A=list(range(int({0}*.8)))
B=list(range({0}-len(A)))
random.shuffle(B)
A.extend(B)'''.format(n), repeat=10, number=1))

        t_ps = min(timeit.repeat(stmt='A.sort()', setup='''
import random
A=list(range(int({0}*.8)))
B=list(range({0}-len(A)))
random.shuffle(B)
A.extend(B)'''.format(n), repeat=10, number=1))

        t_ts = min(timeit.repeat(stmt='tim_sort(A)', setup='''
import random
from ch05.timsort import tim_sort
A=list(range(int({0}*.8)))
B=list(range({0}-len(A)))
random.shuffle(B)
A.extend(B)'''.format(n), repeat=10, number=1))

        tbl.row([n, t_ms, t_qs, t_ts, t_ps])

#######################################################################
if __name__ == '__main__':
    timing_nlogn_sorting()

    from random import shuffle
    from algs.sorting import is_sorted
    arr=list(range(22))
    shuffle(arr)
    tim_sort(arr)
    print(arr[:100])
    is_sorted(arr)
