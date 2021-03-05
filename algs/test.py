"""Test cases for book package."""
import unittest

from algs.counting import RecordedItem
from algs.node import Node
from algs.table import DataTable, Model

class TestHashing(unittest.TestCase):
    """Test cases for book package."""

    def test_counting(self):
        """Test basic mechanics of RecordedItem."""
        ri1 = RecordedItem(1)
        ri2 = RecordedItem(2)

        RecordedItem.clear()
        self.assertTrue(ri1 < ri2)
        self.assertEqual(0, RecordedItem.report()[0])
        self.assertEqual(1, RecordedItem.report()[1])
        self.assertEqual(0, RecordedItem.report()[2])

        RecordedItem.clear()
        self.assertFalse(ri1 > ri2)
        self.assertEqual(0, RecordedItem.report()[0])
        self.assertEqual(0, RecordedItem.report()[1])
        self.assertEqual(1, RecordedItem.report()[2])

        RecordedItem.clear()
        self.assertFalse(ri1 == ri2)
        self.assertEqual(1, RecordedItem.report()[0])
        self.assertEqual(0, RecordedItem.report()[1])
        self.assertEqual(0, RecordedItem.report()[2])

    def test_recorded_item(self):
        self.assertEqual(('eq', 'lt', 'gt'), RecordedItem.header())

    def test_helper(self):
        self.assertEqual([RecordedItem(0), RecordedItem(1)], RecordedItem.range(2))

    def test_node(self):
        n = Node('sample')
        self.assertEqual('[sample]', str(n))

    def test_node_2(self):
        node1 = Node('sample')
        node2 = Node('other', node1)
        self.assertEqual('other', node2.value)
        self.assertEqual('sample', node2.next.value)

        self.assertEqual(['other', 'sample'], list(node2))

    def test_table(self): 
        tbl = DataTable([8, 8, 8], ['N', 'Another', 'SquareRoot'], output=False, decimals=4)
        tbl.format('Another', 'd')
        for n in range(2,10):
            tbl.row([n, n, n ** 0.5])
        self.assertEqual(tbl.entry(3, 'Another'), 3)

        tbl = DataTable([8, 8, 8], ['N', 'Another', 'SquareRoot'], decimals=4)
        tbl.format('Another', 'd')
        for n in range(2,10):
            tbl.row([n, n, n ** 0.5])

        self.assertEqual(list(range(2,10)), tbl.column('Another'))

        model = tbl.best_model('Another')[0]
        self.assertEqual(model[0], Model.LINEAR)
        self.assertAlmostEqual(model[3], 1.0000, places=5)

#######################################################################
if __name__ == '__main__':
    unittest.main()
