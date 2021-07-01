"""Code for chapter 07."""

import timeit
import random

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from algs.table import DataTable, caption, FigureNum, TableNum, SKIP
from algs.output import image_file
from resources.highway import highway_map

from ch07.dependencies import tkinter_error, plt_error
from ch07.maze import Maze, to_networkx
from ch07.snapshot import tkinter_register_snapshot
from ch07.search import path_to, bfs_search, dfs_search_recursive, guided_search
from ch07.single_source_sp import dijkstra_sp, edges_path_to, bellman_ford
from ch07.plot_map import plot_path, plot_node_from
from ch07.tmg_load import tmg_load, compute_distance, plot_gps, plot_highways, bounding_ids
from ch07.all_pairs_sp import floyd_warshall

def make_sample_graph():
    """Create sample graph."""
    G = nx.Graph()
    G.add_node('A2')
    G.add_nodes_from(['A3', 'A4', 'A5'])
    G.add_edge('A2', 'A3')
    G.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

    for i in range(2, 6):
        G.add_edge('B{}'.format(i), 'C{}'.format(i))
        if 2 < i < 5:
            G.add_edge('B{}'.format(i), 'B{}'.format(i+1))
        if i < 5:
            G.add_edge('C{}'.format(i), 'C{}'.format(i+1))

    print(G.number_of_nodes(), 'nodes and', G.number_of_edges(), 'edges.')
    print('adjacent nodes to C3:', list(G['C3']))
    print('edges adjacent to C3:', list(G.edges('C3')))
    return G

def make_sample_directed_graph():
    """Create sample graph."""
    DG = nx.DiGraph()

    DG.add_node('A2')
    DG.add_nodes_from(['A3', 'A4', 'A5'])
    DG.add_edge('A2', 'A3')
    DG.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

    DG.add_edges_from([('B3', 'B4'), ('B2', 'B4')])
    DG.add_edges_from([('B4', 'B5'), ('B3', 'B5')])

    for i in range(2, 6):
        DG.add_edge('B{}'.format(i), 'C{}'.format(i))
        if i < 5:
            DG.add_edge('C{}'.format(i), 'C{}'.format(i+1))

    print(DG.number_of_nodes(), 'nodes and', DG.number_of_edges(), 'edges.')
    print('adjacent nodes to C3:', list(DG['C3']))
    print('edges adjacent to C3:', list(DG.edges('C3')))
    return DG

def topological_example(G, N):
    """Create stylized graph with N^2 nodes and edges to lead to sink node."""
    for i in range(N):
        label = chr(ord('A') + i)
        for j in range(i+1):
            G.add_node(label + str(j+1))

    for i in range(N-1,0,-1):
        label = chr(ord('A') + N + (N-i) - 1)
        for j in range(i):
            G.add_node(label + str(j+1))

    for i in range(N-1):
        for j in range(i+1):
            label = chr(ord('A') + i)
            u = label + str(j+1)
            for k in range(i+2):
                label = chr(ord('A') + (i+1))
                v = label + str(k+1)
                G.add_edge(u, v)

    for i in range(N-2,-1,-1):
        for j in range(i+2):
            label = chr(ord('A') + N + (N-i) - 3)
            u = label + str(j+1)
            for k in range(i+1):
                label = chr(ord('A') + N + (N-i) - 2)
                v = label + str(k+1)
                G.add_edge(u, v)

def table_topological_example(max_k=8, output=True, decimals=4):
    """Compare Topological sort performance."""
    DG = nx.DiGraph()
    topological_example(DG,4)

    tbl = DataTable([8, 10, 12, 12], ['N', 'E', 'Built-In', 'Topological Sort'],
                    output=output, decimals=decimals)
    tbl.format('E', ',d')
    for N in [2**k for k in range(1, max_k)]:
        built_in = 1000*min(timeit.repeat(stmt='''nx.topological_sort(DG)''', setup='''
from ch07.book import topological_example
try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx
DG = nx.DiGraph()    
topological_example(DG,{})'''.format(N), repeat=5, number=3))

        mtime = 1000*min(timeit.repeat(stmt='''topological_sort(DG)''', setup='''
from ch07.digraph_search import topological_sort
from ch07.book import topological_example
try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx
DG = nx.DiGraph()    
topological_example(DG,{})'''.format(N), repeat=5, number=3))
        DG = nx.DiGraph()
        topological_example(DG, N)
        tbl.row([len(list(DG.nodes())), len(list(DG.edges())), built_in, mtime])
    return tbl

