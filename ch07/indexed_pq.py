"""
Indexed minimum priority queue
"""
class IndexedMinPQ:
    """
    Heap storage for an indexed min priority queue.
    """
    def __init__(self, size):
        self.size = size
        self.priorities = [None] * (size+1)   # binary heap using 1-based indexing
        self.values = [None] * (size+1)
        self.location = {}                 # For each value, remember its location in storage
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def __contains__(self, v):
        """Determine if idx is currently in the priority queue."""
        return v in self.location

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

        self.values[self.N], self.priorities[self.N] = v, p
        self.location[v] = self.N                 # record where it is being stored
        self.swim(self.N)

    def decrease_priority(self, v, lower_priority):
        """Reduce associated priority with v to move it closer to head of priority queue."""
        if not v in self.location:
            raise ValueError('{} not in the indexed min priority queue.'.format(v))
        idx = self.location[v]
        if lower_priority >= self.priorities[idx]:
            raise RuntimeError('Value {} has existing priority of {} which is already lower than {}'.format(v, self.priorities[idx], lower_priority))

        self.priorities[idx] = lower_priority
        self.swim(idx)

    def less(self, i, j):
        """
        Helper function to determine if priorities[j] has higher
        priority than priorities[i]. Min PQ means > is operator to use.
        """
        return self.priorities[i] > self.priorities[j]

    def swap(self, i, j):
        """Switch the values in storage[i] and storage[j]."""
        self.values[i],self.values[j] = self.values[j],self.values[i]
        self.priorities[i],self.priorities[j] = self.priorities[j],self.priorities[i]

        self.location[self.values[i]] = i
        self.location[self.values[j]] = j

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
        """Peek without disturbing the value at the top of the priority queue."""
        if self.N == 0:
            raise RuntimeError('IndexMinPriorityQueue is empty!')

        return self.values[1]

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        min_value = self.values[1]
        self.values[1] = self.values[self.N]
        self.priorities[1] = self.priorities[self.N]
        self.location[self.values[1]] = 1

        self.values[self.N] = self.priorities[self.N] = None
        self.location.pop(min_value)   # remove from dictionary

        self.N -= 1
        self.sink(1)
        return min_value
