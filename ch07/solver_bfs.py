"""Animates the Breadth First Search solution of a maze."""
import time
import random

from ch07.maze import Maze, to_networkx
from ch07.viewer import Viewer
from ch07.dependencies import tkinter_error

class BreadthFirstSearchSolver():
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
        self.bfs_visit(self.start)

        # draw BACK edges to solution
        pos = self.end
        while pos != self.start:
            self.viewer.color_cell(pos, 'lightgray')
            pos = self.node_from[pos]
        self.master.update()

    def bfs_visit(self, pos):
        """Recursive depth-first search investigating given position."""
        from ch04.list_queue import Queue

        queue = Queue()
        self.viewer.color_cell(pos, 'blue')
        queue.enqueue(pos)

        while not queue.is_empty():
            cell = queue.dequeue()
            self.master.update()
            if self.refresh_rate:
                time.sleep(self.refresh_rate)

            for next_cell in self.g.neighbors(cell):
                if not next_cell in self.marked:
                    self.node_from[next_cell] = cell
                    self.marked[next_cell] = True
                    self.viewer.color_cell(next_cell, 'blue')
                    if self.stop_end and next_cell == self.end:
                        return True
                    queue.enqueue(next_cell)

        return False

#######################################################################
if __name__ == '__main__':
    if tkinter_error:
        print('tkinter is not installed so unable to launch BFS solver application')
    else:
        import tkinter
        random.seed(15)
        m = Maze(60,60)
        root = tkinter.Tk()
        dfs = BreadthFirstSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
        root.mainloop()
