"""
Python script to load up TMG file as a Graph and generate figure
for book, which contains highway network, waypoints, and a
Breadth-First Search solution
"""

from math import cos, asin, sqrt, pi
import matplotlib.pyplot as plt

from algs.output import image_file
from resources.highway import highway_map

from ch07.dijkstra_sp import dijkstra_sp
from ch07.graph import WEIGHT
from ch07.plot_map import plot_node_from
from ch07.tmg_load import tmg_load, distance
from ch07.search import bfs_search, path_to, dfs_search_recursive, smart_search

try:
    import networkx as nx
except ImportError:
    from ch07.graph import Replacement
    nx = Replacement()

def plot_gps(positions, s=8, marker='.', color='blue'):
    """Draw positions of individual nodes."""
    x = []
    y = []
    for i in positions:
        pos = positions[i]
        x.append(pos[1])
        y.append(pos[0])
    plt.scatter(x, y, marker=marker, s=s, color=color)

def plot_highways(positions, edges, color='gray'):
    """Plot highways with linesegments."""
    for e in edges:
        head = positions[e[0]]
        tail = positions[e[1]]
        plt.plot([head[1], tail[1]],[head[0], tail[0]], linewidth=1, color=color)

def compute_distance(positions, src, target):
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

#######################################################################
if __name__ == '__main__':    
    (G,positions) = tmg_load(highway_map())
    #print(len(list(G.nodes())), len(list(G.edges())))
    # Border of New York State (389) to Provincetown (2256)
    src = 389
    target = 2256

    (dist_to, edge_to) = dijkstra_sp(G, src)
    print('Dijkstra shortest distance is {:.1f}'.format(dist_to[target]))

    plot_gps(positions)
    plot_highways(positions, G.edges())

    node_from = bfs_search(G, src)
    total = compute_distance(positions, src, target)    

    plot_node_from(G, positions, src, target, node_from, color='purple')
    print('{0} total steps for Breadth First Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target)), total))

    plt.savefig(image_file('figure-mass-highway-bfs.png'))
    print(image_file('figure-mass-highway-bfs.png'))

    plt.clf()

    plot_gps(positions)
    plot_highways(positions, G.edges())

    node_from = dfs_search_recursive(G, src)
    total = compute_distance(positions, src, target)    
    
    plot_node_from(G, positions, src, target, node_from, color='purple')
    print('{0} total steps for Depth First Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target)), total))
    
    plt.savefig(image_file('figure-mass-highway-dfs.png'))
    print(image_file('figure-mass-highway-dfs.png'))

    plt.clf()

    plot_gps(positions)
    plot_highways(positions, G.edges())

    def distance_gps(from_cell, to_cell):
        """These ids are indexed into positions to get gps coordinates."""
        return abs(positions[from_cell][0] - positions[to_cell][0]) + abs(positions[from_cell][1] - positions[to_cell][1])

    node_from = smart_search(G, src, target, distance=distance_gps)
    total = compute_distance(positions, src, target)    
    
    plot_node_from(G, positions, src, target, node_from, color='purple')
    print('{0} total steps for Smart Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target)), total))
    
    plt.savefig(image_file('figure-mass-highway-smart.png'))
    print(image_file('figure-mass-highway-smart.png'))