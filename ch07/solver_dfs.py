"""Animates the Depth First Search solution of a maze."""
import time
import random

from ch07.maze import Maze, to_networkx
from ch07.viewer import Viewer
from ch07.dependencies import tkinter_error

class DepthFirstSearchSolver():
    """
    Solves a maze using Depth First Search, showing results graphically.
    """
    def __init__(self, master, maze, size, refresh_rate=0.01, stop_end=False):
        self.master = master
        self.viewer = Viewer(maze, size)
        self.marked = {}
        self.node_from = {}

        self.g = to_networkx(maze)
        self.start = maze.start()
        self.end = maze.end()
        self.stop_end = stop_end

        self.refresh_rate = refresh_rate

        master.after(0, self.animate)
        self.canvas = self.viewer.view(master)

    def animate(self):
        """Start animation by initiating DFS."""
        self.dfs_visit_nr(self.start)

        # draw BACK edges to solution
        pos = self.end
        while pos != self.start:
            self.viewer.color_cell(pos, 'lightgray')
            pos = self.node_from[pos]
        self.master.update()

    def dfs_visit_nr(self, pos):
        """Non-recursive depth-first search investigating given position."""
        from ch07.list_stack import Stack
        stack = Stack()
        self.viewer.color_cell(pos, 'blue')
        stack.push(pos)

        while not stack.is_empty():
            cell = stack.pop()
            self.master.update()
            if self.refresh_rate:
                time.sleep(self.refresh_rate)

            if self.stop_end and cell == self.end:
                self.marked[cell] = True
                self.viewer.color_cell(cell, 'blue')
                return True

            for next_cell in self.g.neighbors(cell):
                if not next_cell in self.marked:
                    self.node_from[next_cell] = cell
                    stack.push(next_cell)
                    self.marked[next_cell] = True
                    self.viewer.color_cell(next_cell, 'blue')

        return False

    def dfs_visit(self, pos):
        """Recursive depth-first search investigating given position."""
        self.marked[pos] = True
        self.viewer.color_cell(pos, 'blue')
        self.master.update()
        if self.refresh_rate:
            time.sleep(self.refresh_rate)

        # immediately force all processing to unwind...
        if self.stop_end and pos == self.end:
            return True

        for cell in self.g.neighbors(pos):
            if not cell in self.marked:
                self.node_from[cell] = pos
                if self.dfs_visit(cell):
                    return True

        self.marked[pos] = True
        self.viewer.color_cell(pos, 'blue')
        return False

#######################################################################
if __name__ == '__main__':
    if tkinter_error:
        print('tkinter is not installed so unable to launch DFS solver application')
    else:
        import tkinter
        random.seed(15)
        m = Maze(60,60)
        root = tkinter.Tk()
        dfs = DepthFirstSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
        root.mainloop()
