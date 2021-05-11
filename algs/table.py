"""
Helper functions for working with the book. This includes methods to
reproduce tables and figures.

When using these models to fit data, it is always challenging to find
the model that is "best". The primary issue is that there is going to
be some overlap, no matter what you do. For example,

  * Linear = A*N + B
  * Quadratic = C*N*N + D*N
  * Log Linear = E*N*Log N + F*N

These are all "equivalent" if C is VERY VERY close to ZERO (effectively
canceling the N^2 term) and E is VERY VERY close to ZERO (effectively
canceling the N*Log N term.

"""
from contextlib import contextmanager

from algs.output import visualize
from algs.modeling import best_models, pearson_correlation

# When a table wants to skip a value, select this one.
SKIP = '*'

class DataTable:
    """
    A class used to represent a table with columns.

    Each column has a fixed width and a format to be applied to its values.

    Standard practice is to do following:

        :Example:

        >>> from algs.table import DataTable
        >>> tbl = DataTable([8, 8], ['N', 'SquareRoot'], decimals=4)
        >>> for n in range(2,10):
        >>>    tbl.row([n, n ** 0.5])
        >>>
               N    SquareRoot
               2      1.4142
               3      1.7321
               4      2.0000
               5      2.2361
               6      2.4495
               7      2.6458
               8      2.8284
               9      3.0000

    """
    def __init__(self, widths, labels, output=True, decimals=3):
        assert len(widths) == len(labels)
        self.output = output
        self.labels = labels
        self.widths = widths
        self.fmt = ''
        self.entry_fmt = ''
        self.values = {}
        self.num_rows = 0
        self.row_index = {}
        symbol = ',d'
        for idx,width in enumerate(widths):
            self.fmt += '{{0[{}]:>{}}}\t'.format(idx, width)
            self.entry_fmt += '{{0[{}]:>{}{}}}\t'.format(idx, width, symbol)
            symbol = '.{}f'.format(decimals)
        if output:
            print(self.fmt.format(labels))

    def set_output(self, status):
        """Turn on/off output status for row() method calls."""
        self.output = status

    def format(self, field, fmt):
        """
        Change the format of this entry from 'f' into the given format.
        Defect: If change first column to 'f', then decimals length is ignored.
        """
        idx = self.labels.index(field)
        if idx < 0:
            raise ValueError('{} is not a valid field'.format(field))

        # {0[IDX]:>FORMAT}
        target = '{{0[{}]:>'.format(idx)
        where = self.entry_fmt.index(target)
        rest = self.entry_fmt.find('}', where)
        prefix = self.entry_fmt[:where + len(target)]
        suffix = self.entry_fmt[rest:]
        self.entry_fmt = prefix + str(self.widths[idx]) + fmt + suffix

    def row(self, row):
        """
        Helper method to load up an entire row of values.
        If any values are SKIP then must eliminate without throwing off the formatting of output
        """
        if self.output:
            formats = self.entry_fmt.split('\t')

            if SKIP in row:
                new_formats = []
                for fmt,val,width in zip(formats, row, self.widths):
                    if val == SKIP:
                        new_formats.append('{}:>{}s}}'.format(fmt.split(':')[0], width))
                    else:
                        new_formats.append(fmt)
                formats = new_formats

            if len(row) == len(self.labels):
                print('\t'.join(formats).format(row))
            else:
                # assume partial rows are left-justified... WILL BE REPLACED WITH SKIP...
                print('\t'.join(formats[:len(row)]).format(row))

        if not row[0] in self.values:
            self.values[row[0]] = {}
            self.row_index[self.num_rows] = row[0]
            self.num_rows += 1

        # replace all values
        for idx in range(1,len(row)):
            self.values[row[0]][self.labels[idx]] = row[idx]

    def header(self, column):
        """Return the header for the row."""
        return self.labels[column]

    def entry(self, row, column):
        """If row and column belongs to value, return entry."""
        if row in self.values:
            vals = self.values[row]
            if column in vals:
                return vals[column]
        return None

    def column(self, column):
        """Return array of values in given column. Eliminate 'SKIP' and remaining."""
        cols = []
        for row in range(self.num_rows):
            label = self.row_index[row]
            vals = self.values[label]

            if column in vals:
                cols.append(vals[column])
            elif column == self.labels[0]:   # might be row label
                cols.append(label)

        # SKIP ALL remaining values...
        if SKIP in cols:
            idx = cols.index(SKIP)
            cols = cols[:idx]

        return cols

    def best_model(self, column, preselected = None):
        """
        Assumes 0th column contains the 'N' value to use; try to find best curve_fit
        whose pearsonr is highest.

        Checks models known to this package.

        If more than one model have pearsonR >= threshold, they are all returned
        in reverse sorted order. If the best model is below this threshold, then
        just it is returned.
        """
        threshold = 0.99
        nvals = []
        yvals = []
        for row in range(self.num_rows):
            n = self.row_index[row]
            vals = self.values[n]
            if column in vals:
                nvals.append(n)
                yvals.append(vals[column])

        # Find all models, sorted in order of likelihood
        models = best_models(nvals, yvals, preselected)

        # If first one is smaller than threshold, just return it, otherwise
        # return all that exceed threshold.
        result = models[0]
        if len(result) <= 1:
            return result
        if result[1] < threshold:
            return result
        return list(filter(lambda x: x[1] >= threshold, models))

    def pearsonr(self, actual, model):
        """Return Pearson correlation coefficient between Actual and Model."""
        y_act = []
        y_fit = []
        for row in range(self.num_rows):
            row_label = self.row_index[row]
            vals = self.values[row_label]
            y_act.append(vals[actual])
            y_fit.append(vals[model])

        return pearson_correlation(y_act, y_fit)

def process(table, chapter, number, description, create_image=True, xaxis='Problem instance size',
            yaxis='Time (in seconds)'):
    """Process Table by printing label/Description and visualizing table."""
    label = '{} {}-{}'.format(number.args[0].element(), chapter, number.args[0])
    print('{}. {}'.format(label, description))
    if create_image:
        visualize(table, description, label, xaxis=xaxis, yaxis=yaxis)
    print()

def caption(chapter, number):
    """
    Return string for 'element chapter-number. description'.
    number is either a TableNum or a FigureNum.
    """
    return '{} {}-{}'.format(number.args[0].element(), chapter, number.args[0])

def comma(n):
    """Return string for integer n with commas at thousands, i.e., '2,345,217'."""
    return '{:,}'.format(n)

class FigureNum:
    """Represents a figure number in a chapter."""
    def __init__(self, num):
        self.number = num

    def element(self):
        return 'Figure'

    @contextmanager
    def __enter__(self):
        return self.number

    def __exit__(self, arg1, arg2, arg3):
        self.number = -1

    def __str__(self):
        return '{}'.format(self.number)

class TableNum:
    """Represents a table number in a chapter."""
    def __init__(self, num):
        self.number = num

    def element(self):
        return 'Table'

    @contextmanager
    def __enter__(self):
        return '{}'.format(self.number)

    def __exit__(self, arg1, arg2, arg):
        self.number = -1

    def __str__(self):
        return '{}'.format(self.number)

class ExerciseNum:
    """Represents an exercise number in a chapter."""
    def __init__(self, num):
        self.number = num

    def element(self):
        return 'Exercise'

    @contextmanager
    def __enter__(self):
        return '{}'.format(self.number)

    def __exit__(self, arg1, arg2, arg):
        self.number = -1

    def __str__(self):
        return '{}'.format(self.number)
