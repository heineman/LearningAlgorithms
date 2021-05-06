"""
Code to blindly search through a Graph in Depth First and Breadth First strategies. Also
contains a rudimentary Guided Search for undirected graphs when there is a metric showing
how far a node is from the target.
"""
import random
try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from ch07.dependencies import plt_error
from ch07.maze import Maze, to_networkx, solution_graph, node_from_field
from ch04.list_queue import Queue

def path_to(node_from, src, target):
    """
    Given a dictionary that results from a search, reproduce path from original src
    to target. Have to follow the node_from in reverse order, which is why the
    nodes discovered are all inserted at index position 0 in the path.

    Performance is O(N) since a path could involve all nodes, in the worst case.
    """
    if not target in node_from:
        raise ValueError('{} is unreachable from {}'.format(target,src))

    path = []
    v = target
    while v != src:
        path.append(v)
        v = node_from[v]
    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path

def dfs_search_recursive(G, src):
    """
    Apply Depth First Search to a graph from src. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.

    Warning: This code is likely to cause a RecursionError when applied
    to a graph with thousands of nodes, because Python sets the recursion
    limit to about 1000.
    """
    marked = {}
    node_from = {}

    def dfs(v):
        marked[v] = True

        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                dfs(w)

    dfs(src)
    return node_from

def dfs_search(G, src):
    """
    Apply non-recursive Depth First Search to a graph from src. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    from ch07.list_stack import Stack
    marked = {}
    node_from = {}

    stack = Stack()
    stack.push(src)
    marked[src] = True

    while not stack.is_empty():
        v = stack.pop()
        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                stack.push(w)

    return node_from

def bfs_search(G, src):
    """
    Apply Depth First Search to a graph from a starting node. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    marked = {}
    node_from = {}

    q = Queue()
    q.enqueue(src)
    marked[src] = True

    while not q.is_empty():
        v = q.dequeue()
        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                q.enqueue(w)

    return node_from

def guided_search(G, src, target, distance):
    """
    Non-recursive depth-first search investigating given position. Needs
    a distance (node1, node2) function to determine distance between two nodes.

    Performance is O(N log N + E) since every edge is visited once for a directed
    graph and twice for an undirected graph. Each of the N nodes is processed by
    the priority queue, where dequeue() and enqueue() operations are each O(log N).
    While it is unlikely that the priority queue will ever contain N nodes, the
    worst case possibility always exists.
    """
    from ch04.heap import PQ
    pq = PQ(G.number_of_nodes())
    marked = {}
    node_from = {}

    dist_to = {}
    dist_to[src] = 0
    marked[src] = True

    # Using a MAX PRIORITY QUEUE means we rely on negative distance to
    # choose the one that is closest...
    pq.enqueue(src, -distance(src, target))

    while not pq.is_empty():
        v = pq.dequeue()

        for w in G.neighbors(v):
            if not w in marked:
                node_from[w] = v
                dist_to[w] = dist_to[v] + 1
                pq.enqueue(w, -distance(w, target))
                marked[w] = True

    return node_from

def draw_solution(G, field, src, target, figsize=(12,6)):
    """
    Use matplotlib to draw the original graph containing the solution to
    a designated target vertex; in the second graph the node_from dictionary
    is visualized.
    """
    if plt_error:
        return
    import matplotlib.pyplot as plt

    H = solution_graph(G, path_to(field, src, target))
    F = node_from_field(G, field)

    _, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    ax = axes.flatten()

    # get original positional location from original graph
    pos_h = nx.get_node_attributes(H, 'pos')
    nx.draw(H, pos_h, with_labels = True, node_color='w', font_size=8, ax=ax[0])
    pos_f = nx.get_node_attributes(F, 'pos')
    nx.draw(F, pos_f, with_labels = True, node_color='w', font_size=8, ax=ax[1])

#######################################################################
if __name__ == '__main__':
    random.seed(15)
    m = Maze(3,5)    # Anything bigger and these are too small to read
    graph = to_networkx(m)

    # Choose whether to use dfs_search, bfs_search, or guided_search
    draw_solution(graph, bfs_search(graph, m.start()), m.start(), m.end())

    import matplotlib.pyplot as plt
    plt.show()
