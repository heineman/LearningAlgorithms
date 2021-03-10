"""Challenge questions for chapter 4

"""
import timeit
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from algs.table import DataTable, comma, best_models
from algs.modeling import n_log_n_model

def merged_arrays(heap1, heap2):
    """Return combined array with sorted values."""
    result = [None] * (heap1.N + heap2.N)
    idx = len(result)-1
    while idx >= 0:
        if heap1.is_empty():
            result[idx] = heap2.dequeue()
        elif heap2.is_empty():
            result[idx] = heap1.dequeue()
        else:
            if heap1.peek().priority > heap2.peek().priority:
                result[idx] = heap1.dequeue()
            else:
                result[idx] = heap2.dequeue()
        idx -= 1

    return result

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_merge_trial(m, n):
    """Generate data for Merge Sort results."""
    return min(timeit.repeat(stmt='merged_arrays(heap1, heap2)', setup = f'''
import random
from ch04.heap import PQ
from ch04.challenge import merged_arrays
heap1 = PQ({m})
heap2 = PQ({n})
random.seed({m})
for _ in range({m}):
    r1 = random.randint(0,16777216)
    heap1.enqueue(r1,r1)
random.seed({n})
for _ in range({n}):
    r2 = random.randint(0,16777216)
    heap2.enqueue(r2,r2)''', repeat=5, number=1))

def combined_sorted():
    """Generate results for different sorting trials."""
    lo = 8 # 16   #16
    hi = 12 # 21   # 23
    tbl = DataTable([8] * (hi-lo+1), ['N'] + [comma(2**k) for k in range(lo,hi)])

    for n in [2**k for k in range(lo,hi)]:
        row = [n]
        for m in [2**k for k in range(lo,hi)]:
            row.append(run_merge_trial(m,n))
        tbl.row(row)

    # Diagonal values are for 2*M*log(M) so divide in HALF for accurate one
    x = [2**k for k in range(lo,hi)]
    y = [tbl.entry(r,comma(r)) for r in [2**k for k in range(lo,hi)]]

    (coeffs,_) = curve_fit(n_log_n_model, np.array(x), np.array(y))
    a = coeffs[0] / 2

    y_fit = [n_log_n_model(r,a) for r in [2**k for k in range(lo,hi)]]

    print()
    print(pearsonr(y, y_fit))
    print()
    print('Prediction')
    model = DataTable([8] * (hi-lo+1), ['N'] + [comma(2**k) for k in range(lo,hi)])
    for n in [2**k for k in range(lo,hi)]:
        row = [n]
        for m in [2**k for k in range(lo,hi)]:
            row.append(n_log_n_model(n,a) + n_log_n_model(m,a))
        model.row(row)

    # Just do one column
    for m in best_models(x, tbl.column(comma(1024))):
        print (m)

def k_smallest(A, k):
    """Super-efficient (and easy to write) k_smallest selection for an arbitrary iterable."""
    from ch04.heap import PQ
    pq = PQ(k)

    # pq is a regular Max Binary Heap. Enqueue first k elements
    for v in A:
        if pq.N < k:
            pq.enqueue(v, v)
        else:
            if v < pq.peek().priority:
                # There is a chance to replace one of k-smallest values with this one
                pq.dequeue()
                pq.enqueue(v,v)

    result = []
    while pq:
        result.append(pq.dequeue())

    return list(reversed(result))

def iterator(pq):
    """
    Provides a Python-generator over a PQ, using a PQ to do it!
    
    Each entry in the pqit iterator has (value, priority) where value is
    an index position into the original pq, while its priority is the
    priority if the entry.
    
    You can add capability for fail-fast iterators IF the heap actively
    increments a count in its pq.storage[0] which is unused anyway.
    """
    from ch04.heap import PQ
    N = len(pq)
    
    # This works with INDEX positions into the heap
    pqit = PQ(N)
    pqit.enqueue(1, pq.peek().priority)
    while pqit:
        idx = pqit.dequeue()
        yield (pq.storage[idx].value, pq.storage[idx].priority)
        
        child = 2*idx
        if child < pq.N:
            pqit.enqueue(child, pq.storage[child].priority)
        child += 1
        if child < pq.N:
            pqit.enqueue(child, pq.storage[child].priority)
    
def iterator_trial():
    """Generate a sample Priority Queue and show develop iterator."""
    from ch04.heap import PQ
    import random
    
    # populate
    pq = PQ(20)
    for k in range(20):
        prior = random.randint(0, 100)
        pq.enqueue(prior, prior)
        
    while pq:
        print([k for k in iterator(pq)])
        print(pq.dequeue())
    

#######################################################################
if __name__ == '__main__':
    iterator_trial()

    t = list(range(100000))
    from random import shuffle
    shuffle(t)
    print(k_smallest(t, 7))

    combined_sorted()
