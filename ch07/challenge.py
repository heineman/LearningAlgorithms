"""
Challenge Exercises for Chapter 7.
"""
from ch07.maze import Maze
import tkinter

def path_to_recursive(node_from, src, target):
    """
    Recursive implementation, which appears similar in logic to a pre-order
    search. First yield the path before me, then yield self.
    """
    if target == src:
        yield src
    else:
        if node_from[target] is None:
            raise ValueError('{} is unreachable from {}'.format(target,src))

        for n in path_to_recursive(node_from, src, node_from[target]):
            yield n
        yield target

def defeat_smart_search():
    """Construct a rectangular maze graph that thwarts smart search."""
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

    root = tkinter.Tk()
    dfs = SmartSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
    root.mainloop()
