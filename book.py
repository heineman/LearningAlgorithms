"""
Generate all Tables/Figures.

Import all external modules that are ever used in the book, so you can 
see now whether there are any surprises, and not later!

"""
import timeit
import itertools
from enum import Enum

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from scipy.special import factorial
import networkx as nx

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
