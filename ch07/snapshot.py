"""
Convenience function for taking a snapshot of a canvas into 
designated file AND terminating tkinter application.
"""
from algs.output import image_file

def tkinter_register_snapshot(root, canvas, file_name):
    """
    Install a callback immediately after launch of application, which
    will save contents of canvas to postscript. Use any of the available
    conversion cools to create PNG or JPG images. Must give it time to
    draw. Certainly one second is more than enough...
    """
    root.after(1000, tkinter_to_file, root, canvas, file_name)

def tkinter_to_file(root, canvas, ps_file):
    """Snapshot the current canvas. Also, cleanly shutdown tkinter so it can run again."""
    canvas.postscript(file=image_file(ps_file), colormode='color')
    root.withdraw()
    root.destroy()
    root.quit()