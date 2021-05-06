"""
Challenge Exercises for Chapter 7.
"""
from ch07.maze import Maze

from ch07.dependencies import tkinter_error

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

def defeat_guided_search():
    """Construct a rectangular maze graph that thwarts guided search."""
    from ch07.solver_guided import GuidedSearchSolver
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

    if tkinter_error:
        print('tkinter is not installed so unable to visualize Guided search being defeated.')
    else:
        import tkinter
        from ch07.snapshot import tkinter_register_snapshot
        root = tkinter.Tk()
        sss = GuidedSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
        tkinter_register_snapshot(root, sss.canvas, 'Ch07-Defeat-Guided-Search.ps')
        root.mainloop()

#######################################################################
if __name__ == '__main__':
    defeat_guided_search()
