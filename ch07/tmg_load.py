"""
Python script to load up TMG file as a Graph.
"""

from math import cos, asin, sqrt, pi

from resources.highway import highway_map
from ch07.single_source_sp import dijkstra_sp
from ch07.replacement import WEIGHT
from ch07.dependencies import plt_error

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

def compute_distance(positions, node_from, src, target):
    """
    Compute total distance from src to target, traversing positions and using
    positions[] information as waypoints for distance.
    """
    total = 0
    last_pos = None
    v = target
    while v != src:
        pos = positions[v]
        v = node_from[v]
        if last_pos:
            total += distance(pos, last_pos)
        last_pos = pos
    total += distance(positions[src], last_pos)
    return total

def plot_gps(positions, s=8, marker='.', color='blue'):
    """Draw positions of individual nodes."""
    if plt_error:
        return 
    import matplotlib.pyplot as plt

    x = []
    y = []
    for i in positions:
        pos = positions[i]
        x.append(pos[1])
        y.append(pos[0])
    plt.scatter(x, y, marker=marker, s=s, color=color)

def plot_highways(positions, edges, color='gray'):
    """Plot highways with linesegments."""
    if plt_error:
        return 
    import matplotlib.pyplot as plt

    for e in edges:
        head = positions[e[0]]
        tail = positions[e[1]]
        plt.plot([head[1], tail[1]],[head[0], tail[0]], linewidth=1, color=color)

def distance(gps1, gps2):
    """
    Return reasonably distance in miles. Based on helpful method found here:

    https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    """
    (lat1, long1) = gps1
    (lat2, long2) = gps2

    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((long2-long1)*p))/2
    return 7917.509282 * asin(sqrt(a))       # convert into miles and use 12742 as earth diameter in KM

def tmg_load(raw_data):
    """
    Load up a TMG 1.0 simple file into a directed weighted graph, using
    long/lat coordinate calculator for distance.
    
        TMG 1.0 simple
        #N #E
        {NODE: LABEL LAT LONG}
        {EDGE: id1 id2 LABEL}
        
    For each edge, compute the distance     
    """
    G = nx.Graph()
    line = 0
    if not 'TMG' in raw_data[line]:
        raise ValueError('Contents is not a valid TMG file ({}).'.format(raw_data[line]))
    line += 1

    (snum_nodes, snum_edges) = raw_data[line].split()
    line += 1
    num_nodes = int(snum_nodes)
    num_edges = int(snum_edges)

    positions = {}

    for i in range(num_nodes):
        (_, slat1, slong1) = raw_data[line].split()
        line += 1

        positions[i] = (float(slat1), float(slong1))
        G.add_node(i)

    for i in range(num_edges):
        (su, sv, _) = raw_data[line].split()
        line += 1

        u = int(su)
        v = int(sv)
        d = distance(positions[u], positions[v])
        G.add_edge(u, v, weight=d)

    return (G, positions)

#######################################################################
if __name__ == '__main__':    
    if not plt_error:
        import matplotlib.pyplot as plt
    
        (G,positions) = tmg_load(highway_map())
        print(G.number_of_nodes(), G.number_of_edges())
    
        src = 389
        target = 2256
    
        paths = nx.single_source_shortest_path(G, src)
        path = paths[target]
    
        total = 0
        for i in range(len(path)-1):
            total += G[path[i]][path[i+1]][WEIGHT]
        print(total)
        print(G.edges(src, data=True))   # 68 -> 89
    
        (dist_to, edge_to) = dijkstra_sp(G, src)
        print(dist_to[target])
    
        plot_gps(positions)
        plot_highways(positions, G.edges())
        plt.show()
