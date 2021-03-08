"""Test code for Chapter 06."""
import unittest
import random
from ch06.recursive_lists import create_linked_list, reverse, sum_list, sum_iterative
from ch06.recursive_lists import iterate_list

class TestChapter06(unittest.TestCase):

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

        # This raises an exception
        with self.assertRaises(RecursionError):
            sum_list(first)

    def test_reverse(self):
        alist = create_linked_list([4, 3, 2, 1])
        (R, _) = reverse(alist)
        self.assertEqual(1, R.value)
        self.assertEqual(2, R.next.value)
        self.assertEqual(3, R.next.next.value)
        self.assertEqual(4, R.next.next.next.value)

        self.assertEqual(1, reverse(create_linked_list([1]))[0].value)

        with self.assertRaises(AttributeError):
            reverse(None)

    def test_bt(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
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
        bt1.put(5,5)
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
        from ch06.avl import check_avl_property
        bt1 = BinaryTree()
        bt1.insert(7)
        bt1.insert(4)
        bt1.insert(10)
        bt1.insert(8)
        self.assertEqual(2, bt1.root.height)
        check_avl_property(bt1.root)
        bt1.remove(7)
        self.assertEqual(1, bt1.root.height)
        check_avl_property(bt1.root)

    def test_avl_stress(self):
        from ch06.balanced import BinaryTree
        from ch06.avl import check_avl_property

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

    def test_pq_stress(self):
        from ch06.pq import PQ
        from ch06.avl import check_avl_property
        
        pq1 = PQ()
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
        N = 31
        keys = list(range(N))
        for k in keys:
            sy1.put(k, k+1)
            self.assertEqual(list(range(k+1)), [key for key,_ in list(sy1)])
            sy1.put(k,k+2)
        self.assertEqual(list(range(N)), [key for key,_ in list(sy1)])

        # remove keys
        for k in keys:
            sy1.remove(k)
            self.assertEqual(list(range(k+1,N)), [key for key,_ in list(sy1)])

        for k in keys:
            sy1.put(k, k+3)
            self.assertEqual(list(range(k+1)), [key for key,_ in list(sy1)])

        self.assertEqual(list(range(N)), [key for key,_ in list(sy1)])

        # remove in reverse order
        for k in reversed(keys):
            sy1.remove(k)
            self.assertEqual(list(range(k)), [key for key,_ in list(sy1)])

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

    def test_count_rotations_avl(self):
        from ch06.balanced import BinaryTree

        bt1 = BinaryTree()
        for i in [50, 30, 70, 20, 40, 60, 10, 45]:
            bt1.insert(i)

        bt1.insert(5)

    def test_string_structure(self):
        from ch06.tree import BinaryTree
        from ch06.challenge import tree_structure
        bt1 = BinaryTree()
        bt1.insert(5)
        bt1.insert(4)
        bt1.insert(6)
        bt1.insert(2)
        bt1.insert(7)
        bt1.insert(1)
        bt1.insert(3)

        # Prefix representation, with value first, then left and then right
        self.assertEqual('(5,(4,(2,(1,,),(3,,)),),(6,,(7,,)))', tree_structure(bt1.root))

    def test_fibonacci_avl_trees(self):
        from ch06.challenge import fibonacci_avl_tree, rotations
        from ch05.challenge import fib
        from ch06.avl import check_avl_property
        
        tree = fibonacci_avl_tree(8)
        check_avl_property(tree.root)
        self.assertEqual(fib(8), tree.root.value)
        
        # multiple rotations detect when remove lARGEST VALUE
        self.assertTrue(fib(9)-1 in tree)
        tree.remove(fib(9)-1)
        self.assertEqual(3, rotations[0])   # three rotations
        
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
        from ch06.avl import check_avl_property
                
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
        self.assertTrue(tbl.entry(5, 'Height') > 3)   # with 5 nodes, can at least get to 3 or maybe more...

#######################################################################
if __name__ == '__main__':
    unittest.main()
