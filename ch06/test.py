"""Test cases for Chapter 06."""

import random
import unittest

from ch06.recursive_lists import create_linked_list, reverse, sum_list, sum_iterative
from ch06.recursive_lists import iterate_list
from ch06.avl import check_avl_property

class TestChapter6(unittest.TestCase):

    # In Python 3.3, this regular expression generates a Deprecation Warning and yields a unit
    # test failure in test_baseline_expression for the "^" operator representing exponentiation
    def test_baseline_expression(self):
        from ch06.expression import Value, build_expression
        num1 = Value(17)
        self.assertEqual(17, num1.eval())

        def exp(left, right):
            """^"""
            return left ** right

        expr = build_expression('((8^2)*(7/4))', new_operators={'^' : exp})
        self.assertEqual(112, expr.eval())

    def test_expression(self):
        from ch06.book import expression_tree, debug_expression
        from ch06.expression import build_expression

        mult7 = expression_tree()
        self.assertEqual(42.0, mult7.eval())
        self.assertEqual('(((3 + 1) / 4) * (((1 + 5) * 9) - (2 * 6)))', str(mult7))

        # Build expression uses floats
        expr = build_expression('(((3 + 1) / 4) * (((1 + 5) * 9) - (2 * 6)))')
        self.assertEqual(42.0, expr.eval())
        self.assertEqual('(((3.0 + 1.0) / 4.0) * (((1.0 + 5.0) * 9.0) - (2.0 * 6.0)))', str(expr))

        mult2 = debug_expression()
        self.assertEqual(54, mult2.eval())
        self.assertEqual('((1 + 5) * 9)', str(mult2))

        def mod(a,b):
            """%"""
            return a % b

        expr = build_expression('((9 % 2) * 5)', new_operators = {'%' : mod})
        self.assertEqual(5.0, expr.eval())
        self.assertEqual([9.0, 2.0, '%', 5.0, '*'], list(expr.postfix()))

        expr = build_expression('(1.9 + 18.232)')
        self.assertEqual(1.9+18.232, expr.eval())

        expr = build_expression('(A1 + 4)')
        self.assertEqual('A1', expr.left.reference)
        self.assertEqual(4.0, expr.right.value)

        expr = build_expression('3')
        self.assertEqual(3.0, expr.value)

    def test_sum_list(self):
        self.assertEqual(0, sum_list(create_linked_list([])))
        self.assertEqual(1, sum_list(create_linked_list([1])))
        self.assertEqual(3, sum_list(create_linked_list([1, 2])))
        self.assertEqual(10, sum_list(create_linked_list([1, 2, 3, 4])))

        self.assertEqual(0, sum_iterative(create_linked_list([])))
        self.assertEqual(1, sum_iterative(create_linked_list([1])))
        self.assertEqual(3, sum_iterative(create_linked_list([1, 2])))
        self.assertEqual(10, sum_iterative(create_linked_list([1, 2, 3, 4])))

    def test_iterate(self):
        alist = create_linked_list([1, 2, 3, 4])
        self.assertEqual([1,2,3,4], list(iterate_list(alist)))

    def test_too_deep_recursion(self):
        from algs.node import Node
        first = n = Node(0)
        for i in range(1,2000):
            n.next = Node(i)
            n = n.next

        self.assertEqual((2000*1999)/2, sum_iterative(first))

        # This raises an exception. With Python 3.5 and higher, this is
        # RecursionError, but to remain compatible with earlier 3.x I've
        # left as a RuntimeError
        with self.assertRaises(RuntimeError):
            sum_list(first)

    def test_reverse(self):
        from ch06.challenge import count
        alist = create_linked_list([4, 3, 2, 1])
        self.assertEqual(1, count(alist, 2))
        (R, _) = reverse(alist)
        self.assertEqual(1, R.value)
        self.assertEqual(2, R.next.value)
        self.assertEqual(3, R.next.next.value)
        self.assertEqual(4, R.next.next.next.value)

        self.assertEqual(1, reverse(create_linked_list([1]))[0].value)

        with self.assertRaises(AttributeError):
            reverse(None)

        alist = create_linked_list([4, 4, 0, 4])
        self.assertEqual(3, count(alist, 4))

    def test_bt(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        self.assertTrue(bt1.remove(7) is None)    # can work even when empty
        self.assertTrue(bt1.min() is None)

        bt1.insert(5)
        self.assertTrue(5 in bt1)

        bt1.insert(2)
        self.assertEqual(5, bt1.root.value)
        self.assertTrue(2 in bt1)
        self.assertEqual([2, 5], list(bt1))

        bt1.insert(1)
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 2, 5], list(bt1))

    def test_bt_remove(self):
        from ch06.tree import BinaryTree

        # delete with left child having right child
        bt1 = BinaryTree()
        bt1.insert(5)
        bt1.insert(2)
        bt1.insert(4)
        bt1.insert(7)
        self.assertEqual([2,4,5,7], list(bt1))

        bt1.remove(5)
        self.assertEqual([2,4,7], list(bt1))

        # delete with left child having only left child
        bt2 = BinaryTree()
        bt2.insert(5)
        bt2.insert(2)
        bt2.insert(1)
        bt2.insert(7)
        bt2.insert(8)
        self.assertEqual([1,2,5,7,8], list(bt2))
        bt2.remove(5)
        self.assertEqual([1,2,7,8], list(bt2))

        # delete with no left child
        bt3 = BinaryTree()
        bt3.insert(5)
        bt3.insert(7)
        bt3.insert(8)
        self.assertEqual([5,7,8], list(bt3))
        bt3.remove(5)
        self.assertEqual([7,8], list(bt3))

        # delete with no children
        bt4 = BinaryTree()
        bt4.insert(5)
        self.assertEqual([5], list(bt4))
        bt4.remove(5)
        self.assertEqual([], list(bt4))

    def test_bt_duplicates(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        bt1.insert(5)
        bt1.insert(5)
        bt1.insert(4)
        bt1.insert(5)
        self.assertEqual([4,5,5,5], list(bt1))

    def test_tree(self):
        from ch06.tree import BinaryTree
        bt1 = BinaryTree()
        for n in [19, 14, 53, 3, 15, 26, 58]:
            bt1.insert(n)

        last = -1
        while not bt1.is_empty():
            m = bt1.min()
            self.assertTrue(m > last)
            last = m
            bt1.remove(m)

    def test_stress(self):
        from ch06.tree import BinaryTree
        bt1 = BinaryTree()
        N = 31
        keys = list(range(N))
        for k in keys:
            bt1.insert(k)
            self.assertEqual(list(range(k+1)), list(bt1))
        self.assertEqual(list(range(N)), list(bt1))

        # remove in order
        for k in keys:
            bt1.remove(k)
            self.assertEqual(list(range(k+1,N)), list(bt1))

        for k in keys:
            bt1.insert(k)
            self.assertEqual(list(range(k+1)), list(bt1))
        self.assertEqual(list(range(N)), list(bt1))

        # remove in reverse order
        for k in reversed(keys):
            bt1.remove(k)

    def test_traversal(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        bt1.insert(23)
        bt1.insert(17)
        bt1.insert(40)
        bt1.insert(30)

        total = 0
        for v in bt1:
            total += v
        self.assertEqual(110, total)

    def test_copy(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        bt1.insert(23)
        bt1.insert(17)
        bt1.insert(40)
        bt1.insert(30)

        bt2 = bt1.copy()

        total = 0
        for v in bt2:
            total += v
        self.assertEqual(110, total)

    def test_bt_stress(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        N = 31
        keys = list(range(N))
        for k in keys:
            bt1.insert(k)
            self.assertEqual(list(range(k+1)), list(bt1))
        self.assertEqual(list(range(N)), list(bt1))

        # remove in order
        for k in keys:
            bt1.remove(k)
            self.assertEqual(list(range(k+1,N)), list(bt1))

        n = 0
        for k in keys:
            bt1.insert(k)
            n += 1
            self.assertEqual(list(range(k+1)), list(bt1))
        self.assertEqual(list(range(N)), list(bt1))

        # remove in reverse order
        for k in reversed(keys):
            bt1.remove(k)

    def test_avl_bt(self):
        from ch06.symbol import BinaryTree

        bt1 = BinaryTree()
        with self.assertRaises(ValueError):
            bt1.put(None, 99)

        self.assertTrue(bt1.remove(None) is None)   # harmless

        self.assertTrue(bt1.is_empty())
        bt1.put(5,5)
        self.assertFalse(bt1.is_empty())
        self.assertEqual('5 -> 5 [0]', str(bt1.root))
        self.assertTrue(5 in bt1)

        bt1.put(3,3)
        self.assertEqual(5, bt1.root.key)
        self.assertTrue(3 in bt1)
        self.assertEqual([3, 5], [key for key,_ in list(bt1)])

        # L-L case
        bt1.put(1,1)
        self.assertEqual(3, bt1.root.key)    # rotate!
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 3, 5], [key for key,_ in list(bt1)])

        self.assertTrue(bt1.get(9999) is None)  # not present

    def test_avl_bt2(self):
        from ch06.symbol import BinaryTree

        bt1 = BinaryTree()
        bt1.put(1,1)
        self.assertTrue(1 in bt1)

        bt1.put(3,3)
        self.assertEqual(1, bt1.root.key)
        self.assertTrue(3 in bt1)
        self.assertEqual([1, 3], [key for key,_ in list(bt1)])

        # R-R case
        bt1.put(5,5)
        self.assertEqual(3, bt1.root.key)    # rotate!
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 3, 5], [key for key,_ in list(bt1)])

    def test_avl_bt3(self):
        from ch06.symbol import BinaryTree

        bt1 = BinaryTree()
        bt1.put(1,1)
        self.assertTrue(1 in bt1)

        bt1.put(5,5)
        self.assertEqual(1, bt1.root.key)
        self.assertTrue(5 in bt1)
        self.assertEqual([1, 5], [key for key,_ in list(bt1)])

        # R-L case
        bt1.put(3,3)
        self.assertEqual(3, bt1.root.key)    # rotate!
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 3, 5], [key for key,_ in list(bt1)])

    def test_avl_bt4(self):
        from ch06.symbol import BinaryTree

        bt1 = BinaryTree()
        bt1.put(5,5)
        self.assertTrue(5 in bt1)

        bt1.put(1,1)
        self.assertEqual(5, bt1.root.key)
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 5], [key for key,_ in list(bt1)])

        # L-R case
        bt1.put(3,3)
        self.assertEqual(3, bt1.root.key)    # rotate!
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 3, 5], [key for key,_ in list(bt1)])

    def test_val_height_valid_on_remove(self):
        from ch06.balanced import BinaryTree
        bt1 = BinaryTree()
        bt1.insert(7)
        self.assertEqual(7, bt1.min())
        bt1.insert(4)
        bt1.insert(10)
        bt1.insert(8)
        self.assertEqual(2, bt1.root.height)
        self.assertEqual(4, bt1.root.size())
        check_avl_property(bt1.root)
        bt1.remove(7)
        self.assertEqual(3, bt1.root.size())
        self.assertEqual(1, bt1.root.height)
        check_avl_property(bt1.root)
        self.assertEqual(4, bt1.min())
        self.assertTrue(4 in bt1)
        self.assertTrue(10 in bt1)
        self.assertTrue(8 in bt1)
        self.assertFalse(7 in bt1)

    def test_avl_stress(self):
        from ch06.balanced import BinaryTree

        bt1 = BinaryTree()
        N = 63
        keys = list(range(N))
        for k in keys:
            bt1.insert(k)
            self.assertEqual(list(range(k+1)), list(bt1))
            check_avl_property(bt1.root)
        self.assertEqual(list(range(N)), list(bt1))

        # remove in order
        for k in keys:
            bt1.remove(k)
            self.assertEqual(list(range(k+1,N)), list(bt1))
            check_avl_property(bt1.root)

        for k in keys:
            bt1.insert(k)
            check_avl_property(bt1.root)
        self.assertEqual(list(range(k+1)), list(bt1))

        self.assertEqual(list(range(N)), list(bt1))

        # remove in reverse order
        for k in reversed(keys):
            bt1.remove(k)
            check_avl_property(bt1.root)
            self.assertEqual(list(range(k)), list(bt1))

        for k in keys:
            bt1.insert(k)
            check_avl_property(bt1.root)
        self.assertEqual(list(range(k+1)), list(bt1))

        self.assertEqual(list(range(N)), list(bt1))

        # remove in random order. This revealed subtle defect in _remove_min()
        shuffled = list(keys)
        random.shuffle(shuffled)
        for k in shuffled:
            bt1.remove(k)
            check_avl_property(bt1.root)

        self.assertTrue(bt1.is_empty())

    def test_binary_tree_from_chapter_06(self):
        from ch06.pq import PQ
        from ch04.test import TestChapter4

        from resources.english import english_words
        words = english_words()
        pair = TestChapter4().priority_queue_stress_test(PQ(), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('formaldehydesulphoxylate'), len('a')), (len(pair[0]), len(pair[1])))

    def test_pq_stress(self):
        from ch06.pq import PQ

        pq1 = PQ()
        self.assertTrue(pq1.is_empty())
        self.assertFalse(pq1.is_full())
        with self.assertRaises(ValueError):
            pq1.enqueue(999, None)

        with self.assertRaises(RuntimeError):
            pq1.peek()

        self.assertFalse(9 in pq1)
        N = 31
        keys = list(range(N))
        n = 0
        for k in keys:
            pq1.enqueue(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))
            check_avl_property(pq1.tree.root)
        self.assertEqual(list(range(N)), [key for key,_ in list(pq1)])

        # remove keys
        for k in keys:
            val1 = pq1.peek()
            val2 = pq1.dequeue()
            self.assertEqual(val1, val2)
            n -= 1
            self.assertEqual(list(range(0,N-k-1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))
            if pq1.tree: check_avl_property(pq1.tree.root)

        for k in keys:
            pq1.enqueue(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))
            check_avl_property(pq1.tree.root)

    def test_symbol_stress(self):
        from ch06.symbol import BinaryTree
        sy1 = BinaryTree()
        N = 127
        keys = list(range(N))
        for k in keys:
            sy1.put(k, k+1)
            self.assertEqual(k+1, sy1.root.size())
            self.assertEqual(list(range(k+1)), [key for key,_ in list(sy1)])
            check_avl_property(sy1.root)
            sy1.put(k,k+2)
        self.assertEqual(list(range(N)), [key for key,_ in list(sy1)])

        # remove keys
        count = sy1.root.size()
        for k in keys:
            sy1.remove(k)
            count -= 1
            if sy1.root:
                check_avl_property(sy1.root)
                self.assertEqual(count, sy1.root.size())
            self.assertEqual(list(range(k+1,N)), [key for key,_ in list(sy1)])

        for k in keys:
            sy1.put(k, k+3)
            self.assertEqual(list(range(k+1)), [key for key,_ in list(sy1)])

        self.assertEqual(list(range(N)), [key for key,_ in list(sy1)])

        # remove in random order
        random.shuffle(keys)
        count = sy1.root.size()
        for k in keys:
            sy1.remove(k)
            count -= 1
            if sy1.root:
                check_avl_property(sy1.root)
                self.assertEqual(count, sy1.root.size())

    def test_insert(self):
        from ch06.book import insert_value
        sample = [2,4,6,7,8,10]
        expected = [2,4,5,6,7,8,10]
        new1 = insert_value(sample, 5)
        self.assertEqual(expected, new1)

        expected = [1,2,4,6,7,8,10]
        new2 = insert_value(sample, 1)
        self.assertEqual(expected, new2)

        expected = [2,4,6,7,8,10,11]
        new3 = insert_value(sample, 11)
        self.assertEqual(expected, new3)

        expected = [2,4,6,7,8,8,10]
        new4 = insert_value(sample, 8)
        self.assertEqual(expected, new4)

    def test_delete(self):
        from ch06.book import remove_value
        sample = [2,4,6,7,8,10]
        expected = [2,4,7,8,10]
        new1 = remove_value(sample, 6)
        self.assertEqual(expected, new1)

        new2 = remove_value(expected,99)    # wasn't there...
        self.assertEqual([2,4,7,8,10], new2)

    def test_count_rotations_avl(self):
        from ch06.balanced import BinaryTree

        bt1 = BinaryTree()
        self.assertTrue(bt1.min() is None)
        for i in [50, 30, 70, 20, 40, 60, 10, 45]:
            bt1.insert(i)
        self.assertEqual(50, bt1.root.value)
        self.assertEqual(30, bt1.root.left.value)
        self.assertEqual(20, bt1.root.left.left.value)
        bt1.insert(5)
        self.assertEqual(10, bt1.root.left.left.value)  # rotate

    def test_string_structure(self):
        from ch06.tree import BinaryTree
        from ch06.challenge import tree_structure
        bt1 = BinaryTree()
        self.assertFalse(99 in bt1)
        bt1.insert(5)
        bt1.insert(4)
        bt1.insert(6)
        bt1.insert(2)
        bt1.insert(7)
        bt1.insert(1)
        bt1.insert(3)

        # Prefix representation, with value first, then left and then right
        self.assertEqual('(5,(4,(2,(1,,),(3,,)),),(6,,(7,,)))', tree_structure(bt1.root))

    def test_all_rotations_challenge(self):
        from ch06.challenge import ObservableBinaryTree
        bt1 = ObservableBinaryTree()
        self.assertTrue(bt1.max_value() is None)
        self.assertTrue(bt1.min_value() is None)
        self.assertTrue(bt1.remove(99) is None)

        vals = list(range(201))
        random.shuffle(vals)
        for v in vals:
            bt1.insert(v)
            check_avl_property(bt1.root)
        for _ in range(10):
            for _ in range(5):
                vmin = bt1.min_value()
                bt1.remove(vmin)
                check_avl_property(bt1.root)
                self.assertFalse(vmin in bt1)
            for _ in range(10):
                bt1.remove(bt1.root.value)
                check_avl_property(bt1.root)
            for _ in range(5):
                bt1.remove(bt1.max_value())
                check_avl_property(bt1.root)

    def test_fibonacci_avl_trees(self):
        from ch06.challenge import fibonacci_avl_tree, rotations
        from ch05.challenge import fib

        tree = fibonacci_avl_tree(8)
        check_avl_property(tree.root)
        self.assertEqual(fib(8), tree.root.value)

        # multiple rotations detect when remove lARGEST VALUE
        last_rotations = rotations[0]
        self.assertTrue(fib(9)-1 in tree)
        tree.remove(fib(9)-1)
        self.assertEqual(3, rotations[0]-last_rotations)   # three rotations

        # Number of rotations continue to increase, every other one
        for n in range(5, 20):
            rotations[0] = 0
            tree = fibonacci_avl_tree(n)
            check_avl_property(tree.root)
            self.assertEqual(fib(n), tree.root.value)
            tree.remove(fib(n)-1)
            check_avl_property(tree.root)
            self.assertEqual((n-1)//2 - 1, rotations[0])

    def test_fill_fibonacci_avl_trees(self):
        from ch06.challenge import fibonacci_avl_tree, rotations
        from ch05.challenge import fib

        tree = fibonacci_avl_tree(6)
        check_avl_property(tree.root)
        orig = tree.root.height
        for i in range(fib(7), 2**(tree.root.height+1)):     # up to a complete tree...
            tree.insert(i)
            check_avl_property(tree.root)
        self.assertTrue(abs(tree.root.height - orig) <= 1)

        # Number of rotations continue to increase. Hope to find some formula
        # to account for these all!
        #    [0, 0, 1, 5, 16, 39, 90, 196, 418, 874, 1809, 3712, 7575, 15389
        for n in range(2, 12):
            rotations[0] = 0

            tree = fibonacci_avl_tree(n)
            check_avl_property(tree.root)
            orig = tree.root.height
            for i in range(fib(n+1), 2**(tree.root.height+1)):     # up to a complete tree...
                tree.insert(i)
                check_avl_property(tree.root)
            self.assertTrue(abs(tree.root.height - orig) <= 1)

    def test_max_heights(self):
        from ch06.challenge import worst_heights
        tbl = worst_heights(max_n=15, output=False)
        self.assertEqual(3, tbl.entry(7, 'WorstHeight'))

    def test_produce_table(self):
        from ch06.challenge import produce_table

        tbl = produce_table(max_k=5, output=False)
        self.assertTrue(tbl.entry(3, 'N') >= 3)

    def test_average_performance(self):
        from ch06.book import average_performance

        tbl = average_performance(max_n = 512, output=False)
        self.assertTrue(tbl.entry(512,'Heap') < tbl.entry(512, 'BinaryTree'))

    def test_generate_list_table(self):
        from ch06.book import generate_list_table

        tbl = generate_list_table(max_k=12, output=False)
        self.assertTrue(tbl.entry(1024,'Remove') < tbl.entry(1024, 'Prepend'))

    def test_compare_avl_pq_with_heap_pq(self):
        from ch06.book import compare_avl_pq_with_heap_pq

        tbl = compare_avl_pq_with_heap_pq(max_k=12, output=False)
        self.assertTrue(tbl.entry(2048,'Heap-pq') <= tbl.entry(2048, 'AVL-pq'))

    def test_compare_dynamic_build_and_access_time(self):
        from ch06.book import compare_dynamic_build_and_access_time

        (build,access) = compare_dynamic_build_and_access_time(repeat=1, num=1, output=False)
        self.assertTrue(build > 0)
        self.assertTrue(access > 0)

    def test_recreate_tree(self):
        from ch06.challenge import recreate_tree, tree_structure
        from ch06.tree import BinaryTree

        root = recreate_tree('(19,,)')
        self.assertEqual('19', root.value)

        root = recreate_tree('(19,3,22)')
        self.assertEqual('3', root.left.value)
        self.assertEqual('22', root.right.value)
        root = recreate_tree('(19,3,(22,21,24))')
        self.assertEqual('3', root.left.value)
        self.assertEqual('22', root.right.value)
        self.assertEqual('21', root.right.left.value)
        self.assertEqual('24', root.right.right.value)

        root = recreate_tree('(26,,(29,,)')
        self.assertEqual('26', root.value)

        root = recreate_tree('(19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))')
        self.assertEqual('19', root.value)
        self.assertEqual(8, root.size())

        # create and flatten again.
        bt1 = BinaryTree()
        bt1.insert(10)
        bt1.insert(15)
        bt1.insert(13)
        bt1.insert(11)
        s = tree_structure(bt1.root)
        self.assertEqual('(10,,(15,(13,(11,,),),))', s)
        n = recreate_tree(s)
        self.assertEqual(s, tree_structure(n))

        bt1 = BinaryTree()
        bt1.insert(12)
        bt1.insert(5)
        s = tree_structure(bt1.root)
        self.assertEqual('(12,(5,,),)', s)
        n = recreate_tree(s)
        self.assertEqual(s, tree_structure(n))

        root = recreate_tree('(26,(23,,),)')
        self.assertEqual('26', root.value)
        
        root = recreate_tree('(23,5,(30,29,))')
        self.assertEqual('23', root.value)

    def test_speaking_tree(self):
        from ch06.speaking import BinaryTree

        bt = BinaryTree()
        self.assertEqual('To insert `5`, create a new subtree with root of `5`.', bt.insert(5))
        self.assertEqual('To insert `3`, `3` is smaller than or equal to `5`, so insert `3` into the left subtree of `5` but there is no left subtree, so create a new subtree with root of `3`.', bt.insert(3))
        self.assertEqual('To insert `1`, `1` is smaller than or equal to `5`, so insert `1` into the left subtree of `5` rooted at `3`. Now `1` is smaller than or equal to `3`, so insert `1` into the left subtree of `3` but there is no left subtree, so create a new subtree with root of `1`.', bt.insert(1))

    def test_stress_recreate(self):
        from ch06.tree import BinaryTree
        from ch06.challenge import tree_structure, recreate_tree
       
        # create all subsets of 1..7
        groups = [[1], [2], [3], [4], [5], [6], [7]]
        for _ in range(6):
            # Create complete tree with three levels.
            for group in groups:
                bt = BinaryTree()
                for x in [4, 2, 6, 1, 3, 5, 7]:
                    bt.insert(x)

                for s in group:
                    bt.remove(s)

                s = tree_structure(bt.root)
                n = recreate_tree(s, int)    # recreate and convert to int
                bt.root = n

                # validate all values BUT in set are found
                for i in range(1, 8):
                    if not i in group:
                        self.assertTrue(i in bt)

            # expand deletions
            new_groups = []
            for group in groups:
                for i in range(1,8):
                    if not i in group:
                        new_groups.append(group + [i])

            groups = new_groups

    def test_produce_height_stats_balanced_integers(self):
        from ch06.challenge import produce_height_stats_balanced_integers

        tbl = produce_height_stats_balanced_integers(max_k=10, output=False)
        self.assertEqual(7, tbl.entry(128, 'height'))

    def test_max_rotations(self):
        from ch06.challenge import find_multiple_rotations, recreate_tree, rotations, ObservableBinaryTree
        extra = 1
        (tree_rep, to_delete) = find_multiple_rotations(extra=extra,
                                        lo=9, hi=30, num_attempts=10000, output=False)
        bt3 = recreate_tree(tree_rep, convert=int)
        tree = ObservableBinaryTree()
        tree.root = bt3
        num_rotations = rotations[0]
        tree.remove(to_delete)
        check_avl_property(tree.root)
        self.assertEqual(num_rotations + extra + 1, rotations[0])  # This exceeds #rotations

    def test_fibonacci_avl(self):
        from ch06.challenge import fibonacci_avl_tree_up_to_2k
        from ch06.challenge import tree_structure

        bt1 = fibonacci_avl_tree_up_to_2k(4)
        self.assertEqual('(3,(2,(1,,),),(5,(4,,),(6,,(7,,))))', tree_structure(bt1.root))

    def test_extract(self):
        from ch06.challenge import extract

        s = extract('this is a (test)', 10)
        self.assertEqual('(test)', s)
        s = extract('this is a (test(bigger))', 10)
        self.assertEqual('(test(bigger))', s)

        with self.assertRaises(ValueError):
            extract('badness', 5)

    def test_challenge_tree(self):
        from ch06.challenge import RankBinaryTree
        
        rbt = RankBinaryTree()
        rbt.insert(8)
        rbt.insert(4)
        rbt.insert(14)
        rbt.insert(5)
        rbt.insert(10)
        
        self.assertEqual(4, rbt.select(0))
        self.assertEqual(5, rbt.select(1))
        self.assertEqual(8, rbt.select(2))
        self.assertEqual(10, rbt.select(3))
        self.assertEqual(14, rbt.select(4))
        
        self.assertEqual(0, rbt.rank(0))    # smaller than all
        self.assertEqual(0, rbt.rank(4))
        self.assertEqual(1, rbt.rank(5))
        self.assertEqual(2, rbt.rank(8))
        self.assertEqual(3, rbt.rank(10))
        self.assertEqual(4, rbt.rank(14))
        self.assertEqual(5, rbt.rank(22))   # bigger than all
        
        self.assertFalse(0 in rbt)
        self.assertTrue(4 in rbt)
        self.assertTrue(5 in rbt)
        self.assertTrue(8 in rbt)
        self.assertTrue(10 in rbt)
        self.assertTrue(14 in rbt)
        self.assertFalse(22 in rbt)

                

        
        

#######################################################################
if __name__ == '__main__':
    unittest.main()

