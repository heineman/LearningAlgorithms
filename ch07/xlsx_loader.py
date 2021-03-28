"""
Load up rudimentary XLSX file.

worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"

Note that Excel files have a space-saving device to reuse formula that are identical from
one cell to another within a region. I saw this in the Fibonacci Example.

<c r="A3">
  <f>(A2+1)</f>
  <v>1</v>
</c>

<c r="A4">
  <f t="shared" ref="A4:A8" si="0">(A3+1)</f>
  <v>2</v>
</c>

This cell shares the formula (with index si="0") in the region A4:A8, as you can see from
the definition of 'A5' which is 'shared' as marked by the 't' tag, and it is recast to
become (A4+1) in relation to the other one above.

<c r="A5">
  <f t="shared" si="0"/>
  <v>3</v>
</c>

"""
from xml.dom import minidom

class Cell:
    """Represents a cell in the spreadsheet XML."""
    def __init__(self, label, value, formula):
        self.label = label
        self.value = value
        self.formula = formula

def load_xlsx(file):
    """Load up XLS file as rudimentary spreadsheet."""
    from zipfile import ZipFile

    # Will return entries, where each key is cell and contents is either value or proper formula
    entries = {}
    shared_formula = {}

    def diff(cell, base):
        # quick and dirty. Only works for single letters
        return (ord(cell[0]) - ord(base[0]), int(cell[1:]) - int(base[1:]))

    def adjust_formula(cell, si):
        """
        Adjust shared formula for new context, based on the 'base' cell. Note that the reference
        is likely also needed for more complicated examples, but I didn't need it for my
        Fibonacci example.
        """
        from ch06.expression import build_expression, Reference, Value
        (ref, base) = shared_formula[si]

        (delta_c, delta_r) = diff(cell, base)

        base_formula = entries[base]
        expr = build_expression(base_formula[1:])

        def modify_in_place(node):
            """Hack/quick-and-dirty way to modify EXPR in place."""
            if isinstance(node, Value):
                return node

            if isinstance(node, Reference):
                oldref = str(node)
                newref = chr(ord(oldref[0]) + delta_c) + str(int(oldref[1:]) + delta_r)
                return Reference(newref)

            node.left = modify_in_place(node.left)
            node.right = modify_in_place(node.right)
            return node

        # replace each reference with delta
        expr = modify_in_place(expr)
        return '=' + str(expr)

    with ZipFile(file, 'r') as zip_file:
        data = zip_file.read('xl/worksheets/sheet1.xml').decode('utf-8')

        def get_all_text(node):
            """Grab up all text in children and make it available in one step."""
            if node.nodeType ==  node.TEXT_NODE:
                return node.data
            text_string = ""
            for child_node in node.childNodes:
                text_string += get_all_text( child_node )
            return text_string

        doc = minidom.parseString(data)
        access_points = doc.getElementsByTagName('c')   # TAG for cell
        for acc in access_points:
            cell = acc.getAttribute('r')
            value = 0
            t = None
            si = None
            ref = None
            formula = None
            for v in acc.getElementsByTagName('v'):     # TAG for value (may be present with formula)
                value = get_all_text(v)
            for f in acc.getElementsByTagName('f'):     # TAG for formula
                formula = get_all_text(f)
                t = f.getAttribute('t')                 # ATTRIB tag to declare sharing
                ref = f.getAttribute('ref')             # ATTRIB region where sharing is scoped [unused]
                si = f.getAttribute('si')               # ATTRIB for shared index

            # Be sure to represent formula signaled by starting '='
            if formula:
                formula = '=' + formula

            if formula or si:
                if not si:
                    # This is a straight formula that is not (yet) shared
                    entries[cell] = str(formula)
                else:
                    if formula:
                        entries[cell] = str(formula)        # This formula will be shared
                        shared_formula[si] = (ref, cell)    # Remember base reference and cell range of scope
                    else:
                        # find formula with reference AND adjust accordingly
                        entries[cell] = adjust_formula(cell, si)
            else:
                entries[cell] = str(value)
    return entries
