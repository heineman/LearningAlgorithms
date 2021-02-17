"""Code for chapter 06."""
import timeit
from ch02.bas import binary_array_search
from algs.table import DataTable

def insert_value(A, val):
    """Return new list with val in its proper location."""
    idx = binary_array_search(A, val)
    if idx < 0:
        idx = -idx - 1

    new_A = [None] * (len(A) + 1)
    new_A[:idx] = A[:idx]
    new_A[idx] = val
    new_A[idx+1:] = A[idx:]
    return new_A

def remove_value(A, val):
    """Return new list with val removed if it existed."""
    idx = binary_array_search(A, val)
    if idx < 0:
        return A

    new_A = [None] * (len(A) - 1)
    new_A[:idx] = A[:idx]
    new_A[idx:] = A[idx+1:]
    return new_A

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_trials_pq_n(clazz, N, factor):
    """Run a single trial."""
    stmt = f'''
from {clazz} import PQ 
one_run(PQ({N}), {N}, {factor})'''
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def run_trials_pq(clazz, N, factor):
    """Run a single trial."""
    stmt = f'''
from {clazz} import PQ 
one_run(PQ(), {N}, {factor})'''
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def average_performance():
    """
    Generate table of average performance for different PQ implementations.

         N        Heap    BinaryTree
         128        2.38        5.15
         256        2.80        5.75
         512        3.22        6.63
       1,024        3.51        7.60
       2,048        3.89        8.42
       4,096        4.35        9.21
       8,192        4.75       10.24
      16,384        5.23       11.38
      32,768        5.96       12.90
    Heap [(<Model.LOG: 1>, 0.9946069479866522, 0.19032820110187337, 0.3676270723813611)]
    BinaryTree [(<Model.LOG: 1>, 0.9945273325485424, 0.48542129185563554, 0.7892486887139494)]

    While both offer O(Log N) performance, heap is more efficient (a little more than
    twice as efficient).

    """
    T = 3
    high = 32768

    tbl = DataTable([8,8,8], ['N','Heap','BinaryTree'], decimals=2)
    N = 128
    while N <= high:
        binary = 1000000*run_trials_pq('ch06.pq', N, T)/(T*N)
        heap   = 1000000*run_trials_pq_n('ch04.heap', N, T)/(T*N)
        tbl.row([N, heap, binary])
        N *= 2

    print ('Heap', tbl.best_model('Heap'))
    print ('BinaryTree', tbl.best_model('BinaryTree'))

def generate_ch06():
    """Generate tables/figures for chapter 06."""
    chapter = 6
    average_performance()
