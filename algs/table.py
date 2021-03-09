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
from enum import Enum
from contextlib import contextmanager

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from scipy.special import factorial
from algs.output import visualize

TABLE = "Table"
FIGURE = "Figure"

# When a table wants to skip a value, select this one.
SKIP = '*'

class Model(Enum):
    """Default models used extensively in algorithmic analysis."""
    LOG = 1
    LINEAR = 2
    N_LOG_N = 3
    LOG_LINEAR = 4
    QUADRATIC = 5

def log_model(n, a):
    """Formula for A*Log_2(N) with single coefficient."""
    return a*np.log(n)/np.log(2)

def linear_model(n, a, b):
    """Formula for A*N + B linear model with two coefficients."""
    return a*n + b

def n_log_n_model(n, a):
    """Formula for A*N*Log_2(N) with single coefficient."""
    return a*n*np.log(n)/np.log(2)

def log_linear_model(n, a, b):
    """Formula for A*N*Log_2(N) + B*N with two coefficients."""
    return a*n*np.log(n)/np.log(2) + b*n

def quadratic_model(n, a, b):
    """Formula for A*N*N + B*N quadratic model with three coefficients."""
    return a*n*n + b*n

def factorial_model(n, a):
    """Models N! or N factorial."""
    return a * factorial(n)

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
            self.fmt += f'{{0[{idx}]:>{width}}}\t'
            self.entry_fmt += f'{{0[{idx}]:>{width}{symbol}}}\t'
            symbol = '.' + str(decimals) + 'f'
        if output:
            print(self.fmt.format(labels))

    def set_output(self, status):
        """Turn on/off output status for row() method calls."""
        self.output = status

    def format(self, field, fmt):
        """Change the format of this entry from 'f' into the given format."""
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
        """"
        Helper method to load up an entire row of values.
        If any values are SKIP then must eliminate without throwing off the formatting of output
        """
        if self.output:
            formats = self.entry_fmt.split('\t')

            if SKIP in row:
                new_formats = []
                for fmt,val,width in zip(formats, row, self.widths):
                    if val == SKIP:
                        new_formats.append(fmt.split(':')[0] + ':>' + str(width) + 's}')
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
        """Return array of values in given column. Elminate 'SKIP' and remaining."""
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

        return pearsonr(y_act, y_fit)

def process(table, chapter, number, description, create_image=True, xaxis='Problem instance size',
            yaxis='Time (in seconds)'):
    """Process Table by printing label/Description and visualizing table."""
    label = '{} {}-{}'.format(number.args[0].element(), chapter, number.args[0])
    print('{}. {}'.format(label, description))
    if create_image:
        visualize(table, description, label, xaxis=xaxis, yaxis=yaxis)
    print()

def captionx(chapter, number):
    """
    Return string for 'element chapter-number. description'.
    number is either a TableNum or a FigureNum
    """
    return '{} {}-{}'.format(number.args[0].element(), chapter, number.args[0])

def caption(chapter, labels, element, title):
    """
    Given a chapter and a dict{} containing [element -> index] and element,
    return string and, more importantly, advance the counter for the type.
    """
    if element in labels:
        labels[element] += 1
    else:
        labels[element] = 1

    return '{} {}-{}. {}'.format(element, chapter, labels[element], title)

def comma(n):
    """Return string for integer n with commas at thousands, i.e., '2,345,217'."""
    return f'{n:,}'

