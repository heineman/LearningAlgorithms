"""Test code for Chapter 06."""
import unittest

class Test_Ch06(unittest.TestCase):

    def test_bt(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        bt1.add(5)
        self.assertTrue(5 in bt1)

        bt1.add(2)
        self.assertEqual(5, bt1.root.value)
        self.assertTrue(2 in bt1)
        self.assertEqual([2, 5], list(bt1))

        bt1.add(1)
        self.assertTrue(1 in bt1)
        self.assertEqual([1, 2, 5], list(bt1))

    def test_bt_remove(self):
        from ch06.tree import BinaryTree

        # delete with left child having right child
        bt1 = BinaryTree()
        bt1.add(5)
        bt1.add(2)
        bt1.add(4)
        bt1.add(7)
        self.assertEqual([2,4,5,7], list(bt1))

        bt1.remove(5)
        self.assertEqual([2,4,7], list(bt1))

        # delete with left child having only left child
        bt2 = BinaryTree()
        bt2.add(5)
        bt2.add(2)
        bt2.add(1)
        bt2.add(7)
        bt2.add(8)
        self.assertEqual([1,2,5,7,8], list(bt2))
        bt2.remove(5)
        self.assertEqual([1,2,7,8], list(bt2))

        # delete with no left child
        bt3 = BinaryTree()
        bt3.add(5)
        bt3.add(7)
        bt3.add(8)
        self.assertEqual([5,7,8], list(bt3))
        bt3.remove(5)
        self.assertEqual([7,8], list(bt3))

        # delete with no children
        bt4 = BinaryTree()
        bt4.add(5)
        self.assertEqual([5], list(bt4))
        bt4.remove(5)
        self.assertEqual([], list(bt4))

    def test_bt_duplicates(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        bt1.add(5)
        bt1.add(5)
        bt1.add(4)
        bt1.add(5)
        self.assertEqual([4,5,5,5], list(bt1))

    def test_bt_stress(self):
        from ch06.tree import BinaryTree

        bt1 = BinaryTree()
        N = 31
        keys = list(range(N))
        n = 0
        for k in keys:
            bt1.add(k)
            n += 1
            self.assertEqual(list(range(k+1)), [v for v in list(bt1)])
            self.assertEqual(n, bt1.size())
        self.assertEqual(list(range(N)), [v for v in list(bt1)])

        # remove in order
        for k in keys:
            bt1.remove(k)
            n -= 1
            self.assertEqual(n, bt1.size())
            self.assertEqual(list(range(k+1,N)), [v for v in list(bt1)])
        self.assertEqual(0, bt1.size())
         
        n = 0
        for k in keys:
            bt1.add(k)
            n += 1
            self.assertEqual(list(range(k+1)), [v for v in list(bt1)])
            self.assertEqual(n, bt1.size())
        self.assertEqual(list(range(N)), [v for v in list(bt1)])  
        
        # remove in reverse order
        for k in reversed(keys):
            bt1.remove(k)
            n -= 1
            self.assertEqual(n, bt1.size())
        self.assertEqual(0, bt1.size())

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

    def test_avl_stress(self):
        from ch06.symbol import BinaryTree

        bt1 = BinaryTree()
        N = 31
        keys = list(range(N))
        n = 0
        for k in keys:
            bt1.put(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(bt1)])
            self.assertEqual(n, bt1.size())
        self.assertEqual(list(range(N)), [key for key,_ in list(bt1)])

        # remove in order
        for k in keys:
            bt1.remove(k)
            n -= 1
            self.assertEqual(list(range(k+1,N)), [key for key,_ in list(bt1)])
            self.assertEqual(n, bt1.size())

        for k in keys:
            bt1.put(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(bt1)])
            self.assertEqual(n, bt1.size())

        self.assertEqual(list(range(N)), [key for key,_ in list(bt1)])

        # remove in reverse order
        for k in reversed(keys):
            bt1.remove(k)
            n -= 1
            self.assertEqual(list(range(k)), [key for key,_ in list(bt1)])
            self.assertEqual(n, bt1.size())

    def test_pq_stress(self):
        from ch06.pq import PQ

        pq1 = PQ()
        N = 31
        keys = list(range(N))
        n = 0
        for k in keys:
            pq1.enqueue(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))
        self.assertEqual(list(range(N)), [key for key,_ in list(pq1)])

        # remove keys
        for k in keys:
            pq1.dequeue()
            n -= 1
            self.assertEqual(list(range(0,N-k-1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))

        for k in keys:
            pq1.enqueue(k, k)
            n += 1
            self.assertEqual(list(range(k+1)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))
        
        self.assertEqual(list(range(N)), [key for key,_ in list(pq1)])

        # remove in reverse order
        for k in reversed(keys):
            pq1.dequeue()
            n -= 1
            self.assertEqual(list(range(k)), [key for key,_ in list(pq1)])
            self.assertEqual(n, len(pq1))

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

#######################################################################
if __name__ == '__main__':
    unittest.main()
