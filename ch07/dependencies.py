"""
Trims away those test cases and book code that relies on tkinter or matplotlib
"""

tkinter_error = []
try:
    import tkinter
except ImportError:
    if tkinter_error == []:
        print('trying to continue without tkinter')
    tkinter_error.append(1)

plt_error = []
try:
    import matplotlib.pyplot as plt
except ImportError:
    if plt_error == []:
        print('trying to continue without matplotlib.pyplot')
    plt_error.append(1)
