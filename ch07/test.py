"""Testing for Chapter 07."""

import unittest

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx
    
class Test_Ch07(unittest.TestCase):

    def test_topological_example(self):
        from ch07.book import topological_example
        DG = nx.DiGraph()
        topological_example(DG, 5)
        print(list(nx.topological_sort(DG)))
        from ch07.digraph_search import topological_sort
        print(list(topological_sort(DG)))
        
    def test_topological_figure(self):
        DG = nx.DiGraph()
        DG.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd')])
        print(list(nx.topological_sort(DG)))
        from ch07.digraph_search import topological_sort
        print(list(topological_sort(DG)))
        
        DG = nx.DiGraph()
        from ch07.book import make_sample_directed_graph
        DG = make_sample_directed_graph()
        print(list(topological_sort(DG)))
    
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

        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(12, G.number_of_edges())
        self.assertEqual(sorted(['C2', 'B3', 'C4']), sorted(list(G['C3'])))
        self.assertEqual(sorted([('C3', 'C2'), ('C3', 'B3'), ('C3', 'C4')]), sorted(list(G.edges('C3'))))

    def test_small_example(self):
        G = nx.Graph()
        self.small_example(G)
        
    def test_small_example_stub_replacement(self):
        import ch07.replacement 
        G = ch07.replacement.Graph()
        self.small_example(G)
        
    def test_representations(self):
        from ch07.replacement import MatrixUndirectedGraph, UndirectedGraph
        self.small_example(UndirectedGraph())
        self.small_example(MatrixUndirectedGraph())

    def test_dijkstra_replacement(self):
        import ch07.replacement 
        DG = ch07.replacement.DiGraph()
        DG.add_edge('a', 'b', weight=6)
        DG.add_edge('a', 'c', weight=10)
        DG.add_edge('b', 'c', weight=2)
        
        from ch07.dijkstra_sp import dijkstra_sp
        (dist_to, edge_to) = dijkstra_sp(DG, 'a')
        self.assertEqual(8, dist_to['c'])
        
    def test_indexed_min_heap(self):
        from ch07.indexed_pq import IndexedMinPQ
        
        impq = IndexedMinPQ(5)
        impq.enqueue(3, 5)
        impq.enqueue(1, 2)
        self.assertEqual(1, impq.dequeue())
        self.assertEqual(3, impq.dequeue())

    def test_imqp_example(self):
        from ch07.dijkstra_sp import dijkstra_sp
        G = nx.DiGraph()
        G.add_edge('a', 'b', weight=6)
        G.add_edge('a', 'c', weight=10)
        G.add_edge('b', 'c', weight=2)
        
        (dist_to, edge_to) = dijkstra_sp(G, 'a')
        self.assertEqual(8, dist_to['c'])
        self.assertEqual('b', edge_to['c'][0])
        self.assertEqual('a', edge_to['b'][0])

    def test_cycle_detection(self):
        from ch07.fibonacci_example import fibonacci_example

        try:
            import tkinter
            from ch07.spreadsheet import Spreadsheet
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

#######################################################################
if __name__ == '__main__':
    unittest.main()
