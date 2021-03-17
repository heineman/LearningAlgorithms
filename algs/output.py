"""
Provide access to where images are output.
"""
import os

IMAGE_DIR = 'images'

def visualize(tbl, description, label, xaxis='Problem instance size', yaxis='Time (in seconds)'):
    """
    Plot the table and store into file. If MatPlotLib is not installed, this
    silently ignores this request.
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except ImportError:
        return

    # make sure interactive is off....
    plt.ioff()

    # Grab x values from the first label in headers
    x_arr = np.array(tbl.column(tbl.labels[0]))
    fig, axes = plt.subplots()

    # It may be that some of these columns are PARTIAL; if so, truncate xs as well
    for hdr in tbl.labels[1:]:
        yvals = np.array(tbl.column(hdr))
        xvals = x_arr[:]
        if len(yvals) < len(xvals):
            xvals = xvals[:len(yvals)]

        axes.plot(xvals, yvals, label=hdr)

    axes.set(xlabel=xaxis, ylabel=yaxis, title=description)
    axes.legend(loc='upper left')
    axes.grid()

    img_file = image_file(label)
    fig.savefig(img_file)
    print('Wrote image to', img_file)
    print()

def image_file(relative_name):
    """
    Return file location where image directory is found, using relative_name.
    If directory does not exist, then just place in current directory.
    """
    # If directory exists, then return
    if os.path.isdir(IMAGE_DIR):
        return ''.join([IMAGE_DIR, os.sep, relative_name])

    if os.path.isdir(''.join(['..', os.sep, IMAGE_DIR])):
        return ''.join(['..', os.sep, IMAGE_DIR, os.sep, relative_name])

    return ''.join(['.',os.sep,relative_name])
