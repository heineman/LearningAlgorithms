import random

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

def distance_to_target(from_cell, to_cell):
    """Compute Manhattan distance between two cells in a rectangular maze."""
    return abs(from_cell[0] - to_cell[0]) + abs(from_cell[1] - to_cell[1])

def to_networkx(maze):
    """Return a NetworkX Graph representing maze."""

    # Undirected graph can represent a maze.
    G = nx.Graph()

    # Add each node with positional information to retain the
    # visual memory of how the maze looks
    for r in range(maze.num_rows):
        for c in range(maze.num_cols):
            G.add_node( (r,c), pos=(c, maze.num_rows - r))

    # An edge between two vertices exists IF THERE IS NO WALL
    for r in range(maze.num_rows):
        for c in range(maze.num_cols):
            if not maze.south_wall[r,c] and r < maze.num_rows -1:
                G.add_edge( (r,c), (r+1,c))
            if not maze.east_wall[r,c]:
                G.add_edge( (r,c), (r,c+1))
    return G

def solution_graph(G, path):
    """
    Return a NetworkX Graph representing solution in maze.
    Remove all vertices that are not in the path
    """
    
    # Bring over positional information from G
    H = nx.DiGraph()
    pos = nx.get_node_attributes(G, 'pos') 
    
    for n in G.nodes():
        H.add_node(n, pos=pos.get(n))
    
    for idx in range(len(path)-1):
        H.add_edge(path[idx], path[idx+1])
    
    return H

def node_from_field(G, node_from):
    """
    Return a directed NetworkX Graph representing structure
    of the node_from dictionary.
    """

    # Bring over positional information from G
    pos = nx.get_node_attributes(G, 'pos') 
    H = nx.DiGraph()
    for n in G.nodes():
        H.add_node(n, pos=pos.get(n))

    # show the former edges.
    for v in node_from:
        H.add_edge(v, node_from[v])

    return H

class Maze:
    """
    Construct a random maze whose entrance is at the middle of the top row
    of the rectangular maze, and the exit is at the middle of the bottom 
    row.
    
    The basic technique is to assemble a maze where every cell has intact walls, 
    and then conduct a depth-first-search through the maze, tearing down walls
    when heading into a new, unvisited cell.
    
    To add a bit of variety, a salt parameter randomly clears additional walls,
    with a default setting of 0.05. If you salt=0, then the maze will have
    perfectly cut rooms, with a long and winding solution to the maze.
    
    This implementation uses stack-based Depth First Search to handle cases
    with large mazes.
    """
    def __init__(self, num_rows, num_cols, salt=0.05):
        """initialize maze"""

        if salt < 0 or salt > 1:
            raise ValueError('salt parameter must be a floating point between 0 and 1 inclusive.')

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.salt = salt
        self.construct()

    def start(self):
        """Starting cell for maze."""
        return (0, self.num_cols//2)

    def end(self):
        """Ending cell for maze."""
        return (self.num_rows-1, self.num_cols//2)

    def clear_wall(self, from_cell, to_cell):
        """Remove wall between two cells"""
        if from_cell[1] == to_cell[1]:
            self.south_wall[min(from_cell[0],to_cell[0]),from_cell[1]] = False
        else:
            self.east_wall[from_cell[0], min(from_cell[1], to_cell[1])] = False

    def clear_all_walls(self, in_cell):
        """Clear all walls for cell as part of attempt to open more solutions."""
        if 0 < in_cell[0] < self.num_rows-1:
            self.south_wall[in_cell[0], in_cell[1]] = False
        if 0 < in_cell[1] < self.num_cols-1:
            self.east_wall[in_cell[0], in_cell[1]] = False

        if 0 < in_cell[1] < self.num_cols-1:
            self.east_wall[in_cell[0], in_cell[1]-1] = False
        if 0 < in_cell[0] < self.num_rows-1:
            self.south_wall[in_cell[0]-1, in_cell[1]] = False

    def dfs_visit_nr(self, sq):
        """conduct non-recursive DFS search to build maze"""
        path = [sq]
        self.marked[sq] = True

        while len(path) > 0:
            sq = path[0]
            more = self.neighbors[sq]
            if len(more) > 0:
                cell = random.choice(self.neighbors[sq])
                self.neighbors[sq].remove(cell)
                if not self.marked[cell]:
                    self.clear_wall(sq, cell)
                    if random.random() < self.salt:
                        self.clear_all_walls(sq)
                    path.insert(0, cell)
                    self.marked[cell] = True
            else:
                self.marked[sq] = True
                del path[0]

    def initialize(self):
        """Reset to initial state with no walls and all neighbors are set."""
        self.marked     = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.east_wall  = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.south_wall = dict( ((r,c), False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.neighbors  = dict( ((r,c), [])    for r in range(self.num_rows) for c in range(self.num_cols) )

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.east_wall[r,c] = True
                self.south_wall[r,c] = True

                if r != 0:
                    self.neighbors[r,c].append((r-1,c))
                if r != self.num_rows-1:
                    self.neighbors[r,c].append((r+1,c))

                if c != 0:
                    self.neighbors[r,c].append((r,c-1))
                if c != self.num_cols-1:
                    self.neighbors[r,c].append((r,c+1))

    def construct(self):
        """construct maze of given height/width and size."""
        self.initialize()
        sq = self.start()
        self.dfs_visit_nr(sq)
        self.south_wall[self.end()] = False

#######################################################################
if __name__ == '__main__':
    random.seed(15)     # 28 is also good
    m = Maze(3,5)
    g = to_networkx(m)
    import matplotlib.pyplot as plt

    pos = nx.get_node_attributes(g, 'pos') 
    nx.draw(g, pos, with_labels = True, node_color='w', font_size=8) 

    plt.show()
