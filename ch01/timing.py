"""Timing results for chapter 1.

Compute whether crossover occurs between tournament_VARIATION() and sorting_two()

Turns out that sorting is just too fast, and all other approaches are slowed
down by extra space requirements. Note the subtle problem with tournament_object
which ends up being an O(N^2) algorithm because of the costs in the del tourn[0:2]
operation.

"""

import timeit
from algs.table import DataTable, SKIP

def timing_trial(output=True, decimals=3):
    """
    Seek possible crossover between tournament_two() and sorting_two().
    Because of the high memory demands, tournament_two() is always slower than
    sorting_two().
    """
    tbl = DataTable([8,8,8,8,8,8], ['N', 'Sorting', 'Tournament', 'Tourn. Object', 'Tourn. Linked', 'Tourn. Losers'], output=output, decimals=decimals)

    for n in [2 ** k for k in range(10, 24)]:
        st_time = timeit.timeit(stmt='sorting_two(x)', setup='''
import random
from ch01.largest_two import sorting_two
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), number=1)

        tt_time = timeit.timeit(stmt='tournament_two(x)', setup='''
import random
from ch01.largest_two import tournament_two
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), number=1)

        if n > 1048576:
            tto_time = SKIP
        else:
            tto_time = timeit.timeit(stmt='tournament_two_object(x)', setup='''
import random
from ch01.largest_two import tournament_two_object
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), number=1)

        ttl_time = timeit.timeit(stmt='tournament_two_losers(x)', setup='''
import random
from ch01.largest_two import tournament_two_losers
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), number=1)

        ttll_time = timeit.timeit(stmt='tournament_two_linked(x)', setup='''
import random
from ch01.largest_two import tournament_two_linked
random.seed({0})
x=list(range({0}))
random.shuffle(x)'''.format(n), number=1)

        tbl.row([n, st_time, tt_time, tto_time, ttll_time, ttl_time])
    return tbl

#######################################################################
if __name__ == '__main__':

    print('Does tournament_two() beat sorting_two().')
    timing_trial()
