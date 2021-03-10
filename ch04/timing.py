"""
Timing Results for chapter 4
"""
import timeit
from algs.table import DataTable

def build_up(pq, N):
    """Populate pq with slate of integers."""
    delta = 993557  # large prime

    k = 0
    for _ in range(N):
        pq.enqueue(k, k)         # use key as the value (doesn't really matter)
        k = (k + delta) % N

def drain(pq, n):
    """invoke remove_max_priority() n times, or until empty. Pass in 0 to drain everything."""
    while pq:
        n -= 1
        pq.dequeue()
        if n == 0:
            return

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_trials(clazz, N, factor):
    stmt = '''
from {} import PQ 
one_run(PQ({}), {}, {})'''.format(clazz,N,N,factor)
    return min(timeit.repeat(stmt=stmt,
                setup='from ch04.timing import one_run', repeat=5, number=10))/10

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_dynamic_trials(clazz, N, factor):
    stmt = '''
from {} import PQ 
one_run(PQ(256), {}, {})'''.format(clazz,N,factor)
    return min(timeit.repeat(stmt=stmt, setup='from ch04.timing import one_run', repeat=5, number=10))/10

def one_run(pq, N, factor):
    """
    Conduct a run that exercised priority queue without causing a failure.
    Assume N divisible by 4 and factor > 2. Total of factor*N operations."""
    build_up(pq, N//2)       # Fill halfway
    drain(pq, N//4)          # Now go back to 1/4 full
    for _ in range(factor-2):
        build_up(pq, N//2)   # bring up to 3/4 full
        drain(pq, N//2)      # now back to 1/4 full

    build_up(pq, N//2)       # back to 3/4 full
    drain(pq, 0)             # empty out...

def trial_factorial_heap(max_n=2097152, output=True, decimals=2):
    """
    Generate trial using factorial heap compared with regular heap up to but not including max_n
    """
    factor = 3
    base = 256
    high = max_n

    tbl = DataTable([10,8,8], ['N', 'Heap', 'FactHeap'], output=output, decimals=decimals)
    N = base
    while N < high:
        heap  = 1000000*run_trials('ch04.heap', N, factor)/(factor*N)
        fheap = 1000000*run_trials('ch04.factorial_heap', N, factor)/(factor*N)
        tbl.row([N, heap, fheap])

        N *= 2
    return tbl

def dynamic_comparison():
    """Generate table for comparing resizable hashtable performance."""
    T = 3
    base = 256
    high = 65536*16
    tbl = DataTable([8,8,8],['N','Heap', 'DHeap'], output=True, decimals=2)

    heap = {}
    dheap = {}
    N = base
    while N <= high:
        heap[N]  = 1000000*run_trials('ch04.heap', N, T)/(T*N)
        dheap[N] = 1000000*run_dynamic_trials('ch04.dynamic_heap', N, T)/(T*N)
        tbl.row([N, heap[N], dheap[N]])

        N *= 2

# All timing costs are scaled by 1000 to convert from seconds into milliseconds.
# Results from runTrials divided by T*N because the number of statements executed
# is directly proportional to that, and we are trying to find the average
# operational cost (of both enqueue and dequeue
if __name__ == '__main__':
    dynamic_comparison()
    trial_factorial_heap()
