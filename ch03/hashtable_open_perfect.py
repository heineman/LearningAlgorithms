"""
    Uses perfect hash generated from English dictionary. Use each designated bucket
    to hold a single Entry. If a non-English word somehow hashes to a bucket, the
    code checks against the key to be sure it is the right one.

    As long as you only use keys from the English dictionary used to construct the
    perfect hash, there will be no collisions.
"""

from ch03.entry import Entry
from ch03.perfect.generated_dictionary import perfect_hash

class Hashtable:
    """Hashtable using perfect hashing from 321,129 English word dictionary."""
    def __init__(self):
        self.table = [None] * 321129
        self.N = 0

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = perfect_hash(k)
        if self.table[hc] and self.table[hc].key == k:
            return self.table[hc].value
        return None

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = perfect_hash(k)
        self.table[hc] = Entry(k, v)
        self.N += 1

    def __iter__(self):
        """Generate all (k, v) tuples for entries in the table."""
        for entry in self.table:
            if not entry is None:
                yield (entry.key, entry.value)
