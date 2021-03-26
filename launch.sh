#!/bin/bash

export PYTHONPATH=.

# update, as needed, to point to your own Python installation or
# just eliminate if you already have python executables in your path
PYTHON3=python3

echo "Running test cases -- should take about 15 minutes."
$PYTHON3 -m unittest discover > tests.txt

echo "Generating figures and tables for the book. This will take about six hours"
$PYTHON3 book.py > book.txt

echo "Generating Timing results for each chapter. Should take about two hours"
$PYTHON3 algs/timing.py > algs.txt
$PYTHON3 ch02/timing.py > ch02.txt
$PYTHON3 ch02/timing.py > ch03.txt
$PYTHON3 ch02/timing.py > ch04.txt
$PYTHON3 ch02/timing.py > ch05.txt
$PYTHON3 ch02/timing.py > ch06.txt
