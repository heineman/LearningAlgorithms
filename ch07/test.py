"""Testing for Chapter 07."""

import unittest

class Test_Ch04(unittest.TestCase):

    def small_example(self, G):
        G.add_node('A2')
        G.add_nodes_from(['A3', 'A4', 'A5'])

        G.add_edge('A2', 'A3')
        G.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

        for i in range(2, 6):
            G.add_edge('B{}'.format(i), 'C{}'.format(i))
            if 2 < i < 5:
                G.add_edge('B{}'.format(i), 'B{}'.format(i+1))
            if i < 5:
                G.add_edge('C{}'.format(i), 'C{}'.format(i+1))

        self.assertEqual(12, len(G.nodes()))
        self.assertEqual(12, len(G.edges()))
        self.assertEqual(['C2', 'B3', 'C4'], list(G['C3']))
        self.assertEqual([('C3', 'C2'), ('C3', 'B3'), ('C3', 'C4')], list(G.edges('C3')))

    def test_small_example(self):
        import networkx as nx
        G = nx.Graph()
        self.small_example(G)
        
    def test_small_example_stub_replacement(self):
        from ch07.graph import Replacement
        nx = Replacement()
        G = nx.Graph()
        self.small_example(G)
