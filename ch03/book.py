"""Tables for Chapter 3.

"""
import timeit
from algs.table import DataTable, captionx, SKIP, comma, process, TableNum, FigureNum
from resources.english import english_words
from ch03.base26 import search_for_base

def generate_hash():
    """Results are different each time since Python salts hash values."""

    s = 'a rose by any other name would smell as sweet'
    tbl = DataTable([8,20,20], ['key', 'hash(key)', 'hash(key) % 15'])
    tbl.format('key', 's')
    tbl.format('hash(key)', 'd')
    tbl.format('hash(key) % 15', 'd')
    for w in s.split():
        tbl.row([w, hash(w), hash(w) % 15])
    return tbl

def readable_table(ht):
    """Return string representing keys in hashtable."""
    return ' '.join([(' -' if s is None else str(s.key)) for s in ht.table])

def sample_hashtable():
    """Generate Figure output."""
    from ch03.hashtable_open import Hashtable
    ht = Hashtable(6)
    vals = [20, 15, 12, 19, 14]
    for i,v in enumerate(vals):
        ht.put(v, 'e{}'.format(i))
        print(readable_table(ht),'        {} % {} = {}'.format(vals[i], ht.M, vals[i] % ht.M))

def time_results_open_addressing():
    """Average time to insert a key in growing hashtable_open (in microseconds)."""
    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    headers = [comma(s) for s in sizes]
    headers.insert(0,'N')
    tbl = DataTable([8,8,8,8,8,8,8,8,10], headers, decimals=3)

    # Now start with M words to be added into a table of size N.
    # Start at 1000 and work up to 2000
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]:
        all_words = english_words()[:num_to_add]

        line = [len(all_words)]
        for size in sizes:
            try:
                tbl.format(comma(size), '.3f')
                t1 = min(timeit.repeat(stmt=f'''
table = Hashtable({size})
for word in {all_words}:
    table.put(word, 99)''', setup='from ch03.hashtable_open import Hashtable',repeat=1,number=100))
                t1 = (100000.0 * t1) / size
            except RuntimeError:
                t1 = SKIP

            line.append(t1)
        tbl.row(line)
    return tbl

def count_collisions_dynamic():
    """Generate data counting collisions for dynamic hashtables."""
    all_words = english_words()
    # start twice as big as the number of words, and reduce steadily, counting collisions
    N = len(all_words)
    M = 2*N

    from ch03.hashtable_linked import DynamicHashtable as DHL
    from ch03.hashtable_linked import stats_linked_lists
    from ch03.hashtable_open import DynamicHashtable as ODHL
    from ch03.hashtable_open import stats_open_addressing

    tbl = DataTable([10,8,8,8,8], ['M', 'Avg LL', 'Max LL', 'Avg OA', 'Max OA'], decimals=2)
    tbl.format('Max LL', 'd')
    tbl.format('Max OA', 'd')
    while M > N/16:
        avg_size_linked_dynamic = stats_linked_lists(all_words, DHL(M), False)
        avg_size_open_dynamic = ('-','-')
        avg_size_open_dynamic = stats_open_addressing(all_words, ODHL(M), False)

        tbl.row([M, avg_size_linked_dynamic[0], avg_size_linked_dynamic[1],
                 avg_size_open_dynamic[0], avg_size_open_dynamic[1]])

        # Start with one ten times as big, then drop down to 2*N
        if M > N:
            M = (M * 95) // 100
        else:
            M = (M * 6) // 10
    return tbl

def count_collisions():
    """Generate table counting collisions."""
    all_words = english_words()
    # start twice as big as the number of words, and reduce steadily, counting collisions
    N = len(all_words)
    M = 2*N

    from ch03.hashtable_linked import Hashtable as HL
    from ch03.hashtable_linked import stats_linked_lists
    from ch03.hashtable_open import Hashtable as OHL
    from ch03.hashtable_open import stats_open_addressing

    tbl = DataTable([10,8,8,8,8], ['M', 'Avg LL', 'Max LL', 'Avg OA', 'Max OA'], decimals=2)
    tbl.format('Max LL', 'd')
    tbl.format('Max OA', 'd')
    while M > N/16:
        avg_size_linked = stats_linked_lists(all_words, HL(M), False)
        if N < M:
            avg_size_open = stats_open_addressing(all_words, OHL(M), False)
        else:
            tbl.format('Avg OA', 's')
            tbl.format('Max OA', 's')
            avg_size_open = ['N/A', 'N/A']

        tbl.row([M, avg_size_linked[0], avg_size_linked[1], avg_size_open[0], avg_size_open[1]])

        # Once below threshold, go down at 60% clip
        if M > N:
            M = (M * 95) // 100
        else:
            M = (M * 6) // 10
    return tbl

def compare_dynamic_build_and_access_time():
    """Generate tables for build and access times."""
    repeat = 25
    num = 10

    # When 'ht = HTLL(...) is inside the STMT, it measures BUILD TIME.
    # When it is included in the setup, we are measuring ACCESS TIME.
    print('build LL')
    ll_build = min(timeit.repeat(stmt='''
ht = HTLL(428221)
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_linked import Hashtable as HTLL
from resources.english import english_words
words = english_words()''', repeat=repeat, number=num))/num

    print('Access LL')
    ll_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch03.hashtable_linked import Hashtable as HTLL
