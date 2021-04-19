"""
Home-grown replacement for networkx IN CASE this package is not found.
This implementation is not meant to be production-quality, but simply
a stub object that provides a reasonable implementation.

Note: Doesn't offer capability to draw graphs.
"""
import unittest
from algs.node import Node

# data associated with an edge can contain a weight
WEIGHT = 'weight'

# Used to declare (if needed) that we are providing stub replacement for networkx.
__version__ = 'replacement'

class UndirectedGraph:
    """
    Use Dictionary to store all vertices. Values are lists of neighboring nodes.
    """
    def __init__(self):
        self.adjacency = {}
        self.positions = {}
        self.weights   = {}
        self.E         = 0

    def add_node(self, u, pos=None):
        """Add node to graph, if not already there."""
        if u in self.adjacency:
            return
        self.adjacency[u] = None
        self.positions[u] = pos

    def add_nodes_from(self, nodes):
        """Add nodes to graph, if not already there."""
        for n in nodes:
            self.add_node(n)

    def __getitem__(self, u):
        """Get neighboring nodes to this node."""
        for node in self.adjacency[u]:
            yield node

    def number_of_nodes(self):
        """Return number of nodes in graph."""
        return len(self.adjacency)

    def nodes(self):
        """Return all nodes."""
        return self.adjacency.keys()

    def edges(self, u=None, data=True):
        """
        Return all edges. Make sure not to double count. data argument is present
        to align with networkx, and it must be here to provide a suitable replacement.
        """
        all_nodes = list(self.nodes())

        if u:
            n = self.adjacency[u]
            while n:
                yield (u, n.value)
                n = n.next
        else:
            seen = []
            for u in all_nodes:
                n = self.adjacency[u]
                while n:
                    if not n.value in seen:
                        yield (u, n.value)
                    n = n.next
                seen.append(u)

    def number_of_edges(self):
        """Return number of edges in graph."""
        return self.E

    def neighbors(self, u):
        """Return neighboring nodes."""
        for node in self.adjacency[u]:
            yield node

    def add_edge(self, u, v):
        """Add edge (u,v) to a graph."""
        if not u in self.adjacency:
            self.adjacency[u] = None

        if not v in self.adjacency:
            self.adjacency[v] = None

        n = self.adjacency[u]
        while n:
            if n.value == v:
                return   # already there
            n = n.next

        self.adjacency[u] = Node(v, self.adjacency[u])
        self.adjacency[v] = Node(u, self.adjacency[v])
        self.E += 1

    def add_edges_from(self, edges):
        """Add edges to graph, if not already there."""
        for u,v in edges:
            self.add_edge(u,v)

class AdjacencyViewer:
    """Provide object to iterate over adjacent nodes."""
    def __init__(self, mat, i, neighbors):
        self.mat = mat
        self.i = i
        self.neighbors = neighbors

    def __getitem__(self, target):
        """Get neighboring nodes to this node by iterating over all nodes."""
        for j in self.neighbors:
            if j == target:
                if (self.i, j) in self.mat.weights:
                    return (self.mat.labels[self.i], self.mat.labels[j], {WEIGHT: self.mat.weights[(self.i,j)]})
                return (self.mat.labels[self.i], self.mat.labels[j])
        return None

    def __iter__(self):
        for j in self.neighbors:
            if (self.i, j) in self.mat.weights:
                yield (self.mat.labels[j], {WEIGHT: self.mat.weights[(self.i,j)]})
            else:
                yield self.mat.labels[j]

