# README file for Learning Algorithms code

This repository contains the Python code for:

	Learning ALgorithms: A Programmer's Guide to Writing Better Code
	George T. Heineman
	ISBN: 978-1-49-209106-6
	
Each chapter has its own folder containing the code for that chapter.
All Python code conforms to Python 3.4 and has been tested to work
with Python 3.3.

## Chapter structure

In addition to the code related to a chapter, each folder contains three 
specific Python scripts:

* `book.py` - Generates the tables and data used for figures in the book
* `challenge.py` - Contains the solutions for the challenge exercises at
                 the end of each chapter
* `timing.py` - Scripts that may take a significant amount of time to 
              complete are pulled out separately
* `test.py` - test cases to validate the algorithms and supporting methods.

A separate `util` folder contains Python scripts that are shared across
the different chapters.

## Documentation

The code documentation style follows the NumPy/SciPy Docstrings style. The
supporting scripts (i.e., `book.py`, `timing.py`, `test.py`) typically have no
documentation.

Within each `book.py` file, the output from sample runs is included within 
the top-level documentation for the script.

## Resources

A dictionary of 321,129 English words is provided in the `words.english.txt` 
file and is used to provide sample inputs throughout the book.

## Dependencies

The code depends on numpy, scipy and networkx. If these libraries are
not installed, the scripts continue to operate in degraded fashion. 
numpy and scipy are only used to model and perform analysis on data 
and runtime performance. networkx is used to construct graphs, and if 
this library is not installed, a replacement graph structure which 
is not efficient or suitable for production use.

## Testing

You can generate code coverage reports for the test cases after you install
the coverage module with:

pip install coverage

Then in the top directory, execute the following commands to generate code
coverage data and then present it as an HTML directory (found in `htmlcov`).
There is a .coveragerc file that ensures only the book code is targeted.

	coverage run -m unittest discover
	coverage run -a book.py
	coverage html

The test cases execute within 15 minutes or so. The book takes up to six hours
to fully run, since it generates all tables and data for figures in the book.
If you want to complete all timing results, then add those as well:

	coverage run -a ch01/timing.py
	coverage run -a ch02/timing.py
	coverage run -a ch03/timing.py
	coverage run -a ch04/timing.py
	coverage run -a ch05/timing.py
	coverage run -a ch06/timing.py
	coverage run -a ch07/timing.py

