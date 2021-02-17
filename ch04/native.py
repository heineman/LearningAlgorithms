"""
Heapq is min heap provided by Python libraries.

In some implementations, two elements with the same priority are
removed from the PQ in the order in which they had been inserted,
but this is not the case.
"""

import heapq

class Item:
    """Represents an item that is comparable by priority."""
    def __init__(self, v, p):
        """An entry in priority queue."""
        self.val = v
        self.priority = p

    def __lt__(self, other):
        """Needed for Item to be in a heap."""
        return self.priority < other.priority

    def __str__(self):
        """return string representation."""
        return '[value={}, priority={}]'.format(self.val, self.priority)

class TimeSpecifiedItem:
    """
    Build in timestamp when an item is enqueued to be able to break
    ties by oldest timestamp.
    """
    ctr = [0]

    def __init__(self, v, p):
        """
        An entry in priority queue with counter since timestamp is
        not precise enough, even with nanosec.
        """
        self.val = v
        self.priority = p
        self.timestamp = TimeSpecifiedItem.ctr[0]
        TimeSpecifiedItem.ctr[0] += 1

    def __lt__(self, other):
        """Needed for Item to be in a heap."""
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority < other.priority

    def __str__(self):
        """return string representation."""
        return '[value={}, priority={}]'.format(self.val, self.priority)

#######################################################################
if __name__ == '__main__':
    X = []
    heapq.heappush(X, Item('A', 5))
    heapq.heappush(X, Item('B', 5))
    heapq.heappush(X, Item('C', 5))
    heapq.heappush(X, Item('D', 5))
    heapq.heappush(X, Item('E', 5))
    heapq.heappush(X, Item('F', 5))
    while X:
        print(heapq.heappop(X))

    # Output above should be A, C, F, E, B, D
    print()

    X = []
    heapq.heappush(X, TimeSpecifiedItem('A', 5))
    heapq.heappush(X, TimeSpecifiedItem('B', 5))
    heapq.heappush(X, TimeSpecifiedItem('C', 5))
    heapq.heappush(X, TimeSpecifiedItem('D', 5))
    heapq.heappush(X, TimeSpecifiedItem('E', 5))
    heapq.heappush(X, TimeSpecifiedItem('F', 5))
    while X:
        print(heapq.heappop(X))

    for N in range(510,514):
        X = []
        for x in list(range(-1, -N, -1)):
            heapq.heappush(X, Item(str(x), x))

        print(N, X[3].priority, X[4].priority, X[5].priority, X[6].priority)
