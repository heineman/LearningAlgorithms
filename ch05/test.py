"""Test code for Chapter 05."""
import unittest

BEST_CASE = list(range(10))
WORST_CASE = list(range(10,0,-1))

class Test_ch05(unittest.TestCase):

    def test_merge_sort(self):
        from ch05.merge import merge_sort
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        merge_sort(sample)
        self.assertEqual(expected, sample)

    def test_merge_sort_counting(self):
        from ch05.merge import merge_sort_counting
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        merge_sort_counting(sample)
        self.assertEqual(expected, sample)

    def test_slice_merge_sort_counting(self):
        from ch05.challenge import slice_merge_sort
        sample = [1, 2, 3, 4, 5, 6, 7, 8]               # drain left
        expected = sorted(sample)
        slice_merge_sort(sample)
        self.assertEqual(expected, sample)

        sample = [5, 6, 7, 8, 1, 2, 3, 4]               # drain right
        expected = sorted(sample)
        slice_merge_sort(sample)
        self.assertEqual(expected, sample)

    def test_quick_sort(self):
        from ch05.sorting import quick_sort
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        quick_sort(sample)
        self.assertEqual(expected, sample)

    def test_selection_sort(self):
        from ch05.sorting import selection_sort
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        selection_sort(sample)
        self.assertEqual(expected, sample)

    def test_selection_sort_counting(self):
        from ch05.sorting import selection_sort_counting
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        selection_sort_counting(sample)
        self.assertEqual(expected, sample)

    def test_insertion_sort(self):
        from ch05.sorting import insertion_sort
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        insertion_sort(sample)
        self.assertEqual(expected, sample)

    def test_insertion_sort_counting(self):
        from ch05.sorting import insertion_sort_counting
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        insertion_sort_counting(sample)
        self.assertEqual(expected, sample)

    def test_insertion_sort_cmp(self):
        from ch05.sorting import insertion_sort_cmp
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = list(reversed(sorted(sample)))
        insertion_sort_cmp(sample, lambda one, two: two < one)
        self.assertEqual(expected, sample)

    def test_insertion_sort_bas(self):
        from ch05.sorting import insertion_sort_bas
        sample = [15,21,20,2,15,24,5,19]               # standard example in chapter
        expected = sorted(sample)
        insertion_sort_bas(sample)
        self.assertEqual(expected, sample)

    def test_challenge_num_swaps(self):
        from ch05.challenge import num_swaps, num_swaps_hashable
        self.assertEqual(6, num_swaps([9, 3, 0, 4, 1, 2, 6, 8, 7, 5]))
        self.assertEqual(6, num_swaps_hashable(['9', '3', '0', '4', '1', '2', '6', '8', '7', '5']))
        self.assertEqual(0, num_swaps_hashable(['A', 'B', 'C', 'D', 'E']))
        self.assertEqual(4, num_swaps_hashable(['B', 'C', 'D', 'E', 'A']))

    def test_find_max(self):
        from ch05.max import find_max
        self.assertEqual(9, find_max([9, 3, 0, 4, 1, 2, 6, 8, 7, 5]))

    def test_heap_sort(self):
        from ch05.heapsort import HeapSort, heap_sort, HeapSortCounting
        from random import shuffle

        # try a bunch of random arrays. Not a full test, but useful stress test
        size = 16
        for _ in range(1000):
            A = list(range(size))
            shuffle(A)
            HeapSort(A).sort()
            self.assertEqual(list(range(size)), A)

        size = 16
        for _ in range(1000):
            A = list(range(size))
            shuffle(A)
            HeapSortCounting(A).sort()
            self.assertEqual(list(range(size)), A)

        size = 16
        for _ in range(50):
            A = list(range(size))
            shuffle(A)
            heap_sort(A)
            self.assertEqual(list(range(size)), A)


    def test_heap_first_step(self):
        from ch05.heapsort import HeapSort

        # This is a heap but shifted over by one to no longer waste
        # first value. After constructing Heap, these values won't change...
        A = [15, 13, 14, 12, 11, 12, 14, 8, 9, 1, 10, 8, 6, 9, 7, 4, 5, 2]
        hs = HeapSort(A)
        self.assertEqual(18, hs.N)
        self.assertEqual([15, 13, 14, 12, 11, 12, 14, 8, 9, 1, 10, 8, 6, 9, 7, 4, 5, 2], A)

        # manually advance one step in sorting process
        hs.swap(1, hs.N)
        hs.N -= 1
        hs.sink(1)

        # note last spot has largest value
        self.assertEqual([14, 13, 14, 12, 11, 12, 9, 8, 9, 1, 10, 8, 6, 2, 7, 4, 5, 15], A)
        self.assertEqual(17, hs.N)

        # manually advance one step in sorting process
        hs.swap(1, hs.N)
        hs.N -= 1
        hs.sink(1)

        # note last spot has largest value
        self.assertEqual([14, 13, 12, 12, 11, 8, 9, 8, 9, 1, 10, 5, 6, 2, 7, 4, 14, 15], A)
        self.assertEqual(16, hs.N)

        # manually advance one step in sorting process
        hs.swap(1, hs.N)
        hs.N -= 1
        hs.sink(1)

        # note last spot has largest value
        self.assertEqual([13, 12, 12, 9, 11, 8, 9, 8, 4, 1, 10, 5, 6, 2, 7, 14, 14, 15], A)
        self.assertEqual(15, hs.N)

        # manually advance one step in sorting process
        hs.swap(1, hs.N)
        hs.N -= 1
        hs.sink(1)

        # note last spot has largest value
        self.assertEqual([12, 11, 12, 9, 10, 8, 9, 8, 4, 1, 7, 5, 6, 2, 13, 14, 14, 15], A)
        self.assertEqual(14, hs.N)

    def test_recursive_two(self):
        from ch05.challenge import recursive_two
        answer = tuple(reversed(sorted(BEST_CASE)[-2:]))    # actual results
        self.assertEqual(recursive_two(BEST_CASE), answer)

        # edge cases
        self.assertEqual(recursive_two([1,2]), (2,1))

        # mutable
        my_list = [9, 1, 8, 2, 3, 6]
        my_copy = list(my_list)
        self.assertEqual(recursive_two(my_list), (9, 8))
        self.assertEqual(my_list, my_copy)

        my_list = [9, 1, 8, 2, 3]     # odd-length-list
        my_copy = list(my_list)
        self.assertEqual(recursive_two(my_list), (9, 8))
        self.assertEqual(my_list, my_copy)

    def test_recursive_counting(self):
        from algs.counting import RecordedItem
        from ch05.challenge import recursive_two

        # Must be power of two
        N = 128
        values = tuple(reversed([RecordedItem(k) for k in range(N)]))
        RecordedItem.clear()
        actual = recursive_two(values)
        self.assertEqual(actual[0].val, N-1)
        self.assertEqual(actual[1].val, N-2)
        self.assertEqual(N + N//2 - 2, RecordedItem.report()[1])

    def test_tim_sort(self):
        from ch05.timsort import insertion_sort, merge, tim_sort
        import random
        A=[9,8,7,6,5,4]
        insertion_sort(A, 2, 4)  # Sort from 2 UP TO AND INCLUDING 4
        self.assertEqual([9,8,5,6,7,4], A)
        A=[2,4,6,8,1,3,5,7]
        merge(A, 0, 3, 7, [None]*8)
        self.assertEqual([1,2,3,4,5,6,7,8], A)

        # tim sort on small size array
        A = list(reversed(range(20)))
        tim_sort(A)
        self.assertEqual(list(range(20)), A)

        A = list(range(100))
        random.shuffle(A)
        tim_sort(A)
        self.assertEqual(list(range(100)), A)
        
    def test_rediscover_heap(self):
        from ch05.challenge import rediscover_heap

        result = rediscover_heap(10)
        if 'none found' in result:
            pass
        elif 'found in' in result:
            pass
        else:
            self.fail('should have found a result or not.')

#######################################################################
if __name__ == '__main__':
    unittest.main()
