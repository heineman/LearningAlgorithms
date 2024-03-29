"""Test cases for Chapter 07."""

import unittest
from os import path
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

    def test_guided_search(self):
        from ch07.maze import Maze, to_networkx, solution_graph, distance_to
        from ch07.search import guided_search, path_to, node_from_field
        import random
        random.seed(15)
        m = Maze(3,5)
        G = to_networkx(m)

        # BFS search solution
        node_from = guided_search(G, m.start(), m.end(), distance_to)
        self.assertEqual((1,2), node_from[(2,2)])

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
        G.add_edge('e', 'f', weight=1)   # separate and disconnected edge...
        (dist_to, node_from) = floyd_warshall(G)
        path = all_pairs_path_to(node_from, 'b', 'c')
        self.assertEqual(3, dist_to['b']['c'])
        self.assertEqual(['b', 'd', 'c'], path)

        path = all_pairs_path_to(node_from, 'a', 'd')
        self.assertEqual(5, dist_to['a']['d'])
        self.assertEqual(['a', 'b', 'd'], path)

        with self.assertRaises(ValueError):
            all_pairs_path_to(node_from, 'a', 'e')

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
        from ch07.challenge import bellman_ford_returns_negative_cycle, NegativeCycleError
        neg_cycle = nx.DiGraph()
        neg_cycle.add_edge('a', 'b', weight=1)
        neg_cycle.add_edge('b', 'd', weight=-3)
        neg_cycle.add_edge('d', 'c', weight=5)
        neg_cycle.add_edge('c', 'b', weight=-4)

        with self.assertRaises(RuntimeError):
            bellman_ford(neg_cycle, 'a')

        with self.assertRaises(NegativeCycleError):
            bellman_ford_returns_negative_cycle(neg_cycle, 'a')

        # Validate semantic information in NegativeCycleError: Note that cycle returned is 
        # implementation-specific, so you could choose to only match regExp on weight=-2
        with self.assertRaisesRegex(NegativeCycleError, 'c->d->b->c with weight=-2'):
            bellman_ford_returns_negative_cycle(neg_cycle, 'a')

        no_neg_cycle = nx.DiGraph()
        no_neg_cycle.add_edge('a', 'b', weight=1)
        no_neg_cycle.add_edge('b', 'd', weight=-3)
        no_neg_cycle.add_edge('d', 'c', weight=5)
        no_neg_cycle.add_edge('c', 'b', weight=-1)

        bellman_ford(no_neg_cycle, 'a')
        bellman_ford_returns_negative_cycle(no_neg_cycle, 'a')

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
        DG.add_edge('e', 'f', weight=1)   # separate and disconnected edge...
        (dist_to, edge_to) = dijkstra_sp(DG, 'a')
        path = edges_path_to(edge_to, 'a', 'c')
        self.assertEqual(6, dist_to['c'])
        self.assertEqual(['a', 'b', 'd', 'c'], path)

        with self.assertRaises(ValueError):  # NO PATH!
            edges_path_to(edge_to, 'a', 'f')

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
        """Common example used in chapter 07."""
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
        return G

    def test_small_example(self):
        from ch07.search import dfs_search, path_to
        from ch07.challenge import path_to_recursive
        G = nx.Graph()
        self.small_example(G)

        node_from = dfs_search(G, 'A2')
        self.assertEqual(['A2', 'A3', 'A4', 'A5'], path_to(node_from, 'A2', 'A5'))
        self.assertEqual(['A2', 'A3', 'A4', 'A5'], list(path_to_recursive(node_from, 'A2', 'A5')))

        with self.assertRaises(ValueError):
            path_to(node_from, 'A2', 'B2')    # No path exists
        with self.assertRaises(ValueError):
            # No path exists: force issue by list(...)
            list(path_to_recursive(node_from, 'A2', 'B2'))

    def test_small_example_stub_replacement(self):
        import ch07.replacement
        G = ch07.replacement.Graph()
        self.small_example(G)

    def test_list_stack(self):
        from ch07.list_stack import Stack

        stack = Stack()
        self.assertTrue(stack.is_empty())
        with self.assertRaises(RuntimeError):
            stack.pop()
        stack.push(5)
        self.assertFalse(stack.is_empty())
        self.assertEqual(5, stack.pop())

    def test_representations(self):
        from ch07.replacement import MatrixUndirectedGraph, UndirectedGraph
        self.small_example(UndirectedGraph())
        G = self.small_example(MatrixUndirectedGraph())
        self.assertEqual(['A3'], list(G['A2']))

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
        with self.assertRaises(RuntimeError):
            impq.peek()
        with self.assertRaises(RuntimeError):
            impq.dequeue()
        impq.enqueue(3, 5)

        # can't increase priority
        with self.assertRaises(RuntimeError):
            impq.decrease_priority(3, 999)

        self.assertEqual(3, impq.peek())
        impq.enqueue(1, 2)
        self.assertEqual(2, len(impq))
        self.assertFalse(impq.is_full())
        self.assertTrue(3 in impq)
        self.assertFalse(999 in impq)
        self.assertEqual(1, impq.dequeue())
        self.assertEqual(3, impq.dequeue())
        self.assertTrue(impq.is_empty())
        for i in range(5):
            impq.enqueue(i, i+10)
        self.assertTrue(impq.is_full())

        with self.assertRaises(RuntimeError):
            impq.enqueue(98, 999)

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
        """Deal with inability to have replacement cycle detection."""
        from ch07.fibonacci_example import fibonacci_example

        if tkinter_error:
            pass
        else:
            import tkinter
            from ch07.spreadsheet import Spreadsheet
            ss = Spreadsheet(tkinter.Tk(), nx.DiGraph())
            fibonacci_example(ss)
            if nx.__version__ == 'replacement':
                pass
            else:
                import networkx.algorithms.cycles
                try:
                    networkx.algorithms.cycles.find_cycle(ss.digraph)
                    self.fail('no cycle yet...')
                except networkx.exception.NetworkXNoCycle:
                    pass

            try:
                ss.set('B2', '=C5')
                self.fail('should have detected cycle')
            except RuntimeError:
                pass

            # just grab the graph and hack it together
            ss.digraph.add_edge('C5', 'B2')
            if nx.__version__ == 'replacement':
                pass
            else:
                networkx.algorithms.cycles.find_cycle(ss.digraph)
                acycle = networkx.algorithms.cycles.find_cycle(ss.digraph)
                self.assertTrue(len(acycle) > 1)

    def test_has_cycle_none_exists(self):
        from ch07.digraph_search import has_cycle, has_cycle_nr
        from ch07.digraph_search import recover_cycle, recover_cycle_nr
        G = nx.DiGraph()
        G.add_edge('a', 'b', weight=6)
        G.add_edge('a', 'c', weight=10)
        G.add_edge('b', 'c', weight=2)

        self.assertFalse(has_cycle(G))
        self.assertFalse(has_cycle_nr(G))

        # There are multiple cycles, so no way to check with each other...
        self.assertTrue(len(recover_cycle(G)) == 0)
        self.assertTrue(len(recover_cycle_nr(G)) == 0)

    def test_has_cycle(self):
        from ch07.digraph_search import has_cycle, has_cycle_nr
        from ch07.digraph_search import recover_cycle, recover_cycle_nr
        G = nx.DiGraph()
        G.add_edge('a', 'b', weight=6)
        G.add_edge('a', 'c', weight=10)
        G.add_edge('b', 'c', weight=2)
        G.add_edge('c', 'd', weight=1)
        G.add_edge('d', 'e', weight=1)

        self.assertFalse(has_cycle(G))
        self.assertFalse(has_cycle_nr(G))

        G.add_edge('e', 'a', weight=1)
        self.assertTrue(has_cycle(G))
        self.assertTrue(has_cycle_nr(G))

        # There are multiple cycles, so no way to check with each other...
        self.assertTrue(len(recover_cycle(G)) > 0)
        self.assertTrue(len(recover_cycle_nr(G)) > 0)

        # However, both cycles contain 'e'
        self.assertTrue('e' in recover_cycle(G))
        self.assertTrue('e' in recover_cycle_nr(G))

    def test_topological_table(self):
        from ch07.book import table_topological_example
        tbl = table_topological_example(max_k=4, output=False)
        self.assertEqual(336, tbl.entry(64, 'E'))

    def test_table_compare_graph_structures(self):
        from ch07.book import table_compare_graph_structures

        tbl = table_compare_graph_structures(max_k=12)
        self.assertTrue(tbl.entry(2048, 'NetworkX') < tbl.entry(2048, 'Adjacency Matrix'))

    def test_generate_guided_search_figure(self):
        from ch07.book import generate_guided_search_figure
        from ch07.tmg_load import tmg_load, highway_map, bounding_ids
        from ch07.dependencies import plt_error

        if not plt_error:
            (G, positions, _) = tmg_load(highway_map())
            (_, EAST, _, WEST) = bounding_ids(positions)
            output_file = generate_guided_search_figure(G, positions, WEST, EAST)
            self.assertTrue(path.isfile(output_file))

    def test_bounding(self):
        from ch07.tmg_load import tmg_load, highway_map, bounding_ids
        (_, positions, _) = tmg_load(highway_map())
        (NORTH, EAST, SOUTH, WEST) = bounding_ids(positions)
        self.assertTrue(positions[NORTH][0] > positions[SOUTH][0])   # LAT Is higher for north
        self.assertTrue(positions[EAST][1] > positions[WEST][1])     # LONG is higher for east

    def test_recursive_dfs(self):
        from ch07.challenge import dfs_search_recursive, path_to_recursive
        G = nx.Graph()
        for i in range(100):
            G.add_edge(i,i+1)

        node_from = dfs_search_recursive(G, 0)
        self.assertEqual(98, node_from[99])
        path = path_to_recursive(node_from, 0, 99)
        self.assertEqual(list(range(100)), list(path))

    def test_xslx_loading(self):
        """
        Load up sample XLSX Microsoft Excel file as a Spreadsheet. Check for resource
        file either in parent/resources our current resources/
        """
        import os
        from ch07.xlsx_loader import load_xlsx
        try:
            entries = load_xlsx(os.path.join('..', 'resources', 'ch07-fibonacci-example.xlsx'))
            self.assertEqual('=(B5 + B6)', entries.get('B7'))
        except FileNotFoundError:
            entries = load_xlsx(os.path.join('resources', 'ch07-fibonacci-example.xlsx'))
            self.assertEqual('=(B5 + B6)', entries.get('B7'))

    def test_dag_shortest(self):
        """Validate same answer from Dijkstra and Topological shortest path on sample mesh."""
        from ch07.challenge import mesh_graph, topological_sp
        from ch07.single_source_sp import dijkstra_sp
        N = 10
        DAG = mesh_graph(N)
        (dist_to, _) = dijkstra_sp(DAG, 1)
        (dist_to_topol, _) = topological_sp(DAG, 1)
        self.assertEqual(dist_to[N*N], dist_to_topol[N*N])

#######################################################################
if __name__ == '__main__':
    unittest.main()
