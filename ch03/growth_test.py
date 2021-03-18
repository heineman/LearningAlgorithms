"""
Linked hashtable that also can grow or shrink.

Count how many times hashcode is computed (i.e., when % is invoked) on PUT.
"""
import timeit
from algs.table import DataTable, SKIP

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

def run_access_trials(max_trials=100000, output=True, decimals=5):
    """Generate performance table for up to max_trials number of runs."""
    tbl = DataTable([10,10,10], ['Dict', 'Raw', 'BAS'], output=output, decimals=decimals)
    tbl.format('Dict', 'f')

    m1 = min(timeit.repeat(stmt='days_in_month[s_data[2]]',
           setup='from ch03.months import s_data, days_in_month', repeat=10, number=max_trials))

    m2 = min(timeit.repeat(stmt='days_mixed(s_data[2])',
            setup='from ch03.months import s_data, days_mixed', repeat=10, number=max_trials))

    m3 = min(timeit.repeat(stmt='days_bas(s_data[2])',
            setup='from ch03.months import s_data, days_bas', repeat=10, number=max_trials))
    tbl.row([m1,m2,m3])
    return tbl

def time_results_open(words, output=True, decimals=4):
    """Average time to find a key in growing hashtable_open."""
    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    widths = [8] + [10] * len(sizes)
    headers = ['N'] + sizes
    tbl = DataTable(widths, headers, output=output, decimals=decimals)

    # Now start with N words to be added into a table of size M.
    # Start at 1000 and work up to 2000
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = words[:num_to_add]

        arow = [num_to_add]
        for size in sizes:
            if num_to_add < size:
                m1 = min(timeit.repeat(stmt='''
table = Hashtable({})
for word in words:
    table.put(word, 99)'''.format(size), setup='''
from ch03.hashtable_open import Hashtable
words={}'''.format(all_words), repeat=1, number=100))
                arow.append((100000.0 * m1) / size)
            else:
                arow.append(SKIP)
        tbl.row(arow)
    return tbl

#######################################################################
if __name__ == '__main__':
    probability_of_failure()
