"""
Code to blindly search through a Graph in Depth First and Breadth First strategies.
"""
import random
from ch07.maze import Maze, to_networkx, solution_graph, vertex_from_field
from ch04.list_queue import Queue

def path_to(vertex_from, src, target):
    """
    Given a dictionary that results from a search, reproduce path from original src
    to target. Have to follow the vertex_from in reverse order, which is why the
    vertices discovered are all inserted at index position 0 in the path.
    """
    path = []
    v = target
    while v != src:
        path.append(v)
        v = vertex_from[v]
    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path

def dfs_search(G, src):
    """
    Apply Depth First Search to a graph from a starting vertex. Return 
    dictionary of explored trail.
    """
    marked = {}
    vertex_from = {}

    def dfs(v):
        marked[v] = True

        for w in G[v]:
            if not w in marked:
                vertex_from[w] = v
                dfs(w)

    dfs(src)
    return vertex_from

def bfs_search(G, src):
    """
    Apply Depth First Search to a graph from a starting vertex. Return 
    dictionary of explored trail.
    """
    marked = {}
    vertex_from = {}
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
                vertex_from[w] = v
                dist_to[w] = dist_to[v] + 1
                marked[w] = True
                q.enqueue(w)

    return vertex_from            
    
#######################################################################
if __name__ == '__main__':
    random.seed(13)
    m = Maze(7,7)
    G = to_networkx(m)

    #print(path_to(dfs_search(G, m.start()), m.start(), m.end()))
    #print(path_to(bfs_search(G, m.start()), m.start(), m.end()))
    
    field = dfs_search(G, m.start())
    H = solution_graph(G, path_to(field, m.start(), m.end()))
    F = vertex_from_field(G, field)
     
    import matplotlib.pyplot as plt
    import networkx as nx

    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    # get original positional location from original graph
    pos_h = nx.get_node_attributes(H, 'pos')
    nx.draw(H, pos_h, with_labels = True, node_color="w", font_size=8, ax=ax[0])
    pos_f = nx.get_node_attributes(F, 'pos')
    nx.draw(F, pos_f, with_labels = True, node_color="w", font_size=8, ax=ax[1])  
    

    plt.show()
