"""
Timing Results for chapter 5.
"""
import timeit
from algs.table import DataTable

def table_trials(max_k=15, output=True, decimals=3):
    """Compare Merge Sort against built in Python sort up to, but not including 2**max_k."""
    tbl = DataTable([8,10,10], ['N', 'MergeSort', 'Built-In Sort'], output=output, decimals=decimals)

    for n in [2**k for k in range(8, max_k)]:
        msort = 1000*min(timeit.repeat(stmt='merge_sort(x)', setup='''
import random
from ch05.merge import merge_sort
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        builtin = 1000*min(timeit.repeat(stmt='x.sort()', setup='''
import random
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        tbl.row([n, msort, builtin])
    return tbl

def quadratic_sort_trials(max_k=12, output=True, decimals=2):
    """Compare Selection Sort against two flavors of Insertion Sort up to (but not including) 2^max_k."""
    tbl = DataTable([8,8,8,8], ['N', 'Select', 'Insert', 'InsertBAS'], output=output, decimals=decimals)

    for n in [2**k for k in range(8, max_k)]:
        if n > 2048:
            m_select = -1
        else:
            m_select = 1000*min(timeit.repeat(stmt='selection_sort(x)', setup='''
import random
from ch05.sorting import selection_sort
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        if n > 8192:
            m_insert = -1
        else:
            m_insert = 1000*min(timeit.repeat(stmt='insertion_sort(x)', setup='''
import random
from ch05.sorting import insertion_sort
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(x)', setup='''
import random
from ch05.sorting import insertion_sort_bas
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        tbl.row([n, m_select, m_insert, m_insert_bas])
    return tbl

#######################################################################
if __name__ == '__main__':
    print('Compare Merge Sort against built in Python sort. This takes unusually long.')
    table_trials()
    print()

    print('Compare Selection Sort against two flavors of Insertion Sort. This takes unusually long.')
    quadratic_sort_trials()
