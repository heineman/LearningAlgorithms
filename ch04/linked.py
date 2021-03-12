"""
Linked list implementation of priority queue structure.

Stores all values in descending.
"""

from ch04.linked_entry import LinkedEntry

class PQ:
    """Heap storage for a priority queue using linked lists."""
    def __init__(self, size):
        self.size = size
        self.first = None
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
            raise RuntimeError('Priority Queue is Full!')
        self.N += 1
        to_add = LinkedEntry(v, p)

        if self.first:
            # find first node SMALLER than key, and keep track of
            # prev so we can insert properly
            n = self.first
            prev = None
            while n:
                if p > n.priority:    # Stop once in the right place
                    if prev:
                        to_add.next = n
                        prev.next = to_add
                    else:
                        to_add.next = self.first
                        self.first = to_add
                    return
                prev, n = n, n.next
            prev.next = LinkedEntry(v, p)
        else:
            self.first = to_add

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.first:
            val = self.first.value
            self.first = self.first.next
            self.N -= 1
            return val

        raise RuntimeError('PriorityQueue is empty!')
