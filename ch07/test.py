"""Testing for Chapter 07."""

import unittest

try:
    import networkx as nx
except ImportError:
    from ch07.graph import Replacement
    nx = Replacement()

class Test_Ch07(unittest.TestCase):

    def test_topological_example(self):
        from ch07.book import topological_example
        DG = nx.DiGraph()
        topological_example(DG, 5)
        print(list(nx.topological_sort(DG)))
    
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

        self.assertEqual(12, len(list(G.nodes())))
        self.assertEqual(12, len(list(G.edges())))
        self.assertEqual(sorted(['C2', 'B3', 'C4']), sorted(list(G['C3'])))
        self.assertEqual(sorted([('C3', 'C2'), ('C3', 'B3'), ('C3', 'C4')]), sorted(list(G.edges('C3'))))

    def test_small_example(self):
        G = nx.Graph()
        self.small_example(G)
        
    def test_small_example_stub_replacement(self):
        from ch07.graph import Replacement
        nx = Replacement()
        G = nx.Graph()
        self.small_example(G)
        
    def test_representations(self):
        from ch07.graph import MatrixUndirectedGraph, UndirectedGraph
        self.small_example(UndirectedGraph())
        self.small_example(MatrixUndirectedGraph())
        
    def test_cycle_detection(self):
        from ch07.spreadsheet import Spreadsheet
        from ch07.fibonacci_example import fibonacci_example
        
        try:
            import tkinter
        except(ImportError):
            print('unable to access tkinter.')
            return
        
        ss = Spreadsheet(tkinter.Tk())
        fibonacci_example(ss)
        try:
            import networkx.algorithms.cycles
            networkx.algorithms.cycles.find_cycle(ss.digraph)
            self.fail('no cycle yet...')
        except:
            pass
        
        try:
            ss.set('B2', '=C5')
            self.fail('should have detected cycle')
        except(RuntimeError):
            pass
        
        # just grab the graph and hack it together
        ss.digraph.add_edge('C5', 'B2')
        #print(networkx.algorithms.cycles.find_cycle(ss.digraph))

if __name__ == '__main__':
    unittest.main()
