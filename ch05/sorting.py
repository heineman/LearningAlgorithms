"""
SelectionSort and InsertionSort
"""

def selection_sort(A):
    """Sort A using Selection Sort."""
    N = len(A)
    for i in range(N-1):
        min_index = i
        for j in range(i+1, N):
            if A[j] < A[min_index]:
                min_index = j

        A[i],A[min_index] = A[min_index],A[i]

def insertion_sort(A):
    """Sort A using Insertion Sort. Use Aj-1 <= Aj to ensure stable sort."""
    N = len(A)
    for i in range(1,N):
        for j in range(i,0,-1):
            if A[j-1] <= A[j]:
                break

            A[j],A[j-1] = A[j-1],A[j]

def insertion_sort_cmp(A, cmp=lambda one,two: one <= two):
    """Sort A using Insertion Sort."""
    N = len(A)
    for i in range(1,N):
        for j in range(i,0,-1):
            if cmp(A[j-1], A[j]):
                break

            A[j],A[j-1] = A[j-1],A[j]

def quick_sort(A):
    """Quicksort using a random pivot select."""
    from ch01.challenge import partition
    from random import randint

    def qsort(lo, hi):
        if hi <= lo:
            return

        pivot_idx = randint(lo, hi)
        location = partition(A, lo, hi, pivot_idx)

        qsort(lo, location-1)
        qsort(location+1, hi)

    qsort(0, len(A)-1)

def insertion_sort_bas(A):
    """
    Sort A using Insertion Sort using Binary Array Search to insert
    value. This code takes advantage of Python ability to insert value
    into an array since Python lists can dynamically resize. Will
    no longer be able to guarantee resulting sort is stable.
    """
    N = len(A)
    for i in range(1,N):
        lo = 0
        hi = i-1
        val = A[i]
        while lo <= hi:
            mid = (lo+hi)//2
            diff = val - A[mid]
            if diff < 0:
                hi = mid-1
            elif diff > 0:
                lo = mid + 1
            else:
                del A[i]             # delete from end first
                A.insert(mid, val)   # insert into proper spot
                break

        if hi < lo < i:           # protect if already in spot
            del A[i]              # delete from end first
            A.insert(lo, val)     # insert into proper spot

def selection_sort_counting(A):
    """Instrumented Selection Sort to return #swaps, #compares."""
    N = len(A)
    num_swap = num_compare = 0
    for i in range(N-1):
        min_index = i
        for j in range(i+1, N):
            num_compare += 1
            if A[j] < A[min_index]:
                min_index = j

        num_swap += 1
        A[i],A[min_index] = A[min_index],A[i]
    return (num_swap, num_compare)

def insertion_sort_counting(A):
    """Instrumented Insertion Sort to return #swaps, #compares."""
    N = len(A)
    num_swap = num_compare = 0
    for i in range(N):
        for j in range(i,0,-1):
            num_compare += 1
            if A[j-1] <= A[j]:
                break
            num_swap += 1
            A[j],A[j-1] = A[j-1],A[j]
    return (num_swap, num_compare)
