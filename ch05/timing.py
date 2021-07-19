"""
Timing Results for chapter 5.

Compare Merge Sort against built in Python sort. This takes unusually long.
       N     MergeSort    Built-In Sort
     256         0.371         0.002
     512         0.825         0.003
   1,024         1.839         0.007
   2,048         3.958         0.015
   4,096         8.455         0.032
   8,192        17.843         0.070
  16,384        37.647         0.153

Compare Selection Sort against two flavors of Insertion Sort. This takes unusually long.
       N      Select      Insert    InsertBAS
     256        1.28        0.20        0.23
     512        5.86        0.77        0.56
   1,024       23.66        3.10        1.33
   2,048       94.52       12.33        3.08

"""
import timeit
from algs.table import DataTable

def table_trials(max_k=15, output=True, decimals=3):
    """Compare Merge Sort against built in Python sort up to, but not including 2**max_k."""
    tbl = DataTable([8,10,10], ['N', 'MergeSort', 'Built-In Sort'],
                    output=output, decimals=decimals)

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
    """
    Compare two flavors of Selection Sort against two flavors of Insertion Sort
    up to (but not including) 2^max_k.
    """
    tbl = DataTable([8,8,8,8,8], ['N', 'Select', 'PythonSelect', 'Insert', 'InsertBAS'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(8, max_k)]:
        if n > 2048:
            m_select = -1
        else:
            m_select = 1000*min(timeit.repeat(stmt='selection_sort(x)', setup='''
import random
from ch05.sorting import selection_sort
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        if n > 2048:
            m_pselect = -1
        else:
            m_pselect = 1000*min(timeit.repeat(stmt='python_selection_sort(x)', setup='''
import random
from ch05.sorting import python_selection_sort
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        if n > 8192:
            m_insert = -1
        else:
            m_insert = 1000*min(timeit.repeat(stmt='insertion_sort(x)', setup='''
import random
from ch05.sorting import insertion_sort
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(x)', setup='''
import random
from ch05.sorting import insertion_sort_bas
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), repeat=20, number=15))/15

        tbl.row([n, m_select, m_pselect, m_insert, m_insert_bas])
    return tbl

#######################################################################
if __name__ == '__main__':
    print('Compare Selection Sort against two flavors of Insertion Sort; takes unusually long.')
    quadratic_sort_trials()

    print('Compare Merge Sort against built-in Python sort. This takes unusually long.')
    table_trials()
    print()
