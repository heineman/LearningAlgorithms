"""
Supporting functions for plotting the latitude/longitude data.
"""

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from ch07.dependencies import plt_error
from ch07.replacement import WEIGHT

def plot_edge_path(positions, src, target, edge_to, marker='.', color='green'):
    if plt_error:
        return 
    import matplotlib.pyplot as plt

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
    """
    Plot path using list of nodes in path[] according to positional information
    in positions.
    """ 
    if plt_error:
        return 
    import matplotlib.pyplot as plt

    px = []
    py = []
    for v in path:
        pos = positions[v]
        px.append(pos[1])
        py.append(pos[0])
    plt.plot(px, py, color=color)
    plt.scatter(px, py, marker=marker, color=color)

def plot_node_from(G, positions, src, target, node_from, marker='.', color='orange'):
    """Plot path from src to target using node_from[] information."""
    if plt_error:
        return 
    import matplotlib.pyplot as plt

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
