"""Test cases for Chapter 01"""

import unittest
import random

from ch01.largest import largest, alternate, just_three, native_largest
from ch01.largest_two import largest_two, tournament_two, mutable_two
from ch01.largest_two import sorting_two, double_two, tournament_two_object
from ch01.challenge import linear_median, is_palindrome_letters_only, counting_sort
from ch01.challenge import counting_sort_improved

BEST_CASE = list(range(10))
WORST_CASE = list(range(10,0,-1))

class Test_Ch01(unittest.TestCase):

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
        a = [2, 3, 1]
        self.assertEqual(2, linear_median(a))

        # Computing median only for Lists of odd length
        for m in range(5, 100, 2):
            a = list(range(m))
            random.shuffle(a)
            self.assertEqual(m//2, linear_median(a))

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

#######################################################################
if __name__ == '__main__':
    unittest.main()
