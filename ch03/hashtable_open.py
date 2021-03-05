"""
    Hashtable to store (key, value) pairs in a fixed hashtable using hash() % N as hash code.
    This table can replace values associated with a given key.  When two keys attempt to use
    the same location, OPEN ADDRESSING resolves the conflict.

    Always leaves at least ONE empty spot so code is simpler, which means that an 
    open addressing hashtable must have M >= 2.
"""

from ch03.entry import Entry, MarkedEntry

class Hashtable:
    """Open Addressing Hashtable."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 2:
            raise ValueError('Hashtable must contain space for at least two (key, value) pairs.')
        self.M = M
        self.N = 0

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = hash(k) % self.M       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None                 # Couldn't find

    def is_full(self):
        """Determine if Hashtable is full."""
        return self.N >= self.M - 1

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                return
            hc = (hc + 1) % self.M

        if self.N >= self.M - 1:
            raise RuntimeError('Table is Full: cannot store {} -> {}'.format(k, v))

        self.table[hc] = Entry(k, v)
        self.N += 1

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if entry:
                yield (entry.key, entry.value)

class DynamicHashtable:
    """Open Addressing Hashtable that supports resizing."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable must contain space for at least two (key, value) pairs.')
        self.M = M
        self.N = 0

        self.load_factor = 0.75

        # Ensure resize event happens NO LATER than M-1, since you need at
        # least one empty bucket
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = hash(k) % self.M       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None                 # Couldn't find

    def resize(self, new_size):
        """Resize table and rehash existing entries into new table."""
        temp = DynamicHashtable(new_size)
        for n in self.table:
            if n:
                temp.put(n.key, n.value)
        self.table = temp.table
        temp.table = None     # ensures memory is freed
        self.M = temp.M
        self.threshold = self.load_factor * self.M

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                return
            hc = (hc + 1) % self.M

        # With Open Addressing, you HAVE to insert first into the
        # empty bucket before checking whether you have hit
        # the threshold, otherwise you have to search again to
        # find an empty space. The impact is that this last entry
        # is "inserted twice" on resize; small price to pay. Note
        # That this last entry COULD be the last empty bucket, but
        # the forced resize below will resolve that issue
        self.table[hc] = Entry(k, v)
        self.N += 1

        if self.N >= self.threshold:
            self.resize(2*self.M + 1)
            hc = hash(k) % self.M

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if entry:
                yield (entry.key, entry.value)

class DynamicHashtablePlusRemove:
    """
    Supports removal of entries, which causes numerous little changes
    throughout the class.

    Note that __iter__() properly filters out entries that have been deleted.
    """
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 2:
            raise ValueError('Hashtable must contain space for at least two (key, value) pairs.')
        self.M = M
        self.N = 0
        self.deleted = 0

        self.load_factor = 0.75

        # Ensure resize event happens NO LATER than M-1, since you need at
        # least one empty bucket
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k and not self.table[hc].is_marked():
                return self.table[hc].value
            hc = (hc + 1) % self.M
        return None                 # Couldn't find

    def resize(self, new_size):
        """Resize table and rehash existing entries into new table."""
        temp = DynamicHashtablePlusRemove(new_size)
        for n in self.table:
            if n and not n.is_marked():
                temp.put(n.key, n.value)
        self.table = temp.table
        temp.table = None     # ensures memory is freed
        self.M = temp.M
        self.threshold = self.load_factor * self.M
        self.deleted = 0

    def remove(self, k):
        """Remove (k,v) entry associated with k."""
        hc = hash(k) % self.M
        while self.table[hc]:
            if self.table[hc].key == k:
                if self.table[hc].is_marked():    # has already been removed
                    return None                   # so return None

                self.table[hc].mark()             # record it's been deleted
                self.N -= 1
                if (self.N < 0):
                    print ("SDSD")
                self.deleted += 1
                return self.table[hc].value       # and return former value
            hc = (hc + 1) % self.M
        return None

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                if self.table[hc].is_marked():      # Was marked as deleted?
                    self.table[hc].unmark()         # Reset
                    self.deleted -= 1               # Adjust counts
                    self.N += 1
                return

            hc = (hc + 1) % self.M

        # With Open Addressing, you HAVE to insert first into the
        # empty bucket before checking whether you have hit
        # the threshold, otherwise you have to search again to
        # find an empty space. The impact is that this last entry
        # is "inserted twice" on resize; small price to pay. Note
        # That this last entry COULD be the last empty bucket, but
        # the forced resize below will resolve that issue
        self.table[hc] = MarkedEntry(k, v)
        self.N += 1

        if (self.N + self.deleted) >= self.threshold:
            self.resize(2*self.M + 1)
            hc = hash(k) % self.M

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if not entry is None and not entry.is_marked():
                yield (entry.key, entry.value)

def stats_open_addressing(words, table, output=False):
    """
    Produce statistics on the open addressing implemented table IF POSSIBLE.
    It may be that the table is not large enough for the provided words. 
    Returns (average chain length for non-empty buckets, max chain length)
    """
    original_size = len(table.table)
    for w in words:
        table.put(w, 1)

    size = len(table.table)
    sizes = {}                      # record how many chains of given size exist
    max_length = 0

    for idx in range(size):
        if table.table[idx]:

            # count to next empty entry. ASSUMES there will be one....
            i = idx
            num = 0
            while table.table[i]:
                i = (i + 1) % size
                num += 1
            
            if num in sizes:
                total = sizes[num] + 1
                sizes[num] = total
            else:
                sizes[num] = 1
                
            if num > max_length:
                max_length = num

    if output:
        print('Open Addressing ({} total entries in base size of {})'.format(words, original_size))
        for i in range(size):
            if i in sizes:
                print('{} entries have size of {}'.format(sizes[i], i))

    weighted_total = 0
    for i in sizes:
        weighted_total += i*sizes[i]

    return (weighted_total/len(words), max_length)