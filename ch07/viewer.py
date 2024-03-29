"""View the contents of Maze, a rectangular maze object, scaled to cells of given size."""
import random

from ch07.maze import Maze
from ch07.dependencies import tkinter_error

class Viewer:
    """
    Tkinter application to view a maze generated from Maze().
    """
    # Ensure drawing is not flush against the left-edge or top-edge of window
    OFFSET = 8

    # inset the circles for the path so they are visible.
    INSET = 2

    def __init__(self, maze, size):
        self.maze = maze
        self.size = size
        self.built = {}
        self.canvas = None

    def view(self, master):
        """Show window with maze and return constructed tkinter canvas into which it was drawn."""
        if tkinter_error:
            return None
        import tkinter

        size = self.size
        w = self.maze.num_cols * size
        h = self.maze.num_rows * size
        canvas = tkinter.Canvas(master, width=w+10, height=h+10)
        canvas.pack()

        offset = self.OFFSET

        # Draw Vertical border at the left edge, then the top row in two pieces to show entrance. Note that
        # the other borders of the maze are drawn as part of each individual cell
        canvas.create_line(offset,                        offset, offset,                    offset+h, width=3)
        canvas.create_line(offset,                        offset, offset + (w/size//2)*size, offset,   width=3)
        canvas.create_line(offset + size*(1+(w/size)//2), offset, offset + (w/size)*size,    offset,   width=3)

        # Draw each cell, by its east (right) edge and south (bottom) walls if they exist.
        for r in range(self.maze.num_rows):
            for c in range(self.maze.num_cols):
                if self.maze.south_wall[r,c]:
                    canvas.create_line(offset + c*size, offset + (r+1)*size, offset + (c+1)*size, offset + (r+1)*size, width=3)
                if self.maze.east_wall[r,c]:
                    canvas.create_line(offset + (c+1)*size, offset + r*size, offset + (c+1)*size, offset + (r+1)*size, width=3)

        self.canvas = canvas
        return canvas

    def color_cell(self, cell, color):
        """
        Either create new visible cell or change its color. Store created elements in self.built
        so they can be recolored if invoked again.
        """
        if cell in self.built:
            self.canvas.itemconfig(self.built[cell], fill=color)
        else:
            # inset the circles for the path so they are visible.
            inset = self.INSET
            size = self.size
            cx = self.OFFSET + cell[1]*size + 1   # fudge factor to move off the wall...
            ry = self.OFFSET + cell[0]*size + 1
            self.built[cell] = self.canvas.create_oval(cx + inset, ry + inset, cx + size - 2*inset, ry + size - 2*inset, fill=color)

#######################################################################
if __name__ == '__main__':
    if tkinter_error:
        print('Unable to visualize maze without tkinter')
    else:
        import tkinter
        random.seed(15)
        m = Maze(50,50,salt=0.05)
        root = tkinter.Tk()
        Viewer(m, 15).view(root)
        root.mainloop()
