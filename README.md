# README file for Learning Algorithms code

This repository contains the Python code for:

	Learning ALgorithms: A Programmer's Guide to Writing Better Code
	George T. Heineman
	ISBN: 978-1-49-209106-6
	
Each chapter has its own folder containing the code for that chapter.
All Python code conforms to Python 3.4 and has been tested to work
with Python 3.3. While the core algorithms presented in the book
will continue to work with earlier versions of Python, some code used
to generate the tables and images in the book will not compile properly
because of changes to Python libraries.

## Chapter structure

In addition to the code related to a chapter, each folder contains three 
specific Python scripts:

* `book.py` - Generates the tables and data used for figures in the book
* `challenge.py` - Contains the solutions for the challenge exercises at
                 the end of each chapter
* `timing.py` - Scripts that may take a significant amount of time to 
              complete are pulled out separately
* `test.py` - test cases to validate the algorithms and supporting methods.

A separate `algs` folder contains Python scripts that are shared across
the different chapters.

## Documentation

The code documentation style follows standard Python documentation style. The
supporting scripts (i.e., `book.py`, `timing.py`, `test.py`) typically have no
documentation.

Sample output for all executions is provided in doc folder.

## Resources

A dictionary of 321,129 English words is provided in the `words.english.txt` 
file and is used to provide sample inputs throughout the book.

A TMG graph file containing a representation of highways in Massachusetts is 
graciously provided by James Teresco from https://travelmapping.net/graphs

## Installation

First make sure Python3 is installed on your system. The following steps
show how to install Python on a windows operating system even if you do
not have administrator privileges:

	1. Download MSI file from python web site
	
	https://www.python.org/ftp/python/3.3.0/python-3.3.0.amd64.msi
	
	2. Invoke MSI installer from command line
	
	https://www.python.org/download/releases/2.4/msi/
	
	msiexec /a python-3.3.0.amd64.msi TARGETDIR=C:\users\heineman\Desktop\Python33
	
	3. Now switch to the directory which contains the LearningAlgorithms code base.
	
	4. modify launch.bat to update proper location for 'python3'
	
	c:\users\heineman\Desktop\Python33\python.exe

## Dependencies

The code depends on [numpy](https://numpy.org/), [scipy](https://www.scipy.org/)
and [networkx](https://networkx.org/). If these libraries are not installed, 
the scripts continue to operate in degraded fashion. 

numpy and scipy are only used to model and perform analysis on data 
and runtime performance. networkx is used to construct graphs, and if 
this library is not installed, a replacement graph structure is used which 
is not efficient or suitable for production use.

## Testing

You can generate code coverage reports for the test cases after you install
the coverage module with:

    pip install coverage

Then in the top directory, execute the following commands to generate code
coverage data and then present it as an HTML directory (found in `htmlcov`).
There is a .coveragerc file that ensures only the book code is targeted.
If you have not installed the coverage module, then replace each 
"coverage run" below with just "python3" and remove the "-a" command 
line option, which is there just to ask coverage to append coverage
data across multiple runs.

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

Each chapter has challenge exercises that have been completely solved, these
can be executed from each chNN/challenge.py file.
