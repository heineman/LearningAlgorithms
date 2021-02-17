"""Tables and Figures for Chapter 5


If you have some time to review Factorial implementations, consider the internal
Python implementation

   https://github.com/python/cpython/blob/master/Modules/mathmodule.c

Or the binary-split formula for N!

   http://www.luschny.de/math/factorial/binarysplitfact.html

"""
import timeit
import random
import numpy as np
from scipy.optimize import curve_fit

from algs.table import caption, TABLE, DataTable
from algs.table import n_log_n_model, log_linear_model, linear_model, quadratic_model
labels_chapter5 = {}

def fact(n):
    """Inefficient recursive implementation to introduce recursion."""
    if n <= 1:
        return 1

    return n * fact(n-1)

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

def modeling_insertion_selection():
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

    [quadratic_comp_ss, _] = curve_fit(quadratic_model, np.array(x), np.array(y_comp_ss))
    [linear_swap_ss, _] = curve_fit(linear_model, np.array(x), np.array(y_swap_ss))

    [quadratic_comp_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_comp_is))
    [quadratic_swap_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_swap_is))

    print('Swap SS Linear    = {:f}*N + {:f}'.format(linear_swap_ss[0], linear_swap_ss[1]))
    print('Comp SS Quadratic = {}*N*N + {}*N'.format(quadratic_comp_ss[0], quadratic_comp_ss[1]))

    print('Swap IS Quadratic = {}*N*N + {}*N'.format(quadratic_swap_is[0], quadratic_swap_is[1]))
    print('Comp IS Quadratic = {}*N*N + {}*N'.format(quadratic_comp_is[0], quadratic_comp_is[1]))
    print()

    tbl = DataTable([12,10,10,10,10,10,10,10,10],
            ['N','AvgCompSS','MCSS', 'AvgSwapSS', 'MSSS', 'AvgCompIS', 'MCIS', 'AvgSwapIS', 'MSIS'],
            output=True, decimals=1)

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

def modeling_merge_heap():
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

    [log_comp_ms, _] = curve_fit(log_linear_model, np.array(x), np.array(y_comp_ms))
    [log_swap_ms, _] = curve_fit(log_linear_model, np.array(x), np.array(y_swap_ms))

    [log_comp_hs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_comp_hs))
    [log_swap_hs, _] = curve_fit(log_linear_model, np.array(x), np.array(y_swap_hs))

    print('Comp MS N*Log N = {}*N*Log(N) + {}*N'.format(log_comp_ms[0], log_comp_ms[1]))
    print('Swap MS N*Log N = {}*N*Log(N) + {}*N'.format(log_swap_ms[0], log_swap_ms[1]))

    print('Comp HS N*Log N = {}*N*Log(N) + {}*N'.format(log_comp_hs[0], log_comp_hs[1]))
    print('Swap HS N*Log N = {}*N*Log(N) + {}*N'.format(log_swap_hs[0], log_swap_hs[1]))
    print()

    tbl = DataTable([12,10,10,10,10,10,10,10,10],
            ['N','AvgCompMS','MCMS', 'AvgSwapMS', 'MSSS', 'AvgCompHS', 'MCHS', 'AvgSwapHS', 'MSHS'],
            output=True, decimals=1)

    for n in [2**k for k in range(4, 15)]:
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

def prototype_table():
    """Generate Table for Insertion Sort."""
    # Evaluate prototype execution
    x = []
    y = []
    for n in [2**k for k in range(8, 12)]:
        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(A)', setup=f'''
import random
from ch05.sorting import insertion_sort_bas
A=list(range({n}))
random.shuffle(A)''', repeat=10, number=10))
        x.append(n)
        y.append(m_insert_bas)

    # Coefficients are returned as first argument
    [log_coeffs, _] = curve_fit(n_log_n_model, np.array(x), np.array(y))
    [quadratic_coeffs, _] = curve_fit(quadratic_model, np.array(x), np.array(y))

    print('Quadratic = {}*N*N + {}*N'.format(quadratic_coeffs[0], quadratic_coeffs[1]))
    print('Log       = {:.12f}*N*log2(N)'.format(log_coeffs[0]))
    print()

    tbl = DataTable([12,10,10,10],['N','Time','Quad','Log'], output=True)
    for n,p in zip(x,y):
        tbl.row([n, p, quadratic_model(n,
                quadratic_coeffs[0], quadratic_coeffs[1]), n_log_n_model(n, log_coeffs[0])])

    for n in [2**k for k in range(12, 18)]:
        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(A)', setup=f'''
