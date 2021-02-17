"""
    Hashtable to store (key, value) pairs in a fixed hashtable using hash() % N as hash code.
    This table can replace values associated with a given key.  When two keys attempt to use
    the same location, OPEN ADDRESSING resolves the conflict.

    Always leaves at least ONE empty spot so code is simpler
"""

from ch03.entry import Entry

class Hashtable:
    """Open Addressing Hashtable."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable must contain at least one (key, value) pair.')
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

class DynamicHashtable:
    """Open Addressing Hashtable that supports resizing."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable must contain at least one (key, value) pair.')
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

class DynamicHashtablePlusRemove:
    """
    Supports removal of entries, which causes numerous little changes
    throughout the class.

    Note that table_entries_filter_deleted() properly filters out all
    entries that had been deleted.
    """
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable must contain at least one (key, value) pair.')
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
        temp = DynamicHashtable(new_size)
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

                self.table[hc].mark()             # record its been deleted
                self.N -= 1
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
                if not self.table[hc].is_marked():  # Weren't deleted?
                    self.table[hc].unmark()         # Return now
                return

            hc = (hc + 1) % self.M

        if (self.N + self.deleted) >= self.threshold:
            self.resize(2*self.M + 1)
            hc = hash(k) % self.M

        self.table[hc] = Entry(k, v)
        self.N += 1

def table_entries_filter_deleted(ht):
    """Generate all (k, v) tuples for entries in DynamicHashtablePlusRemove."""
    for entry in ht.table:
        if not entry is None and not entry.is_marked():
            yield (entry.key, entry.value)

def table_entries(ht):
    """Generate all (k, v) tuples for entries in the table."""
    for entry in ht.table:
        if not entry is None:
            yield (entry.key, entry.value)

def stats_open_addressing(words, table, output=False):
    """Produce stats on the table for open addressing IF POSSIBLE."""
    original_size = len(table.table)
    for w in words:
        table.put(w, 1)

    size = len(table.table)
    sizes = {}                      # record how many chains of given size exist
    total_search = 0
    max_length = 0

    for idx in range(size):
        if table.table[idx]:

            # compute hash code for entry found there AND see how far away it is from where
            # it should have been. Anything more than 1 shows the inherent inefficiencies
            start = hash(table.table[idx].key) % size
            num = 1

            if start == idx:
                num = 1              # in proper location
            elif start > idx:        # wrap around!
                num = (size - start) + idx
            else:
                num = idx - start + 1
            total_search += num      # each entry in the linked list requires more searches to find

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

    return ((1.0*total_search) / len(words), max_length)