class MatrixUndirectedGraph:
    """
    Use Two Dimensional Matrix to store whether there is an edge between U and V.
    """
    NO_EDGE = float('-inf')

    def __init__(self):
        self.matrix = None
        self.positions = {}
        self.labels    = []
        self.weights   = {}
        self.E         = 0

    def add_node(self, u, pos=None):
        """Add node to graph, if not already there."""
        if u in self.labels:
            return
        self.labels.append(u)
        self.positions[u] = pos
        N = len(self.labels)

        # Either initialize 1x1 matrix or extend with new column and one new '0' in each column.
        if self.matrix is None:
            self.matrix =  [[MatrixUndirectedGraph.NO_EDGE] * 1] * 1
        else:
            self.matrix.append([MatrixUndirectedGraph.NO_EDGE] * (N-1))
            for i in range(N):
                self.matrix[i].append(MatrixUndirectedGraph.NO_EDGE)

    def add_nodes_from(self, nodes):
        """Add nodes to graph, if not already there."""
        for n in nodes:
            self.add_node(n)

    def __getitem__(self, u):
        """Get neighboring nodes to this node by iterating over all nodes."""
        idx = self.labels.index(u)
        neighbors = {}
        for j in range(len(self.labels)):
            if self.matrix[idx][j] != MatrixUndirectedGraph.NO_EDGE:
                neighbors[j] = self.matrix[idx][j]
        return AdjacencyViewer(self, idx, neighbors)

    def number_of_nodes(self):
        """Return number of nodes in graph."""
        return len(self.labels)

    def nodes(self):
        """Return all nodes."""
        for n in self.labels:
            yield n

    def edges(self, u=None, data=True):
        """Return all edges. Make sure not to double count..."""
        if u:
            idx = self.labels.index(u)
            for j in range(len(self.labels)):
                if self.matrix[idx][j] != MatrixUndirectedGraph.NO_EDGE:
                    u,v = self.labels[idx], self.labels[j]
                    if (idx,j) in self.weights and data:
                        yield (u, v, {WEIGHT: self.weights[(idx,j)]})
                    else:
                        yield (u, v)
        else:
            for i in range(len(self.labels)-1):
                for j in range(i+1, len(self.labels)):
                    if self.matrix[i][j] != MatrixUndirectedGraph.NO_EDGE:
                        u,v = self.labels[i], self.labels[j]
                        if (i,j) in self.weights and data:
                            yield (u, v, {WEIGHT: self.weights[(i,j)]})
                        else:
                            yield (u, v)

    def get_edge_data(self, u, v):
        """Return weight for edge."""
        if not u in self.labels:
            return None

        if not v in self.labels:
            return None

        i = self.labels.index(u)
        j = self.labels.index(v)
        if self.matrix[i][j] == MatrixUndirectedGraph.NO_EDGE:
            return None
        return {WEIGHT: self.weights[(i,j)]}

    def number_of_edges(self):
        """Return number of edges in graph."""
        return self.E

    def neighbors(self, u):
        """Return neighboring nodes."""
        idx = self.labels.index(u)
        for j in range(len(self.labels)):
            if self.matrix[idx][j] != MatrixUndirectedGraph.NO_EDGE:
                yield self.labels[j]

    def add_edge(self, u, v, weight=None):
        """Add edge (u,v) to a graph."""
        if not u in self.labels:
            self.add_node(u)

        if not v in self.labels:
            self.add_node(v)

        if weight == MatrixUndirectedGraph.NO_EDGE:
            raise ValueError('{} is reserved to represent that edge does not exist.'.format(weight))

        # already there
        i = self.labels.index(u)
        j = self.labels.index(v)
        if self.matrix[i][j] != MatrixUndirectedGraph.NO_EDGE:
            return
        self.matrix[i][j] = True
        self.matrix[j][i] = True
        self.E += 1
        if weight:
            self.weights[(i,j)] = weight
            self.weights[(j,i)] = weight

    def remove_edge(self, u, v):
        """Remove edge from u => v."""
        if not u in self.labels:
            return

        if not v in self.labels:
            return

        # Not present? leave now
        i = self.labels.index(u)
        j = self.labels.index(v)
        if self.matrix[i][j] == MatrixUndirectedGraph.NO_EDGE:
            return

        self.matrix[i][j] = MatrixUndirectedGraph.NO_EDGE
        self.matrix[j][i] = MatrixUndirectedGraph.NO_EDGE
        self.E -= 1
        if (i,j) in self.weights:
            self.weights.pop((i,j), None)
            self.weights.pop((j,i), None)

    def add_edges_from(self, edges):
        """Add edges to graph, if not already there."""
        for triple in edges:
            if len(triple) == 2:
                self.add_edge(triple[0],triple[1])
            elif len(triple) == 3:
                weight = MatrixUndirectedGraph.NO_EDGE
                if WEIGHT in triple[2]:
                    weight = triple[2][WEIGHT]
                if weight == MatrixUndirectedGraph.NO_EDGE:
                    raise ValueError('Unable to process {}'.format(triple))
                self.add_edge(triple[0],triple[1], weight)
            else:
                raise ValueError('Unable to process {}'.format(triple))

