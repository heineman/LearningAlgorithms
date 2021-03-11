"""Stand-alone script to compare timing results with perfect hashing."""

import timeit
import random

from ch03.perfect.generated_dictionary import perfect_hash, G
from resources.english import english_words
from algs.table import DataTable

def simple_stats(words):
    """Generate stats on specific words from perfect hash structures."""
    print('G has',len(G),'entries.')
    for i in words:
        print(i, perfect_hash(i))

def compare_time(words, output=True, decimals=4):
    """Generate table of performance differences with linked hashtable and perfect hashing."""
    tbl = DataTable([8,8,8],['N', 'Linked', 'Perfect'], output=output, decimals=decimals)

    t_perfect = min(timeit.repeat(stmt='''
ht = HL()
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open_perfect import Hashtable as HL
words={}'''.format(words),
                repeat=3, number=5))/5

    t_linked = min(timeit.repeat(stmt='''
ht = HL(len(words))
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_linked import Hashtable as HL
words={}'''.format(words),
                repeat=3, number=5))/5

    tbl.row([len(words), t_linked, t_perfect])
    return tbl

#######################################################################
if __name__ == '__main__':
    ewords = english_words()
    simple_stats(ewords[:10])

    random.shuffle(ewords)
    compare_time(ewords)
