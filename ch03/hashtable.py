"""
    Hashtable to store (key, value) pairs in a fixed hashtable using
    hash() % N as hash code. This table can replace values associated
    with a given key, but if two keys attempt to use the same
    location, a RuntimeError is raised.

    Not able to handle collisions. Do not use this for production code!
    Only here as an example demonstrating that something needs fixing.
"""

from ch03.entry import Entry

class Hashtable:
    """Weak Hashtable implementation with no collision strategy."""
    def __init__(self, M=10):
        if M < 1:
            raise ValueError('Hashtable storage must be at least 1.')

        self.table = [None] * M
        self.M = M

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = hash(k) % self.M
        return self.table[hc].value if self.table[hc] else None

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M
        entry = self.table[hc]
        if entry:
            if entry.key == k:
                entry.value = v
            else:
                raise RuntimeError('Key Collision between {} and {}'.format(k, entry.key))
        else:
            self.table[hc] = Entry(k, v)
