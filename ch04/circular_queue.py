"""A fixed-capacity queue implemented as circular queue.

Queue can become full.

* enqueue is O(1)
* dequeue is O(1)

"""

class Queue:
    """
    Implementation of a Queue using a circular buffer.
    """
    def __init__(self, size):
        self.size = size
        self.storage = [None] * size
        self.first = 0
        self.last = 0
        self.N = 0

    def is_empty(self):
        """Determine if queue is empty."""
        return self.N == 0

    def is_full(self):
        """Determine if queue is full."""
        return self.N == self.size

    def enqueue(self, item):
        """Enqueue new item to end of queue."""
        if self.is_full():
            raise RuntimeError('Queue is full')

        self.storage[self.last] = item
        self.N += 1
        self.last = (self.last + 1) % self.size

    def dequeue(self):
        """Remove and return first item from queue."""
        if self.is_empty():
            raise RuntimeError('Queue is empty')

        val = self.storage[self.first]
        self.N -= 1
        self.first = (self.first + 1) % self.size
        return val
