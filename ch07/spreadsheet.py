"""
Spreadsheet application using tkinter to visualize a working spreadsheet.
"""
from ch06.expression import build_expression
from ch07.digraph_search import has_cycle

try:
    import networkx as nx
except ImportError:
    import ch07.replacement as nx

from ch07.dependencies import tkinter_error

def is_formula(s):
    """Determine if string is a formula."""
    return s[0] == '=' if len(s) > 0 else False

class Spreadsheet:
    """
    Represents a spreadsheet.

        Attributes
        ----------
        digraph         - A directed Graph to maintain all cell-based dependencies
                          to detect cycles. When cell 'A2' is set to '=(B3+1)' then
                          an edge B3 -> A2 is added to the graph, so whenever B3 changes,
                          A2 knows it also has to change.
        values          - When a cell contains a formula, this is its floating point value
        expressions     - When a cell contains a formula, this maintains the expression tree
        expressions_raw - When a cell contains a formula, this is its initial string contents
        entries         - For the tkinter GUI, this is text widget for given cell
        string_vars     - For the tkinter GUI, this is StringVar containing the value backing
                          an entry.
    """
    undefined = 'Undef'

    def __init__(self, master, new_digraph, num_rows=10, num_cols=5):
        self.master   = master
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.digraph  = new_digraph
        self.values           = {}
        self.expressions      = {}
        self.expressions_raw  = {}
        self.entries          = {}
        self.string_vars      = {}
        self.make_gui()

    def make_gui(self):
        """Construct the necessary widgets for spreadsheet GUI and set up the event handlers."""
        if tkinter_error:
            return
        import tkinter
        self.canvas = tkinter.Canvas(self.master)

        for r in range(1,self.num_rows):
            tkinter.Label(self.master, text=str(r)).grid(row=r, column=0)
        for c in range(self.num_cols):
            tkinter.Label(self.master, text=chr(ord('A')+c)).grid(row=0, column=c+1)

        for r in range(1, self.num_rows):
            for c in range(1, self.num_cols+1):
                label = chr(ord('A')+c-1) + str(r)
                sv = tkinter.StringVar(self.master, name=label)
                widget = tkinter.Entry(self.master, textvariable=sv)
                widget.bind('<Return>', lambda s=sv, lab=label: self.entry_update(lab, s))
                widget.bind('<FocusIn>', lambda s=sv, lab=label: self.show_formula(lab, s))
                widget.bind('<FocusOut>', lambda s=sv, lab=label: self.show_value(lab, s))
                widget.grid(row=r, column=c)
                self.entries[label] = widget
                self.string_vars[label] = sv

    def entry_update(self, label, event):
        """Updates the contents of a spreadsheet cell in response to user input."""
        try:
            self.set(label, self.string_vars[label].get())
        except RuntimeError:
            self.string_vars[label].set('#Cycle')

    def show_formula(self, label, event):
        """Changes a label's view to a formula, if present, when cell gains focus."""
        if label in self.expressions_raw:
            self.string_vars[label].set(self.expressions_raw[label])

    def show_value(self, label, event):
        """Resumes showing the value for a label, when cell loses focus."""
        if label in self.expressions_raw:
            self.string_vars[label].set(self.values[label])

    def get(self, cell):
        """Return the value of a cell, or 0 if not yet available."""
        if cell in self.values:
            return self.values[cell]
        return 0

    def set(self, cell, sval):
        """
        Update the value of a cell. Raises Runtime Error if cycle would be induced, otherwise
        make change and recompute other cells.
        """
        if cell in self.expressions:                               # Clear old dependencies IN CASE changed...
            for v in set(self.expressions[cell].references()):     # convert to set to eliminate duplicates
                self.digraph.remove_edge(v, cell)

        self.string_vars[cell].set(sval)                           # Set contents (non-numeric is set to zero)
        self.digraph.add_node(cell)                                # Make sure node is in DiGraph

        if is_formula(sval):
            self.values[cell] = self.undefined
            self.expressions_raw[cell] = sval
            self.expressions[cell] = build_expression(self.expressions_raw[cell][1:], self.values)
            for v in set(self.expressions[cell].references()):     # convert to set to eliminate duplicates
                self.digraph.add_edge(v, cell)

            if has_cycle(self.digraph):
                for v in set(self.expressions[cell].references()): # convert to set to eliminate duplicates
                    self.digraph.remove_edge(v, cell)
                self.expressions.pop(cell, None)      # Pythonic way of deleting key
                self.expressions_raw.pop(cell, None)  # Pythonic way of deleting key
                raise RuntimeError('Changing {} to {} creates cycle.'.format(cell, sval))
        else:
            self.expressions.pop(cell, None)          # Pythonic way of deleting key
            self.expressions_raw.pop(cell, None)      # Pythonic way of deleting key

        self._recompute(cell)                         # now recompute dependencies

    def _recompute(self, cell):
        """Internal API to recursively ripple changes through spreadsheet."""
        if cell in self.expressions:
            try:
                self.values[cell] = self.expressions[cell].eval()
            except TypeError:
                self.values[cell] = 0        # bad formula
            self.string_vars[cell].set(str(self.values[cell]))
        else:
            try:
                self.values[cell] = float(self.string_vars[cell].get())
            except ValueError:
                self.values[cell] = self.string_vars[cell].get()

        if cell in self.digraph:
            for w in self.digraph[cell]:
                self._recompute(w)

#######################################################################
if __name__ == '__main__':
    if tkinter_error:
        print('Unable to launch spreadsheet application without access to tkinter')
    else:
        import tkinter
        root = tkinter.Tk()
        root.title('You must press ENTER to change the contents of a cell.')
        ss = Spreadsheet(root, nx.DiGraph())
        root.mainloop()
