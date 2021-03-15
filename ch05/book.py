"""Tables and Figures for Chapter 5


If you have some time to review Factorial implementations, consider the internal
Python implementation

   https://github.com/python/cpython/blob/master/Modules/mathmodule.c

Or the binary-split formula for N!

   http://www.luschny.de/math/factorial/binarysplitfact.html

Lengthy runs (several hours) for timing results in:

Building models for Insertion Sort. This may take awhile...
Quadratic SS = 4.586897358514126e-09*N*N + 1.406849880773368e-07*N
Quadratic IS = 4.504032979491163e-09*N*N + 1.8245472574666622e-07*N

           N        TimeSS       ModelSS        TimeIS       ModelIS
         256         0.000         0.000         0.000         0.000
         512         0.001         0.001         0.001         0.001
       1,024         0.005         0.005         0.005         0.005
       2,048         0.020         0.020         0.019         0.019
       4,096         0.078         0.078         0.076         0.076
       8,192         0.307         0.309         0.304         0.304
      16,384         1.238         1.234         1.221         1.212
      32,768         4.881         4.930         4.754         4.842
      65,536        19.585        19.710        19.716        19.357

"""
import timeit
import random
from algs.table import captionx, FigureNum

from algs.table import DataTable
from algs.modeling import n_log_n_model, log_linear_model, linear_model, quadratic_model
from algs.modeling import numpy_error

def fact(N):
    """Inefficient recursive implementation to introduce recursion."""
    if N <= 1:
        return 1

    return N * fact(N-1)

def modeling_insertion_worst_case():
    """Generate table for worst case of Insertion Sort."""
    from ch05.sorting import insertion_sort_counting

    tbl = DataTable([8,12,12],['N', 'Swaps', 'Comparisons'])
    tbl.format('Swaps', ',d')
    tbl.format('Comparisons', ',d')

    for n in [2**k for k in range(4, 8)]:
        A=list(range(n))
        A.reverse()
        (num_swaps, num_compares) = insertion_sort_counting(A)

        tbl.row([n, num_swaps, num_compares])

def modeling_insertion_selection(output=True, decimals=1):
    """Generate table for Insertion Sort."""
    from ch05.sorting import selection_sort_counting, insertion_sort_counting
    trials = 100

    x = []
    y_comp_ss = []
    y_swap_ss = []
    y_comp_is = []
    y_swap_is = []
    for n in [2**k for k in range(4, 8)]:
        total_compares_ss = 0
        total_swaps_ss = 0
        total_compares_is = 0
        total_swaps_is = 0
        for _ in range(trials):
            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = selection_sort_counting(A)
            total_swaps_ss += num_swaps
            total_compares_ss += num_compares

            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = insertion_sort_counting(A)
            total_swaps_is += num_swaps
            total_compares_is += num_compares

        x.append(n)
        y_comp_ss.append(total_compares_ss/trials)
        y_swap_ss.append(total_swaps_ss/trials)
        y_comp_is.append(total_compares_is/trials)
        y_swap_is.append(total_swaps_is/trials)

    if numpy_error:
        quadratic_comp_ss = linear_swap_ss = quadratic_comp_is = quadratic_swap_is = [0,0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [quadratic_comp_ss, _] = curve_fit(quadratic_model, np.array(x), np.array(y_comp_ss))
        [linear_swap_ss, _] = curve_fit(linear_model, np.array(x), np.array(y_swap_ss))
        [quadratic_comp_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_comp_is))
        [quadratic_swap_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_swap_is))

    if output:
        print('Swap SS Linear    = {:f}*N + {:f}'.format(linear_swap_ss[0], linear_swap_ss[1]))
        print('Comp SS Quadratic = {}*N*N + {}*N'.format(quadratic_comp_ss[0], quadratic_comp_ss[1]))
    
        print('Swap IS Quadratic = {}*N*N + {}*N'.format(quadratic_swap_is[0], quadratic_swap_is[1]))
        print('Comp IS Quadratic = {}*N*N + {}*N'.format(quadratic_comp_is[0], quadratic_comp_is[1]))
        print()

    tbl = DataTable([12,10,10,10,10,10,10,10,10],
            ['N','AvgCompSS','MCSS', 'AvgSwapSS', 'MSSS', 'AvgCompIS', 'MCIS', 'AvgSwapIS', 'MSIS'],
            output=output, decimals=decimals)

    for n in [2**k for k in range(4, 10)]:
        total_compares_ss = 0
        total_swaps_ss = 0
        total_compares_is = 0
        total_swaps_is = 0

        for _ in range(trials):
            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = selection_sort_counting(A)
            total_swaps_ss += num_swaps
            total_compares_ss += num_compares

            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = insertion_sort_counting(A)
            total_swaps_is += num_swaps
            total_compares_is += num_compares

        tbl.row([n,
                  total_compares_ss/trials,
                  quadratic_model(n, quadratic_comp_ss[0], quadratic_comp_ss[1]),
                  total_swaps_ss/trials,
                  linear_model(n, linear_swap_ss[0],  linear_swap_ss[1]),

                  total_compares_is/trials,
                  quadratic_model(n, quadratic_comp_is[0], quadratic_comp_is[1]),
                  total_swaps_is/trials,
                  quadratic_model(n, quadratic_swap_is[0], quadratic_swap_is[1]),
                  ])
    return tbl

