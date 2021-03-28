"""
Trims away those test cases and book code that relies on tkinter
"""

tkinter_error = []
try:
    import tkinter
except ImportError:
    if tkinter_error == []:
        print('trying to continue without tkinter')
    tkinter_error.append(1)
