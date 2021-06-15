"""Test cases for Chapter 02."""

import random
import unittest

from algs.sorting import check_sorted

class TestChapter2(unittest.TestCase):

    def test_mult(self):
        from ch02.mult import create_pair, mult_pair, create_random_pair
        (up, down) = create_pair(5)
        self.assertEqual(12345,up)
        self.assertEqual(98765,down)

        (up, down) = create_pair(12)
        self.assertEqual(123456789123,up)
        self.assertEqual(987654321987,down)

        self.assertEqual(77, mult_pair([7, 11]))

        (up, down) = create_random_pair(12)
        self.assertTrue(100000000000 < up < 999999999999)
        self.assertTrue(100000000000 < down < 999999999999)

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

    def test_random(self):
        from ch02.random_sort import permutation_sort, random_sort

        # CAUTION! Only do this with small sizes.
        A = [8, 7, 6, 5, 4]
        random_sort(A)
        self.assertTrue(check_sorted(A))

        # CAUTION! Only do this with small sizes.
        A = [8, 7, 6, 5, 4]
        permutation_sort(A)
        self.assertTrue(check_sorted(A))

    def test_challenge(self):
        from ch02.challenge import run_max_sort_worst_case, run_permutation_sort

        tbl = run_permutation_sort(max_n=8, output=False)
        self.assertTrue(tbl.entry(2, 'PermutationSort') >= 0)

        tbl = run_max_sort_worst_case(max_k=10, output=False)
        self.assertTrue(tbl.entry(128, 'MaxSort') >= 0)

    def test_performance_bas(self):
        from ch02.challenge import performance_bas

        tbl = performance_bas(max_k=10, output=False)
        self.assertTrue(tbl.entry(32,'T(N)') < tbl.entry(512,'T(N)'))

    def test_range(self):
        A = [1, 2, 2, 2, 3, 4]
        from ch02.challenge import worst_range, best_range
        self.assertIsNone(worst_range([], 2))
        self.assertIsNone(best_range([], 2))

        self.assertEqual((1,3), worst_range(A, 2))
        self.assertEqual((0,0), worst_range(A, 1))
        self.assertEqual((4,4), worst_range(A, 3))
        self.assertEqual((5,5), worst_range(A, 4))

        self.assertIsNone(worst_range(A,0))
        self.assertIsNone(worst_range(A,7))

        self.assertEqual((1,3), best_range(A, 2))
        self.assertEqual((0,0), best_range(A, 1))
        self.assertEqual((4,4), best_range(A, 3))
        self.assertEqual((5,5), best_range(A, 4))

        self.assertIsNone(best_range(A,0))
        self.assertIsNone(best_range(A,7))

        A = [3] * 10000
        self.assertEqual((0,9999), worst_range(A, 3))
        self.assertEqual((0,9999), best_range(A, 3))

        # a bit of a stress test....
        tgt = random.random()
        alist = [tgt] * 999
        for _ in range(5000):
            alist.append(random.random())
        alist = sorted(alist)
        self.assertEqual(worst_range(A, tgt), best_range(A, tgt))

        # All single ones....
        nums = list(range(100))
        for i in range(100):
            self.assertEqual((i,i), best_range(nums, i))
            self.assertEqual((i,i), worst_range(nums, i))

        nums = list(range(0,100,2))
        for i in range(1,100,2):
            self.assertIsNone(best_range(nums, i))
            self.assertIsNone(worst_range(nums, i))

#######################################################################
if __name__ == '__main__':
    unittest.main()
