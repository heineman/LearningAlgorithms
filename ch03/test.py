"""Test cases for Chapter 03."""

import random
import unittest

from algs.table import SKIP

def key(i):
    """Helper method to generate a meaningful key."""
    return 'key{}'.format(i)

def sample(i):
    """Helper method to generate a meaningful sample value."""
    return 'sample{}'.format(i)

class TestChapter3(unittest.TestCase):

    def test_base26(self):
        from ch03.base26 import base26
        j = ord('j') - ord('a')
        u = ord('u') - ord('a')
        n = ord('n') - ord('a')
        e = ord('e') - ord('a')
        self.assertEqual(17576*j + 676*u + 26*n + e, base26('june'))

    def test_builtin(self):
        from ch04.builtin import PQ
        pq = PQ(5)
        for v,p in [('a',1), ('b',2), ('c', 3), ('d',4), ('e',5)]:
            pq.enqueue(v, p)
        self.assertTrue(pq.is_full())

    def test_search_for_base(self):
        from ch03.base26 import search_for_base, base26
        (m, data) = search_for_base()
        self.assertEqual(34, m)

        # this is good
        self.assertEqual(31, data[base26('August') % m])
        self.assertEqual(28, data[base26('February') % m])

        # this is not good
        self.assertEqual(31, data[base26('abbreviated') % m])

    def test_entry(self):
        from ch03.entry import Entry, LinkedEntry, MarkedEntry
        e = Entry('key1', 'val1')
        self.assertEqual('key1 -> val1', str(e))

        le = LinkedEntry('key1', 'val1')
        self.assertEqual('key1 -> val1', str(le))

        me = MarkedEntry('key1', 'val1')
        self.assertEqual('key1 -> val1', str(me))
        me.mark()
        self.assertEqual('key1 -> val1 [Marked]', str(me))
        self.assertTrue(me.is_marked())
        me.unmark()
        self.assertFalse(me.is_marked())
        self.assertEqual('key1 -> val1', str(me))

    def test_valid_weak_hashtable(self):
        from ch03.hashtable import Hashtable

        # Need M > 1
        with self.assertRaises(ValueError):
            _ = Hashtable(0)

        ht = Hashtable(11)
        ht.put(13,sample(13))
        self.assertEqual(sample(13), ht.get(13))

        # CLASH since 24 is 2 mod 11, much like 13 is 2 mod 11
        with self.assertRaises(RuntimeError):
            ht.put(24, 'anotherOne')

    def test_overwrite_works(self):
        from ch03.hashtable import Hashtable
        ht = Hashtable(11)
        for i in range(11):
            ht.put(i, sample(i))
        self.assertEqual(sample(9), ht.get(9))

        for i in range(11):
            ht.put(i, 'other{}'.format(i))
        self.assertEqual('other3', ht.get(3))

    def test_open_addressing_table(self):
        """The order of values in table is irrelevant."""
        from ch03.hashtable_open import Hashtable, stats_open_addressing

        # Need M > 1
        with self.assertRaises(ValueError):
            _ = Hashtable(0)

        S = 100
        ht = Hashtable(S)
        self.assertEqual((0,0), stats_open_addressing(ht))   # empty hash table
        for i in range(S-1):
            ht.put(key(i), sample(i))
        for i in range(S-1):
            self.assertEqual(sample(i), ht.get(key(i)))
        for i in range(S-1):
            ht.put(key(i), sample(i+1))  # replace
        self.assertEqual(S-1, ht.N)
        self.assertTrue(ht.get(key(-999)) is None)

        self.assertTrue(ht.is_full())
        with self.assertRaises(RuntimeError):
            ht.put(key(S), 'Should be full')

    def test_linked_list_table(self):
        """The order of values in table is irrelevant."""
        from ch03.hashtable_linked import Hashtable

        # Need M > 1
        with self.assertRaises(ValueError):
            _ = Hashtable(0)

        S = 1000
        ht = Hashtable(77)
        for i in range(S):
            ht.put(key(i), sample(i))
        for i in range(S):
            self.assertEqual(sample(i), ht.get(key(i)))
        self.assertEqual(S, ht.N)

        # Now go and delete values, in any order
        to_remove = list(range(S))
        random.shuffle(to_remove)
        for s in to_remove:
            self.assertIsNotNone(ht.remove(key(s)))
        self.assertEqual(0, ht.N)

    def test_confirm_day_of_week_one_line(self):
        """Find first date where computations diverge."""
        from ch03.months import month_length, key_array, day_of_week_one_line
        from datetime import date
        for y in range (1753, 9999):
            for m in range(1, 13):
                for d in range(1, month_length[m-1]):
                    computed = day_of_week_one_line(y, m, d)       # computes so Monday = 1
                    wd = date(y,m,d).weekday()          # computes so Monday = 0
                    wd = (wd + 1) % 7
                    if computed != wd:
                        self.fail('Diverged at {}{}{}'.format(y, key_array[m-1], d))
                        return

    def test_confirm_day_of_week(self):
        """Find first date where computations diverge."""
        from ch03.months import month_length, key_array, day_of_week
        from datetime import date
        for y in range (1753, 9999):
            for m in range(1, 13):
                for d in range(1, month_length[m-1]):
                    computed = day_of_week(y, m, d)       # computes so Monday = 1
                    wd = date(y,m,d).weekday()          # computes so Monday = 0
                    wd = (wd + 1) % 7
                    if computed != wd:
                        self.fail('Diverged at {}{}{}'.format(y, key_array[m-1], d))
                        return

    def test_monthly_arrays(self):
        """test days_in_month."""
        from ch03.months import s_data, days_in_month, days_mixed, days_bas
        for m in s_data:
            if days_in_month[m] != days_mixed(m) or days_mixed(m) != days_bas(m):
                self.fail('Error in {}'.format(m))

        self.assertEqual(0, days_bas('bad_month'))
        self.assertEqual(0, days_mixed('bad_month'))

    def test_search_for_data(self):
        # As you can see there is a match
        from ch03.months import search_for_data, s_data, s_num, month_index

        (best_tuple, best) = search_for_data()
        for idx,data in enumerate(s_data):
            self.assertEqual(s_num[idx], best[month_index(data, best_tuple[0], best_tuple[1])])

    def test_search_for_hashes(self):
        from ch03.months import search_for_hashes

        result = search_for_hashes()
        self.assertTrue(not result is None)

    def test_craft_table(self):
        from ch03.months import craft_table

        ht = craft_table()
        self.assertTrue(ht.M > 0)

    def test_iterate_open_addressing(self):
        from ch03.hashtable_open import Hashtable
        ht = Hashtable(11)
        ht.put(13,sample(13))
        ht.put(7,sample(7))
        ht.put(24,sample(24))

        entries = []
        for pair in ht:
            entries.append(pair)

        # tuples can be sorted - key is the first one, so appropriate.
        entries.sort()
        self.assertEqual([(7,sample(7)), (13,sample(13)), (24, sample(24))], entries)

    def test_linked_list_updates(self):
        from ch03.hashtable_linked import Hashtable
        ht = Hashtable(11)
        ht.put(13,sample(13))
        ht.put(13,sample(17))
        self.assertEqual(sample(17), ht.get(13))
        self.assertTrue(ht.get(99) is None)
        self.assertTrue(ht.remove(99) is None)
        self.assertTrue(ht.remove(13) == sample(17))

        # add to same bucket
        ht.put(0, sample(0))
        ht.put(11, sample(11))
        ht.put(22, sample(22))
        ht.put(33, sample(33))
        self.assertEqual(sample(22), ht.remove(22))
        self.assertEqual(sample(33), ht.remove(33))
        self.assertEqual(sample(0), ht.remove(0))

    def test_linked_list_stats(self):
        from ch03.hashtable_linked import Hashtable, stats_linked_lists
        M = 13
        ht = Hashtable(M)
        for w in [0,1*M,2*M,3*M,4*M]:
            ht.put(w, 1)
        (avg_len, max_len) = stats_linked_lists(ht)

        # Only one bucket is non-empty! Average is max
        self.assertEqual(5, max_len)
        self.assertEqual(5, avg_len)

        ht = Hashtable(M)
        for w in  [0,1*M,2*M,3*M,4*M,2,M+2]:
            ht.put(w, 1)
        (avg_len, max_len) = stats_linked_lists(ht)

        self.assertEqual(5, max_len)
        self.assertEqual(3.5, avg_len)

    def test_open_addressing_stats(self):
        from ch03.hashtable_open import Hashtable, stats_open_addressing
        M = 13
        ht = Hashtable(M)
        for w in [0,1*M,2*M,3*M,4*M]:
            ht.put(w, 1)
        (avg_len, max_len) = stats_open_addressing(ht)

        # single bucket spills over, with 5 / 4 / 3 / 2 / 1 for avg. of 3
        self.assertEqual(5, max_len)
        self.assertEqual(3, avg_len)

        ht = Hashtable(M)
        for w in [0,1*M,2*M,3*M,4*M, M-2, M-3]:
            ht.put(w, 1)
        (avg_len, max_len) = stats_open_addressing(ht)
        self.assertEqual(5, max_len)
        self.assertEqual(18/7, avg_len)

    def test_iterate_linked_list(self):
        from ch03.hashtable_linked import Hashtable
        ht = Hashtable(11)
        ht.put(13,sample(13))
        ht.put(7,sample(7))
        ht.put(24,sample(24))

        entries = []
        for pair in ht:
            entries.append(pair)

        # tuples can be sorted - key is the first one, so appropriate.
        entries.sort()
        self.assertEqual([(7,sample(7)), (13,sample(13)), (24, sample(24))], entries)

    def test_perfect(self):
        from ch03.hashtable_open_perfect import Hashtable
        ht = Hashtable()
        self.assertTrue(ht.get('zyzzyvas') is None)
        ht.put('a', 99)
        ht.put('zyzzyvas', 101)
        self.assertEqual('a', ht.table[0].key)
        self.assertEqual('zyzzyvas', ht.table[321128].key)

        self.assertEqual(99, ht.get('a'))
        self.assertEqual(101, ht.get('zyzzyvas'))

        self.assertEqual([('a',99), ('zyzzyvas',101)], list(ht))

    def test_resize_hash_small_open_addressing(self):
        from ch03.hashtable_open import DynamicHashtable

        with self.assertRaises(ValueError):
            DynamicHashtable(0)

        for size in range(1,10):
            ht = DynamicHashtable(size)
            for val in range(1,10*size):
                ht.put(val, val)
                ht.put(val, val+1)  # make sure we validate put as well
            for i in range(1,10):
                self.assertEqual(i+1, ht.get(i))

            self.assertEqual(list(range(1, 10*size)), sorted([i[0] for i in ht]))

    def test_resize_validate_chain_remove(self):
        from ch03.hashtable_open import DynamicHashtablePlusRemove

        ht = DynamicHashtablePlusRemove(50)
        for i in range(100):
            ht.put('sample{}'.format(i), i)
        self.assertEqual(100, len(ht))
        for i in range(99, -1, -1):
            ht.remove('sample{}'.format(i))
        self.assertEqual(0, len(ht))
        ht.remove('samplenotthere')
        self.assertEqual(0, len(ht))

    def test_resize_hash_small_open_addressing_remove(self):
        from ch03.hashtable_open import DynamicHashtablePlusRemove

        with self.assertRaises(ValueError):
            DynamicHashtablePlusRemove(-2)

        # Intricate test that uncovered some subtle defects when
        # reusing MarkedEntry objects...
        for size in range(2,20):
            ht = DynamicHashtablePlusRemove(size)
            for val in range(1,20):
                ht.put(val, val)
                ht.put(val, val+1)  # make sure we validate put as well
            self.assertEqual(19, len(list(ht)))
            for i in range(1,20):
                self.assertEqual(i+1, ht.get(i))
            for i in range(1,20):
                self.assertEqual(i+1, ht.remove(i))
            for i in range(1,20):
                self.assertTrue(ht.remove(i) is None)   # double remove should return None
            self.assertEqual(0, ht.N)
            self.assertEqual(19, ht.deleted)
            for val in range(1,100):
                ht.put(val, val)
                ht.put(val, val+1)  # make sure we validate put as well
            self.assertEqual(99, ht.N)   # NOTE: reused deleted ones!
            for val in range(1,100):
                self.assertEqual(val+1, ht.remove(val))
            for val in range(300,400):
                ht.put(val, val)
            self.assertEqual(100, ht.N)
            for val in range(1,100):
                self.assertTrue(ht.get(val) is None)

    def test_resize_hash_small_linked_remove(self):
        from ch03.hashtable_linked import DynamicHashtable
        from ch03.challenge import ValueBadHash

        # Forces long chains.
        ht = DynamicHashtable(20)
        self.assertTrue(ht.get(99) is None)
        for i in range(10):
            ht.put(ValueBadHash(i), i)
        for i in range(10):
            self.assertEqual(i, ht.remove(ValueBadHash(i)))

    def test_resize_hash_small_linked(self):
        from ch03.hashtable_linked import DynamicHashtable
        for size in range(1,10):
            ht = DynamicHashtable(size)
            for val in range(1,50):
                ht.put(val, val)
                ht.put(val, val+1)   # make sure we validate put as well
            for i in range(1,50):
                self.assertEqual(i+1, ht.get(i))
            ht.put(99, 101)
            self.assertEqual(101, ht.remove(99))
            self.assertTrue(ht.remove(99) is None)
            for i in range(1,25):
                self.assertEqual(i+1, ht.remove(i))

            self.assertEqual(list(range(26,51)), sorted([i[1] for i in ht]))

    def test_resize_open_addressing(self):
        from ch03.hashtable_open import DynamicHashtable
        ht = DynamicHashtable(5)
        ht.put(1, 1)
        ht.put(2, 2)
        ht.put(3, 3)
        self.assertEqual(3, ht.N)
        self.assertEqual(5, ht.M)
        ht.put(12,12)
        self.assertEqual(11, ht.M)
        for i in [1,2,3,12]:
            self.assertEqual(i, ht.get(i))

    def test_resize_separate_chaining(self):
        from ch03.hashtable_linked import DynamicHashtable
        ht = DynamicHashtable(5)
        ht.put(1, 1)
        ht.put(2, 2)
        ht.put(3, 3)
        self.assertEqual(3, ht.N)
        self.assertEqual(5, ht.M)
        ht.put(12,12)
        self.assertEqual(11, ht.M)
        for i in [1,2,3,12]:
            self.assertEqual(i, ht.get(i))

    def test_dynamic_resizing_valid(self):
        from ch03.challenge import DynamicHashtableIncrementalResizing as Hashtable

        with self.assertRaises(ValueError):
            Hashtable(0, 10)

        with self.assertRaises(ValueError):
            Hashtable(10, 0)

        ht = Hashtable(7, 5)
        self.assertTrue(ht.get(99) is None)
        self.assertTrue(ht.remove(99) is None)
        ht.put(5, 10)
        self.assertEqual(10, ht.get(5))
        ht.put(5, 11)
        self.assertEqual(11, ht.get(5))
        self.assertEqual(11, ht.remove(5))

        # Harder to get dynamic resizing
        ht = Hashtable(10, 3)
        for i in range(12):
            # at i=8, the move happens / old table has 3,4,5,6,7 and the
            # new table has 0,1,2,8
            ht.put(i, i)
            ht.put(3, 99)    # this validates that you can change value in OLD table

        ht.put(3, 3)
        for i in range(12):
            self.assertEqual(i, ht.get(i))

        for i in range(12):
            ht.put(i, i+1)

        for i in range(12):
            self.assertEqual(i+1, ht.get(i))

    def test_simulation(self):
        from ch03.challenge import PythonSimulationHashtable as Hashtable

        ht = Hashtable(5)
        self.assertTrue(ht.get(99) is None)
        for i in range(12):
            ht.put('key{}'.format(i), i)

        for i in range(12):
            self.assertEqual(i, ht.get('key{}'.format(i)))

        for i in range(12):
            ht.put('key{}'.format(i), i+1)

        for i in range(12):
            self.assertEqual(i+1, ht.get('key{}'.format(i)))

        self.assertEqual(list(range(1,13)), sorted([e[1] for e in ht]))

    def test_challenge_small(self):
        from ch03.challenge import DynamicHashtableIncrementalResizing as Hashtable
        values = list(['val{}'.format(k) for k in range(55)])
        ht = Hashtable(7, 5)
        for w in values:
            ht.put(w, w)

        # make sure all still present
        print('-----')
        for w in values:
            self.assertEqual(w, ht.get(w))

    def test_challenge(self):
        from ch03.challenge import DynamicHashtableIncrementalResizing as Hashtable
        from resources.english import english_words
        ht = Hashtable(31, 5)
        for w in english_words():
            ht.put(w, w)

        # make sure all still present
        for w in english_words():
            self.assertEqual(w, ht.get(w))

        # now remove them one at a time
        for w in english_words():
            self.assertEqual(w, ht.remove(w))

    def test_prime_number_difference(self):
        from ch03.challenge import prime_number_difference
        K = ['a', 'rose', 'by', 'any', 'other', 'name', 'would', 'smell', 'as', 'sweet']
        tbl = prime_number_difference(words=K, output=False)
        self.assertEqual('Prime', tbl.entry(428977, 'Prime'))

    def test_bad_timing(self):
        from resources.english import english_words
        from ch03.challenge import bad_timing

        tbl = bad_timing(english_words()[:100], output=False)
        self.assertTrue(tbl.entry('Good', 'Max Len') > 0)

    def test_measure_performance_resize(self):
        from ch03.challenge import measure_performance_resize

        # cannot have test cases since the values in each row are based on hashing
        # results and change each time
        (_, _, tbl_d) = measure_performance_resize(max_d=5, output=False)
        self.assertTrue(tbl_d.entry(1, 'Average') > 0)

    def test_count_hash(self):
        from ch03.book import count_hash

        tbl = count_hash(output=False)
        self.assertEqual(321129, tbl.entry('zyzzyvas', 'N'))

    def test_run_access_trials(self):
        from ch03.timing import run_access_trials

        tbl = run_access_trials(max_trials=100, output=False)
        self.assertEqual('Dict', tbl.labels[0])

    def test_time_results_open(self):
        from ch03.timing import time_results_open

        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        tbl = time_results_open(words, output=False)
        self.assertEqual(SKIP, tbl.entry(16384, 8192))

    def test_iteration_order(self):
        from ch03.book import iteration_order
        from algs.sorting import check_sorted
        tbl = iteration_order(output=False)    # these are in ascending order with perfect hash
        self.assertTrue(check_sorted(tbl.column('Perfect Hash')))

    def test_avoid_digit(self):
        from ch03.book import avoid_digit
        alist = avoid_digit(22,1)
        self.assertEqual([0, 2, 3, 4, 5, 6, 7, 8, 9, 20], list(alist))

    def test_compare_dynamic_build_and_access_time(self):
        from ch03.book import compare_dynamic_build_and_access_time

        tbl = compare_dynamic_build_and_access_time(repeat=1, max_m=1250, output=False)
        self.assertTrue(tbl.entry('Fixed', 'BuildLL') <= tbl.entry(1250, 'BuildLL'))

    def test_count_collisions(self):
        from ch03.book import count_collisions

        tbl = count_collisions(num_rows=4, output=False)
        self.assertTrue(tbl.entry(642258, 'Max LL') > 0)

    def test_count_collisions_dynamic(self):
        from ch03.book import count_collisions_dynamic

        tbl = count_collisions_dynamic(num_rows=4, output=False)
        self.assertTrue(tbl.entry(642258, 'Max LL') > 0)

    def test_time_results_open_addressing(self):
        from ch03.book import time_results_open_addressing

        tbl = time_results_open_addressing(num_rows=2, output=False)
        self.assertTrue(tbl.entry(32,'8,192') < tbl.entry(64,'8,192'))

    def test_triangle_number_hash(self):
        from ch03.challenge import HashtableTriangleNumbers

        with self.assertRaises(ValueError):
            HashtableTriangleNumbers(-2)
        with self.assertRaises(ValueError):
            HashtableTriangleNumbers(3)

        ht = HashtableTriangleNumbers(16)
        self.assertFalse(ht.is_full())
        ht.put(77, 99)
        ht.put(77, 101)
        self.assertEqual(101, ht.get(77))
        self.assertEqual([(77,101)], [k for k in ht])

        # place 14 more values until full (since must leave ONE empty).
        for k in range(14):
            ht.put(k, k)
        for k in range(14):
            self.assertEqual(k, ht.get(k))
        self.assertTrue(ht.get(1010) is None)

        with self.assertRaises(RuntimeError):
            ht.put(999,99)

    def test_sorted_linked_list_hash_table(self):
        from ch03.challenge import HashtableSortedLinkedLists
        
        with self.assertRaises(ValueError):
            HashtableSortedLinkedLists(-2)

        ht = HashtableSortedLinkedLists()
        self.assertEqual(0, len(ht))
        ht.put(10, 10)
        self.assertEqual(1, len(ht))
        self.assertTrue(ht.get(5) is None)
        self.assertTrue(ht.get(20) is None)
        ht.put(5, 5)
        self.assertEqual(2, len(ht))
        self.assertEqual(5, ht.get(5))
        ht.put(15, 15)
        self.assertEqual(15, ht.get(15))
        self.assertEqual(3, len(ht))

        ht.put(10, 20)
        ht.put(5, 10)
        ht.put(15, 30)
        ht.remove(5)
        self.assertEqual([(10, 20), (15, 30)], sorted(list(ht)))
        self.assertEqual(2, len(ht))
        self.assertEqual(30, ht.remove(15))
        self.assertEqual(1, len(ht))
        ht.remove(10)
        self.assertEqual(0, len(ht))
        self.assertTrue(ht.remove(25) is None)

        ht.put(30, 60)
        ht.put(40, 70)
        ht.put(10, 50)
        ht.put(20, 80)
        self.assertEqual(4, len(ht))
        ht.remove(40)
        ht.remove(30)
        ht.remove(20)
        ht.remove(10)
        self.assertEqual(0, len(ht))


    def test_evaluate_dynamic_plus_remove(self):
        from ch03.challenge import evaluate_DynamicHashtablePlusRemove

        tbl = evaluate_DynamicHashtablePlusRemove(output=False)
        self.assertTrue(tbl.entry(512, 'Separate Chaining') <= tbl.entry(2048, 'Separate Chaining'))

#######################################################################
if __name__ == '__main__':
    unittest.main()
