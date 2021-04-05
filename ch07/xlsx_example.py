"""
Load up XLSX Fibonacci file.

This is only a proof of concept and not meant to work for arbitrary XLSX files!
"""
import os
from ch07.xlsx_loader import load_xlsx

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from ch07.dependencies import tkinter_error

def load_fibonacci_from_resource(ss):
    """Load up sample XLSX Microsoft Excel file as a Spreadsheet."""
    entries = load_xlsx(os.path.join('..', 'resources', 'ch07-fibonacci-example.xlsx'))
    for k in entries:
        ss.set(k,entries[k])

#######################################################################
if __name__ == '__main__':

    if tkinter_error:
        print('tkinter is not installed so unable to launch spreadsheet application')
    else:
        import tkinter
        from ch07.spreadsheet import Spreadsheet

        root = tkinter.Tk()
        ss = Spreadsheet(root, nx.DiGraph())
        load_fibonacci_from_resource(ss)

        # Might not be necessary IF entries are loaded in proper topological order!
        from ch07.digraph_search import topological_sort
        print(list(topological_sort(ss.digraph)))
        root.mainloop()
