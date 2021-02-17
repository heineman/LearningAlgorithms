"""Unusually poor sorting algorithms that work (eventually)."""
from random import shuffle
from itertools import permutations
from algs.sorting import check_sorted

def random_sort(A):
    """
    Randomly shuffle A until it is sorted.
    This can take arbitrarily long and may never actually
    produce the sorted answer. However, with non-zero
    probability it might generate the answer.
    """
    while not check_sorted(A):
        shuffle(A)

def permutation_sort(A):
    """
    Generates all permutation of A until one is sorted.
    Guaranteed to sort the values in A.
    """
    for attempt in permutations(A):
        if check_sorted(attempt):
            A[:] = attempt[:]         # copy back into A
            return
