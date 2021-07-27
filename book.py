"""Generate all Tables/Figures for entire book

   Learning Algorithms:
   A programmer's guide to writing better code
   (C) 2021, George T. Heineman

Import all external modules that are ever used in the book, so you can 
see now whether there are any surprises, and not later!

"""
import timeit
import itertools

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
    print('will attempt to use stub implementation to complete tables and figures.')

from ch01.book import generate_ch01
from ch02.book import generate_ch02
from ch03.book import generate_ch03
from ch04.book import generate_ch04
from ch05.book import generate_ch05
from ch06.book import generate_ch06
from ch07.book import generate_ch07

#######################################################################
from datetime import datetime

# Generate all chapters, with timestamps
print("ch01:", datetime.now())
generate_ch01()
print("ch02:", datetime.now())
generate_ch02()
print("ch03:", datetime.now())
generate_ch03()
print("ch04:", datetime.now())
generate_ch04()
print("ch05:", datetime.now())
generate_ch05()
print("ch06:", datetime.now())
generate_ch06()
print("ch07:", datetime.now())
generate_ch07()
