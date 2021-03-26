"""
Challenge Exercises for Chapter 3.
"""

import math
from algs.table import DataTable

class ValueBadHash:
    """
    Class with horrendous hash() method (just four possible values) to 
    ensure clashes.
    """
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return 'ValueBadHash({})'.format(self.v)

    def __hash__(self):
        """only four different values."""
        return hash(self.v) % 4

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.v == other.v)

def bad_timing(words, size=50000, output=True):
    """Statistics on hashtables."""
    from ch03.hashtable_linked import Hashtable, stats_linked_lists

    tbl = DataTable([8,10,10], ['Type', 'Avg. Len', 'Max Len'], output=output)
    tbl.format('Type', 's')
    tbl.format('Max Len', 'd')
    good_ht = Hashtable(size)
    bad_ht = Hashtable(size)

    for w in words:
        good_ht.put(w, True)
        bad_ht.put(ValueBadHash(w), True)

    good = stats_linked_lists(good_ht)
    tbl.row(['Good', good[0], good[1]])
    bad = stats_linked_lists(bad_ht)
    tbl.row(['Bad', bad[0], bad[1]])
    return tbl

def prime_number_difference(words, output=True, decimals=2):
    """Identify sensitivity of M to being prime or not."""

    from ch03.hashtable_linked import Hashtable as Linked_Hashtable, stats_linked_lists
    from ch03.hashtable_open import Hashtable as Open_Hashtable, stats_open_addressing
    from ch03.base26 import base26

    # these are prime numbers between 428880 and 428980
    lo = 428880
    primes = [428899, 428951, 428957, 428977]
    hi = 428980

    keys = [base26(w) for w in words]
    tbl = DataTable([12,6,8,8,8,8], ['M', 'Prime', 'Avg. LL', 'Max LL', 'Avg. OA', 'Max OA'],
                    output=output, decimals=decimals)
    tbl.format('Prime', 's')
    tbl.format('Max LL', 'd')
    tbl.format('Max OA', 'd')
    worst = 0
    worst_m = 0
    for m in range(lo, hi+1):
        is_p = 'Prime' if m in primes else ''
        ht_linked = Linked_Hashtable(m)
        ht_open = Open_Hashtable(m)

        for k in keys:
            ht_linked.put(k, 1)
            ht_open.put(k, 1)

        (avg_length_linked, max_length_linked) = stats_linked_lists(ht_linked)
        if max_length_linked > worst:
            worst_m = m
            worst = max_length_linked
        (avg_length_open, max_length_open) = stats_open_addressing(ht_open)
        tbl.row([m, is_p, avg_length_linked, max_length_linked, avg_length_open, max_length_open])

    # Now try to find any more that exceed this maximum amount
    if output:
        print('Worst was {} for M={}'.format(worst, worst_m))
        for m in range(worst_m, worst_m + 10000, 13):
            ht_linked = Linked_Hashtable(m)

            (avg_length_linked, max_length_linked) = stats_linked_lists(ht_linked, False)
            if max_length_linked > worst:
                worst_m = m
                worst = max_length_linked
                print('Worst of {} for M={}'.format(worst, worst_m))
        print('Done')

    return tbl

