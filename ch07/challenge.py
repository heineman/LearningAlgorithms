"""
Challenge Exercises for Chapter 7.
"""
from algs.table import DataTable, ExerciseNum, caption
from ch07.dependencies import tkinter_error, plt_error
import timeit

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx
    
from ch07.maze import Maze
from ch07.dependencies import tkinter_error

def dfs_search_recursive(G, src):
    marked = {}
    node_from = {}

    def dfs(v):
        """Recursive DFS."""
        marked[v] = True
        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                dfs(w)

    dfs(src)
    return node_from

def path_to_recursive(node_from, src, target):
    """
    Recursive implementation, which appears similar in logic to a pre-order
    search. First yield the path before me, then yield self.
    """
    if target == src:
        yield src
    else:
        if target not in node_from:
            raise ValueError('{} is unreachable from {}'.format(target,src))

        for n in path_to_recursive(node_from, src, node_from[target]):
            yield n
        yield target

def defeat_guided_search(n=15):
    """Construct a rectangular maze graph that thwarts guided search."""
    from ch07.solver_guided import GuidedSearchSolver
    m = Maze(n,n)
    m.initialize()                     # back to scratch WITH ALL WALLS

    for r in range(0, m.num_rows-2):   # leave open the first and last
        for c in range(0, m.num_cols):
            m.south_wall[(r,c)] = False
    m.south_wall[(m.num_rows-2,0)] = False
    m.south_wall[(m.num_rows-2,m.num_cols-1)] = False
    m.east_wall[(m.num_rows-1,0)] = False
    m.east_wall[(m.num_rows-1,m.num_cols-2)] = False
    m.east_wall[(0,0)] = False
    m.east_wall[(0,m.num_cols-2)] = False

    for r in range(0, m.num_rows):   # leave open the first and last
        for c in range(1, m.num_cols-2):
            m.east_wall[(r,c)] = False

    if tkinter_error:
        print('tkinter is not installed so unable to visualize Guided search being defeated.')
    else:
        import tkinter
        from ch07.snapshot import tkinter_register_snapshot
        root = tkinter.Tk()
        sss = GuidedSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
        tkinter_register_snapshot(root, sss.canvas, 'Ch07-Defeat-Guided-Search.ps')
        root.mainloop()

def avoid_interstate_90():
    """Find shortest path from westernmost-MA to easternmost-MA that avoids I-90."""
    if plt_error:
        return None
    import matplotlib.pyplot as plt
    from ch07.single_source_sp import dijkstra_sp, edges_path_to
    from ch07.tmg_load import tmg_load, plot_gps, plot_highways, bounding_ids
    from resources.highway import highway_map
    from ch07.plot_map import plot_path
    from algs.output import image_file
    (G,positions,labels) = tmg_load(highway_map())
    
    # Since graph is undirected, we will visit each edge twice. Make sure to
    # only remove when u < v to avoid deleting same edge twice
    edges_to_remove = []
    destination = None
    for u in G.nodes():
        if labels[u] == 'I-90@134&I-93@20&MA3@20(93)&US1@I-93(20)':       # SPECIAL LABEL in BOSTON
            destination = u
        for v in G.adj[u]:
            if 'I-90' in labels[u] and 'I-90' in labels[v] and u < v:
                edges_to_remove.append((u,v))

    print('num edges:', G.number_of_edges())
    for e in edges_to_remove:
        G.remove_edge(e[0], e[1])
    print('num edges:', G.number_of_edges())
    
    # create a new graph whose edges are not wholly on I-90
    (_,_,_,WEST) = bounding_ids(positions)
    (dist_to, edge_to) = dijkstra_sp(G, WEST)
    print('Dijkstra shortest distance is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, WEST, destination))-1, dist_to[destination]))
    path = edges_path_to(edge_to,WEST, destination)
    plt.clf()
    plot_gps(positions)
    plot_highways(positions, G.edges())
    plot_path(positions, path)
   
    output_file = image_file('figure-mass-no-I-90-dijkstra.svg')
    plt.savefig(output_file, format="svg")
    print(output_file)
    plt.clf()
    return output_file

def mesh_graph(n):
    """Return a mesh graph with N^2 nodes(labeled 1 to N^2) and edges that form a mesh."""
    G = nx.DiGraph()

    # add nodes/edges in expanding left of mesh
    label = 1
    num = 1
    while num < n:
        for idx in range(num):
            G.add_edge(label, label+num, weight=1)     # two edges for each node
            G.add_edge(label, label+num+1, weight=1)
            label += 1
        num += 1

    # add nodes in collapsing right of mesh
    while n > 1:
        for idx in range(n):
            if idx != 0:
                G.add_edge(label, label+n-1, weight=1)     # two edges for each node
            if idx != n-1:
                G.add_edge(label, label+n, weight=1)
            label += 1
        n -= 1

    return G

def topological_sp(DAG, src):
    """Given a DAG, compute shortest path from src."""
    from ch07.digraph_search import topological_sort
    from ch07.single_source_sp import WEIGHT
    
    inf = float('inf')
    dist_to = {v:inf for v in DAG.nodes()}
    dist_to[src] = 0
    edge_to = {}
    
    def relax(e):
        n, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[n] + weight < dist_to[v]:
            dist_to[v] = dist_to[n] + weight
            edge_to[v] = e
            
    for n in topological_sort(DAG):
        for e in DAG.edges(n, data=True):
            relax(e)
    
    return (dist_to, edge_to)

def dag_trials(output=True):
    """Confirm DAG single-source shortest path is O(E+N)."""
    tbl = DataTable([8,10,10],['N', 'Dijkstra', 'Topologic'], output=output)

    for n in [2**k for k in range(2,7)]:
        dijkstra = 1000*min(timeit.repeat(stmt='dijkstra_sp(dg,1)', setup='''
from ch07.challenge import mesh_graph
from ch07.single_source_sp import dijkstra_sp
dg=mesh_graph({})'''.format(n), repeat=20, number=15))/15

        topologic = 1000*min(timeit.repeat(stmt='topological_sp(dg,1)', setup='''
from ch07.challenge import mesh_graph, topological_sp
dg=mesh_graph({})'''.format(n), repeat=20, number=15))/15

        tbl.row([n*n, dijkstra, topologic])

#######################################################################
if __name__ == '__main__':
    chapter = 7
    #avoid_interstate_90()
    dag_trials()
    
    with ExerciseNum(1) as exercise_number:
        print('dfs_search_recursive in ch07.challenge')
        print(caption(chapter, exercise_number), 'Recursive depth first search')
        print()

    with ExerciseNum(2) as exercise_number:
        print('path_to_recursive implementation')
        print(caption(chapter, exercise_number), 'Recursive Path_to')
        print()

    with ExerciseNum(3) as exercise_number:
        print('recover_cycle in ch07.digraph_search')
        print()
        print(caption(chapter, exercise_number), 'Recover cycle')

    print('A maze that defeats Guided Search.')
    defeat_guided_search()
