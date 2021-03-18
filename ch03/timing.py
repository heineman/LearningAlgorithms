"""Timing results for chapter 3."""
import timeit

from resources.english import english_words
from algs.table import DataTable, comma

def time_results_linked(output=True, decimals=3):
    """Average time to find a key in growing hashtable_open."""

    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    tbl = DataTable([8] + [8]*len(sizes), ['N'] + [comma(sz) for sz in sizes],
                    output=output, decimals=decimals)
    # Now start with M words to be added into a table of size N.
    # Start at 1000 and work up to 2000
    words = english_words()
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = words[:num_to_add]

        line = [num_to_add]
        for size in sizes:
            time1 = min(timeit.repeat(stmt='''
table = Hashtable({})
for word in words:
    table.put(word, 99)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
words={}'''.format(all_words), repeat=1, number=100))
            line.append(1000000*time1/size)
        tbl.row(line)
    return tbl
#######################################################################
if __name__ == '__main__':
    print('Average search Times with separate chaining hashtables (time in ns)')
    time_results_linked()
