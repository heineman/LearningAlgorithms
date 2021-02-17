"""Test cases for chapter 2."""
import random
import unittest
from algs.sorting import check_sorted

class Test_Ch02(unittest.TestCase):

    def test_valid(self):
        from ch02.bas import binary_array_search
        A = []
        self.assertEqual(-1, binary_array_search(A, 6))    # placed into empty array

        A = [6]
        self.assertEqual(0, binary_array_search(A, 6))
        self.assertEqual(-1, binary_array_search(A, 2))    # placed BEFORE 6
        self.assertEqual(-2, binary_array_search(A, 11))   # placed AFTER 6

        A = [2,4,6]
        self.assertEqual(-1, binary_array_search(A, 1))    # placed BEFORE 2
        self.assertEqual(-2, binary_array_search(A, 3))    # placed BEFORE 4
        self.assertEqual(-3, binary_array_search(A, 5))    # placed BEFORE 6
        self.assertEqual(-4, binary_array_search(A, 7))    # placed AFTER 6

    def test_max_sort(self):
        from ch02.challenge import max_sort
        A = list(range(20))
        random.shuffle(A)
        self.assertTrue(check_sorted(max_sort(A)))

#######################################################################
if __name__ == '__main__':
    unittest.main()
