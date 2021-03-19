"""
All PairsShortest path algorithm.
"""
from ch07.indexed_pq import IndexedMinPQ
from ch07.replacement import WEIGHT

def all_pairs_sp(G):
    """
    Compute All Pairs Shortest Path using Floyd Warshall and return  
    dist_to[] with results and edge_to[] to be able to recover the 
    shortest paths.
    """
    N = G.number_of_nodes()

    inf = float('inf')
    dist_to = {}
    node_from = {}
    for u in G.nodes():
        inner = {}
        inner_nf = {}
        for v in G.nodes():
            inner[v] = inf
            inner_nf[v] = None
        
        dist_to[u] = inner
        node_from[u] = inner_nf
        
        dist_to[u][u] = 0
        
        for e in G.edges(u, data=True):
            v = e[1]
            dist_to[u][v] = e[2][WEIGHT]
            node_from[u][v] = u
            
    for k in G.nodes():
        for u in G.nodes():
            for v in G.nodes():
                new_len = dist_to[u][k] + dist_to[k][v]
                if new_len < dist_to[u][v]:
                    dist_to[u][v] = new_len
                    node_from[u][v] = node_from[k][v]       # CRITICAL
                
    return (dist_to, node_from)

def all_pairs_path_to(edge_to, src, target):
    """Recover path from src to target."""
    if edge_to[target] is None:
        raise ValueError('{} is unreachable from {}'.format(target,src))
    
    path = []
    v = target
    while v != src:
        path.append(v)
        v = edge_to[src][v]
        
    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path
