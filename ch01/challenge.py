"""
Challenge Exercises for Chapter 1.
"""

import random
import timeit

from algs.table import DataTable, ExerciseNum, caption
from algs.counting import RecordedItem

def partition(A, lo, hi, idx):
    """
    Partition using A[idx] as value. Note lo and hi are INCLUSIVE on both
    ends and idx must be valid index. Count the number of comparisons
    by populating A with RecordedItem instances.
    """
    if lo == hi:
        return lo

    A[idx],A[lo] = A[lo],A[idx]    # swap into position
    i = lo
    j = hi + 1
    while True:
        while True:
            i += 1
            if i == hi: break
            if A[lo] < A[i]: break

        while True:
            j -= 1
            if j == lo: break
            if A[j] < A[lo]: break

        # doesn't count as comparing two values
        if i >= j: break

        A[i],A[j] = A[j],A[i]

    A[lo],A[j] = A[j],A[lo]
    return j

def linear_median(A):
    """
    Efficient implementation that returns median value in arbitrary list,
    assuming A has an odd number of values. Note this algorithm will
    rearrange values in A.
    """
#     if len(A) % 2 == 0:
#         raise ValueError('linear_median() only coded to work with odd number of values.')
    lo = 0
    hi = len(A) - 1
    mid = hi // 2
    while lo < hi:
        idx = random.randint(lo, hi)     # select valid index randomly
        j = partition(A, lo, hi, idx)

        if j == mid:
            return A[j]
        if j < mid:
            lo = j+1
        else:
            hi = j-1
    return A[lo]

def counting_sort(A, M):
    """
    Update A in place to be sorted in ascending order if all elements
    are guaranteed to be in the range 0 to and not including M.
    """
    counts = [0] * M
    for v in A:
        counts[v] += 1

    pos = 0
    v = 0
    while pos < len(A):
        for idx in range(counts[v]):
            A[pos+idx] = v
        pos += counts[v]
        v += 1

def counting_sort_improved(A,M):
    """
    Update A in place to be sorted in ascending order if all elements
    are guaranteed to be in the range 0 to and not including M.
    """
    counts = [0] * M
    for val in A:
        counts[val] += 1

    pos = 0
    val = 0
    while pos < len(A):
        if counts[val] > 0:
            A[pos:pos+counts[val]] = [val] * counts[val]
            pos += counts[val]
        val += 1

def run_counting_sort_trials(max_k=15, output=True):
    """Generate table for counting sort up to (but not including) max_k=15."""
    tbl = DataTable([8,15,15],
                    ['N', 'counting_sort', 'counting_sort_improved'], output=output)

    M = 20 # arbitrary value, and results are dependent on this value.
    trials = [2**k for k in range(8, max_k)]
    for n in trials:
        t_cs = min(timeit.repeat(stmt='counting_sort(a,{})\nis_sorted(a)'.format(M),
                                 setup='''
import random
from ch01.challenge import counting_sort
from algs.sorting import is_sorted
w = [{0}-1] * {1}
b = [0] * {1} 
a = list(range({0})) * {1}
random.shuffle(a)'''.format(M,n), repeat=100, number=1))
        t_csi = min(timeit.repeat(stmt='counting_sort_improved(a,{})\nis_sorted(a)'.format(M),
                                  setup='''
import random
from ch01.challenge import counting_sort_improved
from algs.sorting import is_sorted
w = [{0}-1] * {1}
b = [0] * {1} 
a = list(range({0})) * {1}
random.shuffle(a)'''.format(M,n), repeat=100, number=1))

        tbl.row([n, t_cs, t_csi])
    return tbl

def run_median_trial():
    """Generate table for Median Trial."""
    tbl = DataTable([10,15,15],['N', 'median_time', 'sort_median'])

    trials = [2**k+1 for k in range(8,20)]
    for n in trials:
        t_med = 1000*min(timeit.repeat(stmt='assert(linear_median(a) == {}//2)'.format(n),
                                       setup='''
import random
from ch01.challenge import linear_median
a = list(range({}))
random.shuffle(a)
'''.format(n), repeat=10, number=5))/5

        t_sort = 1000*min(timeit.repeat(stmt='assert(sorted(a)[{0}//2] == {0}//2)'.format(n),
                                        setup='''
import random
from ch01.challenge import linear_median
a = list(range({}))
random.shuffle(a)
'''.format(n), repeat=10, number=5))/5

        tbl.row([n, t_med, t_sort])

    return tbl

