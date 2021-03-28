"""
 Single-source Shortest path algorithms, including Dijkstra and Bellman-Ford.
"""
from ch07.indexed_pq import IndexedMinPQ
from ch07.replacement import WEIGHT

def bellman_ford(G, src):
    """
    Compute Single Source Shortest Path using Bellman_ford and return
    dist_to[] with results and edge_to[] to be able to recover the
    shortest paths. Can work even if there are negative edge weights,
    but NOT if a negative cycle exists. Fortunately it can detect
    this situation.
    """
    inf = float('inf')
    dist_to = {v:inf for v in G.nodes()}
    dist_to[src] = 0
    edge_to = {}

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            return True
        return False

    #debug_state('initialize', G, node_from, dist_to)
    for i in range(G.number_of_nodes()+1):
        for e in G.edges(data=True):
            if relax(e):
                if i == G.number_of_nodes():
                    raise RuntimeError('Negative Cycle exists in graph.')

    return (dist_to, edge_to)

def dijkstra_sp(G, src):
    """
    Compute Dijkstra's algorithm using src as source and return dist_to[] with
    results and edge_to[] to be able to recover the shortest paths.
    """
    N = G.number_of_nodes()

    inf = float('inf')
    dist_to = {v:inf for v in G.nodes()}
    dist_to[src] = 0

    impq = IndexedMinPQ(N)
    impq.enqueue(src, dist_to[src])
    for v in G.nodes():
        if v != src:
            impq.enqueue(v, inf)

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            impq.decrease_priority(v, dist_to[v])

    edge_to = {}
    while not impq.is_empty():
        v = impq.dequeue()
        for e in G.edges(v, data=True):
            relax(e)

    return (dist_to, edge_to)

def edges_path_to(edge_to, src, target):
    """Recover path from src to target."""
    if edge_to[target] is None:
        raise ValueError('{} is unreachable from {}'.format(target, src))

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
