import random


def to_networkx(maze):
    """Return a NetworkX Graph representing maze."""
    try:
        import networkx as nx
    except ModuleNotFoundError:
        print('Python networkx library is not installed.')
        return

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

class Maze:
    """
    Construct a random maze whose entrance is at the middle of the top row
    of the rectangular maze, and the exit is at the middle of the bottom 
    row.
    """
    def __init__(self, num_rows, num_cols):
        """initialize maze"""
        self.num_rows = num_rows
        self.num_cols = num_cols
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

    def dfs_visit(self, sq):
        """conduct DFS search to build maze"""
        self.marked[sq] = True

        while len(self.neighbors[sq]) > 0:
            cell = random.choice(self.neighbors[sq])
            self.neighbors[sq].remove(cell)
            if not self.marked[cell]:
                self.clear_wall(sq, cell)
                self.dfs_visit(cell)

        self.marked[sq] = True

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
                    path.insert(0, cell)
                    self.marked[cell] = True
            else:
                self.marked[sq] = True
                del path[0]

    def construct(self):
        """construct maze of given height/width and size"""
        self.marked = dict( ((r,c),False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.east_wall = dict( ((r,c),False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.south_wall = dict( ((r,c),False) for r in range(self.num_rows) for c in range(self.num_cols) )
        self.neighbors = dict( ((r,c),[]) for r in range(self.num_rows) for c in range(self.num_cols) )

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

        sq = self.start()
        self.dfs_visit_nr(sq)
        self.south_wall[self.end()] = False    # self.num_rows-1,self.num_cols//2

if __name__ == "__main__":
    random.seed(11)
    m = Maze(7,7)
    g = to_networkx(m)
    import matplotlib.pyplot as plt
    import networkx as nx

    T = nx.dfs_tree(g, source=(0,3))
    print(list(T.edges()))

    pos = nx.get_node_attributes(g, 'pos') 
    nx.draw(g, pos, with_labels = True, node_color="w", font_size=8) 

    plt.show()