def measure_performance_resize(max_d=50, output=True):
    """Generate table of statistics for table resizing up to (but not including maxd=50)."""
    from ch03.hashtable_linked import DynamicHashtable
    from resources.english import english_words

    try:
        # Added in Python 3.7
        from time import time_ns
        timing = time_ns
    except ImportError:
        from time import time
        timing = time

    if output:
        print('Dynamic Resizing Hashtable')
    tbl = DataTable([8, 15, 15, 10, 10], ['idx', 'word', 'time', 'old-size', 'new-size'],
                    output=output, decimals=2)
    tbl.format('idx', 'd')
    tbl.format('word', 's')
    tbl.format('old-size', ',d')
    tbl.format('new-size', ',d')

    ht = DynamicHashtable(1023)
    idx = 1
    last = None
    average = 0
    words = english_words()
    for w in words:
        before = timing()
        old_size = len(ht.table)
        ht.put(w,w)
        new_size = len(ht.table)
        after = timing()
        average += (after-before)
        if last:
            if after - before > last:
                last = after-before
                tbl.row([idx,w,last,old_size,new_size])
        else:
            last = after-before
        idx += 1

    average /= len(words)
    ht = None
    if output:
        print('Average was ', average)
        print('Incremental Resizing Hashtable')

    tbl_ir = DataTable([8, 15, 15, 10, 10], ['idx', 'word', 'time', 'old-size', 'new-size'],
                       output=output, decimals=2)
    tbl_ir.format('idx', 'd')
    tbl_ir.format('word', 's')
    tbl_ir.format('old-size', ',d')
    tbl_ir.format('new-size', ',d')
    ht = DynamicHashtableIncrementalResizing(1023,10)
    idx = 1
    last = None
    average = 0
    words = english_words()
    for w in words:
        before = timing()
        old_size = len(ht.table)
        ht.put(w,w)
        new_size = len(ht.table)
        after = timing()
        average += (after-before)
        if last:
            if after - before > last:
                last = after-before
                tbl_ir.row([idx,w,last,old_size,new_size])
        else:
            last = after-before
        idx += 1

    ht = None

    average /= len(words)
    if output:
        print('Average was ', average)
        print('Incremental Resizing dependent on Delta')
        print()

    tbl_d = DataTable([8,10],['Delta', 'Average'], output=output)
    tbl_d.format('Delta', 'd')
    for delta in range(1, max_d):
        ht = DynamicHashtableIncrementalResizing(1023, delta)
        average = 0
        words = english_words()
        for w in words:
            before = timing()
            ht.put(w,w)
            after = timing()
            average += (after-before)

        average /= len(words)
        #print (delta,'Average is', average)
        tbl_d.row([delta, average])

    return (tbl, tbl_ir, tbl_d)

class DynamicHashtableIncrementalResizing:
    """
    Hashtable that supports incremental resizing.

    Performance is still limiting because of (a) costs when allocating
    very large array; and (b) when rehashing existing values, you will
    eventually have to search through very large array for next
    non-empty bucket.
    """
    def __init__(self, M=10, delta=1):
        self.table = [None] * M
        self.old_table = None
        if M < 1:
            raise ValueError('Hashtable storage must be at least 1.')
        if delta < 1:
            raise ValueError('delta must be at least 1 since growth factor is 2*M+1')
        self.M = M
        self.N = 0
        self.delta = delta
        self.last_idx = 0
        self.old_M = 0

        self.load_factor = 0.75

        # Ensure resize event happens NO LATER than M-1, to align
        # with open addressing
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        """
        Retrieve value associated with key, k. Must check old table
        if not present in the new table.
        """
        h = hash(k)
        hc = h % self.M       # First place it could be
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                return entry.value
            entry = entry.next

        # if old table, might be there
        if self.old_table:
            hc_old = h % self.old_M
            entry = self.old_table[hc_old]
            while entry:
                if entry.key == k:
                    return entry.value
                entry = entry.next

        return None                 # Couldn't find

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        h = hash(k)
        hc = h % self.M       # First place it could be
        entry = self.table[hc]
        while entry:
            if entry.key == k:      # Overwrite if already here
                entry.value = v
                return
            entry = entry.next

        if self.old_table:
            hc_old = h % self.old_M
            entry = self.old_table[hc_old]
            while entry:
                if entry.key == k:  # Overwrite if already here
                    entry.value = v
                    return
                entry = entry.next

        # insert, and then trigger resize if hit threshold.
        from ch03.entry import LinkedEntry
        self.table[hc] = LinkedEntry(k, v, self.table[hc])
        self.N += 1

        if self.N >= self.threshold:
            self.resize(2*self.M + 1)
        else:
            # after every put() move over delta values as well.
            if self.old_table:
                self.move_r()

    def move_r(self):
        """
        Incrementally move self.delta entries from old to new table. Should the old
        table become empty of entries, set self.old_table to None.
        """
        num_to_move = self.delta
        while num_to_move > 0 and self.last_idx < self.old_M:
            moving_entry = self.old_table[self.last_idx]
            if moving_entry is None:
                self.last_idx += 1
            else:
                while moving_entry and num_to_move > 0:
                    idx = hash(moving_entry.key) % self.M
                    self.old_table[self.last_idx] = moving_entry.next
                    moving_entry.next = self.table[idx]
                    self.table[idx] = moving_entry

                    moving_entry = self.old_table[self.last_idx]
                    num_to_move -= 1

        if self.last_idx == self.old_M:
            self.old_table = None

    def resize(self, new_size):
        """Resize table to prepare for new entries, but none are moved."""
        # prepare for incremental resizing by recording old_M
        # and recording where we will be sweeping entries from.
        self.last_idx = 0
        self.old_M = self.M
        self.M = new_size

        self.old_table = self.table
        self.table = [None] * self.M

        self.threshold = self.load_factor * self.M

    def remove(self, k):
        """Remove (k,v) entry associated with k."""
        hc = hash(k) % self.M       # First place it could be
        entry = self.table[hc]
        prev = None
        while entry:
            if entry.key == k:
                if prev:
                    prev.next = entry.next
                else:
                    self.table[hc] = entry.next
                self.N -= 1
                return entry.value

            prev, entry = entry, entry.next

        return None                 # Nothing was removed

