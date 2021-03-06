"""A priority queue using an array of unordered values.

Unordered array is a fixed-length size, so it can become full.

* enqueue is O(1)
* dequeue is O(N)

"""

from ch04.entry import Entry

class PQ:
    """A priority queue using a fixed-size array for storage."""
    def __init__(self, size):
        self.size = size
        self.storage = [None] * size
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_full(self):
        """If priority queue has run out of storage, return True."""
        return self.size == self.N

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == self.size:
            raise RuntimeError('Priority Queue is full!')
        self.storage[self.N] = Entry(v, p)
        self.N += 1

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        max_pos = 0
        for i in range(1,self.N):
            if self.storage[i].priority > self.storage[max_pos].priority:
                max_pos = i

        max_entry = self.storage[max_pos]
        self.storage[max_pos] = self.storage[self.N-1]
        self.storage[self.N-1] = None
        self.N -= 1

        return max_entry.value
