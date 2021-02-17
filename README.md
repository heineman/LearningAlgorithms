# README file for Learning Algorithms code

This repository contains the Python code for:

	Learning ALgorithms: A Programmer's Guide to Writing Better Code
	George T. Heineman
	ISBN: 978-1-49-209106-6
	
Each chapter has its own folder containing the code for that chapter.
All Python code conforms to Python 3.

## Chapter structure

In addition to the code related to a chapter, each folder contains three 
specific Python scripts:

* `book.py` - Generates the tables and data used for figures in the book
* `challenge.py` - Contains the solutions for the challenge questions at
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

A dictionary of 321,165 English words is provided in the `words.english.txt` 
file and is used to provide sample inputs throughout the book.

## Testing

You can generate code coverage reports for the test cases after you install
the coverage module with:

pip install coverage

Then in the top directory, execute the following commands to generate code
coverage data and then present it as an HTML directory (found in `htmlcov`) 

	coverage run --source=algs,ch01,ch02,ch03,ch04,ch05,ch06 -m unittest discover
	coverage html
