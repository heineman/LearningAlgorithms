"""
Generate all Tables/Figures.

Import all external modules that are ever used in the book, so you can 
see now whether there are any surprises, and not later!

"""
import timeit
import itertools
from enum import Enum

try:
    import numpy as np
except ImportError:
    print('numpy is not installed. Consider installing with pip install --user numpy')
    
try:
    from scipy.optimize import curve_fit
    from scipy.stats.stats import pearsonr
    from scipy.special import factorial
except ImportError:
    print('scipy is not installed. Consider installing with pip install --user scipy')

try:
    import networkx as nx
except ImportError:
    print('networkx is not installed. Consider installing with pip install --user networkx')

from ch01.book import generate_ch01
from ch02.book import generate_ch02
from ch03.book import generate_ch03
from ch04.book import generate_ch04
from ch05.book import generate_ch05
from ch06.book import generate_ch06

#######################################################################

generate_ch01()
generate_ch02()
generate_ch03()
generate_ch04()
generate_ch05()
generate_ch06()
