"""Testing for Chapter 07."""

import unittest
from algs.table import DataTable, SKIP

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from ch07.dependencies import tkinter_error

class TestChapter7(unittest.TestCase):

    def assert_equal_edges(self, e1, e2):
        """Compare edges but ignore weights."""
        if e1[0] != e2[0]:
            self.fail('{} not same as {}'.format(e1,e2))
        if e1[1] != e2[1]:
            self.fail('{} not same as {}'.format(e1,e2))

    def assert_equal_edges_weights(self, e1, e2):
        """Compare edges and also edge weights."""
        from ch07.replacement import WEIGHT
        self.assert_equal_edges(e1, e2)
        if e1[2][WEIGHT] != e2[2][WEIGHT]:
            self.fail('{} not same as {}'.format(e1,e2))

    def test_distance_to(self):
        from ch07.maze import distance_to
        one   = (2,2)
        two   = (3,4)
        three = (1,0)
        self.assertEqual(3, distance_to(one, two))
        self.assertEqual(6, distance_to(three, two))

    def test_maze(self):
        from ch07.maze import Maze, to_networkx
        import random
        random.seed(15)
        m = Maze(3,5)
        self.assertEqual((0,2), m.start())
        self.assertEqual((2,2), m.end())

        G = to_networkx(m)
        self.assertEqual([(0, 1), (0, 3), (1, 2)], sorted(list(G[(0,2)])))

    def test_bfs_search(self):
        from ch07.maze import Maze, to_networkx, solution_graph
        from ch07.search import bfs_search, path_to, node_from_field
        import random
        random.seed(15)
        m = Maze(3,5)
        G = to_networkx(m)

        # BFS search solution
        node_from = bfs_search(G, m.start())
        self.assertEqual((1,0), node_from[(2,0)])

        # Create graph resulting from the BFS search results
        F = node_from_field(G, node_from)
        self.assertEqual(14, len(list(F.edges())))

        # The actual solution is a two-edge, three node straight path
        H = solution_graph(G, path_to(node_from, m.start(), m.end()))
        self.assertEqual(2, len(list(H.edges())))

    def test_allpairs_sp(self):
        from ch07.all_pairs_sp import floyd_warshall, all_pairs_path_to
        G = nx.Graph()
        G.add_edge('a', 'b', weight=3)
        G.add_edge('a', 'c', weight=5)
        G.add_edge('b', 'c', weight=9)
        G.add_edge('b', 'd', weight=2)
        G.add_edge('d', 'c', weight=1)
        (dist_to, node_from) = floyd_warshall(G)
        path = all_pairs_path_to(node_from, 'b', 'c')
        self.assertEqual(3, dist_to['b']['c'])
        self.assertEqual(['b', 'd', 'c'], path)

        path = all_pairs_path_to(node_from, 'a', 'd')
        self.assertEqual(5, dist_to['a']['d'])
        self.assertEqual(['a', 'b', 'd'], path)

        tbl = DataTable([6,6,6,6,6], ['.', 'a', 'b', 'c', 'd'], output=False)
        tbl.format('.','s')
        for f in 'abcd':
            tbl.format(f, 's')
        for u in 'abcd':
            row = [u]
            for v in 'abcd':
                if node_from[u][v]:
                    row.append(node_from[u][v])
                else:
                    row.append(SKIP)
            tbl.row(row)

        self.assertEqual('d', tbl.entry('b', 'c'))

    def test_allpairs_directed_sp(self):
        from ch07.all_pairs_sp import floyd_warshall, all_pairs_path_to, debug_state
        DG = nx.DiGraph()
        DG.add_edge('a', 'b', weight=4)
        DG.add_edge('b', 'a', weight=2)
        DG.add_edge('a', 'c', weight=3)
        DG.add_edge('b', 'd', weight=5)
        DG.add_edge('c', 'b', weight=6)
        DG.add_edge('d', 'b', weight=1)
        DG.add_edge('d', 'c', weight=7)
        (dist_to, node_from) = floyd_warshall(DG)

        path = all_pairs_path_to(node_from, 'b', 'c')
        self.assertEqual(5, dist_to['b']['c'])
        self.assertEqual(['b', 'a', 'c'], path)

        path = all_pairs_path_to(node_from, 'd', 'c')
        self.assertEqual(6, dist_to['d']['c'])
        self.assertEqual(['d', 'b', 'a', 'c'], path)

        (tbl, tbl_dist_to) = debug_state('test case', DG, node_from, dist_to, output=False)

        tbl_path = DataTable([6,12,12,12,12], ['.', 'a', 'b', 'c', 'd'], output=False)
        tbl_path.format('.','s')
        for f in 'abcd':
            tbl_path.format(f, 's')
        for u in 'abcd':
            path_row = [u]
            for v in 'abcd':
                if u == v:
                    path_row.append(SKIP)
                else:
                    path_row.append('->'.join(all_pairs_path_to(node_from, u, v)))
            tbl_path.row(path_row)

        # edge on shortest path into 'c', when starting from 'd', came from 'a'
        self.assertEqual('d->b->a->c', tbl_path.entry('d', 'c'))
        self.assertEqual(6, tbl_dist_to.entry('d', 'c'))
        self.assertEqual('a', tbl.entry('d', 'c'))

    def test_bellman_ford_negative_cycle_sp(self):
        from ch07.single_source_sp import bellman_ford

        NegCycle = nx.DiGraph()
        NegCycle.add_edge('a', 'b', weight=3)
        NegCycle.add_edge('b', 'c', weight=-2)
        NegCycle.add_edge('c', 'd', weight=-3)
        NegCycle.add_edge('d', 'b', weight=4)
        NegCycle.add_edge('d', 'e', weight=5)

        with self.assertRaises(RuntimeError):
            bellman_ford(NegCycle, 'a')

    def test_bad_dijkstra_sp(self):
        from ch07.single_source_sp import dijkstra_sp

        DG = nx.DiGraph()
        DG.add_edge('a', 'b', weight=3)
        DG.add_edge('a', 'c', weight=1)
        DG.add_edge('c', 'd', weight=1)
        DG.add_edge('b', 'd', weight=-2)
        with self.assertRaises(ValueError):
            dijkstra_sp(DG, 'a')

    def test_dijkstra_sp(self):
        from ch07.single_source_sp import dijkstra_sp, edges_path_to, bellman_ford

        DG = nx.DiGraph()
        DG.add_edge('a', 'b', weight=3)
        DG.add_edge('a', 'c', weight=9)
        DG.add_edge('b', 'c', weight=4)
        DG.add_edge('b', 'd', weight=2)
        DG.add_edge('d', 'c', weight=1)
        (dist_to, edge_to) = dijkstra_sp(DG, 'a')
        path = edges_path_to(edge_to, 'a', 'c')
        self.assertEqual(6, dist_to['c'])
        self.assertEqual(['a', 'b', 'd', 'c'], path)

        (dist_to_bf, edge_to_bf) = bellman_ford(DG, 'a')
        path = edges_path_to(edge_to_bf, 'a', 'c')
        self.assertEqual(6, dist_to_bf['c'])
        self.assertEqual(['a', 'b', 'd', 'c'], path)

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
        self.assertEqual(sorted([('C3', 'C2'), ('C3', 'B3'), ('C3', 'C4')]),
                         sorted(list(G.edges('C3'))))

    def test_small_example(self):
        from ch07.search import dfs_search, path_to
        from ch07.challenge import path_to_recursive
        G = nx.Graph()
        self.small_example(G)

        node_from = dfs_search(G, 'A2')
        self.assertEqual(['A2', 'A3', 'A4', 'A5'], path_to(node_from, 'A2', 'A5'))
        self.assertEqual(['A2', 'A3', 'A4', 'A5'], list(path_to_recursive(node_from, 'A2', 'A5')))

    def test_small_example_stub_replacement(self):
        import ch07.replacement
        G = ch07.replacement.Graph()
        self.small_example(G)

    def test_representations(self):
        from ch07.replacement import MatrixUndirectedGraph, UndirectedGraph
        self.small_example(UndirectedGraph())
        self.small_example(MatrixUndirectedGraph())

    def test_dijkstra_replacement(self):
        from ch07.replacement import WEIGHT, DiGraph
        DG = DiGraph()
        DG.add_edge('a', 'b', weight=6)
        DG.add_edge('a', 'c', weight=10)
        DG.add_edge('b', 'c', weight=2)

        from ch07.single_source_sp import dijkstra_sp
        (dist_to, edge_to) = dijkstra_sp(DG, 'a')
        self.assertEqual(8, dist_to['c'])
        self.assert_equal_edges_weights(('b', 'c', {WEIGHT:2}), edge_to['c'])

    def test_indexed_min_heap(self):
        from ch07.indexed_pq import IndexedMinPQ

        impq = IndexedMinPQ(5)
        impq.enqueue(3, 5)
        impq.enqueue(1, 2)
        self.assertEqual(1, impq.dequeue())
        self.assertEqual(3, impq.dequeue())

    def test_imqp_example(self):
        from ch07.single_source_sp import dijkstra_sp
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

        if tkinter_error:
            pass
        else:
            import tkinter
            from ch07.spreadsheet import Spreadsheet
            ss = Spreadsheet(tkinter.Tk(), nx.DiGraph())
            fibonacci_example(ss)
            try:
                import networkx.algorithms.cycles
                networkx.algorithms.cycles.find_cycle(ss.digraph)
                self.fail('no cycle yet...')
            except Exception:
                pass

            try:
                ss.set('B2', '=C5')
                self.fail('should have detected cycle')
            except RuntimeError:
                pass

            # just grab the graph and hack it together
            ss.digraph.add_edge('C5', 'B2')
            acycle = networkx.algorithms.cycles.find_cycle(ss.digraph)
            self.assertTrue(len(acycle) > 1)

#######################################################################
if __name__ == '__main__':
    unittest.main()