class DirectedGraph:
    """
    Use Dictionary to store all vertices. Values are lists of neighboring nodes.
    """
    def __init__(self):
        self.adjacency = {}
        self.positions = {}
        self.weights   = {}
        self.E         = 0

    def __contains__(self, v):
        """Determine if v is in the graph."""
        return v in self.adjacency

    def add_node(self, u, pos=None):
        """Add node to graph, if not already there."""
        if u in self.adjacency:
            return
        self.adjacency[u] = []
        self.positions[u] = pos

    def add_nodes_from(self, nodes):
        """Add nodes to graph, if not already there."""
        for n in nodes:
            self.add_node(n)

    def __getitem__(self, u):
        """Get neighboring nodes to this node."""
        if u in self.adjacency:
            for node in self.adjacency[u]:
                yield node

    def get_edge_data(self, u, v):
        """Return weight for edge."""
        if not u in self.adjacency:
            return None

        if not v in self.adjacency[u]:
            return None

        return {WEIGHT: self.weights[(u,v)]}

    def nodes(self):
        """Return all nodes."""
        return self.adjacency.keys()

    def number_of_nodes(self):
        """Return number of nodes in graph."""
        return len(self.adjacency)

    def edges(self, u=None, data=True):
        """Return all edges, with weights as optional data."""
        if u:
            for v in self.adjacency[u]:
                if (u,v) in self.weights and data:
                    yield (u, v, {WEIGHT: self.weights[(u,v)]})
                else:
                    yield (u, v)
        else:
            for u in self.nodes():
                for v in self.adjacency[u]:
                    if (u,v) in self.weights and data:
                        yield (u, v, {WEIGHT: self.weights[(u,v)]})
                    else:
                        yield (u, v)

    def number_of_edges(self):
        """Return number of edges in graph."""
        return self.E

    def add_edge(self, u, v, weight=None):
        """Add edge from u => v with optional weight associated with edge."""
        if not u in self.adjacency:
            self.adjacency[u] = []

        if not v in self.adjacency:
            self.adjacency[v] = []

        # already there
        if v in self.adjacency[u]:
            return
        self.adjacency[u].append(v)
        self.E += 1
        if weight:
            self.weights[(u,v)] = weight

    def remove_edge(self, u, v):
        """Remove edge from u => v."""
        if not u in self.adjacency:
            return

        if not v in self.adjacency:
            return

        # Not present? leave now
        if not v in self.adjacency[u]:
            return

        self.adjacency[u].remove(v)
        self.E -= 1
        if (u,v) in self.weights:
            self.weights.pop((u,v), None)

    def add_edges_from(self, edges):
        """Add edges to graph, if not already there."""
        for edge in edges:
            if len(edge) == 2:
                self.add_edge(edge[0], edge[1])
            else:
                self.add_edge(edge[0], edge[1], edge[2])    # weights

class Graph(MatrixUndirectedGraph):
    """Replacement graph structure for undirected graphs."""
    def __init__(self):
        MatrixUndirectedGraph.__init__(self)

class DiGraph(DirectedGraph):
    """Replacement graph structure for directed graphs."""
    def __init__(self):
        DirectedGraph.__init__(self)

