"""
Dijkstra's Single-source Shortest path algorithm.
"""
from ch07.indexed_pq import IndexedMinPQ
from ch07.replacement import WEIGHT

def dijkstra_sp(G, s):
    """
    Compute Dijkstra's algorithm using s as source and return dist_to[] with 
    results and edge_to[] to be able to recover the shortest paths.
    """
    N = G.number_of_nodes()

    inf = float('inf')
    dist_to = {}
    for v in G.nodes():
        dist_to[v] = inf
    edge_to = {}
    dist_to[s] = 0

    impq = IndexedMinPQ(N)
    impq.enqueue(s, dist_to[s])
    for v in G.nodes():
        if v != s:
            impq.enqueue(v, inf)

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            impq.decrease_priority(v, dist_to[v])

    while not impq.is_empty():
        v = impq.dequeue()
        for e in G.edges(v, data=True):
            relax(e)

    return (dist_to, edge_to)

def edges_path_to(edge_to, src, target):
    """Recover path from src to target."""
    if edge_to[target] is None:
        raise ValueError('{} is unreachable from {}'.format(target,src))
    
    path = []
    v = target
    while v != src:
        path.append(v)
        v = edge_to[v][0]
        
    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path
