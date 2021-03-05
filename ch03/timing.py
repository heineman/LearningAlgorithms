"""Timing results for chapter 3."""
import timeit

from resources.english import english_words

def compare_constant_time():
    """Generate table of performance to access constants."""
    print('\nCompute\tSearch')
    m1 = min(timeit.repeat(stmt='''
ct = 0
for day in s_data:
    ct += computed[ord(day[1]) + ord(day[2]) - 199]
''', setup='from ch03.months import computed,s_data', repeat=10, number=100000))

    m2 = min(timeit.repeat(stmt='''
ct = 0
for day in s_data:
    idx = s_data.index(day)
    ct += s_num[idx]
''', setup='from ch03.months import computed,s_data,s_num,monthIndex', repeat=10, number=100000))

    print('{0:.5f}\t{1:.5f}'.format(m1, m2))

def timeResults_linked(words):
    """Average time to find a key in growing hashtable_open."""
    print('link', end='')
    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    for s in sizes:
        print('\t' + str(s), end='')
    print()

    # Now start with M words to be added into a table of size N.
    # Start at 1000 and work up to 2000
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = words[:num_to_add]

        line = str(len(all_words))
        for size in sizes:

            m1 = min(timeit.repeat(stmt=f'''
table = Hashtable({size})
for word in {all_words}:
    table.put(word, 99)''', setup='from ch03.hashtable_linked import Hashtable',
                            repeat=1, number=100))
            line = line + "\t" + '{0:.4f}'.format((100000.0*m1)/size)
        print(line)

#######################################################################
if __name__ == '__main__':
    print()
    timeResults_linked(english_words())
    print()

    # the following *SHOULDN'T* cause an exception but it still might because of collisions
    from ch03.hashtable import Hashtable
    table = Hashtable(100)
    try:
        table.put('April', 30)
        table.put('May', 31)
        table.put('September', 30)

        print(table.get('August'), 'should be None')
        print(table.get('September'), 'should be 30')
    except RuntimeError as ex:
        print('RuntimeError could happen: {0}'.format(ex))

    compare_constant_time()