def table_compare_graph_structures(max_k=15, output=True):
    """
    Compare Matrix implementation vs. Adjacency list implementation vs. NetworkX up to
    but not including max_k=15.
    """

    tbl = DataTable([8, 10, 10, 10], ['N', 'NetworkX', 'Adjacency List', 'Adjacency Matrix'], output=output)
    for N in [2**k for k in range(8, max_k)]:
        undirect_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.replacement import UndirectedGraph
G = UndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))

        networkx_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.replacement import UndirectedGraph
G = UndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))

        matrix_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.replacement import MatrixUndirectedGraph
G = MatrixUndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))

        tbl.row([N, networkx_mtime, undirect_mtime, matrix_mtime])
    return tbl

def output_adjacency_matrix():
    """Output adjacency matrix for example maze."""
    random.seed(15)
    m = Maze(3,5)
    g = to_networkx(m)
    N = g.number_of_nodes()
    count = 0
    for r in g.nodes():
        row = [str(r)]
        for c in g.nodes():
            if c in g[r]:
                row.append('1')
                count += 1
            else:
                row.append('')
        print('\t'.join(row))
    print(count / (N*N))

def output_adjacency_list():
    """Output adjacency list for example maze."""
    random.seed(15)
    m = Maze(3,5)
    g = to_networkx(m)
    N = g.number_of_nodes()
    tbl = DataTable([8] + [3]*N, ['node'] + ['n{}'.format(i) for i in range(N)])
    tbl.format('node', 's')
    for i in range(N):
        tbl.format('n{}'.format(i), 's')

    for r in g.nodes():
        row = [str(r)]
        for c in g[r]:
            row.append(str(c))
        tbl.row(row)

