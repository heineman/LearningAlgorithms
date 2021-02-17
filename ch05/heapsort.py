"""
Contains implementation of Heap Sort as a stand-alone class.

HeapSortCounting also provides ability to record number of swaps
and number of times less was invoked.
"""

class HeapSort:
    """
    Wrapper class that provides Heap Sort implementation.
    """
    def __init__(self, A):
        self.storage = A
        self.N = len(A)

        for k in range(self.N//2, 0, -1):
            self.sink(k)

    def sort(self):
        """Use Heap to Sort array in place."""
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)

    def less(self, i, j):
        """Determine if A[i] < A[j], using updated index locations."""
        return self.storage[i-1] < self.storage[j-1]

    def swap(self, i, j):
        """Swap A[i] and A[j]."""
        self.storage[i-1],self.storage[j-1] = self.storage[j-1],self.storage[i-1]

    def sink(self, parent):
        """Reestablish heap-ordered property from parent down."""
        while 2*parent <= self.N:
            child = 2*parent
            if child < self.N and self.less(child, child+1):
                child += 1
            if not self.less(parent, child):
                break
            self.swap(child, parent)

            parent = child

class HeapSortCounting:
    """
    Wrapper class that provides Heap Sort implementation.

    Counts number of times less() and swap() were invoked.
    """
    def __init__(self, A):
        self.storage = A
        self.N = len(A)
        self.num_swaps = 0
        self.num_comparisons = 0

        for k in range(self.N//2, 0, -1):
            self.sink(k)

    def sort(self):
        """Use Heap to Sort array in place."""
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)

    def less(self, i, j):
        """Determine if A[i] < A[j], using updated index locations. Increments num_comparisons"""
        self.num_comparisons += 1
        return self.storage[i-1] < self.storage[j-1]

    def swap(self, i, j):
        """Swap A[i] and A[j], incrementing num_swaps count."""
        self.num_swaps += 1
        self.storage[i-1],self.storage[j-1] = self.storage[j-1],self.storage[i-1]

    def sink(self, parent):
        """Reestablish heap-ordered property from parent down."""
        while 2*parent <= self.N:
            child = 2*parent
            if child < self.N and self.less(child, child+1):
                child += 1
            if not self.less(parent, child):
                break
            self.swap(child, parent)

            parent = child
