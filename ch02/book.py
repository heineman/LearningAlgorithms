"""Tables for Chapter 2.

This script requires that `numpy` and `scipy` be installed within the
Python environment you are running this script in.

"""

import timeit
import math

from algs.table import DataTable, TableNum, FigureNum, captionx, process, SKIP
from algs.modeling import n_log_n_model, quadratic_model, linear_model, numpy_error

def actual_table(output=True):
    """Produce sample table to use for curve fitting."""
    # Sample data
    xvals = [100, 1000, 10000]
    yvals = [0.063, 0.565, 5.946]

    # Coefficients are returned as first argument
    if numpy_error:
        a,b = 0,0
    else:
        [(a,b), _] = curve_fit(linear_model, np.array(xvals), np.array(yvals))
        if output:
            print('Linear = {}*N + {}'.format(a, b))

    tbl = DataTable([8,8,8], ['N', 'Actual', 'Model'], output=output)

    tbl.row([100, 0.063, linear_model(100,a,b)])
    tbl.row([1000, 0.565, linear_model(1000,a,b)])
    tbl.row([10000, 5.946, linear_model(10000,a,b)])

    print (tbl.pearsonr('Actual', 'Model'))
    return tbl

def prototype_table(output=True, decimals=3):
    """
    Generate table of results for prototype application.

    The prototype application is simply a request to sort the N values.
    """
    trials = [100, 1000, 10000]
    nvals = []
    yvals = []
    for n in trials:
        sort_time = 1000*min(timeit.repeat(stmt='x.sort()', setup='''
import random
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=100, number=100))
        nvals.append(n)
        yvals.append(sort_time)

    def quad_model(n, a, b):
        if a < 0:     # attempt to PREVENT negative coefficient.
            return 1e10
        return a*n*n + b*n
    # Coefficients are returned as first argument
    if numpy_error:
        nlog_n_coeffs = linear_coeffs = quadratic_coeffs = [0,0]
    else:
        [nlog_n_coeffs, _] = curve_fit(n_log_n_model, np.array(nvals), np.array(yvals))
        [linear_coeffs, _] = curve_fit(linear_model, np.array(nvals), np.array(yvals))
        [quadratic_coeffs, _] = curve_fit(quad_model, np.array(nvals), np.array(yvals))

    if output:
        print('Linear    = {:f}*N + {:f}'.format(linear_coeffs[0], linear_coeffs[1]))
        print('Quadratic = {}*N*N + {}*N'.format(quadratic_coeffs[0], quadratic_coeffs[1]))
        print('N Log N   = {:.12f}*N*log2(N)'.format(nlog_n_coeffs[0]))
        print()

    tbl = DataTable([12,10,10,10,10],['N','Time','Linear','Quad','NLogN'], output=output, decimals=decimals)

    for n,p in zip(nvals,yvals):
        tbl.row([n, p,
            linear_model(n, linear_coeffs[0], linear_coeffs[1]),
            quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
            n_log_n_model(n, nlog_n_coeffs[0])])

    for n in [100000, 1000000, 10000000]:
        sort_time = 1000*min(timeit.repeat(stmt='x.sort()', setup='''
import random
x=list(range({}))
random.shuffle(x)'''.format(n), repeat=100, number=100))
        tbl.row([n, sort_time,
            linear_model(n, linear_coeffs[0], linear_coeffs[1]),
            quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
            n_log_n_model(n, nlog_n_coeffs[0])])

    if output:
        print ('Linear', tbl.pearsonr('Time', 'Linear'))
        print ('Quad', tbl.pearsonr('Time', 'Quad'))
        print ('NLogN', tbl.pearsonr('Time', 'NLogN'))
        print (tbl.best_model('Time'))
    return tbl

def incremental_multiplication():
    """
    Compute results for multiplying large numbers.
    This takes several hours to run, and is not executed by default.
    """
    num = 1000
    for n in range(10, 2048):
        all_times = timeit.repeat(stmt='idx += 1\nmult_pair(pairs[idx])', setup='''
from ch02.mult import create_random_pair, mult_pair
idx = -1 
pairs = [create_random_pair({}) for _ in range({})]'''.format(n,num), repeat=20, number=num)

        print(n,min(all_times), max(all_times))

def large_multiplication():
    """Compute results for multiplying large numbers."""
    num = 1000
    x = []
    y = []
    log2_3 = math.log2(3)
    for n in [2**k for k in range(8,13)]:
        mult_time = timeit.timeit(stmt='mult_pair(x)', setup='''
from ch02.mult import create_pair, mult_pair 
x=create_pair({})'''.format(n), number=num)
        x.append(n)
        y.append(mult_time)

    def karatsuba(n, a):
        """Models a*N^k where k = log 3 in base 2."""
        return a * (n ** log2_3)

    def tkn(n, a, b):
        """Models a*N^k +b*n where k = log 3 in base 2."""
        return a * (n ** log2_3) + b*n

    # Coefficients are returned as first argument
    if numpy_error:
        pass
        linear_coeffs = quadratic_coeffs = karatsuba_coeffs = tkn_coeffs = [0,0]
    else:
        [linear_coeffs, _] = curve_fit(linear_model, np.array(x), np.array(y))
        [quadratic_coeffs, _] = curve_fit(quadratic_model, np.array(x), np.array(y))
        [karatsuba_coeffs, _] = curve_fit(karatsuba, np.array(x), np.array(y))
        [tkn_coeffs, _] = curve_fit(tkn, np.array(x), np.array(y))

    print('Karatsuba={}*N^1.585'.format(karatsuba_coeffs[0]))
    print('TK={}*N^1.585+{}*N'.format(tkn_coeffs[0], tkn_coeffs[1]))
    print()

    tbl = DataTable([8,12,12,12,12,12],['N', 'Time', 'Linear', 'Quad', 'Karatsuba', 'TKN'],
                    decimals=4)

    for n,mult_time in zip(x,y):
        tbl.row([n, mult_time,
              linear_model(n, linear_coeffs[0], linear_coeffs[1]),
              quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
              karatsuba(n, karatsuba_coeffs[0]),
              tkn(n, tkn_coeffs[0], tkn_coeffs[1])])

    for n in [2**k for k in range(13,20)]:
        mult_time = timeit.timeit(stmt='mult_pair(x)', setup='''
from ch02.mult import create_pair, mult_pair 
x=create_pair({})'''.format(n), number=num)

        tbl.row([n, mult_time,
              linear_model(n, linear_coeffs[0], linear_coeffs[1]),
              quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]),
              karatsuba(n, karatsuba_coeffs[0]),
              tkn(n, tkn_coeffs[0], tkn_coeffs[1])])

    return tbl

def algorithms_a_b():
    """Generate table for estimates of time for three computers and two algorithms."""
    
    def alg_a(n):
        """Number of operations for algorithm A."""
        return 5*n

    def alg_b(n):
        """Number of operations for algorithm B."""
        return 2020*math.log(n)/math.log(2)

    tbl = DataTable([15,15,8,8,8,8,8], ['N', 'A', 'B', 'A_slow', 'A_fast', 'B_fast', 'A_fastest'], decimals=1)
    tbl.format('A', ',d')
    tbl.format('B', ',d')
    for n in [2**k for k in range(2, 24)]:
        tbl.row([n, alg_a(n), int(alg_b(n)), alg_a(n)/1500, alg_a(n)/3000, alg_b(n)/1500, alg_a(n)/(250*3000)])
    return tbl

def growth_table():
    """Generate table for growth of different computations."""
    labels = ['N', 'log N', 'Linear', 'N log N', 'N^2', 'N^3', '2^N', 'N!']
    tbl = DataTable([15,15,15,15,15,15,15,15], labels)
    for hdr in labels:
        tbl.format(hdr, ',d')
    
    def fact(n):
        try:
            return int(factorial(n))
        except (Exception):
            return float('inf')
    
    def exp(n):
        pass
    
    for n in [2**k for k in range(2, 12)]:
        fact_value = fact(n)
        if fact_value == float('inf'):
            fact_value = SKIP
        elif fact_value > 1e100:
            fact_value = SKIP
        elif fact_value > 1e8:
            tbl.format('N!', '.2e')
            
        exp_value = pow(2, n)
        if exp_value > 1e8:
            tbl.format('2^N', '.2e')
        if exp_value > 1e100:
            exp_value = SKIP
            
        cubic_value = n*n*n
        if cubic_value > 1e8:
            tbl.format('N^3', '.2e')
                       
        tbl.row([n, int(math.log(n)/math.log(2)), n, int(n*math.log(n)/math.log(2)), n*n, cubic_value, exp_value, fact_value])
    return tbl

def generate_ch02():
    """Generate tables/figures for chapter 02."""
    chapter = 2
    
    with TableNum(1) as table_number:
        process(actual_table(),
                chapter, table_number, 
                'Prototype run-time performance')

#    with TableNum(2) as table_number:
#        process(prototype_table(),
#                chapter, table_number, 
#                'Comparing different mathematical models with actual performance')
        
#    with TableNum(3) as table_number:
#        process(large_multiplication(),
#                chapter, table_number, 
#                'Multiplying two n-digit integers')

    with FigureNum(1) as figure_number:
        print (captionx(chapter, figure_number),
               'Compare models against performance')
        
    with FigureNum(2) as figure_number:
        algorithms_a_b()
        print (captionx(chapter, figure_number),
               'Complexity classes provide context to understand performance')

    with FigureNum(3) as figure_number:
        print (captionx(chapter, figure_number),
               'Visualizing the numbers from Figure 2-2')
        
    with TableNum(4) as table_number:
        process(growth_table(),
                chapter, table_number, 
                'Growth of different computations')
        
    with FigureNum(8) as figure_number:
        print (captionx(chapter, figure_number),
               'Plot runtime performance against problem instance size for complexity classes')

#######################################################################
if __name__ == '__main__':
    generate_ch02()
