"""
Contains all numpy/scipy-dependent code, in case user is unable
to install these packages.

If numpy_error contains [1] there was a problem in loading numpy. This can easily
be detected by the code that imports this file as follows:

    if numpy_error:
        pass
    else:
        here is code that needs numpy or scipy

"""
import math

numpy_error = []
try:
    import numpy as np
    from scipy.optimize import curve_fit
    from scipy.stats.stats import pearsonr
    from scipy.special import factorial

    def log_model(n, a):
        """Formula for A*Log_2(N) with single coefficient."""
        return a*np.log2(n)

    def linear_model(n, a, b):
        """Formula for A*N + B linear model with two coefficients."""
        return a*n + b

    def n_log_n_model(n, a):
        """Formula for A*N*Log_2(N) with single coefficient."""
        return a*n*np.log2(n)

    def log_linear_model(n, a, b):
        """Formula for A*N*Log_2(N) + B*N with two coefficients."""
        return a*n*np.log2(n) + b*n

    def quadratic_model(n, a, b):
        """Formula for A*N*N + B*N quadratic model with three coefficients."""
        return a*n*n + b*n

    def factorial_model(n, a):
        """Models N! or N factorial."""
        return a * factorial(n)

except ImportError:
    if numpy_error == []:
        print('trying to continue without numpy or scipy')
    numpy_error.append(1)

    def log_model(n, a):
        """Formula for A*Log_2(N) with single coefficient."""
        return a*math.log2(n)

    def linear_model(n, a, b):
        """Formula for A*N + B linear model with two coefficients."""
        return a*n + b

    def n_log_n_model(n, a):
        """Formula for A*N*Log_2(N) with single coefficient."""
        return a*n*math.log2(n)

    def log_linear_model(n, a, b):
        """Formula for A*N*Log_2(N) + B*N with two coefficients."""
        return a*n*math.log2(n) + b*n

    def quadratic_model(n, a, b):
        """Formula for A*N*N + B*N quadratic model with three coefficients."""
        return a*n*n + b*n

    def factorial_model(n, a):
        """Models N! or N factorial."""
        return a * math.factorial(n)

class Model:
    """Default models used extensively in algorithmic analysis."""
    ERROR = 0
    LOG = 1
    LINEAR = 2
    N_LOG_N = 3
    LOG_LINEAR = 4
    QUADRATIC = 5

    @classmethod
    def to_string(cls, tpe):
        """Return string representation of model."""
        if Model.ERROR <= tpe <= Model.QUADRATIC:
            return ['ERROR', 'LOG', 'LINEAR', 'N LOG N', 'LOG LINEAR', 'QUADRATIC'][tpe]
        raise ValueError('unknown Model type:{}'.format(tpe))

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
    if numpy_error:
        return [[(Model.ERROR,0,0,0,0)]]

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

def pearson_correlation(y_act, y_fit):
    """Return pearson correlation, if numpy is available, otherwise just 0.0."""
    if numpy_error:
        return 0.0
    return pearsonr(y_act, y_fit)
