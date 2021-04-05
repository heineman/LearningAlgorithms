set PYTHONPATH=.

REM   Update, as needed, to point to your own Python installation or
REM   just eliminate if you already have Python executables in your path
REM   ------------------------------------------------------------------
set COVERAGE3=c:\python37\Scripts\coverage-3.7.exe

echo "Running test cases -- should take about 15 minutes."
%COVERAGE3% run -m unittest discover > tests.txt

echo "Generating figures and tables for the book. This will take about six hours"
%COVERAGE3% run -a book.py > book.txt

echo "Generating Timing results for each chapter. Should take about two hours"
%COVERAGE3% run -a algs\timing.py > algs.txt
%COVERAGE3% run -a ch02\timing.py > ch02.txt
%COVERAGE3% run -a ch03\timing.py > ch03.txt
%COVERAGE3% run -a ch04\timing.py > ch04.txt
%COVERAGE3% run -a ch05\timing.py > ch05.txt
%COVERAGE3% run -a ch06\timing.py > ch06.txt
%COVERAGE3% run -a ch07\timing.py > ch07.txt

echo "Generating coverage report in htmlcov\index.html"
%COVERAGE3% html
