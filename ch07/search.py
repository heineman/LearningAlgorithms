"""
Code to blindly search through a Graph in Depth First and Breadth First strategies. Also
contains a rudimentary Smart Search for undirected graphs when there is a metric showing
how far a node is from the target.
"""
import random
from ch07.maze import Maze, to_networkx, solution_graph, node_from_field
from ch04.list_queue import Queue

try:
    import networkx as nx
except ImportError:
    from ch07.graph import Replacement
    nx = Replacement()

def path_to(node_from, src, target):
    """
    Given a dictionary that results from a search, reproduce path from original src
    to target. Have to follow the node_from in reverse order, which is why the
    nodes discovered are all inserted at index position 0 in the path.
    """
    if node_from[target] is None:
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
    Apply Depth First Search to a graph from a starting node. Return 
    dictionary of explored trail. Fails if recursion is too deep.
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
    """Conduct non-recursive Depth First Search on G starting from s."""
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

def distance_to_target(from_cell, to_cell):
        return abs(from_cell[0] - to_cell[0]) + abs(from_cell[1] - to_cell[1])

def smart_search(G, src, target):
    """Non-recursive depth-first search investigating given position."""
    from ch04.heap import PQ
    pq = PQ(len(G.nodes))
    marked = {}
    node_from = {}
    
    dist_to = {}
    dist_to[src] = 0
    marked[src] = True
    
    # Using a MAX PRIORITY QUEUE means we rely on negative distance to
    # choose the one that is closest...
    pq.enqueue(src, -distance_to_target(src, target))
    
    while not pq.is_empty():
        v = pq.dequeue()
       
        for w in G.neighbors(v):
            if not w in marked:
                node_from[w] = v
                dist_to[w] = dist_to[v] + 1
                pq.enqueue(w, -distance_to_target(w, target))
                marked[w] = True

    return node_from

def draw_solution(G, field, src, target):
    import matplotlib.pyplot as plt
    
    H = solution_graph(G, path_to(field, src, target))
    F = node_from_field(G, field)
 
    _, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    # get original positional location from original graph
    pos_h = nx.get_node_attributes(H, 'pos')
    nx.draw(H, pos_h, with_labels = True, node_color="w", font_size=8, ax=ax[0])
    pos_f = nx.get_node_attributes(F, 'pos')
    nx.draw(F, pos_f, with_labels = True, node_color="w", font_size=8, ax=ax[1])  
    
#######################################################################
if __name__ == '__main__':
    random.seed(15)
    m = Maze(3,5)    # Anything bigger and these are too small to read
    graph = to_networkx(m)
    
    #draw_solution(graph, dfs_search(graph, m.start()), m.start(), m.end())
    draw_solution(graph, bfs_search(graph, m.start()), m.start(), m.end())
    #draw_solution(graph, smart_search(graph, m.start(), m.end()), m.start(), m.end())
    
    import matplotlib.pyplot as plt
    plt.show()
