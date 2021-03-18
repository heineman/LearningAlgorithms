"""
max binary Heap.
"""
from ch04.entry import Entry

class PQ:
    """
    Heap storage for a priority queue.
    """
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_empty(self):
        """Returns whether priority queue is empty."""
        return self.N == 0

    def is_full(self):
        """If priority queue has run out of storage, return True."""
        return self.size == self.N

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == self.size:
            raise RuntimeError('Priority Queue is full!')
        self.N += 1

        self.storage[self.N] = Entry(v, p)
        self.swim(self.N)

    def less(self, i, j):
        """
        Helper function to determine if storage[j] has higher
        priority than storage[i].
        """
        return self.storage[i].priority < self.storage[j].priority

    def swap(self, i, j):
        """Switch the values in storage[i] and storage[j]."""
        self.storage[i],self.storage[j] = self.storage[j],self.storage[i]

    def swim(self,child):
        """Reestablish heap-order property from storage[child] up."""
        while child > 1 and self.less(child//2, child):
            self.swap(child, child//2)
            child = child//2

    def sink(self, parent):
        """Reestablish heap-order property from storage[parent] down."""
        while 2*parent <= self.N:
            child = 2*parent
            if child < self.N and self.less(child, child+1):
                child += 1
            if not self.less(parent, child):
                break
            self.swap(child, parent)

            parent = child

    def peek(self):
        """
        Peek without disturbing the value at the top of the priority queue. Must
        return entire Entry, since the one calling might like to know priority and value
        """
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        return self.storage[1]

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        max_entry = self.storage[1]
        self.storage[1] = self.storage[self.N]
        self.storage[self.N] = None
        self.N -= 1
        self.sink(1)
        return max_entry.value
