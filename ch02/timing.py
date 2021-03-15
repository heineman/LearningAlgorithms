"""
Generate timing results for inefficient sorting algorithms.

    :Sample Output:

    Permutation Sort Trials (up to N=12): These can take Unusually Long.
    Factorial    = 3.7490738642164824e-07*N!
           N    TimeToSort       Model    
           1      0.0000      0.0000    
           2      0.0000      0.0000    
           3      0.0000      0.0000    
           4      0.0000      0.0000    
           5      0.0000      0.0000    
           6      0.0003      0.0003    
           7      0.0018      0.0019    
           8      0.0149      0.0151    
           9      0.1350      0.1360    
          10      1.3777      1.3605    
          11     15.7066     14.9651    
          12    194.1625    179.5812    

    Random Sort Trials (up to N=11): These can take Unusually Long.
    Factorial    = 5.975750448109412e-07*N!
           N    TimeToSort       Model    
           1      0.0000      0.0000    
           2      0.0000      0.0000    
           3      0.0000      0.0000    
           4      0.0000      0.0000    
           5      0.0000      0.0001    
           6      0.0012      0.0004    
           7      0.0011      0.0030    
           8      0.1574      0.0241    
           9      0.1935      0.2168    
          10     21.2817      2.1685    
          11    137.0447     23.8533    
"""

import timeit
from algs.table import DataTable
from algs.modeling import numpy_error, factorial_model

def run_permutation_sort_worst_case(top):
    """Generate table for permutation sort from 1 up to and including top."""
    
    # Build model for runs of size 1 through 9.
    x = []
    y = []
    for n in range(1,10):
        sort_time = timeit.timeit(stmt='permutation_sort(x)', setup='''
from ch02.random_sort import permutation_sort
x=list(range({},0,-1))'''.format(n), number=1)
        x.append(n)
        y.append(sort_time)

def run_random_sort(top):
    """Generate table for random sort."""
    
    # Build model for runs of size 1 through 9.
    x = []
    y = []
    for n in range(1,10):
        sort_time = timeit.timeit(stmt='random_sort(x)', setup='''
import random
from ch02.random_sort import random_sort
x=list(range({}))
random.shuffle(x)'''.format(n), number=1)
        x.append(n)
        y.append(sort_time)

    # Coefficients are returned as first argument
    if numpy_error:
        factorial_coeffs = [0]
    else:
        import numpy as np
        from scipy.optimize import curve_fit

        [factorial_coeffs, _] = curve_fit(factorial_model, np.array(x), np.array(y))
    print('Factorial    = {}*N!'.format(factorial_coeffs[0]))

    tbl = DataTable([8,8,8], ['N', 'TimeToSort', 'Model'], decimals=4)

    for n in range(1,top+1):
        sort_time = timeit.timeit(stmt='random_sort(x)', setup='''
import random
from ch02.random_sort import random_sort
x=list(range({}))
random.shuffle(x)'''.format(n), number=1)
        tbl.row([n, sort_time, factorial_model(n, factorial_coeffs[0])])

#######################################################################
if __name__ == '__main__':
    print('Permutation Sort Trials (up to N=12): These can take Unusually Long.')
    run_permutation_sort_worst_case(12)

    print('Random Sort Trials (up to N=11): These can take Unusually Long.')
    run_random_sort(11)