from resources.english import english_words
ht = HTLL(428221)
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

    print('build OA')
    oa_build = min(timeit.repeat(stmt='''
ht = HTOA(428221)
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open import Hashtable as HTOA
from resources.english import english_words
words = english_words()
''', repeat=repeat, number=num))/num

    print('Access OA')
    oa_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch03.hashtable_open import Hashtable as HTOA
from resources.english import english_words
ht = HTOA(428221)
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

    tbl = DataTable([8,10,10,10,10],['M', 'BuildLL', 'AccessLL', 'BuildOA', 'AccessOA'], decimals=3)

    M = 625
    while M <= 640000:
        t1_build = min(timeit.repeat(stmt=f'''
ht = DHL({M})
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_linked import DynamicHashtable as DHL
from resources.english import english_words
words = english_words()''', repeat=repeat, number=num))/num

        t1_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup=f'''
from ch03.hashtable_linked import DynamicHashtable as DHL
from resources.english import english_words
ht = DHL({M})
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

        t2_build = min(timeit.repeat(stmt=f'''
ht = DHL({M})
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open import DynamicHashtable as DHL
from resources.english import english_words
words = english_words()''', repeat=repeat, number=num))/num

        t2_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup=f'''
from ch03.hashtable_open import DynamicHashtable as DHL
from resources.english import english_words
ht = DHL({M})
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

        tbl.row([M, t1_build, t1_access, t2_build, t2_access])
        M = M * 2

    tbl.format('M', 's')
    tbl.row(['Fixed', ll_build, ll_access, oa_build, oa_access])
    return tbl

def count_hash():
    """
    For all English words, starting with a hashtable of size 1,024 and
    a load factor of 0.75, count how many times the hash code (i.e., %)
    is invoked.
    """
    from ch03.growth_test import DynamicHashtableLinkedCounting

    ht = DynamicHashtableLinkedCounting(1023)
    tbl = DataTable([20,10,10,10],['Word', 'N', '#insert', 'average'], decimals=2)
    tbl.format('Word', 's')
    tbl.format('N', ',d')
    tbl.format('#insert', ',d')

    last_word = None
    for w in english_words():
        last_word = w
        last = ht.hash_count
        ht.put(w, w)
        if ht.hash_count != last + 1:
            tbl.row([w, ht.N, ht.hash_count, ht.hash_count/ht.N])

    tbl.row([last_word, ht.N, ht.hash_count, ht.hash_count/ht.N])

    # determine when next resize event would occur...
    for i in range(1, 200000):
        last = ht.hash_count
        ht.put(last_word + str(i), last_word)
        if ht.hash_count != last + 1:
            print()
            print('next resize would happen after', i, 'more keys when N=', ht.N)
            print('The total number of insertions would be', comma(ht.hash_count),
                  'for an average of {:.2f}'.format(ht.hash_count/ht.N))
            break
    return tbl

def iteration_order():
    """Generate iteration orders for multiple hashtable types."""

    s = 'a rose by any other name would smell as sweet'
    from ch03.hashtable_open import Hashtable as Open_Hashtable, table_entries
    from ch03.hashtable_linked import Hashtable as Linked_Hashtable, linked_list_entries
    from ch03.hashtable_open_perfect import Hashtable as Perfect_Hashtable
    ht_oa = Open_Hashtable(13)
    ht_ll = Linked_Hashtable(13)
    ht_ph = Perfect_Hashtable()

    for w in s.split():
        ht_oa.put(w, w)
        ht_ll.put(w, w)
        ht_ph.put(w, w)

    tbl = DataTable([8,8,8], ['Open Addressing', 'Separate Chaining', 'Perfect Hash'])
    tbl.format('Open Addressing', 's')
    tbl.format('Separate Chaining', 's')
    tbl.format('Perfect Hash', 's')
    for p1,p2,p3 in zip(table_entries(ht_oa), linked_list_entries(ht_ll), table_entries(ht_ph)):
        tbl.row([p1[0], p2[0], p3[0]])

def generate_ch03():
    """Generate Tables and Figures for chapter 03."""
    chapter = 3

    with FigureNum(1) as figure_number:
        description  = 'Array containing month lengths interspersed with unneeded -1 values'
        label = captionx(chapter, figure_number)
        (_, day_array) = search_for_base()
        print('day_array =', day_array)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(1) as table_number:
        process(generate_hash(),
                chapter, table_number, 
                'Example hash() and hash code expressions for a table of size 15', create_image=False)

    with FigureNum(2) as figure_number:
        description  = 'Structure of Hashtable storage after adding five (key, value) pairs'
        label = captionx(chapter, figure_number)
        sample_hashtable()
        print('{}. {}'.format(label, description))
        print()

    with TableNum(2) as table_number:
        process(time_results_open_addressing(),
                chapter, table_number,
                'Average performance to insert N keys into a Hashtable of size M',
                yaxis='Time (in microseconds)')

    with TableNum(3) as table_number:
        process(compare_dynamic_build_and_access_time(),
                chapter, table_number,
                'Comparing resizable hash tables against fixed-size (time in ms)')

    with TableNum(4) as table_number:
        process(count_hash(),
                chapter, table_number,
                'Words whose addition causes a resize event, with total # of insertions and average')

    with TableNum(5) as table_number:
        process(count_collisions(),
                chapter, table_number,
                'Dynamic growing hash tables')

    with TableNum(6) as table_number:
        process(count_collisions_dynamic(), 
                chapter, table_number,
                'Dynamic growing hash tables')