def run_median_less_than_trial(max_k=20, output=True):
    """Use RecordedItem to count # of times Less-than invoked up to (but not including) max_k=20."""
    tbl = DataTable([10,15,15],['N', 'median_count', 'sort_median_count'], output=output)
    tbl.format('median_count', ',d')
    tbl.format('sort_median_count', ',d')

    trials = [2**k+1 for k in range(8, max_k)]
    for n in trials:
        A = list([RecordedItem(i) for i in range(n)])
        random.shuffle(A)

        # Generated external sorted to reuse list
        RecordedItem.clear()
        med2 = sorted(A)[n//2]
        sort_lt = RecordedItem.report()[1]

        RecordedItem.clear()
        med1 = linear_median(A)
        lin_lt = RecordedItem.report()[1]

        assert med1 == med2

        tbl.row([n, lin_lt, sort_lt])

    return tbl

def is_palindrome1(w):
    """Create slice with negative step and confirm equality with w."""
    return w[::-1] == w

def is_palindrome2(w):
    """Strip outermost characters if same, return false when mismatch."""
    while len(w) > 1:
        if w[0] != w[-1]:     # if mismatch, return False
            return False
        w = w[1:-1]           # strip characters on either end; repeat

    return True               # must have been a Palindrome

def is_palindrome_letters_only(s):
    """
    Confirm Palindrome, even when string contains non-alphabet letters
    and ignore capitalization.

    casefold() method, which was introduced in Python 3.3, could be
    used instead of this older method, which converts to lower().
    """
    i = 0
    j = hi = len(s) - 1
    while i < j:
        # This type of logic appears in partition.
        # Find alpha characters and compare
        while not s[i].isalpha():
            i += 1
            if i == hi: break
        while not s[j].isalpha():
            j -= 1
            if j == 0: break

        if s[i].lower() != s[j].lower(): return False
        i += 1
        j -= 1

    return True

def tournament_allows_odd(A):
    """
    Returns two largest values in A. Works for odd lists
    """
    from ch01.largest_two import Match
    if len(A) < 2:
        raise ValueError('Must have at least two values')

    tourn = []
    for i in range(0, len(A)-1, 2):
        tourn.append(Match(A[i], A[i+1]))
    odd_one_out = None
    if len(A) % 2 == 1:
        odd_one_out = A[-1]

    while len(tourn) > 1:
        tourn.append(Match.advance(tourn[0], tourn[1]))
        del tourn[0:2]

    # Find where second is hiding!
    m = tourn[0]
    largest = m.larger
    second = m.smaller

    # Wait until the end, and see where it belongs
    if odd_one_out:
        if odd_one_out > largest:
            largest,second = odd_one_out,largest
        elif odd_one_out > second:
            second = odd_one_out

    while m.prior:
        m = m.prior
        if second < m.smaller:
            second = m.smaller

    return (largest,second)

def two_largest_attempt(A):
    """Failed attempt to implement two largest."""
    m1 = max(A[:len(A)//2])
    m2 = max(A[len(A)//2:])
    if m1 < m2:
        return (m2, m1)
    return (m1, m2)

#######################################################################
if __name__ == '__main__':
    chapter = 1

    with ExerciseNum(1) as exercise_number:
        sample = 'A man, a plan, a canal. Panama!'
        print(sample,'is a palindrome:', is_palindrome_letters_only(sample))
        print(caption(chapter, exercise_number),
              'Palindrome Detector')

    with ExerciseNum(2) as exercise_number:
        run_median_less_than_trial()
        print()
        run_median_trial()
        print(caption(chapter, exercise_number),
              'Median Counting')

    with ExerciseNum(3) as exercise_number:
        run_counting_sort_trials()
        print(caption(chapter, exercise_number),
              'Counting Sort Trials')

    with ExerciseNum(4) as exercise_number:
        print('see tournament_allows_odd in ch01.challenge')
        print(caption(chapter, exercise_number),
              'Odd tournament')

    with ExerciseNum(5) as exercise_number:
        print('Should print (9, 8)', two_largest_attempt([9, 3, 5, 7, 8, 1]))
        print('Fails to print (9, 8)', two_largest_attempt([9, 8, 5, 7, 3, 1]))
        print(caption(chapter, exercise_number),
              'Failed Two largest')
