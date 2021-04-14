"""
Challenge Exercises for Chapter 3.
"""

import math
import sys
import time
import timeit

from algs.table import DataTable, ExerciseNum, caption
from ch03.entry import Entry, LinkedEntry

class HashtableTriangleNumbers:
    """Open Addressing Hashtable using Triangle Number probing. make sure M is power of 2."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 2:
            raise ValueError('HashtableTriangleNumbers must contain space for at least two (key, value) pairs.')
        exp = int(math.log2(M))

        if M != 2 ** exp:
            raise ValueError('HashtableTriangleNumbers requires M to be a power of 2.') 

        self.M = M
        self.N = 0

    def get(self, k):
        """Retrieve value associated with key, k, using delta=Tn probing."""
        hc = hash(k) % self.M       # First place it could be
        delta = 0
        idx = 0
        while self.table[hc]:
            idx += 1
            if self.table[hc].key == k:
                return self.table[hc].value
            delta += idx
            hc = (hc + delta) % self.M
        return None                 # Couldn't find

    def is_full(self):
        """Determine if Hashtable is full."""
        return self.N >= self.M - 1

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        delta = 0
        idx = 0
        while self.table[hc]:
            idx += 1
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                return
            delta += idx
            hc = (hc + delta) % self.M

        if self.N >= self.M - 1:
            raise RuntimeError('Table is Full: cannot store {} -> {}'.format(k, v))

        self.table[hc] = Entry(k, v)
        self.N += 1

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if entry:
                yield (entry.key, entry.value)

class ValueBadHash:
    """
    Class with horrendous hash() method (just four possible values) to
    ensure clashes.
    """
    def __init__(self, v):
        self.v = v

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

class PythonSimulationHashtable:
    """
    Simulate Open Addressing Hashtable in Python.
    Because we are not using modulo (%) but & (bitwise and) we have to make
    sure that the computed hash(k) is positive. If it becomes negative,
    the the while loops may not complete, among other disasters.
    
    To prevent this, simply use bitwise and (&) with each hash() invocation
    """

    # highly tuned constant
    PERTURB_SHIFT = 5

    def __init__(self, M=10):
        if M < 8:
            M = 8
        else:
            M = 2 ** int(math.log(M)/math.log(2))
        self.table = [None] * M
        self.M = M
        self.N = 0

        self.load_factor = 0.75

        # Ensure resize event happens NO LATER than M-1, since you need at
        # least one empty bucket
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        """Retrieve value associated with key, k."""
        perturb = hash(k) & sys.maxsize
        hc = perturb & (self.M-1)       # First place it could be
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            perturb >>= PythonSimulationHashtable.PERTURB_SHIFT
            hc = (hc*5 + perturb + 1) & (self.M-1)
        return None                 # Couldn't find

    def resize(self, new_size):
        """Resize table and rehash existing entries into new table."""
        temp = PythonSimulationHashtable(new_size)
        for n in self.table:
            if n:
                temp.put(n.key, n.value)
        self.table = temp.table
        temp.table = None     # ensures memory is freed
        self.M = temp.M
        self.threshold = self.load_factor * self.M

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        perturb = hash(k) & sys.maxsize
        hc = perturb & (self.M-1)       # First place it could be

        while self.table[hc]:
            if self.table[hc].key == k:     # Overwrite if already here
                self.table[hc].value = v
                return
            perturb >>= PythonSimulationHashtable.PERTURB_SHIFT
            hc = (hc*5 + perturb + 1) & (self.M-1)
        
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
            self.resize(2*self.M)

    def __iter__(self):
        """Generate all (k, v) tuples for actual (i.e., non-deleted) entries."""
        for entry in self.table:
            if entry:
                yield (entry.key, entry.value)

def compare_python_hashtable():
    """Compare statistics from simulated Python Hashtable vs. existing Hashtable."""
    
    build_dhl = min(timeit.repeat(stmt='''
ht = DynamicHashtable(8)
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open import DynamicHashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

    build_phl = min(timeit.repeat(stmt='''
pht = PythonSimulationHashtable(8)
for w in words:
    pht.put(w,w)''', setup='''
from ch03.challenge import PythonSimulationHashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

    print('Open addressing Simulation build time:', build_dhl)
    print('Python addressing HT build time:', build_phl)

def exercise_triangle_number_probing(output=True, decimals=4):
    """Compare triangle number probing with M=powers of 2."""
    
    tbl = DataTable([20,8], ['Type', 'Time to Search'], output=output, decimals=decimals)
    tbl.format('Type', 's')
    timing_oa = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch03.hashtable_open import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable(524288)
for w in words[:160564]:
    ht.put(w,w)''', repeat=7, number=5))/5
    tbl.row(['Open Addressing', timing_oa])
    
    timing_sc = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch03.hashtable_linked import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable(524288)
for w in words[:160564]:
    ht.put(w,w)''', repeat=7, number=5))/5
    tbl.row(['Separate Chaining', timing_sc])
    
    timing_tn = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch03.challenge import HashtableTriangleNumbers
from resources.english import english_words
words = english_words()
ht = HashtableTriangleNumbers(524288)
for w in words[:160564]:
    ht.put(w,w)''', repeat=7, number=5))/5
    tbl.row(['Triangle Probing', timing_tn])

class HashtableSortedLinkedLists:
    """Hashtable using array of M linked lists where keys appear in sorted order."""
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable storage must be at least 1.')
        self.M = M
        self.N = 0

    def get(self, k):
        """Retrieve value associated with key, k. STOP when entry is bigger than key."""
        hc = hash(k) % self.M       # First place it could be
        entry = self.table[hc]
        while entry:
            if entry.key > k:     # Doesn't exist since keys in sorted order
                return None
            if entry.key == k:
                return entry.value
            entry = entry.next
        return None                 # Couldn't find

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        entry = self.table[hc]
        if entry is None:
            self.N = 1
            self.table[hc] = LinkedEntry(k, v, self.table[hc])
            return 

        prev = None
        while entry:
            if entry.key > k:       # Can insert since we didn't find
                self.N += 1
                if prev is None:    # new First
                    self.table[hc] = LinkedEntry(k, v, entry)            
                else:
                    prev.next = LinkedEntry(k, v, entry)
                return

            if entry.key == k:      # Overwrite if already here
                entry.value = v
                return
            
            prev = entry
            entry = entry.next

        # If we get here, key is largest among all, so append to end
        prev.next = LinkedEntry(k, v)
        self.N += 1

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

    def __iter__(self):
        """Generate all (k, v) tuples for entries in all linked lists table."""
        for entry in self.table:
            while entry:
                yield (entry.key, entry.value)
                entry = entry.next

def evaluate_hashtable_sorted_chains(output=True, decimals=4):
    """Evaluate performance of separate chaining Hashtable with sorted entries."""

    print('Best Case Build Time')
    tbl = DataTable([8,20,20,20], ['M', 'Open Addressing', 'Separate Chaining', 'Sorted Chains'], output=output, decimals=decimals)

    for size in [214129, 524287, 999983]:
        timing_oa = min(timeit.repeat(stmt='''
ht = Hashtable({})
for w in reversed(words[:160564]):
    ht.put(w,w)'''.format(size), setup='''
from ch03.hashtable_open import Hashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

        timing_sc = min(timeit.repeat(stmt='''
ht = Hashtable({})
for w in reversed(words[:160564]):
    ht.put(w,w)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

        timing_sorted = min(timeit.repeat(stmt='''
ht = HashtableSortedLinkedLists({})
for w in reversed(words[:160564]):
    ht.put(w,w)'''.format(size), setup='''
from ch03.challenge import HashtableSortedLinkedLists
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5
        tbl.row([size, timing_oa, timing_sc, timing_sorted])

    print('Worst Case Build Time')
    tbl = DataTable([8,20,20,20], ['M', 'Open Addressing', 'Separate Chaining', 'Sorted Chains'], output=output, decimals=decimals)

    for size in [214129, 524287, 999983]:
        timing_oa = min(timeit.repeat(stmt='''
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), setup='''
from ch03.hashtable_open import Hashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5

        timing_sc = min(timeit.repeat(stmt='''
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5
       
        timing_sorted = min(timeit.repeat(stmt='''
ht = HashtableSortedLinkedLists({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), setup='''
from ch03.challenge import HashtableSortedLinkedLists
from resources.english import english_words
words = english_words()''', repeat=7, number=5))/5
        tbl.row([size, timing_oa, timing_sc, timing_sorted])
    
    print('Search First Half')
    tbl = DataTable([8,20,20,20], ['M', 'Open Addressing', 'Separate Chaining', 'Sorted Chains'], output=output, decimals=decimals)
    
    for size in [214129, 524287, 999983]:
        search_oa = min(timeit.repeat(stmt='''
for w in words[:160564]:
    ht.get(w)''', setup='''
from ch03.hashtable_open import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5

        search_sc = min(timeit.repeat(stmt='''
for w in words[:160564]:
    ht.get(w)''', setup='''
from ch03.hashtable_linked import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5

        search_sorted = min(timeit.repeat(stmt='''
for w in words[:160564]:
    ht.get(w)''', setup='''
from ch03.challenge import HashtableSortedLinkedLists
from resources.english import english_words
words = english_words()
ht = HashtableSortedLinkedLists({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5
        tbl.row([size, search_oa, search_sc, search_sorted])
        
    print('Search Back Half')
    tbl = DataTable([8,20,20,20], ['M', 'Open Addressing', 'Separate Chaining', 'Sorted Chains'], output=output, decimals=decimals)
    
    for size in [214129, 524287, 999983]:
        search_oa = min(timeit.repeat(stmt='''
for w in words[160564:]:
    ht.get(w)''', setup='''
from ch03.hashtable_open import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5

        search_sc = min(timeit.repeat(stmt='''
for w in words[160564:]:
    ht.get(w)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
from resources.english import english_words
words = english_words()
ht = Hashtable({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5

        search_sorted = min(timeit.repeat(stmt='''
for w in words[160564:]:
    ht.get(w)''', setup='''
from ch03.challenge import HashtableSortedLinkedLists
from resources.english import english_words
words = english_words()
ht = HashtableSortedLinkedLists({})
for w in words[:160564]:
    ht.put(w,w)'''.format(size), repeat=7, number=5))/5
        tbl.row([size, search_oa, search_sc, search_sorted])

def flip_every_k(ht, k, n):
    """Starting from 1 to n in steps of k, flip every one."""
    for i in range(0, n, k):
        if ht.get(i):
            ht.remove(i)
        else:
            ht.put(i,i+1)

def evaluate_DynamicHashtablePlusRemove(output=True):
    """
    Compare performance using ability in open addressing to mark deleted values.
    Nifty trick to produce just the squares as keys in the hashtable.
    """
    # If you want to compare, then add following to end of executable statements:
    #    print([e[0] for e in ht])
    
    tbl = DataTable([8,20,20], ['M', 'Separate Chaining', 'Open Addressing w/ Remove'], output=output)
    for size in [512, 1024, 2048]:
        linked_list = min(timeit.repeat(stmt='''
ht = Hashtable({0})
N = {0} // 4
for i in range(1, N, 1):
    flip_every_k(ht, i, N)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
from ch03.challenge import flip_every_k'''.format(size), repeat=7, number=5))/5
    
        hashtable_plus = min(timeit.repeat(stmt='''
ht = DynamicHashtablePlusRemove({0})
N = {0} // 4
for i in range(1, N, 1):
    flip_every_k(ht, i, N)'''.format(size), setup='''
from ch03.hashtable_open import DynamicHashtablePlusRemove
from ch03.challenge import flip_every_k'''.format(size), repeat=7, number=5))/5
        tbl.row([size, linked_list, hashtable_plus])
    return tbl

def count_hash_incremental_move(output=True, decimals=4):
    """
    For all English words, starting with a hashtable of size 1,024 and
    a load factor of 0.75, count how many times the hash code (i.e., %)
    is invoked.
    """
    from ch03.book import CountableHash
    from resources.english import english_words
    from ch03.hashtable_linked import DynamicHashtable

    print('Each emitted row contains an operation more costly than any before...')
    ht_dynamic = DynamicHashtable(1023)
    tbl = DataTable([20,10,10],['Word', 'N', 'cost'],
                    output=output, decimals=decimals)
    tbl.format('Word', 's')
    tbl.format('N', ',d')

    max_cost = 0
    now = time.time()
    for w in english_words():
        before = time.time()
        ht_dynamic.put(CountableHash(w), w)
        cost = time.time() - before
        if cost > max_cost:
            max_cost = cost
            tbl.row([w, ht_dynamic.N, cost])
    total_normal = time.time() - now
    print('Normal:{}'.format(total_normal))

    for delta in [512, 256, 128, 64, 32, 16, 8, 4]:
        ht = DynamicHashtableIncrementalResizing(1023, delta=delta)
       
        tbl = DataTable([20,10,10],['Word', 'N', 'cost'],
                        output=output, decimals=decimals)
        tbl.format('Word', 's')
        tbl.format('N', ',d')
    
        max_cost = 0
        now =  time.time()
        for w in english_words():
            before = time.time()
            ht.put(CountableHash(w), w)
            cost = time.time() - before
            if cost > max_cost:
                max_cost = cost
                tbl.row([w, ht.N, cost])
        total_delta = time.time() - now
        print('delta={}, Normal:{}'.format(delta, total_delta))
    
#######################################################################
if __name__ == '__main__':
    chapter = 3
    count_hash_incremental_move()
    
    with ExerciseNum(1) as exercise_number:
        exercise_triangle_number_probing()
        print(caption(chapter, exercise_number),
              'Fragment evaluation')

    with ExerciseNum(2) as exercise_number:
        evaluate_hashtable_sorted_chains()
        print(caption(chapter, exercise_number),
              'Hashtable with sorted linked list chains')
    
    with ExerciseNum(3) as exercise_number:
        bad_timing()
        print(caption(chapter, exercise_number),
              'ValueBadHash exercise')
    
    with ExerciseNum(4) as exercise_number:
        from resources.english import english_words
        prime_number_difference(english_words())
        print(caption(chapter, exercise_number),
              'Prime Number exercise')
        
    with ExerciseNum(5) as exercise_number:
        evaluate_DynamicHashtablePlusRemove
        print(caption(chapter, exercise_number),
              'Open Addressing with Marked Elements as deleted.')
        
    with ExerciseNum(6) as exercise_number:
        count_hash_incremental_move()
        print(caption(chapter, exercise_number),
              'Compare incremental resize strategy against geometric resizing.')