def generate_bfs_and_dijkstra_figure(src, target):
    """Generate BFS solution overlaying Massachusetts highway."""
    if plt_error:
        return None
    import matplotlib.pyplot as plt

    (G, positions, _) = tmg_load(highway_map())
    (dist_to, edge_to) = dijkstra_sp(G, src)
    print('Dijkstra shortest distance is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, src, target))-1, dist_to[target]))
    path = edges_path_to(edge_to, src, target)
    plt.clf()
    plot_gps(positions)
    plot_highways(positions, G.edges())
    plot_path(positions, path)
    node_from = bfs_search(G, src)
    total = compute_distance(positions, node_from, src, target)

    plot_node_from(positions, src, target, node_from, color='purple')
    print('{0} total steps for Breadth First Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target))-1, total))
    plt.axis('off')
    output_file = image_file('figure-mass-highway-bfs.svg')
    plt.savefig(output_file, format="svg")
    print(output_file)
    plt.clf()
    return output_file

def generate_dfs_figure(src, target):
    """Generate DFS solution overlaying Massachusetts highway."""
    if plt_error:
        return None
    import matplotlib.pyplot as plt

    (G, positions, _) = tmg_load(highway_map())
    plt.clf()
    plot_gps(positions)
    plot_highways(positions, G.edges())

    node_from = dfs_search_recursive(G, src)
    total = compute_distance(positions, node_from, src, target)

    plot_node_from(positions, src, target, node_from, color='purple')
    print('{0} total steps for Depth First Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target))-1, total))
    plt.axis('off')
    output_file = image_file('figure-mass-highway-dfs.svg')
    plt.savefig(output_file, format="svg")
    print(output_file)
    plt.clf()
    return output_file

def generate_guided_search_figure(G, positions, src, target):
    """Generate Guided Search solution .. ultimately omitted from book."""
    if plt_error:
        return None
    import matplotlib.pyplot as plt

    (G, positions, _) = tmg_load(highway_map())
    plt.clf()
    plot_gps(positions)
    plot_highways(positions, G.edges())

    def distance_gps(from_cell, to_cell):
        """These ids are indexed into positions to get GPS coordinates."""
        return abs(positions[from_cell][0] - positions[to_cell][0]) + abs(positions[from_cell][1] - positions[to_cell][1])

    node_from = guided_search(G, src, target, distance=distance_gps)
    total = compute_distance(positions, node_from, src, target)

    plot_node_from(positions, src, target, node_from, color='purple')
    print('{0} total steps for Guided Search with distance={1:.1f} miles'.format(len(path_to(node_from, src, target))-1, total))
    plt.axis('off')
    output_file = image_file('figure-mass-highway-guided.svg')
    plt.savefig(output_file, format="svg")
    print(output_file)
    plt.clf()
    return output_file

def visualize_dijkstra_small_graph(DG):
    """
    Compute Dijkstra's algorithm using src as source and return dist_to[] with
    results and edge_to[] to be able to recover the shortest paths.
    """
    from ch07.indexed_pq import IndexedMinPQ
    from ch07.replacement import WEIGHT

    N = DG.number_of_nodes()
    src = 'a'
    inf = float('inf')
    dist_to = {v:inf for v in DG.nodes()}
    dist_to[src] = 0

    impq = IndexedMinPQ(N)
    impq.enqueue(src, dist_to[src])
    for v in DG.nodes():
        if v != src:
            impq.enqueue(v, inf)

    def debug_state():
        print('|'.join([' {:>3} '.format(k) for k in dist_to]))
        print('|'.join([' {:>3} '.format(dist_to[k]) for k in dist_to]))
        print()

    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            impq.decrease_priority(v, dist_to[v])

    edge_to = {}
    while not impq.is_empty():
        debug_state()
        v = impq.dequeue()
        for e in DG.edges(v, data=True):
            relax(e)

    return (dist_to, edge_to)

def visualize_results_floyd_warshall(DG, output=True):
    """Output the node_from and dist_to arrays for floyd-warshall after completion."""
    from ch07.all_pairs_sp import all_pairs_path_to

    (dist_to, node_from) = floyd_warshall(DG)

    if output:
        output_node_from_floyd_warshall(DG, node_from)
        print()
        output_dist_to_floyd_warshall(DG, dist_to)
        print()

    tbl_path = DataTable([20] * DG.number_of_nodes(), list(DG.nodes()), output=output)
    for n in DG.nodes():
        tbl_path.format(n, 's')
    for n in DG.nodes():
        row = []
        for v in DG.nodes():
            if n == v:
                row.append(SKIP)
            else:
                if node_from[n][v]:
                    nodes = all_pairs_path_to(node_from, n, v)
                    row.append(' -> '.join(nodes))
                else:
                    row.append(SKIP)
        tbl_path.row(row)

    if output:
        print()

def floyd_warshall_just_initialize(G):
    """
    Compute All Pairs Shortest Path using Floyd-Warshall and return
    dist_to[] with results and node_from[] to be able to recover the
    shortest paths.
    """
    from ch07.replacement import WEIGHT
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

    return (dist_to, node_from)

def visualize_results_floyd_warshall_just_initialize(DG):
    """Output the node_from and dist_to arrays for floyd-warshall after initialization."""
    (dist_to, node_from) = floyd_warshall_just_initialize(DG)

    output_node_from_floyd_warshall(DG, node_from)
    print()

    output_dist_to_floyd_warshall(DG, dist_to)
    print()

def output_node_from_floyd_warshall(DG, node_from, output=True):
    """Create data table for node_from."""
    tbl_nf = DataTable([8] * DG.number_of_nodes(), list(DG.nodes()), output=output)
    for n in DG.nodes():
        tbl_nf.format(n, 's')

    for n in DG.nodes():
        row = []
        for v in DG.nodes():
            if node_from[n][v]:
                row.append(node_from[n][v])
            else:
                row.append(SKIP)
        tbl_nf.row(row)
    return tbl_nf

def output_dist_to_floyd_warshall(DG, dist_to, output=True):
    """Create data table for dist_to."""
    tbl_dt = DataTable([8] * DG.number_of_nodes(), list(DG.nodes()), output=output, decimals=1)
    tbl_dt.format(list(DG.nodes())[0],'f')  #  only first one, since this would have been N in tbl
    for n in DG.nodes():
        row = []
        for v in DG.nodes():
            row.append(dist_to[n][v])
        tbl_dt.row(row)
    return tbl_dt

def visualize_results_floyd_warshall_two_steps(DG):
    """Output the node_from and dist_to arrays for floyd-warshall after first two steps."""
    (dist_to, node_from) = floyd_warshall_just_initialize(DG)

    print('changes after k=a is processed.')
    k = 'a'
    for u in DG.nodes():
        for v in DG.nodes():
            new_len = dist_to[u][k] + dist_to[k][v]
            if new_len < dist_to[u][v]:
                dist_to[u][v] = new_len
                node_from[u][v] = node_from[k][v]

    output_node_from_floyd_warshall(DG, node_from)
    print()

    output_dist_to_floyd_warshall(DG, dist_to)
    print()

    print('changes after k=b is processed.')
    k = 'b'
    for u in DG.nodes():
        for v in DG.nodes():
            new_len = dist_to[u][k] + dist_to[k][v]
            if new_len < dist_to[u][v]:
                dist_to[u][v] = new_len
                node_from[u][v] = node_from[k][v]

    tbl_nf = DataTable([8] * DG.number_of_nodes(), list(DG.nodes()))
    for n in DG.nodes():
        tbl_nf.format(n, 's')

    output_node_from_floyd_warshall(DG, node_from)
    print()

    output_dist_to_floyd_warshall(DG, dist_to)
    print()

def generate_ch07():
    """Generate Tables and Figures for chapter 07."""
    chapter = 7

    with FigureNum(1) as figure_number:
        description  = 'Modeling different problems using graphs'
        print('by hand')
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(2) as figure_number:
        description  = 'An undirected graph of 12 vertices and 12 edges'
        make_sample_graph()
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(3) as figure_number:
        description = 'A graph modeling a rectangular maze'
        label = caption(chapter, figure_number)
        from ch07.viewer import Viewer

        random.seed(15)
        m = Maze(3,5)
        g = to_networkx(m)

        postscript_output = '{}-graph.ps'.format(label)
        if tkinter_error:
            print('unable to generate {}'.format(postscript_output))
        else:
            import tkinter
            root = tkinter.Tk()
            canvas = Viewer(m, 50).view(root)
            tkinter_register_snapshot(root, canvas, postscript_output)
            root.mainloop()

        # For obscure reasons, this must come AFTER root.mainloop()
        if plt_error:
            pass
        else:
            import matplotlib.pyplot as plt
            pos = nx.get_node_attributes(g, 'pos')
            nx.draw(g, pos, with_labels = True, node_color='w', font_size=8)
            output_file = image_file('{}-graph.svg'.format(label))
            plt.savefig(output_file, format="svg")
            print('created {}'.format(output_file))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(4) as figure_number:
        description  = 'Hitting a dead end while exploring a maze'
        print('Hand drawn overlay to Figure 7-2.')
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(5) as figure_number:
        from ch07.search import dfs_search, draw_solution

        description  = 'Depth First Search locates target if reachable from source'
        label = caption(chapter, figure_number)
        random.seed(15)
        m = Maze(3,5)
        graph = to_networkx(m)

        if plt_error:
            print('unable to draw graph')
        else:
            draw_solution(graph, dfs_search(graph, m.start()), m.start(), m.end())
            output_file = image_file('{}-graph.svg'.format(label))
            plt.savefig(output_file, format="svg")
            print('created {}'.format(output_file))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(6) as figure_number:
        description  = 'Breadth First Search will locate shortest path to target, if reachable from source'
        print('Hand drawn overlay to Figure 7-2.')
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(7) as figure_number:
        description  = 'Breadth First Search finds shortest path to each node'
        label = caption(chapter, figure_number)
        random.seed(15)
        m = Maze(3,5)
        graph = to_networkx(m)

        if plt_error:
            print('unable to draw graph')
        else:
            draw_solution(graph, bfs_search(graph, m.start()), m.start(), m.end())
            output_file = image_file('{}-graph.svg'.format(label))
            plt.savefig(output_file, format="svg")
            print('created {}'.format(output_file))
            print('{}. {}'.format(label, description))
            print()

    with FigureNum(8) as figure_number:
        description = 'Comparing Depth First Search, Breadth First Search, and Guided Search'
        label = caption(chapter, figure_number)

        from ch07.solver_bfs import BreadthFirstSearchSolver
        from ch07.solver_dfs import DepthFirstSearchSolver
        from ch07.solver_guided import GuidedSearchSolver

        random.seed(15)
        m = Maze(13,13)
        if tkinter_error:
            print('unable to generate {}'.format(postscript_output))
        else:
            import tkinter
            root = tkinter.Tk()
            bfs = BreadthFirstSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
            tkinter_register_snapshot(root, bfs.canvas, '{}-BFS.ps'.format(label))
            root.mainloop()

            root = tkinter.Tk()
            dfs = DepthFirstSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
            tkinter_register_snapshot(root, dfs.canvas, '{}-DFS.ps'.format(label))
            root.mainloop()

            root = tkinter.Tk()
            sfs = GuidedSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
            tkinter_register_snapshot(root, sfs.canvas, '{}-Guided.ps'.format(label))
            root.mainloop()
            print('Generated BFS, DFS and Guided Postscript files for {}'.format(label))

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(9) as figure_number:
        description = 'Adjacency Matrix vs. Adjacency List representation'
        label = caption(chapter, figure_number)
        output_adjacency_matrix()
        output_adjacency_list()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(10) as figure_number:
        description = 'Sample directed graph with 12 nodes and 14 edges.'
        label = caption(chapter, figure_number)
        make_sample_directed_graph()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(11) as figure_number:
        description = 'Sample spreadsheet with underlying directed graph.'
        label = caption(chapter, figure_number)
        print('Screen shots from Excel, together with graph from Figure 7-9')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(12) as figure_number:
        description = 'Visualizing execution of Depth First Search for Cycle Detection.'
        label = caption(chapter, figure_number)
        print('Done by hand.')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(13) as figure_number:
        description = 'Visualizing execution of Depth First Search for Topological Sort.'
        label = caption(chapter, figure_number)
        print('Done by hand.')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(14) as figure_number:
        description = 'Modeling highway infrastructure in Massachusetts.'
        label = caption(chapter, figure_number)
        (_, mapPositions, _) = tmg_load(highway_map())
        (_,EAST,_,WEST) = bounding_ids(mapPositions)
        output_file = generate_bfs_and_dijkstra_figure(WEST, EAST)
        print('Generated {}'.format(output_file))
        print('Augmented by hand in SVG')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(15) as figure_number:
        description = 'Modeling highway infrastructure in Massachusetts.'
        label = caption(chapter, figure_number)
        (_, mapPositions, _) = tmg_load(highway_map())
        (_,EAST,_,WEST) = bounding_ids(mapPositions)
        output_file = generate_dfs_figure(WEST, EAST)
        print('Generated {}'.format(output_file))
        print('Augmented by hand in SVG')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(16) as figure_number:
        description = 'The shortest path from a to c has accumulated total of 8'
        label = caption(chapter, figure_number)
        print('Done by hand.')
        print('{}. {}'.format(label, description))
        print()

    with TableNum(1) as table_number:
        description = "Executing Dijkstra's algorithm on small graph"
        label = caption(chapter, table_number)
        DG_GOOD = nx.DiGraph()
        DG_GOOD.add_edge('a', 'b', weight=3)
        DG_GOOD.add_edge('a', 'c', weight=9)
        DG_GOOD.add_edge('b', 'c', weight=4)
        DG_GOOD.add_edge('b', 'd', weight=2)
        DG_GOOD.add_edge('d', 'c', weight=1)
        visualize_dijkstra_small_graph(DG_GOOD)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(2) as table_number:
        description = "A negative edge weight in the wrong place breaks Dijkstra's algorithm"
        label = caption(chapter, table_number)
        DG_GOOD = nx.DiGraph()
        DG_GOOD.add_edge('a', 'b', weight=3)
        DG_GOOD.add_edge('a', 'c', weight=1)
        DG_GOOD.add_edge('b', 'd', weight=-2)   # THIS BREAKS IT
        DG_GOOD.add_edge('c', 'd', weight=1)
        try:
            visualize_dijkstra_small_graph(DG_GOOD)
            print('WARNING: ValueError should have occurred! WARNING WARNING!')
        except ValueError:
            print('Unable to relax from final "b" node')

        print('{}. {}'.format(label, description))
        print()

    with FigureNum(17) as figure_number:
        description = 'Two graphs with negative edge weights, but only one has a negative cycle'
        label = caption(chapter, figure_number)
        DG_GOOD = nx.DiGraph()
        DG_GOOD.add_edge('a', 'b', weight=1)
        DG_GOOD.add_edge('b', 'd', weight=-3)
        DG_GOOD.add_edge('d', 'c', weight=5)
        DG_GOOD.add_edge('c', 'b', weight=-1)

        (dist_to, _) = bellman_ford(DG_GOOD, 'a')
        print('Good Graph: shortest distance from a to b is {}'.format(dist_to['b']))

        DG_BAD = nx.DiGraph()
        DG_BAD.add_edge('a', 'b', weight=1)
        DG_BAD.add_edge('b', 'd', weight=-3)
        DG_BAD.add_edge('d', 'c', weight=5)
        DG_BAD.add_edge('c', 'b', weight=-4)

        try:
            (dist_to, _) = bellman_ford(DG_BAD, 'a')
            print('WARNING: RuntimeError should have occurred! WARNING WARNING!')
        except RuntimeError:
            print('Bad Graph: Negative cycle exists in the graph.')

        print('Done by hand.')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(18) as figure_number:
        description = 'Example for all-pairs shortest path problem'
        label = caption(chapter, figure_number)
        DG_AP = nx.DiGraph()
        DG_AP.add_edge('a', 'b', weight=4)
        DG_AP.add_edge('b', 'a', weight=2)
        DG_AP.add_edge('a', 'c', weight=3)
        DG_AP.add_edge('b', 'd', weight=5)
        DG_AP.add_edge('c', 'b', weight=6)
        DG_AP.add_edge('d', 'b', weight=1)
        DG_AP.add_edge('d', 'c', weight=7)
        print(DG_AP.nodes())
        print(DG_AP.edges(data=True))
        print('Done by hand.')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(19) as figure_number:
        description = 'Intuition behind the all-pairs shortest path problem'
        label = caption(chapter, figure_number)
        print('by hand')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(20) as figure_number:
        description = 'Actual shortest paths, dist_to[][], and node_from[][] for example'
        label = caption(chapter, figure_number)
        DG_TABLE = nx.DiGraph()
        DG_TABLE.add_edge('a', 'b', weight=4)
        DG_TABLE.add_edge('b', 'a', weight=2)
        DG_TABLE.add_edge('a', 'c', weight=3)
        DG_TABLE.add_edge('b', 'd', weight=5)
        DG_TABLE.add_edge('c', 'b', weight=6)
        DG_TABLE.add_edge('d', 'b', weight=1)
        DG_TABLE.add_edge('d', 'c', weight=7)
        visualize_results_floyd_warshall(DG_TABLE)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(21) as figure_number:
        description = 'Initialize dist_to[][] and node_from[][] based on G'
        label = caption(chapter, figure_number)
        DG_TABLE = nx.DiGraph()
        DG_TABLE.add_edge('a', 'b', weight=4)
        DG_TABLE.add_edge('b', 'a', weight=2)
        DG_TABLE.add_edge('a', 'c', weight=3)
        DG_TABLE.add_edge('b', 'd', weight=5)
        DG_TABLE.add_edge('c', 'b', weight=6)
        DG_TABLE.add_edge('d', 'b', weight=1)
        DG_TABLE.add_edge('d', 'c', weight=7)
        visualize_results_floyd_warshall_just_initialize(DG_TABLE)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(22) as figure_number:
        description = 'Changes to node_from[][] and dist_to[][] after k processes a and b'
        label = caption(chapter, figure_number)
        DG_TABLE = nx.DiGraph()
        DG_TABLE.add_edge('a', 'b', weight=4)
        DG_TABLE.add_edge('b', 'a', weight=2)
        DG_TABLE.add_edge('a', 'c', weight=3)
        DG_TABLE.add_edge('b', 'd', weight=5)
        DG_TABLE.add_edge('c', 'b', weight=6)
        DG_TABLE.add_edge('d', 'b', weight=1)
        DG_TABLE.add_edge('d', 'c', weight=7)
        visualize_results_floyd_warshall_two_steps(DG_TABLE)
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    generate_ch07()
