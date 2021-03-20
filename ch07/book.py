"""Code for chapter 07."""

import timeit
try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx
    
from algs.table import DataTable, captionx, FigureNum, TableNum, process

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

    print(G.number_of_nodes(), 'nodes and ', G.number_of_edges(), 'edges.')
    print('neighbors of C3:', list(G['C3']))
    print('edges adjacent to C3:', list(G.edges('C3')))

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

    print(DG.number_of_nodes(), 'nodes and ', DG.number_of_edges(), 'edges.')
    print('neighbors of C3:', list(DG['C3']))
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

def table_topological_example():
    """Compare Topological sort performance."""
    try:
        import networkx as nx
    except ImportError:
        from ch07.graph import Replacement
        nx = Replacement()
        
    DG = nx.DiGraph()    
    topological_example(DG,4)
   
    tbl = DataTable([8, 8, 12, 12], ['N', 'E', 'Built-In', 'Topological Sort'], decimals=4)
    tbl.format('E', ',d')
    for N in [2**k for k in range(1, 8)]:
        built_in = 1000*min(timeit.repeat(stmt='''nx.topological_sort(DG)''', setup='''
from ch07.book import topological_example
try:
    import networkx as nx
except ImportError:
    from ch07.graph import Replacement
    nx = Replacement()
DG = nx.DiGraph()    
topological_example(DG,{})'''.format(N), repeat=5, number=3))
        
        mtime = 1000*min(timeit.repeat(stmt='''topological_sort(DG)''', setup='''
from ch07.digraph_search import topological_sort
from ch07.book import topological_example
try:
    import networkx as nx
except ImportError:
    from ch07.graph import Replacement
    nx = Replacement()
DG = nx.DiGraph()    
topological_example(DG,{})'''.format(N), repeat=5, number=3))
        DG = nx.DiGraph()    
        topological_example(DG, N)
        tbl.row([len(list(DG.nodes())), len(list(DG.edges())), built_in, mtime])
    return tbl

def generate_ch07():
    """Generate Tables and Figures for chapter 07."""
    chapter = 7

    with FigureNum(1) as figure_number:
        description  = 'An undirected graph of 12 vertices and 12 edges'
        make_sample_graph()
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

def table_compare_graph_structures():
    """Compare Matrix implementation vs. Adjacency list implementation vs. NetworkX."""
    
    tbl = DataTable([8, 10, 10, 10], ['N', 'NetworkX', 'Adjacency List', 'Adjacency Matrix'])
    for N in [2**k for k in range(8, 20)]:
        undirect_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.graph import UndirectedGraph
G = UndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))

        networkx_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.graph import UndirectedGraph
G = UndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))

        matrix_mtime = 1000*min(timeit.repeat(stmt='''
total=0
for w in G[0]:
    total += w''', setup='''
from ch07.graph import MatrixUndirectedGraph
G = MatrixUndirectedGraph()
G.add_nodes_from(list(range({0})))
for o in range(10):
    G.add_edge(0, {0}-o-1)'''.format(N), repeat=20, number=20))
        
        tbl.row([N, networkx_mtime, undirect_mtime, matrix_mtime])
    return tbl

def defeat_smart_search():
    """Construct a rectangular maze graph that thawarts smart search."""
    from ch07.maze import Maze
    from ch07.solver_smart import SmartSearchSolver
    m = Maze(13,13)
    m.initialize()    # back to scratch WITH ALL WALLS
    
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
        
    import tkinter
    
    root = tkinter.Tk()
    dfs = SmartSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
    root.mainloop()

#######################################################################
if __name__ == '__main__':
    """
    Need strategy for dealing with situations when pyplot not installed.
    """
    defeat_smart_search()
    make_sample_graph()
    table_topological_example()
    #make_sample_directed_graph()
    #defeat_smart_search()
    #generate_ch07()