import random
from ch05.sorting import insertion_sort_bas
A=list(range({n}))
random.shuffle(A)''', repeat=10, number=10))
        tbl.row([n, m_insert_bas,
            quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
            n_log_n_model(n, log_coeffs[0])])

def timing_selection_insertion():
    """
    Because Insertion Sort is so sensitive to its inputs, we take average time
    over all of its runs.
    """
    print('Building models for Insertion Sort. This may take awhile...')
    # Build model from Generate 5 data points
    x = []
    y_is = []
    y_ss = []
    for n in [2**k for k in range(8, 13)]:
        # Not much need to repeat since Selection Sort behaves the same
        # every time. I'll do it five times.
        t_ss = min(timeit.repeat(stmt='selection_sort(A)', setup=f'''
import random
from ch05.sorting import selection_sort
A=list(range({n}))
random.shuffle(A)''', repeat=5, number=10))/10

        # Insertion Sort is highly dependent upon its input, so execute
        # far more repetitions, and take average. This is the only time
        # in the book where I alter my approach for measuring performance
        # since it could happen that a given data set has long runs of
        # ascending data, which would significantly reduce the execution
        # time. Instead, I total all 100 runs and provide an average.
        t_is = sum(timeit.repeat(stmt='insertion_sort(A)', setup=f'''
import random
from ch05.sorting import insertion_sort
A=list(range({n}))
random.shuffle(A)''', repeat=100, number=10))/(10*100)

        x.append(n)
        y_ss.append(t_ss)
        y_is.append(t_is)

    # Coefficients are returned as first argument
    [quadratric_ss, _] = curve_fit(quadratic_model, np.array(x), np.array(y_ss))
    [quadratric_is, _] = curve_fit(quadratic_model, np.array(x), np.array(y_is))

    print('Quadratic SS = {}*N*N + {}*N'.format(quadratric_ss[0], quadratric_ss[1]))
    print('Quadratic IS = {}*N*N + {}*N'.format(quadratric_is[0], quadratric_is[1]))
    print()

    tbl = DataTable([12,10,10,10,10],['N','TimeSS','ModelSS','TimeIS', 'ModelIS'])
    for n,t_ss,t_is in zip(x,y_ss,y_is):
        tbl.row([n, t_ss, quadratic_model(n, quadratric_ss[0], quadratric_ss[1]),
                    t_is, quadratic_model(n, quadratric_is[0], quadratric_is[1])])

    for n in [2**k for k in range(13, 16)]:
        t_ss = min(timeit.repeat(stmt='selection_sort(A)', setup=f'''
import random
from ch05.sorting import selection_sort
A=list(range({n}))
random.shuffle(A)''', repeat=50, number=10))/10

        # Once again, take average for Insertion Sort, this time
        # for 50 runs.
        t_is = sum(timeit.repeat(stmt='insertion_sort(A)', setup=f'''
import random
from ch05.sorting import insertion_sort
A=list(range({n}))
random.shuffle(A)''', repeat=50, number=10))/(10*50)

        tbl.row([n, t_ss, quadratic_model(n, quadratric_ss[0], quadratric_ss[1]),
                    t_is, quadratic_model(n, quadratric_is[0], quadratric_is[1])])

def generate_ch05():
    """Generate tables/figures for chapter 5."""
    chapter = 5
    
    timing_selection_insertion()

    print(caption(chapter, labels_chapter5, TABLE,
        'Modeling Insertion Sort and Selection Sort'))
    modeling_insertion_selection()

    print(fact(7))

    modeling_insertion_worst_case()
    print(caption(chapter, labels_chapter5, TABLE,
                  'Comparing different mathematical models with actual performance'))
    prototype_table()

    print(caption(chapter, labels_chapter5, TABLE,
        'Modeling Insertion Sort and Selection Sort'))
    modeling_insertion_selection()
