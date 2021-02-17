"""
Array of unordered values.
"""
from ch04.entry import Entry

def by_priority(entry):
    """Extract priority to be evaluated for sorting."""
    return entry.priority

class PQ:
    """Priority Queue using built-in list."""
    def __init__(self, size):
        self.size = size
        self.storage = []

    def __len__(self):
        """Return number of values in priority queue."""
        return len(self.storage)

    def is_full(self):
        """If priority queue has run out of storage, return True."""
        return self.size == len(self.storage)

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        if len(self.storage) == self.size:
            raise RuntimeError('Priority Queue is Full!')
        self.storage.append(Entry(v, p))

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.storage:
            m = max(self.storage, key=by_priority)  # finds left-most max
            self.storage.remove(m)                  # removes left-most with same index
            return m.value

        raise RuntimeError('PriorityQueue is empty!')

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