def single_source_shortest_path(graph, src):
    """
    Act on Single Source Shortest Path and return path as dictionary, where
    each node is expanded to have its
    """
    from ch07.single_source_sp import dijkstra_sp
    (_, edge_to) = dijkstra_sp(graph, src)

    expanded = {}
    for n in graph.nodes():
        if n == src:
            expanded[src] = []
        else:
            path = []
            t = n
            while t != src:
                path.insert(0, t)
                t = edge_to[t][0]
            path.insert(0, src)
            expanded[n] = path

    return expanded

def topological_sort(digraph):
    """Link in with Topological sort."""
    from ch07.digraph_search import topological_sort as ts
    return ts(digraph)

def get_node_attributes(graph, pos='pos'):
    """I am not going to provide this capability; must have 'pos' to conform to networkx."""
    return graph.positions

def draw(graph, pos, with_labels = True, node_color='w', font_size=8, ax=None):
    """I am not going to provide this capability."""
    return

def dijkstra_path(G, src, target):
    """Dijkstra delegation."""
    from ch07.single_source_sp import dijkstra_sp

    return dijkstra_sp(G, src, target)

#######################################################################
# Test case is here so replacement can be tested independently of whether
# networkx is installed on your computer or not.
#######################################################################

class TestChapter7(unittest.TestCase):
    def test_directed_graph(self):
        DG = DirectedGraph()

        DG.add_edge('A2', 'A3')
        DG.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

        edge_list = [ ('B{}'.format(i), 'C{}'.format(i)) for i in range(2,6)]
        DG.add_edges_from(edge_list)
        for i in range(2, 6):
            if 2 < i < 5:
                DG.add_edge('B{}'.format(i), 'B{}'.format(i+1))
            if i < 5:
                DG.add_edge('C{}'.format(i), 'C{}'.format(i+1))

        self.assertEqual(12, DG.number_of_nodes())
        self.assertEqual(12, DG.number_of_edges())
        self.assertEqual(sorted(['B5', 'C4']), sorted(list(DG['B4'])))
        self.assertEqual(sorted([('C3', 'C4')]),
                         sorted(list(DG.edges('C3'))))

        DG.remove_edge('C3', 'C4')
        self.assertEqual(12, DG.number_of_nodes())
        self.assertEqual(11, DG.number_of_edges())
        self.assertEqual(sorted(['B4', 'C3']), sorted(list(DG['B3'])))
        self.assertEqual(sorted([('B3', 'B4'), ('B3', 'C3')]),
                         sorted(list(DG.edges('B3'))))

    def test_undirected_graph(self):
        G = UndirectedGraph()
        G.add_edge('A2', 'A3')
        self.assertEqual(2, len(list(G.nodes())))
        G.add_node('A2')   # has no effect
        self.assertEqual(2, len(list(G.nodes())))
        G.add_edge('A2', 'A3')   # confirm doesn't have an effect...

        self.assertEqual(['A2', 'A3'], sorted(list(G.nodes())))
        G.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

        self.assertEqual(['A2', 'A4'], sorted(list(G.neighbors('A3'))))

        self.assertEqual([('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5')], sorted(list(G.edges())))

        edge_list = [ ('B{}'.format(i), 'C{}'.format(i)) for i in range(2,6)]
        G.add_edges_from(edge_list)
        self.assertEqual(sorted(edge_list + [('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5')]), sorted(list(G.edges())))
        for i in range(2, 6):
            if 2 < i < 5:
                G.add_edge('B{}'.format(i), 'B{}'.format(i+1))
            if i < 5:
                G.add_edge('C{}'.format(i), 'C{}'.format(i+1))

        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(12, G.number_of_edges())
        self.assertEqual(sorted(['B3', 'B5', 'C4']), sorted(list(G['B4'])))
        self.assertEqual(sorted([('C3', 'B3'), ('C3', 'C2'), ('C3', 'C4')]),
                         sorted(list(G.edges('C3'))))

    def test_matrix_undirected_graph(self):
        G = MatrixUndirectedGraph()

        G.add_edge('A2', 'A3')
        self.assertEqual(2, len(list(G.nodes())))
        G.add_node('A2')   # has no effect
        self.assertEqual(2, len(list(G.nodes())))
        G.add_edge('A2', 'A3')   # confirm doesn't have an effect...

        self.assertEqual(['A2', 'A3'], sorted(list(G.nodes())))
        G.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

        self.assertEqual(['A2', 'A4'], sorted(list(G.neighbors('A3'))))

        self.assertEqual([('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5')], sorted(list(G.edges())))

        edge_list = [ ('B{}'.format(i), 'C{}'.format(i)) for i in range(2,6)]
        G.add_edges_from(edge_list)
        self.assertEqual(sorted(edge_list + [('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5')]), sorted(list(G.edges())))
        for i in range(2, 6):
            if 2 < i < 5:
                G.add_edge('B{}'.format(i), 'B{}'.format(i+1))
            if i < 5:
                G.add_edge('C{}'.format(i), 'C{}'.format(i+1))

        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(12, G.number_of_edges())
        self.assertEqual(sorted(['B3', 'B5', 'C4']), sorted(list(G['B4'])))
        self.assertEqual(sorted([('C3', 'B3'), ('C3', 'C2'), ('C3', 'C4')]),
                         sorted(list(G.edges('C3'))))

        G.remove_edge('C3', 'C4')
        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(11, G.number_of_edges())
        self.assertEqual(sorted(['B4', 'C3']), sorted(list(G['B3'])))
        self.assertEqual(sorted([('B3', 'B4'), ('B3', 'C3')]),
                         sorted(list(G.edges('B3'))))

    def test_matrix_undirected_graph_weighted(self):
        G = MatrixUndirectedGraph()

        with self.assertRaises(ValueError):
            G.add_edge('A2', 'A3', weight=MatrixUndirectedGraph.NO_EDGE)

        G.add_edge('A2', 'A3', weight=1)
        self.assertEqual([('A2', 'A3', {'weight': 1})], list(G.edges()))

        self.assertEqual(1, G.get_edge_data('A2', 'A3')[WEIGHT])
        self.assertTrue(G.get_edge_data('A2', 'Nothing') is None)
        self.assertTrue(G.get_edge_data('Nothing', 'A2') is None)

        G.add_edge('A2', 'A3', weight=2)   # confirm doesn't have an effect. First one there gets it.
        self.assertEqual([('A2', 'A3', {'weight': 1})], list(G.edges()))

        self.assertEqual(['A2', 'A3'], sorted(list(G.nodes())))
        G.add_edges_from([('A3', 'A4', {'weight': 2}), ('A4', 'A5', {'weight': 3})])

        self.assertTrue(G.get_edge_data('A2', 'A4') is None)
        self.assertEqual(['A3'], list(G.neighbors('A2')))

        edge_list = [ ('B{}'.format(i), 'C{}'.format(i), {'weight': 2}) for i in range(2,6)]
        G.add_edges_from(edge_list)
        self.assertEqual(sorted(edge_list + [('A2', 'A3', {'weight': 1}), ('A3', 'A4', {'weight': 2}), ('A4', 'A5', {'weight': 3})]), sorted(list(G.edges())))
        for i in range(2, 6):
            if 2 < i < 5:
                G.add_edge('B{}'.format(i), 'B{}'.format(i+1), weight=i)
            if i < 5:
                G.add_edge('C{}'.format(i), 'C{}'.format(i+1), weight=1)

        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(12, G.number_of_edges())
        self.assertEqual([('B3', {'weight': 3}), ('B5', {'weight': 4}), ('C4', {'weight': 2})], sorted(list(G['B4'])))
        self.assertEqual(sorted([('C3', 'B3', {'weight': 2}), ('C3', 'C2', {'weight': 1}), ('C3', 'C4', {'weight': 1})]),
                         sorted(list(G.edges('C3'))))

        G.remove_edge('C3', 'C4')
        self.assertEqual(12, G.number_of_nodes())
        self.assertEqual(11, G.number_of_edges())
        self.assertEqual(sorted([('C3', {'weight': 2}), ('B4', {'weight': 3})]), sorted(list(G['B3'])))
        self.assertEqual(sorted([('B3', 'B4', {'weight': 3}), ('B3', 'C3', {'weight': 2})]),
                         sorted(list(G.edges('B3'))))

        self.assertEqual(11, len(list(G.edges())))
        G.remove_edge('A2', 'nothing')  # NO IMPACT
        G.remove_edge('nothing', 'A2')  # NO IMPACT

        G.remove_edge('A2', 'A3')
        self.assertEqual(10, len(list(G.edges())))

    def test_matrix_directed_graph_weighted(self):
        DG = DirectedGraph()

        DG.add_edge('A2', 'A3', 1)
        self.assertEqual([('A2', 'A3', {'weight': 1})], list(DG.edges()))

        self.assertEqual(1, DG.get_edge_data('A2', 'A3')[WEIGHT])
        self.assertTrue(DG.get_edge_data('A2', 'Nothing') is None)
        self.assertTrue(DG.get_edge_data('Nothing', 'A2') is None)

        DG.add_edge('A2', 'A3', weight=2)   # confirm doesn't have an effect.
        self.assertEqual([('A2', 'A3', {'weight': 1})], list(DG.edges()))

        self.assertEqual(['A2', 'A3'], sorted(list(DG.nodes())))
        DG.add_edges_from([('A3', 'A4', 2), ('A4', 'A5', 3)])

        self.assertTrue(DG.get_edge_data('A2', 'A4') is None)

        edge_list = [ ('B{}'.format(i), 'C{}'.format(i)) for i in range(2,6)]
        DG.add_edges_from(edge_list)
        self.assertEqual(sorted(edge_list + [('A2', 'A3', {'weight': 1}), ('A3', 'A4', {'weight': 2}), ('A4', 'A5', {'weight': 3})]), sorted(list(DG.edges())))
        for i in range(2, 6):
            if 2 < i < 5:
                DG.add_edge('B{}'.format(i), 'B{}'.format(i+1))
            if i < 5:
                DG.add_edge('C{}'.format(i), 'C{}'.format(i+1))

        self.assertEqual(12, DG.number_of_nodes())
        self.assertEqual(12, DG.number_of_edges())
        self.assertEqual(sorted(['B5', 'C4']), sorted(list(DG['B4'])))
        self.assertEqual(sorted([('C3', 'C4')]), sorted(list(DG.edges('C3'))))

        DG.remove_edge('C3', 'C4')
        self.assertEqual(12, DG.number_of_nodes())
        self.assertEqual(11, DG.number_of_edges())
        self.assertEqual(sorted(['B4', 'C3']), sorted(list(DG['B3'])))
        self.assertEqual(sorted([('B3', 'B4'), ('B3', 'C3')]),
                         sorted(list(DG.edges('B3'))))

        self.assertEqual(11, len(list(DG.edges())))
        DG.remove_edge('A2', 'nothing')  # NO IMPACT
        DG.remove_edge('nothing', 'A2')  # NO IMPACT

        DG.remove_edge('A2', 'A3')
        self.assertEqual(10, len(list(DG.edges())))

    def test_dijkstra_sp(self):
        DG = DirectedGraph()
        DG.add_edge('a', 'b', weight=3)
        DG.add_edge('a', 'c', weight=9)
        DG.add_edge('b', 'c', weight=4)
        DG.add_edge('b', 'd', weight=2)
        DG.add_edge('d', 'c', weight=1)
        expanded = single_source_shortest_path(DG, 'a')
        path = expanded['c']
        self.assertEqual(['a', 'b', 'd', 'c'], path)

#######################################################################
if __name__ == '__main__':
    unittest.main()
