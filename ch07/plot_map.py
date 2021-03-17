import matplotlib.pyplot as plt
import networkx as nx
from ch07.dijkstra_sp import dijkstra_sp, path_to as sp_path_to
from ch07.graph import WEIGHT

from ch07.tmg_load import tmg_load, plot_gps, plot_highways
from ch07.search import bfs_search, path_to

def plot_edge_path(positions, src, target, edge_to, marker='.', color='green'):
    nx = []
    ny = []
    e = edge_to[target]
    my_total = 0
    while e[0] != src:
        pos = positions[e[0]]
        nx.append(pos[1])
        ny.append(pos[0])
        my_total += e[2][WEIGHT]
        e = edge_to[e[0]]
    my_total += e[2][WEIGHT]
    print('my total={}'.format(my_total))
    plt.plot(nx, ny, color=color)
    plt.scatter(nx, ny, marker=marker, color=color)

def plot_path(positions, path, marker='.', color='red'):
    px = []
    py = []
    for v in path:
        pos = positions[v]
        px.append(pos[1])
        py.append(pos[0])
    plt.plot(px, py, color=color)
    plt.scatter(px, py, marker=marker, color=color)
    
def plot_node_from(G, positions, src, target, node_from, marker='.', color='orange'):
    nx = []
    ny = []
    v = target
    while v != src:
        pos = positions[v]
        nx.append(pos[1])
        ny.append(pos[0])
        v = node_from[v]
    plt.plot(nx, ny, color=color)
    plt.scatter(nx, ny, marker=marker, color=color)

#######################################################################
if __name__ == '__main__':
    (G,positions) = tmg_load('C:\\Users\\Home\\Downloads\\MA-region-simple.tmg')
    plot_gps(positions)
    
    src = 389
    target = 2256
    
    path = nx.dijkstra_path(G, src, target)
    total = 0
    for i in range(len(path)-1):
        total += G[path[i]][path[i+1]][WEIGHT]
    print('networkx total={}'.format(total))
    
    #nn = dfs_search_recursive(G, src)
    #plot_node_from(G, positions, src, target, nn, color='orange')
    plot_highways(positions, G.edges())
    
    node_from = bfs_search(G, src)
    plot_node_from(G, positions, src, target, node_from, color='purple')
    print('{} total steps for Breadth First Search'.format(len(path_to(node_from, src, target))))
    
    plot_path(positions, path)
    
    (dist_to, edge_to) = dijkstra_sp(G, src)
    print('{} total steps for Dijkstra Single-source Shortest Path Search'.format(len(sp_path_to(edge_to, src, target))))
    
    plot_edge_path(positions, src, target, edge_to)
    
    plt.show()
