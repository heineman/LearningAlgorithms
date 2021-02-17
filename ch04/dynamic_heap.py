"""
max binary Heap that can grow and shrink as needed. Typically this
functionality is not needed. self.size records initial size and never
changes, which prevents shrinking logic from reducing storage below
this initial amount.
"""
from ch04.entry import Entry

class PQ:
    """Priority Queue implemented using a heap."""
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_empty(self):
        """Determine whether Priority Queue is empty."""
        return self.N == 0

    def is_full(self):
        """If priority queue has run out of storage, return True."""
        return self.size == self.N

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if self.N == len(self.storage) - 1:
            self.resize(self.N*2)
        self.N += 1

        self.storage[self.N] = Entry(v, p)
        self.swim(self.N)

    def less(self, i, j):
        """
        Helper function to determine if storage[i] has higher
        priority than storage[j].
        """
        return self.storage[i].priority < self.storage[j].priority

    def swap(self, i, j):
        """Switch the values in storage[i] and storage[j]."""
        self.storage[i],self.storage[j] = self.storage[j],self.storage[i]

    def swim(self, child):
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

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        max_entry = self.storage[1]
        self.swap(1, self.N)
        self.storage[self.N] = None
        self.N -= 1
        self.sink(1)
        storage_size = len(self.storage)
        if storage_size > self.size and self.N < storage_size // 4:
            self.resize(self.N // 2)
        return max_entry.value

    def resize(self, new_size):
        """Resize storage array to accept more elements."""
        replace = [None] * (new_size+1)
        replace[0:self.N+1] = self.storage[0:self.N+1]
        self.storage = replace

#######################################################################
if __name__ == '__main__':
    pq = PQ(20)
    for idx in range(2000):
        pq.enqueue('sample' + str(idx), idx)

    while not pq.is_empty():
        print(pq.dequeue())

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