def best_models(nval, yval, preselected = None):
    """
    Given two 1-dimensional arrays, returns list of computed models, in
    decreasing order of likelihood.

    Each tuple contains (Type, Pearson, RMS-error, coefficients).

    Identifying a model for data is a bit of an art. You have to interpret the
    results carefully. For example, what if your curve_fit suggests a quadratic
    model, but the first coefficient (of the n^2 term) is 10^-12? This suggests
    that a linear model would be more accurate.

    Safest approach is to pass in a preselected model to restrict to just one
    and select this model in advance.
    """
    npx = np.array(nval)
    npy = np.array(yval)

    if preselected is Model.LOG or preselected is None:
        [log_coeffs, _]        = curve_fit(log_model, npx, npy)
    else:
        log_coeffs = [-1]

    if preselected is Model.LINEAR or preselected is None:
        [linear_coeffs, _]     = curve_fit(linear_model, npx, npy)
    else:
        linear_coeffs = [-1]

    if preselected is Model.N_LOG_N or preselected is None:
        [n_log_n_coeffs, _]    = curve_fit(n_log_n_model, npx, npy)
    else:
        n_log_n_coeffs = [-1]

    if preselected is Model.LOG_LINEAR or preselected is None:
        [log_linear_coeffs, _] = curve_fit(log_linear_model, npx, npy)
    else:
        log_linear_coeffs = [-1]

    if preselected is Model.QUADRATIC or preselected is None:
        [quadratic_coeffs, _]  = curve_fit(quadratic_model, npx, npy)
    else:
        quadratic_coeffs = [-1]

    m_log = []
    m_linear = []
    m_n_log_n = []
    m_log_linear = []
    m_quadratic = []

    # Models have all their values, but y values must be curtailed because towards
    # the end of some tables, it is too computationally expensive to reproduce.
    num = min(len(yval), len(nval))
    for i in range(num):
        n = nval[i]
        if log_coeffs[0] > 0:
            m_log.append(log_model(n, log_coeffs[0]))
        if linear_coeffs[0] > 0:
            m_linear.append(linear_model(n, linear_coeffs[0], linear_coeffs[1]))
        if n_log_n_coeffs[0] > 0:
            m_n_log_n.append(n_log_n_model(n, n_log_n_coeffs[0]))
        if log_linear_coeffs[0] > 0:
            m_log_linear.append(log_linear_model(n, log_linear_coeffs[0], log_linear_coeffs[1]))
        if quadratic_coeffs[0] > 0:
            m_quadratic.append(quadratic_model(n, quadratic_coeffs[0], quadratic_coeffs[1]))

    # If the lead coefficient is NEGATIVE then the model can be discounted

    # compute square Root Mean Square error for all models.
    # RMS error is the square Root of the Mean of the Sum
    models = []
    if m_log:
        rms_log = np.sqrt(np.sum((pow((np.array(m_log)-npy),2)))/num)
        models.append((Model.LOG,
                       pearsonr(yval, m_log)[0], rms_log,
                       log_coeffs[0]))
    if m_linear:
        rms_linear = np.sqrt(np.sum((pow((np.array(m_linear)-npy),2)))/num)
        models.append((Model.LINEAR,
                       pearsonr(yval, m_linear)[0], rms_linear,
                       linear_coeffs[0], linear_coeffs[1]))
    if m_n_log_n:
        rms_n_log_n = np.sqrt(np.sum((pow((np.array(m_n_log_n)-npy),2)))/num)
        models.append((Model.N_LOG_N,
                       pearsonr(yval, m_n_log_n)[0], rms_n_log_n, n_log_n_coeffs[0]))
    if m_log_linear:
        rms_log_linear = np.sqrt(np.sum((pow((np.array(m_log_linear)-npy),2)))/num)
        models.append((Model.LOG_LINEAR,
                       pearsonr(yval, m_log_linear)[0], rms_log_linear,
                       log_linear_coeffs[0], log_linear_coeffs[1]))
    if m_quadratic:
        rms_quadratic = np.sqrt(np.sum((pow((np.array(m_quadratic)-npy),2)))/num)
        models.append((Model.QUADRATIC,
                       pearsonr(yval, m_quadratic)[0], rms_quadratic,
                       quadratic_coeffs[0], quadratic_coeffs[1]))

    # sort in reverse order by Pearson, but receiving end should also check RMS
    models.sort(key=lambda x:x[1], reverse=True)
    return models

class Chapter:
    """Represents a chapter."""
    def __init__(self, num):
        self.number = num

    @contextmanager
    def __enter__(self):
        return self.number

    def __exit__(self, arg1, arg2, arg3):
        self.number = -1

    def __str__(self):
        return '{}'.format(self.number)

class FigureNum:
    """Represents a figure number in a chapter."""
    def __init__(self, num):
        self.number = num

    def element(self):
        return "Figure"

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
        return "Table"

    @contextmanager
    def __enter__(self):
        return '{}'.format(self.number)

    def __exit__(self, arg1, arg2, arg):
        self.number = -1

    def __str__(self):
        return '{}'.format(self.number)