class PythonSimultationHashtable:
    # highly tuned constant
    PERTURB_SHIFT = 5
    
    """Simulate Open Addressing Hashtable in Python."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 8:
            M = 8
        else:
            M = 2 ** int(math.log(M)/math.log(2))
        self.M = M
        self.N = 0

        self.load_factor = 0.75

        # Ensure resize event happens NO LATER than M-1, since you need at
        # least one empty bucket
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        """Retrieve value associated with key, k."""
        perturb = hash(k)
        hc = perturb & (self.M-1)       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            perturb >>= PythonSimultationHashtable.PERTURB_SHIFT
            hc = (hc*5 + perturb + 1) & (self.M-1)
        return None                 # Couldn't find

    def resize(self, new_size):
        """Resize table and rehash existing entries into new table."""
        temp = PythonSimultationHashtable(new_size)
        for n in self.table:
            if n:
                temp.put(n.key, n.value)
        self.table = temp.table
        temp.table = None     # ensures memory is freed
        self.M = temp.M
        self.threshold = self.load_factor * self.M

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        perturb = hash(k)
        hc = perturb & (self.M-1)       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                return
            perturb >>= PythonSimultationHashtable.PERTURB_SHIFT
            hc = (hc*5 + perturb + 1) & (self.M-1)

        # With Open Addressing, you HAVE to insert first into the
        # empty bucket before checking whether you have hit
        # the threshold, otherwise you have to search again to
        # find an empty space. The impact is that this last entry
        # is "inserted twice" on resize; small price to pay. Note
        # That this last entry COULD be the last empty bucket, but
        # the forced resize below will resolve that issue
        from ch03.entry import Entry
        self.table[hc] = Entry(k, v)
        self.N += 1

        if self.N >= self.threshold:
            self.resize(2*self.M)
            hc = hash(k) & (self.M-1)

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if entry:
                yield (entry.key, entry.value)
                
def compare_python_hashtable():
    """Compare statistics from simulated Python Hashtable vs. existing Hashtable."""
    import timeit
    
    build_dhl = min(timeit.repeat(stmt='''
ht = DynamicHashtable(8)
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open import DynamicHashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

    build_phl = min(timeit.repeat(stmt='''
pht = PythonSimultationHashtable(8)
for w in words:
    pht.put(w,w)''', setup='''
from ch03.challenge import PythonSimultationHashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5
    
    print('Open addressing Simulation build time:', build_dhl)
    print('Python addressing HT build time:', build_phl)
    
    
compare_python_hashtable()
# pht = PythonSimultationHashtable(8)
# 
# from resources.english import english_words
# for w in english_words():
#     pht.put(w, 1)
#     print(w)