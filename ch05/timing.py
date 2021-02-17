import timeit

def table_trials():
    """Compare Merge Sort against built in Python sort."""
    for n in [2**k for k in range(8, 20)]:
        msort = 1000*min(timeit.repeat(stmt='sort(x)', setup=f'''
import random
from ch05.merge import sort
x=list(range({n}))
random.shuffle(x)''', repeat=20, number=20))

        builtin = 1000*min(timeit.repeat(stmt='x.sort()', setup=f'''
import random
from ch05.merge import sort
x=list(range({n}))
random.shuffle(x)''', repeat=20, number=20))

        print('{}\t{}\t{}'.format(n, msort, builtin))

def quadratic_sort_trials():
    """Compare Selection Sort against two flavors of Insertion Sort."""
    print('{}\t{}\t{}\t{}'.format('N', 'Select', 'Insert', 'InsertBAS'))
    for n in [2**k for k in range(8, 16)]:
        if n > 2048:
            m_select = -1
        else:
            m_select = 1000*min(timeit.repeat(stmt='selection_sort(x)', setup=f'''
import random
from ch05.sorting import selection_sort
x=list(range({n}))
random.shuffle(x)''', repeat=20, number=20))

        if n > 8192:
            m_insert = -1
        else:
            m_insert = 1000*min(timeit.repeat(stmt='insertion_sort(x)', setup=f'''
import random
from ch05.sorting import insertion_sort
x=list(range({n}))
random.shuffle(x)''', repeat=20, number=20))

        m_insert_bas = 1000*min(timeit.repeat(stmt='insertion_sort_bas(x)', setup=f'''
import random
from ch05.sorting import insertion_sort_bas
x=list(range({n}))
random.shuffle(x)''', repeat=20, number=20))

        print('{}\t{:.1f}\t{:.1f}\t{:.1f}'.format(n, m_select, m_insert, m_insert_bas))

#######################################################################
if __name__ == '__main__':
    quadratic_sort_trials()
    table_trials()
