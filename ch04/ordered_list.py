"""
List of ordered values. Use BinaryArraySearch to locate where we should be
and take advantage of Python's ability to extend list efficiently.
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
    """A Priority Queue implemented as a sorted list."""
    def __init__(self, size):
        self.size = size
        self.storage = [None] * size
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_full(self):
        """Priority queue has no fixed limit."""
        return False

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == self.size:
            raise RuntimeError('Priority Queue is Full!')

        to_add = Entry(v, p)
        idx = binary_array_search(self.storage, self.N-1, p)
        if idx < 0:
            self.storage.insert(-idx-1,to_add)
        else:
            self.storage.insert(idx,to_add)

        self.N += 1

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        self.N -= 1
        to_return = self.storage[self.N]
        self.storage[self.N] = None
        return to_return.value

#######################################################################
if __name__ == '__main__':
    pq = PQ(20)

    pq.enqueue('apple', 5)
    pq.enqueue('ball', 8)
    print(pq.dequeue())
    pq.enqueue('alternate', 5)
    pq.enqueue('car', 11)
    pq.enqueue('desk', 7)
    print(pq.dequeue())
    print(pq.dequeue())
    print(pq.dequeue())
    print(pq.dequeue())
