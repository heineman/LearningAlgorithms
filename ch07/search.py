"""
Code to blindly search through a Graph in Depth First and Breadth First strategies.
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
    dist_to = {}
    
    for v in G.nodes():
        dist_to[v] = float('inf')
    
    q = Queue()
    q.enqueue(src)
    dist_to[src] = 0
    marked[src] = True
    
    while not q.is_empty():
        v = q.dequeue()
        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                dist_to[w] = dist_to[v] + 1
                marked[w] = True
                q.enqueue(w)

    return node_from            
    
#######################################################################
if __name__ == '__main__':
    random.seed(28)
    m = Maze(7,7)
    G = to_networkx(m)
    
    # dfs_search_nr and dfs_search() produce different results
    field = dfs_search(G, m.start())
    H = solution_graph(G, path_to(field, m.start(), m.end()))
    F = node_from_field(G, field)
     
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    # get original positional location from original graph
    pos_h = nx.get_node_attributes(H, 'pos')
    nx.draw(H, pos_h, with_labels = True, node_color="w", font_size=8, ax=ax[0])
    pos_f = nx.get_node_attributes(F, 'pos')
    nx.draw(F, pos_f, with_labels = True, node_color="w", font_size=8, ax=ax[1])  
    

    plt.show()
