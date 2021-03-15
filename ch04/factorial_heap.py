"""
max Heap where each successive level has one more child, which leads to levels
containing k! elements, where k is the level.
"""
from ch04.entry import Entry

# SUMS of factorials. 1st id on a new level is 1 + this
_factorials = [0, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800 ]
_sums =       [0, 1, 3, 9, 33, 153, 873, 5913, 46233, 409113, 4037913, 43954713 ]

_firsts =     [0, 1, 2, 4, 10, 34, 154, 874, 5914, 46234, 409114, 4037914, 40325914 ]
_constants =  [0, 2, 6, 16, 50, 204, 1078, 6992, 53226, 462340, 4500254, 48454968, 524236882]

def fh_parent(k,lev):
    """Return index of parent for index k on level lev."""
    if lev <= 0:
        return 1    # HACK. Covers base case inelegantly
    return (k + _constants[lev-1]) // (lev+1)    # was firsts[lev-1]*lev

def fh_child(k,lev):
    """Return index of first child of index k on level lev."""
    return k*(lev+2) - _constants[lev]      # was firsts[lev]*(lev+1)

def validate_level(pq, lev, k):
    """Validate node k on a given level."""

    # If no child possible leave
    fc = fh_child(k,lev)
    count = 0
    while fc <= pq.N and count <= lev:
        if pq.less(k, fc):
            return False
        if not validate_level(pq, lev+1, fc):
            return False

        count += 1
        fc += 1

    return True   # checks out!

def validate(pq):
    """Validate heap-ordered property is valid (assumed heap-shape)."""
    return validate_level(pq, 0, 1)

class PQ:
    """
    Factorial Heap storage for a priority queue.
    """
    def __init__(self, size):
        self.size = size
        self.storage = [None] * (size+1)
        self.N = 0
        self.level = 0

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
        if self.N > _sums[self.level+1]:
            self.level += 1

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

    def swim(self, k):
        """Reestablish heap-order property from storage[child] up."""
        lev = self.level
        parent = fh_parent(k,lev)
        while k > 1 and self.less(parent, k):
            self.swap(parent, k)
            k = parent
            lev -= 1
            parent = fh_parent(k, lev)

    def sink(self, k):
        """Reestablish heap-order property from storage[parent] down."""
        lev = 0             # always starts at 1 on level 0

        # If no child possible leave
        fc = fh_child(k,lev)
        while fc <= self.N:
            # Find largest of children
            largest = fc
            offset = 1
            lev += 1
            while fc+offset < self.N and offset <= lev:
                if self.less(largest, fc+offset):
                    largest = fc+offset
                offset += 1

            if not self.less(k, largest):
                break

            self.swap(k, largest)

            k = largest
            fc = fh_child(k,lev)

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        max_entry = self.storage[1]
        self.swap(1, self.N)
        self.N -= 1
        if self.N == _sums[self.level]:          # advance to next level
            self.level -= 1

        self.storage[self.N+1] = None           # avoid lingering
        self.sink(1)

        return max_entry.value
