"""Test cases for Chapter 01."""

import random
import unittest

from ch01.largest import largest, alternate, just_three, native_largest
from ch01.largest_two import largest_two, tournament_two, mutable_two
from ch01.largest_two import sorting_two, double_two, tournament_two_object
from ch01.challenge import linear_median, is_palindrome_letters_only, counting_sort
from ch01.challenge import counting_sort_improved, is_palindrome1, is_palindrome2

BEST_CASE = list(range(10))
WORST_CASE = list(range(10,0,-1))

class TestChapter1(unittest.TestCase):

    def test_flawed(self):
        from ch01.book import flawed
        self.assertEqual(5, flawed([3,2,1,4,5]))
        self.assertEqual(0, flawed([-3,-2,-1,-4,-5]))   # This is the mistake

    def test_largest(self):
        self.assertEqual(9, native_largest(BEST_CASE))

    def test_alternate(self):
        self.assertEqual(None, alternate([]))

    def test_largest_two(self):
        # default case
        with self.assertRaises(ValueError):
            largest_two([])

        with self.assertRaises(ValueError):
            largest_two([5])

        # six possible
        self.assertEqual((3,2), largest_two([1,2,3]))
        self.assertEqual((3,2), largest_two([1,3,2]))
        self.assertEqual((3,2), largest_two([2,1,3]))
        self.assertEqual((3,2), largest_two([2,3,1]))
        self.assertEqual((3,2), largest_two([3,1,2]))
        self.assertEqual((3,2), largest_two([3,2,1]))

    def test_sorting_two(self):
        with self.assertRaises(ValueError):
            sorting_two([])

        with self.assertRaises(ValueError):
            sorting_two([5])

        self.assertEqual((3,2), sorting_two([1,2,3]))
        self.assertEqual((3,2), sorting_two([1,3,2]))
        self.assertEqual((3,2), sorting_two([2,1,3]))
        self.assertEqual((3,2), sorting_two([2,3,1]))
        self.assertEqual((3,2), sorting_two([3,1,2]))
        self.assertEqual((3,2), sorting_two([3,2,1]))

    def test_double_two(self):
        with self.assertRaises(ValueError):
            double_two([])

        with self.assertRaises(ValueError):
            double_two([5])

        self.assertEqual((3,2), double_two([1,2,3]))
        self.assertEqual((3,2), double_two([1,3,2]))
        self.assertEqual((3,2), double_two([2,1,3]))
        self.assertEqual((3,2), double_two([2,3,1]))
        self.assertEqual((3,2), double_two([3,1,2]))
        self.assertEqual((3,2), double_two([3,2,1]))

    def test_largest_alternate(self):
        self.assertEqual(largest(BEST_CASE), max(BEST_CASE))
        self.assertEqual(largest(WORST_CASE), max(WORST_CASE))
        self.assertEqual(alternate(BEST_CASE), max(BEST_CASE))
        self.assertEqual(alternate(WORST_CASE), max(WORST_CASE))

        # edge cases
        self.assertEqual(largest([1]), 1)
        self.assertEqual(alternate([1]), 1)

        # no elements throws IndexError
        with self.assertRaises(IndexError):
            largest([])

    def test_tournament_two(self):
        answer = tuple(reversed(sorted(BEST_CASE)[-2:]))    # actual results
        self.assertEqual(largest_two(BEST_CASE), answer)
        self.assertEqual(tournament_two(BEST_CASE), answer)

        # mutable
        my_list = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(tournament_two(my_list), (9, 6))

        my_list = [1, 3, 1, 4, 9, 5, 6, 2]
        self.assertEqual(tournament_two(my_list), (9, 6))

        # edge cases
        self.assertEqual(largest_two([1,2]), (2,1))
        self.assertEqual(tournament_two([1,2]), (2,1))

        # mutable
        my_list = [9, 1, 8, 2, 3, 6]
        my_copy = list(my_list)
        self.assertEqual(mutable_two(my_list), (9, 8))
        self.assertEqual(my_list, my_copy)

        with self.assertRaises(ValueError):
            mutable_two([])

    def test_tournament_two_objects(self):
        self.assertEqual(tournament_two_object([1,2]), (2,1))

        with self.assertRaises(ValueError):
            tournament_two_object([])
        with self.assertRaises(ValueError):
            tournament_two_object([1,2,3])

        # mutable
        my_list = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(tournament_two_object(my_list), (9, 6))

        my_list = [1, 3, 1, 4, 9, 5, 6, 2]
        self.assertEqual(tournament_two_object(my_list), (9, 6))

    def test_just_three(self):
        self.assertEqual(3, just_three([1, 2, 3]))
        self.assertEqual(3, just_three([1, 3, 2]))
        self.assertEqual(3, just_three([2, 3, 1]))
        self.assertEqual(3, just_three([2, 1, 3]))
        self.assertEqual(3, just_three([3, 2, 1]))
        self.assertEqual(3, just_three([3, 1, 2]))

        with self.assertRaises(ValueError):
            just_three([])

    def test_median(self):
        from ch01.challenge import partition
        random.seed(10)
        a = [2, 3, 1]
        self.assertEqual(2, linear_median(a))
        self.assertEqual(2, linear_median([2,3]))
        self.assertEqual(2, linear_median([2]))

        a = [1]
        self.assertEqual(0, partition(a, 0, 0, 0))

        # For even numbered, lists, choose the value just to the left of middle.
        for m in range(5, 100, 1):
            a = list(range(m))
            random.shuffle(a)
            self.assertEqual((m-1)//2, linear_median(a))

    def test_counting_sort(self):
        original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = sorted(original)
        counting_sort(original, 10)
        self.assertEqual(expected, original)

    def test_counting_sort_improved(self):
        original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = sorted(original)
        counting_sort_improved(original, 10)
        self.assertEqual(expected, original)

    def test_palindromes(self):
        for pal in ['aba', 'abba', 'a']:
            self.assertTrue(is_palindrome1(pal))
            self.assertTrue(is_palindrome2(pal))
            self.assertFalse(is_palindrome1(pal+'x'))
            self.assertFalse(is_palindrome2(pal+'x'))

        palindromes = [
            'Able was I ere I saw Elba',
            'A man, a plan, a canal - Panama',
            "Madam, I'm Adam",
            'Never odd or even',
            'Doc, note: I dissent. A fast never prevents a fatness. I diet on cod',
            "T. Eliot, top bard, notes putrid tang emanating, is sad; I'd assign it a name: gnat dirt upset on drab pot toilet."
        ]
        for pal in palindromes:
            self.assertTrue(is_palindrome_letters_only(pal))

    def test_run_median_less_than_trial(self):
        from ch01.challenge import run_median_less_than_trial

        tbl = run_median_less_than_trial(max_k=10, output=False)
        self.assertTrue(tbl.entry(513,'median_count') < tbl.entry(513,'sort_median_count'))

    def test_run_counting_sort_trials(self):
        from ch01.challenge import run_counting_sort_trials

        tbl = run_counting_sort_trials(max_k=12, output=False)
        self.assertTrue(tbl.entry(2048,'counting_sort_improved') <= tbl.entry(2048,'counting_sort'))

    def test_linear_median(self):
        self.assertEqual(5, linear_median([5]))
        self.assertEqual(5, linear_median([3,5,7]))
        self.assertEqual(5, linear_median([3,5,6,7]))

        with self.assertRaises(IndexError):
            linear_median([])

    def test_tournament_allows_odd(self):
        from ch01.challenge import tournament_allows_odd
        A = [3, 87 , 2]
        self.assertEqual((87, 3), tournament_allows_odd(A))

        # sanity check, doesn't prove anything....
        for _ in range(200):
            A = list(range(11))
            random.shuffle(A)
            self.assertEqual((10, 9), tournament_allows_odd(A))

        with self.assertRaises(ValueError):
            tournament_allows_odd([2])

    def test_just_compare_sort_tournament_two(self):
        from ch01.book import just_compare_sort_tournament_two

        tbl = just_compare_sort_tournament_two(max_k=15, output=False)
        self.assertTrue(tbl.entry(8192, "sorting_two") < tbl.entry(16384, "sorting_two"))

    def test_run_largest_two_trials(self):
        from ch01.book import run_largest_two_trials, Order

        tbl = run_largest_two_trials(Order.REVERSED, max_k=15, output=False)
        self.assertTrue(tbl.entry(8192, 'double_two') < tbl.entry(16384, 'double_two'))

#######################################################################
if __name__ == '__main__':
    unittest.main()
