"""
Challenge Exercises for Chapter 4.
"""

import timeit
from algs.modeling import numpy_error

from algs.table import DataTable, ExerciseNum, comma, caption
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
    return min(timeit.repeat(stmt='merged_arrays(heap1, heap2)', setup = '''
import random
from ch04.heap import PQ
from ch04.challenge import merged_arrays
heap1 = PQ({0})
heap2 = PQ({1})
random.seed({0})
for _ in range({0}):
    r1 = random.randint(0,16777216)
    heap1.enqueue(r1,r1)
random.seed({1})
for _ in range({1}):
    r2 = random.randint(0,16777216)
    heap2.enqueue(r2,r2)'''.format(m,n), repeat=5, number=1))

def combined_sorted(lo=8, hi=12, output=True):
    """Generate results for different sorting trials."""
    tbl = DataTable([8] * (hi-lo+1), ['N'] + [comma(2**k) for k in range(lo,hi)], output=output)

    for n in [2**k for k in range(lo,hi)]:
        row = [n]
        for m in [2**k for k in range(lo,hi)]:
            row.append(run_merge_trial(m,n))
        tbl.row(row)

    # Diagonal values are for 2*M*log(M) so divide in HALF for accurate one
    # build model ONLY for first five values
    x = [2**k for k in range(lo,min(lo+5,hi))]
    y = [tbl.entry(r,comma(r)) for r in [2**k for k in range(lo,min(lo+5,hi))]]
    if numpy_error:
        a = 0
    else:
        import numpy as np
        from scipy.optimize import curve_fit
        from scipy.stats.stats import pearsonr

        (coeffs,_) = curve_fit(n_log_n_model, np.array(x), np.array(y))
        a = coeffs[0] / 2

        y_fit = [n_log_n_model(r,a) for r in [2**k for k in range(lo,min(lo+5,hi))]]

        print()
        print(pearsonr(y, y_fit))
        print()
        print('Prediction')
        model = DataTable([8] * (hi-lo+1), ['N'] + [comma(2**k) for k in range(lo,hi)], output=output)
        for n in [2**k for k in range(lo,hi)]:
            row = [n]
            for m in [2**k for k in range(lo,hi)]:
                row.append(n_log_n_model(n,a) + n_log_n_model(m,a))
            model.row(row)
    return tbl

def k_smallest(A, k):
    """
    Super-efficient (and easy to write) k-smallest selection for an arbitrary iterable.
    Time (and space) will be proportional to O(log k).
    """
    from ch04.heap import PQ
    pq = PQ(k)

    # pq is a regular Max Binary Heap. Enqueue first k elements. If any 
    # subsequent value is LARGER than our largest, it can be ignored, otherwise
    # remove the largest (since one is now smaller) and enqueue it.
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

def random_trial_k_smallest(n, k):
    """Conduct a random k_smallest trial."""
    from random import shuffle
    vals = list(range(n))
    shuffle(vals)
    return k_smallest(vals, k)

def iterator(pq):
    """
    Provides a Python-generator over a PQ, using a PQ to do it!

    Each entry in the pqit iterator has (value, priority) where value is
    an index position into the original pq, while its priority is the
    priority if the entry.

    You can add capability for fail-fast iterators IF the heap actively
    increments a count in its pq.storage[0] which is unused anyway.
    
    Returned values include both the (value, priority) for maximum flexibility.
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
        if child <= pq.N:
            pqit.enqueue(child, pq.storage[child].priority)
        child += 1
        if child <= pq.N:
            pqit.enqueue(child, pq.storage[child].priority)

def iterator_trial():
    """Generate a sample Priority Queue and show develop iterator."""
    from ch04.heap import PQ
    import random

    # populate
    pq = PQ(63)
    pq2 = PQ(63)
    for _ in range(63):
        prior = random.randint(0, 100)
        pq.enqueue(prior, prior)
        pq2.enqueue(prior, prior)

    for p in iterator(pq2):
        vp = pq.dequeue()
        if p[0] != vp:
            raise RuntimeError('Unexpected that iterator is different.')

def inspect_heap_array():
    """
    After inserting N elements in ascending order, is there a pattern in the
    values in the arrays in the heap? Same for inserting in descending order. 
    """
    from ch04.heap import PQ

    num=31
    pq = PQ(num)
    for i in range(1,num+1):
        pq.enqueue(i, i)

    i = 1
    rights = []
    while i <= num:
        rights.append(pq.storage[i].value)
        i = (i*2) + 1
    print(rights)
    print([i.value for i in pq.storage[1:]])

    pq = PQ(num)
    for i in range(num, 0, -1):
        pq.enqueue(i, i)

#######################################################################
if __name__ == '__main__':
    chapter = 4

    with ExerciseNum(1) as exercise_number:
        print('implementation in ch04.circular_queue')
        print(caption(chapter, exercise_number), 'Circular Queue')
        print()

    with ExerciseNum(2) as exercise_number:
        inspect_heap_array()
        print('When inserting N=2^k-1 values in ascending order, right most values')
        print('in each of the k levels contains largest. When inserting in reverse')
        print('order, each value remains where it was inserted, so all are descending.')
        print(caption(chapter, exercise_number),'Values in heap')
        print()

    with ExerciseNum(3) as exercise_number:
        combined_sorted(hi=16)
        print(caption(chapter, exercise_number),
              'Merging two heaps in O(M*log(M) + N*log(N)')
        print()

    with ExerciseNum(4) as exercise_number:
        print(random_trial_k_smallest(5, 2**20), 'are the 5 smallest values in 0 .. 2**20')
        print(caption(chapter, exercise_number),
              'Find k smallest values from a collection in time O(log k).')
        print()

    with ExerciseNum(5) as exercise_number:
        from ch04.timing import trial_factorial_heap
        trial_factorial_heap()
        print(caption(chapter, exercise_number),
              'Factorial Heap.')
        print()

    with ExerciseNum(6) as exercise_number:
        print(caption(chapter, exercise_number),
              'standard extension of Heap to dynamically resize.')
        print()

    with ExerciseNum(7) as exercise_number:
        iterator_trial()
        print(caption(chapter, exercise_number),
              'Non-destructive iterator for a max binary heap.')
        print()
