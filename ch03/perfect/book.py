"""
How many unused indices in G are there for the perfect hash?
"""

from ch03.perfect.generated_dictionary import G
from algs.table import comma

def count_unused():
    """Count unused entries in G."""
    count = 0
    for _,val in enumerate(G):
        if val == 0:
            count += 1
    print('From G which has', comma(len(G)), 'entries', comma(count),
          'of them are zero ({:.2f}%)'.format(100*count/len(G)))

#######################################################################
if __name__ == '__main__':
    count_unused()
