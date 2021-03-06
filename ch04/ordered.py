"""
Array of ordered values. Use BinaryArraySearch to locate where we should be
"""

from ch04.entry import Entry

def binary_array_search(A, hi, target):
    """
    Use binary array search to search for target in ordered list A.
    If target is found, a non-negative value is returned marking the
    location in A; if a negative number, x, is found then -x-1 is the
    location where target would need to be inserted.
    """
    lo = 0
    while lo <= hi:
        mid = (lo + hi) // 2

        diff = target - A[mid].priority
        if diff < 0:
            hi = mid-1
        elif diff > 0:
            lo = mid+1
        else:
            return mid

    return -(1+lo)

class PQ:
    """A Priority Queue implemented as list."""
    def __init__(self, size):
        self.size = size
        self.storage = [None] * size
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_full(self):
        """Determine if array is full."""
        return self.size == self.N

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == self.size:
            raise RuntimeError('Priority Queue is Full!')
        idx = binary_array_search(self.storage, self.N-1, p)

        if idx < 0:             # might be duplicate,  might not...
            idx = -idx-1

        # move each element up to make room
        for i in range(self.N, idx, -1):
            self.storage[i] = self.storage[i-1]
        self.storage[idx] = Entry(v, p)

        self.N += 1

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        self.N -= 1
        to_return = self.storage[self.N]
        self.storage[self.N] = None
        return to_return.value
