"""
Challenge Exercises for Chapter 7.
"""
import timeit
from algs.table import DataTable, ExerciseNum, caption
from ch07.dependencies import tkinter_error, plt_error
from ch07.maze import Maze

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

def dfs_search_recursive(G, src):
    """Entry to recursive Depth First Search."""
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

def defective_bellman_ford(G, src):
    """
    Conducts ONE TOO FEW iterations of Bellman-Ford
    """
    from ch07.single_source_sp import WEIGHT
    inf = float('inf')
    dist_to = {v:inf for v in G.nodes()}
    dist_to[src] = 0
    edge_to = {}

    def relax(e):
        u, v, weight = e[0], e[1], e[2][WEIGHT]
        if dist_to[u] + weight < dist_to[v]:
            dist_to[v] = dist_to[u] + weight
            edge_to[v] = e
            return True
        return False

    # Don't bother to check for negative cycle, since this is defect!
    num = 0
    for _ in range(G.number_of_nodes()-2):   # DEFECT! ONE FEWER THAN MUST HAVE
        num += 1
        for e in G.edges(data=True):
            relax(e)

    print ('Defective Bellman-Ford only does {} iterations'.format(num))
    return (dist_to, edge_to)

def challenge_bellman_ford():
    """Construct a directed, weighted graph to requires 4 iterations of Bellman-Ford"""
    from ch07.single_source_sp import bellman_ford
    DG = nx.DiGraph()
    DG.add_edge('d', 'e', weight=1)
    DG.add_edge('c', 'd', weight=1)
    DG.add_edge('b', 'c', weight=1)
    DG.add_edge('s', 'b', weight=1)
    
    (defective_dist_to, _) = defective_bellman_ford(DG, 's')
    (dist_to, _) = bellman_ford(DG, 's')

    if dist_to != defective_dist_to:    
        print('Proper Bellman-Ford computes {} but with one fewer iteration it is {}'.format(dist_to, defective_dist_to))

def maze_to_defeat_guided_search(n=15):
    """Construct maze that defeats guided search by forcing exploration of XXX cells."""
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

    return m

def defeat_guided_search(n=15):
    """Construct a rectangular maze graph that thwarts guided search."""
    from ch07.solver_guided import GuidedSearchSolver
    m = maze_to_defeat_guided_search(n)

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

    (_,_,_,WEST) = bounding_ids(positions)
    (dist_to, edge_to) = dijkstra_sp(G, WEST)
    print('Original Dijkstra shortest distance is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, WEST, destination))-1, dist_to[destination]))

    print('num edges:', G.number_of_edges())
    for e in edges_to_remove:
        G.remove_edge(e[0], e[1])
    print('num edges:', G.number_of_edges())

    # create a new graph whose edges are not wholly on I-90
    (_,_,_,WEST) = bounding_ids(positions)
    (dist_to, edge_to) = dijkstra_sp(G, WEST)
    print('Dijkstra shortest distance avoiding I-90 is {} total steps with distance={:.1f}'.format(len(edges_path_to(edge_to, WEST, destination))-1, dist_to[destination]))
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

def annotated_dfs_search(G, src, target):
    """
    Apply non-recursive Depth First Search to a graph from src. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    from ch07.list_stack import Stack
    marked = {}
    node_from = {}

    stack = Stack()
    marked[src] = True
    stack.push(src)

    while not stack.is_empty():
        v = stack.pop()
        if v == target:
            return len(marked)

        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                stack.push(w)

    return len(marked)

def annotated_bfs_search(G, src, target):
    """
    Apply Depth First Search to a graph from a starting node. Return
    dictionary of explored trail.

    Performance is O(N+E) since every edge is visited once for a directed
    graph and twice for an undirected graph.
    """
    from ch07.search import Queue
    marked = {}
    node_from = {}

    q = Queue()
    marked[src] = True
    q.enqueue(src)

    while not q.is_empty():
        v = q.dequeue()
        if v == target:
            return len(marked)

        for w in G[v]:
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                q.enqueue(w)

    return len(marked)

def annotated_guided_search(G, src, target, distance):
    """
    Non-recursive depth-first search investigating given position. Needs
    a distance (node1, node2) function to determine distance between two nodes.

    Performance is O(N log N + E) since every edge is visited once for a directed
    graph and twice for an undirected graph. Each of the N nodes is processed by
    the priority queue, where dequeue() and enqueue() operations are each O(log N).
    While it is unlikely that the priority queue will ever contain N nodes, the
    worst case possibility always exists.
    """
    from ch04.heap import PQ
    marked = {}
    node_from = {}

    pq = PQ(G.number_of_nodes())
    marked[src] = True

    # Using a MAX PRIORITY QUEUE means we rely on negative distance to
    # choose the one that is closest...
    pq.enqueue(src, -distance(src, target))

    while not pq.is_empty():
        v = pq.dequeue()
        if v == target:
            return len(marked)

        for w in G.neighbors(v):
            if not w in marked:
                node_from[w] = v
                marked[w] = True
                pq.enqueue(w, -distance(w, target))

    return len(marked)

def search_trials():
    """
    For randomly constructed NxN mazes, compute efficiency of searching strategies
    on 512 random mazes, as N grows from 4x4 to 128x128
    """
    import random
    from ch07.maze import to_networkx, distance_to
    
    tbl = DataTable([8,8,8,8],['N', 'BFS', 'DS', 'GS'], decimals=2)
    for N in [4, 8, 16, 32, 64, 128]:
        num_bfs = 0
        num_dfs = 0
        num_gs = 0
        for i in range(512):
            random.seed(i)   
            m = Maze(N,N)  
            G = to_networkx(m)
             
            num_bfs += annotated_bfs_search(G, m.start(), m.end())
            num_dfs += annotated_dfs_search(G, m.start(), m.end())
            num_gs += annotated_guided_search(G, m.start(), m.end(), distance_to)
 
        tbl.row([N, num_bfs/512, num_dfs/512, num_gs/512])

    tbl = DataTable([8,8,8,8],['N', 'BFS', 'DS', 'GS'], decimals=2)
    for N in [4, 8, 16, 32, 64, 128]:
        m = maze_to_defeat_guided_search(N)
        G = to_networkx(m)
            
        num_bfs = annotated_bfs_search(G, m.start(), m.end())
        num_dfs = annotated_dfs_search(G, m.start(), m.end())
        num_gs = annotated_guided_search(G, m.start(), m.end(), distance_to)

        tbl.row([N, num_bfs, num_dfs, num_gs])

#######################################################################
if __name__ == '__main__':
    chapter = 7

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
        print(caption(chapter, exercise_number), 'Recover cycle')
        print()

    with ExerciseNum(4) as exercise_number:
        print('recover_negative_cycle in ch07.digraph_search')
        print('tbd')    # TODO
        print(caption(chapter, exercise_number), 'Recover Negative cycle')

    with ExerciseNum(5) as exercise_number:
        print('Construct graph with N=5 nodes requiring 4 iterations')
        challenge_bellman_ford()
        print(caption(chapter, exercise_number), 'Recover cycle')
        print()

    with ExerciseNum(6) as exercise_number:
        search_trials()
        print(caption(chapter, exercise_number), 'Random NxN graphs, N=4 .. 128')
        print()

    with ExerciseNum(7) as exercise_number:
        dag_trials()
        print(caption(chapter, exercise_number), 'DAG trials')

    with ExerciseNum(8) as exercise_number:
        avoid_interstate_90()
        print(caption(chapter, exercise_number), 'Altered route when avoiding I-90')
