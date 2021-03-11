"""Code for chapter 07."""

import networkx as nx
from algs.table import captionx, FigureNum, TableNum, process

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

    print(len(G.nodes()), 'nodes and ', len(G.edges()), 'edges.')
    print('neighbors of C3:', list(G['C3']))
    print('edges adjacent to C3:', list(G.edges('C3')))

def generate_ch06():
    """Generate Tables and Figures for chapter 07."""
    chapter = 7

    with FigureNum(1) as figure_number:
        description  = 'An undirected graph of 12 vertices and 12 edges'
        make_sample_graph()
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    generate_ch06()
