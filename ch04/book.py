"""Tables and Figures for Chapter 4

"""
import timeit

from algs.table import DataTable, TableNum, process

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_trials(clazz, N, factor):
    """Run a single trial."""
    stmt = f'''
from {clazz} import PQ 
one_run(PQ({N}), {N}, {factor})'''
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def average_performance():
    """Generate table of average performance for different PQ implementations."""
    T = 3
    base = 256
    cutoff = 16384
    high = 65536

    heap = {}
    order_ar = {}
    order_ll = {}
    N = base
    while N <= high:
        order_ll[N] = 1000000*run_trials('ch04.ordered_list', N, T)/(T*N)
        heap[N]     = 1000000*run_trials('ch04.heap', N, T)/(T*N)
        N *= 2

    N = base
    array = {}
    linked = {}
    builtin = {}
    while N <= cutoff:
        print(N,'...')
        order_ar[N]  = 1000000*run_trials('ch04.ordered', N, T)/(T*N)
        linked[N]    = 1000000*run_trials('ch04.linked', N, T)/(T*N)
        array[N]     = 1000000*run_trials('ch04.array', N, T)/(T*N)
        builtin[N]   = 1000000*run_trials('ch04.builtin', N, T)/(T*N)

        N *= 2

    N = base
    tbl = DataTable([8,8,8,8,8,8,8],
                    ['N','Heap','OrderL','Linked','OrderA','Built-in','Array'],
                    decimals=2)
    while N <= high:
        if N <= cutoff:
            tbl.row([N, heap[N], order_ll[N], linked[N], order_ar[N], builtin[N], array[N]])
        else:
            #tbl.set_output(False)
            tbl.row([N, heap[N], order_ll[N]])
        N *= 2
    print()

    print ('Heap', tbl.best_model('Heap'))
    print ('OrderL', tbl.best_model('OrderL'))
    print ('Linked', tbl.best_model('Linked'))
    print ('OrderA', tbl.best_model('OrderA'))
    print ('Built-in', tbl.best_model('Built-in'))
    print ('Array', tbl.best_model('Array'))
    return tbl

def generate_ch04():
    """Generate tables/figures for chapter 04."""
    chapter = 4

    with TableNum(1) as table_number:
        process(average_performance(),
                chapter, table_number,
                'Average operation performance (time in ns) on problem instances of size N',
                yaxis='Time (in nanoseconds)')
