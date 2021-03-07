"""Test cases for chapter 3."""
import random
import unittest

def key(i):
    """Helper method to generate a meaningful key."""
    return 'key{}'.format(i)

def sample(i):
    """Helper method to generate a meaningful sample value."""
    return 'sample{}'.format(i)

class Test_Ch03(unittest.TestCase):

    def test_base26(self):
        from ch03.base26 import base26
        j = ord('j') - ord('a')
        u = ord('u') - ord('a')
        n = ord('n') - ord('a')
        e = ord('e') - ord('a')
        self.assertEqual(17576*j + 676*u + 26*n + e, base26('june'))
        
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
        from ch03.hashtable_open import Hashtable

        # Need M > 1
        with self.assertRaises(ValueError):
            _ = Hashtable(0)

        S = 100
        ht = Hashtable(S)
        for i in range(S-1):
            ht.put(key(i), sample(i))
        for i in range(S-1):
            self.assertEqual(sample(i), ht.get(key(i)))
        self.assertEqual(S-1, ht.N)
        self.assertTrue(ht.get(key(-999)) == None)

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
        self.assertTrue(ht.get(99) == None)
        self.assertTrue(ht.remove(99) == None)
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
        (avg_len, max_len) = stats_linked_lists([0,1*M,2*M,3*M,4*M], Hashtable(M))
        
        # Only one bucket is non-empty! Average is max
        self.assertEqual(5, max_len)
        self.assertEqual(5, avg_len)
        
        (avg_len, max_len) = stats_linked_lists([0,1*M,2*M,3*M,4*M,2,M+2], Hashtable(M))
        self.assertEqual(5, max_len)
        self.assertEqual(3.5, avg_len)

    def test_open_addressing_stats(self):
        from ch03.hashtable_open import Hashtable, stats_open_addressing
        M = 13
        (avg_len, max_len) = stats_open_addressing([0,1*M,2*M,3*M,4*M], Hashtable(M))
        
        # single bucket spills over, with 5 / 4 / 3 / 2 / 1 for avg. of 3
        self.assertEqual(5, max_len)
        self.assertEqual(3, avg_len)
        
        (avg_len, max_len) = stats_open_addressing([0,1*M,2*M,3*M,4*M, M-2, M-3], Hashtable(M))
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
        ht.put('a', 99)
        ht.put('zyzzyvas', 99)
        self.assertEqual('a', ht.table[0].key)
        self.assertEqual('zyzzyvas', ht.table[321164].key)

    def test_resize_hash_small_open_addressing(self):
        from ch03.hashtable_open import DynamicHashtable
        
        with self.assertRaises(ValueError):
            DynamicHashtable(0)
        
        for size in range(1,10):
            ht = DynamicHashtable(size)
            for val in range(1,10):
                ht.put(val, val)
                ht.put(val, val+1)  # make sure we validate put as well
            for i in range(1,10):
                self.assertEqual(i+1, ht.get(i))

    def test_resize_hash_small_open_addressing_remove(self):
        from ch03.hashtable_open import DynamicHashtablePlusRemove
        
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

    def test_resize_hash_small_linked(self):
        from ch03.hashtable_linked import DynamicHashtable
        for size in range(1,10):
            ht = DynamicHashtable(size)
            for val in range(1,10):
                ht.put(val, val)
                ht.put(val, val+1)   # make sure we validate put as well
            for i in range(1,10):
                self.assertEqual(i+1, ht.get(i))
            ht.put(99, 101)
            self.assertEqual(101, ht.remove(99))

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

    def test_challenge_small(self):
        from ch03.challenge import DynamicHashtableIncrementalResizing as Hashtable
        values = list(['val{}'.format(k) for k in range(55)])
        ht = Hashtable(7, 5)
        for w in values:
            ht.put(w, w)
        
        # make sure all still present
        print ('-----')
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

if __name__ == '__main__':
    unittest.main()
