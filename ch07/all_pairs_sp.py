"""
All PairsShortest path algorithm.
"""
from ch07.replacement import WEIGHT

def debug_state(title, G, node_from, dist_to, output=True):
    """Useful to show state of all pairs shortest path."""
    from algs.table import DataTable

    print('debug :', title)
    labels = list(G.nodes())

    tbl = DataTable([6] + [6]*len(labels), ['.'] + labels, output=output)
    tbl.format('.','s')
    for f in labels:
        tbl.format(f, 's')
    for u in labels:
        row = [u]
        for v in labels:
            row.append(node_from[u][v]) if node_from[u][v] else row.append('.')
        tbl.row(row)
    print()

    tbl_dist_to = DataTable([6] + [6]*len(labels), ['.'] + labels, output=output, decimals=1)
    tbl_dist_to.format('.','s')
    for u in labels:
        row = [u]
        for v in labels:
            if u == v:
                row.append(0) 
            else:
                row.append(dist_to[u][v])
        tbl_dist_to.row(row)
    print()
    return (tbl, tbl_dist_to)

def floyd_warshall(G):
    """
    Compute All Pairs Shortest Path using Floyd Warshall and return  
    dist_to[] with results and node_from[] to be able to recover the 
    shortest paths.
    """
    inf = float('inf')
    dist_to = {}
    node_from = {}
    for u in G.nodes():
        dist_to[u]   = {v:inf for v in G.nodes()}
        node_from[u] = {v:None for v in G.nodes()}

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
                    node_from[u][v] = node_from[k][v]                 # CRITICAL

    return (dist_to, node_from)

def all_pairs_path_to(node_from, src, target):
    """Recover path from src to target."""
    if node_from[src][target] is None:
        raise ValueError('{} is unreachable from {}'.format(target,src))

    path = []
    v = target
    while v != src:
        path.append(v)
        v = node_from[src][v]

    # last one to push is the source, which makes it
    # the first one to be retrieved
    path.append(src)
    path.reverse()
    return path
