import random
import tkinter

from ch07.maze import Maze

class Viewer:
    # Ensure drawing is not flush against the left-edge or top-edge of window
    OFFSET = 5

    def __init__(self, maze, size):
        self.maze = maze
        self.size = size
        self.built = {}
        self.canvas = None

    def view(self, master):
        """Show window with maze."""
        size = self.size
        w = self.maze.num_cols * size
        h = self.maze.num_rows * size
        canvas = tkinter.Canvas(master, width=w+10, height=h+10)
        canvas.pack()
    
        offset = self.OFFSET
        canvas.create_line(offset,                        offset, offset,                    offset+h, width=3)
        canvas.create_line(offset,                        offset, offset + (w/size//2)*size, offset,   width=3)
        canvas.create_line(offset + size*(1+(w/size)//2), offset, offset + (w/size)*size,    offset,   width=3)
    
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
            inset = 2
            size = self.size
            cx = self.OFFSET + cell[1]*size
            ry = self.OFFSET + cell[0]*size
            self.built[cell] = self.canvas.create_oval(cx + inset, ry + inset, cx + size - 2*inset, ry + size - 2*inset, fill=color)

if __name__ == "__main__":
    random.seed(11)
    m = Maze(50,50)
    root = tkinter.Tk()
    Viewer(m, 15).view(root)
    root.mainloop()
