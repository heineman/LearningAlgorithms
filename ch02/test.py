"""Test cases for chapter 2."""
import random
import unittest
from algs.sorting import check_sorted

class Test_Ch02(unittest.TestCase):

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
        from ch02.challenge import log_log_table, run_max_sort_worst_case, run_permutation_sort

        tbl = log_log_table(output=False)
        self.assertEqual(4, tbl.entry(1024, 'NumSqrt'))

        tbl = run_permutation_sort(max_n=8, output=False)
        self.assertTrue(tbl.entry(2, 'PermutationSort') > 0)
        self.assertTrue(tbl.entry(2, 'Model') > 0)

        tbl = run_max_sort_worst_case(max_k=10, output=False)
        self.assertTrue(tbl.entry(128, 'MaxSort') > 0)
        self.assertTrue(tbl.entry(128, 'Model') > 0)

    def test_performance_bas(self):
        from ch02.challenge import performance_bas

        tbl = performance_bas(max_k=10, output=False)
        self.assertTrue(tbl.entry(32,'T(N)') < tbl.entry(512,'T(N)'))

#######################################################################
if __name__ == '__main__':
    unittest.main()
