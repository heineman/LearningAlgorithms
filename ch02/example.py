"""Compare three different processing behaviors."""
import random
import timeit

def dataset1(n):
    """First data set."""
    return ['{}{}'.format('a' * 40, random.randint(0,n)) for _ in range(n)]

def insertion_sort(A):
    """Insertion Sort."""
    for i in range(1, len(A)):
        v = A[i]
        j = i-1
        while j >= 0 and v < A[j]:
            A[j+1] = A[j]
            j -= 1
        A[j+1] = v

def run_trial():
    """Generate table for times on Insertion Sort."""
    print('N\tTime')
    trials = [100, 1000]
    for n in trials:
        sort_time = timeit.timeit(stmt='insertion_sort(x)', setup='''
from ch02.example import dataset1, insertion_sort
x=dataset1({})'''.format(n), number=100)

        print('{0:d}\t{1:.4f}'.format(n, sort_time))

#######################################################################
if __name__ == '__main__':
    run_trial()
