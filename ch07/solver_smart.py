"""Animates the Smart Search solution of a maze."""
import time
import random

from ch07.maze import Maze, to_networkx
from ch07.viewer import Viewer
from ch07.dependencies import tkinter_error

class SmartSearchSolver():
    """
    Solves a maze by taking advantage of Euclidean distance to solution.
    """
    def __init__(self, master, maze, size, refresh_rate=0.01, stop_end=False):
        self.master = master
        self.viewer = Viewer(maze, size)
        self.marked = {}
        self.node_from = {}
        self.size = maze.num_rows * maze.num_cols

        self.g = to_networkx(maze)
        self.start = maze.start()
        self.end = maze.end()
        self.stop_end = stop_end

        self.refresh_rate = refresh_rate

        master.after(0, self.animate)
        self.canvas = self.viewer.view(master)

    def animate(self):
        """Start animation by initiating DFS."""
        self.smart_search(self.start)

        # draw BACK edges to solution
        pos = self.end
        while pos != self.start:
            self.viewer.color_cell(pos, 'lightgray')
            if pos in self.node_from:
                pos = self.node_from[pos]
            else:
                # Turns out there was no solution...
                break
        self.master.update()

    def distance_to(self, to_cell):
        """Return Manhattan distance between cells."""
        return abs(self.end[0] - to_cell[0]) + abs(self.end[1] - to_cell[1])

    def smart_search(self, pos):
        """use Manhattan distance to maze end as priority in PQ to guide search."""
        from ch04.heap import PQ
        pq = PQ(self.size)
        self.viewer.color_cell(pos, 'blue')
        src = self.start
        dist_to = {}
        dist_to[src] = 0

        # Using a MAX PRIORITY QUEUE means we rely on negative distance to
        # choose the one that is closest...
        self.marked[src] = True
        pq.enqueue(src, -self.distance_to(src))

        while not pq.is_empty():
            cell = pq.dequeue()
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
                    dist_to[next_cell] = dist_to[cell] + 1
                    pq.enqueue(next_cell, -self.distance_to(next_cell))
                    self.marked[next_cell] = True
                    self.viewer.color_cell(next_cell, 'blue')

        return False

#######################################################################
if __name__ == '__main__':
    if tkinter_error:
        print('tkinter is not installed so unable to launch Smart solver application')
    else:
        import tkinter
        random.seed(15)
        m = Maze(60,60)
        root = tkinter.Tk()
        dfs = SmartSearchSolver(root, m, 15, refresh_rate=0, stop_end=True)
        root.mainloop()
