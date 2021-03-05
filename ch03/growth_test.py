"""
Linked hashtable that also can grow or shrink.

Count how many times hashcode is computed (i.e., when % is invoked) on PUT.

>> TODO: Redo time_results_open using DataTable
>> >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

"""

import timeit
from ch03.entry import LinkedEntry

class DynamicHashtableLinkedCounting:
    """
    Instrumented Resizable Hashtable with Linked Lists to count the
    total number of times any entry is PUT into the Hashtable. This
    helps account for the costs of resizing.
    """
    def __init__(self, M=10):
        self.table = [None] * M
        if M < 1:
            raise ValueError('Hashtable storage must be at least 1.')
        self.M = M
        self.N = 0
        self.hash_count = 0

        self.load_factor = 0.75
        self.reduce_factor = 0.25
        self.threshold = M * self.load_factor
        self.reduce = M * self.reduce_factor

    def get(self, k):
        """Retrieve value associated with key, k."""
        hc = hash(k) % self.M       # First place it could be
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                return entry.value
            entry = entry.next
        return None                 # Couldn't find

    def put(self, k, v):
        """Associate value, v, with the key, k."""
        hc = hash(k) % self.M       # First place it could be
        self.hash_count += 1
        entry = self.table[hc]
        while entry:
            if entry.key == k:      # Overwrite if already here
                entry.value = v
                return
            entry = entry.next

        if self.N + 1 >= self.threshold:   # If this one puts you over edge
            self.resize(2*self.M + 1)
            hc = hash(k) % self.M
            self.hash_count += 1

        self.table[hc] = LinkedEntry(k, v, self.table[hc])
        self.N += 1

    def resize(self, new_size):
        """Resize table and rehash all existing entries into new table."""
        temp = DynamicHashtableLinkedCounting(new_size)
        for n in self.table:
            while n:
                temp.put(n.key, n.value)
                n = n.next
        self.table = temp.table
        self.hash_count += temp.hash_count  # don't forget to allocate these
        temp.table = None                   # ensures memory is freed
        self.M = temp.M
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

                if self.N < self.reduce:
                    self.resize(self.M // 2)

                return entry.value

            prev, entry = entry, entry.next

        return None                 # Nothing was removed

# Range from 63 to 190 when run, which reveals some of the unknowns that occur with hashing.
def probability_of_failure():
    """Produce report of failures resulting from collisions."""
    from ch03.months import key_array
    from ch03.hashtable import Hashtable

    failures = 0
    low = 100
    high = 1000
    for N in range(low, high):
        table = Hashtable(N)
        try:
            for day in key_array:
                table.put(day, 'ignore')
        except RuntimeError:
            failures += 1

    print('Out of', (high - low), 'attempts there were', failures, 'failures')

def run_trials():
    print('\nDict\tRaw\tBAS')
    m1 = min(timeit.repeat(stmt='days_in_month[s_data[2]]',
           setup='from ch03.months import s_data, days_in_month', repeat=10, number=100000))

    m2 = min(timeit.repeat(stmt='days_mixed(s_data[2])',
            setup='from ch03.months import s_data, days_mixed', repeat=10, number=100000))

    m3 = min(timeit.repeat(stmt='days_bas(s_data[2])',
            setup='from ch03.months import s_data, days_bas', repeat=10, number=100000))

    print('{0:.5f}\t{1:.5f}\t{2:.5f}'.format(m1, m2, m3))

def time_results_open(file):
    """Average time to find a key in growing hashtable_open."""
    print('open', end='')
    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    for s in sizes:
        print('\t' + str(s), end='')
    print()

    # Now start with M words to be added into a table of size N.
    # Start at 1000 and work up to 2000
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = []
        with open(file) as fp:
            for line in fp:
                line = line[:-1]  # eliminate final \n
                all_words.append(line)
                if len(all_words) >= num_to_add:
                    break

        line = str(len(all_words))
        for size in sizes:
            if num_to_add < size:
                m1 = min(timeit.repeat(stmt=f'''
table = Hashtable({size})
for word in {all_words}:
    table.put(word, 99)''', setup='from ch03.hashtable_open import Hashtable',repeat=1,number=100))
                line = line + "\t" + '{0:.4f}'.format((100000.0 * m1) / size)
            else:
                line = line + "\t*"
        print(line)

if __name__ == '__main__':
    probability_of_failure()
    run_trials()