def modeling_merge_heap(max_k=5, output=True, decimals=1):
    """Generate table for Merge Sort vs. Heap Sort."""
    from ch05.merge import merge_sort_counting
    from ch05.heapsort import HeapSortCounting

    trials = 500

    x = []
    y_comp_ms = []
    y_swap_ms = []
    y_comp_hs = []
    y_swap_hs = []
    for n in [2**k for k in range(4, 8)]:
        total_compares_ms = 0
        total_swaps_ms = 0
        total_compares_hs = 0
        total_swaps_hs = 0
        for _ in range(trials):
            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = merge_sort_counting(A)
            total_swaps_ms += num_swaps
            total_compares_ms += num_compares

            A=list(range(n))
            random.shuffle(A)
            hsc = HeapSortCounting(A)
            hsc.sort()
            total_swaps_hs += hsc.num_swaps
            total_compares_hs += hsc.num_comparisons

        x.append(n)
        y_comp_ms.append(total_compares_ms/trials)
        y_swap_ms.append(total_swaps_ms/trials)
        y_comp_hs.append(total_compares_hs/trials)
        y_swap_hs.append(total_swaps_hs/trials)

    if numpy_error:
        log_comp_ms = log_swap_ms = log_comp_hs = log_swap_hs = [0, 0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [log_comp_ms, _] = curve_fit(log_linear_model, np.array(x), np.array(y_comp_ms))
        [log_swap_ms, _] = curve_fit(log_linear_model, np.array(x), np.array(y_swap_ms))
        [log_comp_hs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_comp_hs))
        [log_swap_hs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_swap_hs))

    if output:
        print('Comp MS N*Log N = {}*N*Log(N) + {}*N'.format(log_comp_ms[0], log_comp_ms[1]))
        print('Swap MS N*Log N = {}*N*Log(N) + {}*N'.format(log_swap_ms[0], log_swap_ms[1]))

        print('Comp HS N*Log N = {}*N*Log(N) + {}*N'.format(log_comp_hs[0], log_comp_hs[1]))
        print('Swap HS N*Log N = {}*N*Log(N) + {}*N'.format(log_swap_hs[0], log_swap_hs[1]))
        print()

    tbl = DataTable([12,10,10,10,10,10,10,10,10],
            ['N','AvgCompMS','MCMS', 'AvgSwapMS', 'MSSS', 'AvgCompHS', 'MCHS', 'AvgSwapHS', 'MSHS'],
            output=output, decimals=decimals)

    for n in [2**k for k in range(4, max_k)]:
        total_compares_ms = 0
        total_swaps_ms = 0
        total_compares_hs = 0
        total_swaps_hs = 0

        for _ in range(trials):
            A=list(range(n))
            random.shuffle(A)
            (num_swaps, num_compares) = merge_sort_counting(A)
            total_swaps_ms += num_swaps
            total_compares_ms += num_compares

            A=list(range(n))
            random.shuffle(A)
            hsc = HeapSortCounting(A)
            hsc.sort()
            total_swaps_hs += hsc.num_swaps
            total_compares_hs += hsc.num_comparisons

        tbl.row([n,
                  total_compares_ms/trials,
                  log_linear_model(n, log_comp_ms[0], log_comp_ms[1]),
                  total_swaps_ms/trials,
                  log_linear_model(n, log_swap_ms[0], log_swap_ms[1]),

                  total_compares_hs/trials,
                  log_linear_model(n, log_comp_hs[0], log_comp_hs[1]),
                  total_swaps_hs/trials,
                  log_linear_model(n, log_swap_hs[0], log_swap_hs[1])
                  ])
    return tbl

def timing_selection_insertion(min_k=8, max_k=13, output=True, decimals=3):
    """
    Because Insertion Sort is so sensitive to its inputs, we take average time
    over all of its runs. Models first using 5 rows from [min_k .. min_k+5]
    and then presents information up to (but not including) max_k.
    """
    if output:
        print('Building models for Insertion Sort. This may take awhile...')
    # Build model from Generate 5 data points
    x = []
    y_is = []
    y_ss = []
    for n in [2**k for k in range(min_k, min_k+5)]:
        # Not much need to repeat since Selection Sort behaves the same
        # every time. I'll do it five times.
        t_ss = timeit.timeit(stmt='selection_sort(A)', setup='''
import random
from ch05.sorting import selection_sort
A=list(range({}))
random.shuffle(A)'''.format(n), number=1)

        # Insertion Sort is highly dependent upon its input, so execute
        # far more repetitions, and take average. This is the only time
        # in the book where I alter my approach for measuring performance
        # since it could happen that a given data set has long runs of
        # ascending data, which would significantly reduce the execution
        # time. Instead, I total all 100 runs and provide an average.
        t_is = sum(timeit.repeat(stmt='insertion_sort(A)', setup='''
import random
from ch05.sorting import insertion_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=100, number=1))/100   # since seeking average from sum

        x.append(n)
        y_ss.append(t_ss)
        y_is.append(t_is)

    # Coefficients are returned as first argument
    if numpy_error:
        quadratric_ss = quadratric_is = [0, 0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [quadratric_ss, _] = curve_fit(quadratic_model, np.array(x), np.array(y_ss))
        [quadratric_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_is))

    if output:
        print('Quadratic SS = {}*N*N + {}*N'.format(quadratric_ss[0], quadratric_ss[1]))
        print('Quadratic IS = {}*N*N + {}*N'.format(quadratric_is[0], quadratric_is[1]))
        print()

    tbl = DataTable([12,10,10,10,10,10,10],
                    ['N','TimeSS','ModelSS','MinIS', 'TimeIS', 'MaxIs', 'ModelIS'],
                    output=output, decimals=decimals)
    for n,t_ss,t_is in zip(x,y_ss,y_is):
        tbl.row([n, t_ss, quadratic_model(n, quadratric_ss[0], quadratric_ss[1]),
                    t_is, t_is, t_is, quadratic_model(n, quadratric_is[0], quadratric_is[1])])

    for n in [2**k for k in range(min_k+5, max_k)]:
        # selection is stable, so just run once
        t_ss = timeit.timeit(stmt='selection_sort(A)', setup='''
import random
from ch05.sorting import selection_sort
A=list(range({}))
random.shuffle(A)'''.format(n), number=1)

        # Once again, take average for Insertion Sort, this time
        # for 50 runs. But also compute min and max for graphing
        all_times = timeit.repeat(stmt='insertion_sort(A)', setup='''
import random
from ch05.sorting import insertion_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=5, number=1)
        t_is = sum(all_times)/5
        t_min = min(all_times)
        t_max = max(all_times)

        tbl.row([n, t_ss, quadratic_model(n, quadratric_ss[0], quadratric_ss[1]),
                    t_min, t_is, t_max, quadratic_model(n, quadratric_is[0], quadratric_is[1])])
    return tbl

def timing_nlogn_sorting(max_k=21, output=True, decimals=3):
    """
    Confirm N Log N performance of Merge Sort, Heap Sort, Quicksort and Python's built-in sort.
    """
    # Build model from Generate 5 data points
    tbl = DataTable([12,10,10,10,10,10],
                    ['N','MergeSort', 'QuickSort', 'HeapSort', 'TimSort', 'PythonSort'],
                    output=output, decimals=decimals)

    x = []
    y_ms = []
    y_qs = []
    y_hs = []
    y_ts = []
    y_ps = []
    for n in [2**k for k in range(8, 16)]:
        t_ms = min(timeit.repeat(stmt='merge_sort(A)', setup='''
import random
from ch05.merge import merge_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_qs = min(timeit.repeat(stmt='quick_sort(A)', setup='''
import random
from ch05.sorting import quick_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_hs = min(timeit.repeat(stmt='heap_sort(A)', setup='''
import random
from ch05.heapsort import heap_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_ts = min(timeit.repeat(stmt='tim_sort(A)', setup='''
import random
from ch05.timsort import tim_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_ps = min(timeit.repeat(stmt='A.sort()', setup='''
import random
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        x.append(n)
        y_ms.append(t_ms)
        y_qs.append(t_qs)
        y_hs.append(t_hs)
        y_ts.append(t_ts)
        y_ps.append(t_ps)

    # Coefficients are returned as first argument
    if numpy_error:
        nlogn_ms = nlogn_qs = nlogn_hs = nlogn_ts = nlogn_ps = [0, 0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        [nlogn_ms, _] = curve_fit(log_linear_model, np.array(x), np.array(y_ms))
        [nlogn_qs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_qs))
        [nlogn_hs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_hs))
        [nlogn_ts, _] = curve_fit(log_linear_model, np.array(x), np.array(y_ts))
        [nlogn_ps, _] = curve_fit(log_linear_model, np.array(x), np.array(y_ps))

    for n,t_ms,t_qs,t_hs,t_ts,t_ps in zip(x,y_ms,y_qs,y_hs,y_ts,y_ps):
        tbl.row([n, t_ms, t_qs, t_hs, t_ts, t_ps])

    for n in [2**k for k in range(16, max_k)]:
        # selection is stable, so just run once
        t_ms = min(timeit.repeat(stmt='merge_sort(A)', setup='''
import random
from ch05.merge import merge_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_qs = min(timeit.repeat(stmt='quick_sort(A)', setup='''
import random
from ch05.sorting import quick_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_hs = min(timeit.repeat(stmt='heap_sort(A)', setup='''
import random
from ch05.heapsort import heap_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_ts = min(timeit.repeat(stmt='tim_sort(A)', setup='''
import random
from ch05.timsort import tim_sort
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        t_ps = min(timeit.repeat(stmt='A.sort()', setup='''
import random
A=list(range({}))
random.shuffle(A)'''.format(n), repeat=10, number=1))

        tbl.row([n, t_ms, t_qs, t_hs, t_ts, t_ps])

    if output:
        print('NLOGN MS = {}*N*N + {}*N'.format(nlogn_ms[0], nlogn_ms[1]))
        print('NLOGN QS = {}*N*N + {}*N'.format(nlogn_qs[0], nlogn_qs[1]))
        print('NLOGN HS = {}*N*N + {}*N'.format(nlogn_hs[0], nlogn_hs[1]))
        print('NLOGN TS = {}*N*N + {}*N'.format(nlogn_ts[0], nlogn_ts[1]))
        print('NLOGN PS = {}*N*N + {}*N'.format(nlogn_ps[0], nlogn_ps[1]))
        print()
    return tbl

def show_partition():
    """Show how Quicksort partitions an array."""
    from ch01.challenge import partition
    A = [15, 21, 20, 2, 15, 24, 5, 19]
    print('|'.join([' {:>2} '.format(k) for k in A]))

    idx = partition(A, 0, len(A)-1, 0)
    print('|'.join([' {:>2} '.format(k) for k in A]))
    print('pivot=A[{}]={}'.format(idx, A[idx]))

def show_heapify():
    """Show how array is turned into a heap, step by step."""
    from ch05.heapsort import HeapSortCounting

    # After a few minutes of tweaking (based on partial results from the challenge
    # problem area), I found this input that produces the Heap. nice!
    A = [14, 13, 12, 5, 10, 6, 14, 12, 9, 1, 11, 8, 15, 9, 7, 4, 8, 2]
    heap = HeapSortCounting(A, output=True)

def tim_sort_figure():
    """Recreate data for timsort figure."""
    from ch05.timsort import insertion_sort, merge
    # Small arrays are sorted using insertion sort
    A=[14, 13, 12, 5, 10, 6, 14, 12, 9, 1, 11, 8, 15, 9, 7, 4, 8, 2]
    print('\t' +'|'.join([' {:>2} '.format(k) for k in A]))

    N = len(A)

    # Insertion sort in strips of 'size'
    size = 4
    for lo in range(0, N, size):
        print('lo={:2d}\t'.format(lo) + '|'.join([' {:>2} '.format(k) for k in A]))
        insertion_sort(A, lo, min(lo+size-1, N-1))

    aux = [None]*N
    while size < N:
        print('size={:2d}\t'.format(size) + '|'.join([' {:>2} '.format(k) for k in A]))

        # Merge all doubled ranges, taking care with last one
        for lo in range(0, N, 2*size):
            mid = min(lo + size - 1, N-1)
            hi  = min(lo + 2*size - 1, N-1)
            merge(A, lo, mid, hi, aux)

        size = 2 * size

    print('size={:2d}\t'.format(size) + '|'.join([' {:>2} '.format(k) for k in A]))

def generate_ch05():
    """Generate Tables and Figures for chapter 05."""
    chapter = 5

    with FigureNum(1) as figure_number:
        description  = 'Sample array, A, to sort'
        label = captionx(chapter, figure_number)
        A = [15, 21, 20, 2, 15, 24, 5, 19]
        print('|'.join([' {:>2} '.format(k) for k in A]))
        moves = [(0,3),(5,7),(1,6),None,(2,4),None,(4,5)]
        for m in moves:
            if m:
                A[m[0]],A[m[1]] = A[m[1]],A[m[0]]
            print('|'.join([' {:>2} '.format(k) for k in A]))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(2) as figure_number:
        description  = 'Sorting sample array using Selection Sort'
        label = captionx(chapter, figure_number)
        A = [15, 21, 20, 2, 15, 24, 5, 19]
        print('|'.join([' {:>2} '.format(k) for k in A]))
        moves = [(0,3),(1,6),(2,3),(3,4),(4,7),(5,7),(6,6)]
        for m in moves:
            if m:
                A[m[0]],A[m[1]] = A[m[1]],A[m[0]]
            print('|'.join([' {:>2} '.format(k) for k in A]))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(3) as figure_number:
        description  = 'Visualizing the formula for triangle numbers: sum of 1 through 7 is 28'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(4) as figure_number:
        description  = 'Sorting sample array using Insertion Sort'
        label = captionx(chapter, figure_number)
        A = [15, 21, 20, 2, 15, 24, 5, 19]
        print('|'.join([' {:>2} '.format(k) for k in A]))
        moves = [None,[(2,1)], [(3,2),(2,1),(1,0)], [(4,3),(3,2)],
                 None, [(6,5),(5,4),(4,3),(3,2),(2,1)],[(7,6),(6,5),(5,4)]]
        for p in moves:
            if p:
                for m in p:
                    A[m[0]],A[m[1]] = A[m[1]],A[m[0]]
            print('|'.join([' {:>2} '.format(k) for k in A]))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(5) as figure_number:
        description  = 'Visualizing the recursive invocation of fact(3)'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()
        
    with FigureNum(6) as figure_number:
        description  = 'Recursive invocation when calling rmax(0,3) on A=[15,21,20,2]'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(7) as figure_number:
        description  = 'Complete recursive invocation of rmax'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(8) as figure_number:
        description  = 'Merging two stacks into one'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(9) as figure_number:
        description  = 'Step by step merge sort of two sorted sub-arrays of size 4'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(10) as figure_number:
        show_partition()
        description  = 'Results of partition(A,0,7,0)'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    generate_ch05()
