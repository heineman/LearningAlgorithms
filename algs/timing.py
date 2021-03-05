"""
Demonstrates timing capabilities of timeit in Python.

    :Example:

    >>> timing_trials()
    5 repetitions of sleeping for 100 milliseconds ten times.
    5    10    1.091816
               Should be about 1.0:

    50 repetitions of sleeping for 100 milliseconds ten times.
    50    10    1.081817
                Should be closer to 1.0 (but might not):

    500 repetitions of sleeping for 100 milliseconds ten times.
    500    10    1.078466
                 Should be even closer to 1.0:

    5 repetitions of sleeping for 100 milliseconds one hundred times.
    5    100    10.884912
                Should be about 10.0:

A number of R repetitions of a trial are run, creating a list of R timing
values. We then retrieve the minimum value from this list, since that is
(at least) a definitive measurement of time. To compute the average, now
divide by X. This is why the timing statements all look like this:

  m = min(timeit.repeat(stmt=... setup=..., repeat = R, number=X))/X

R is the number of independent trials. X becomes higher when the statement
to be executed is too fast, and the only way to measure it using the
granularity of the OS timer is to have it execute the statement X times
in sequence.

If the stmt to be executed depends on some parameter N, then you have to
additionally divide the final result by N to normalize and retrieve
average operation cost.

  m = min(timeit.repeat(stmt='''f({N})''' setup=..., repeat = R, number=X))/(X*N)

"""

import timeit

def run_trial(rep, num):
    """Sleep for 100 milliseconds, 'num' times; repeat for 'rep' attempts."""
    sleep = 'sleep(0.1)'
    return min(timeit.repeat(stmt=sleep, setup = 'from time import sleep', repeat=rep, number=num))

def ten_million_addition_trial():
    """Time the addition of first ten million numbers."""
    loop = '''
x = 0
for i in range(10000000):
    x += i
'''
    return min(timeit.repeat(stmt=loop, repeat=10, number=1))

def stages_of_timing():
    """
    Show when stages are invoked.

    Demonstrates that 'setup' is invoked once before each repetition.

    Shows that the statement is repeated 'number' of times. Also observe
    that the state is shared from one number to another (but not across
    repetitions.

        :Expected:
        >>> stages_of_timing():
        in setup
        real statement 1
        real statement 2
        real statement 3
        in setup
        real statement 1
        real statement 2
        real statement 3

    """
    return min(timeit.repeat(stmt='''
print('real statement', val)
val += 1''', setup = '''
print('in setup')
val = 1''', repeat=2, number=3))

def timing_trials():
    """Complete sequence of timing trials, showing how to use timeit."""
    reps = 5
    num = 10
    print('5 repetitions of sleeping for 100 milliseconds ten times.')
    print('{}\t{}\t{:.6f}'.format(reps, num, run_trial(reps, num)))
    print('\t\tShould be about 1.0:')
    print()

    reps = 50
    print('50 repetitions of sleeping for 100 milliseconds ten times.')
    print('{}\t{}\t{:.6f}'.format(reps, num, run_trial(reps, num)))
    print('\t\tShould be closer to 1.0 (but might not):')
    print()

    reps = 500
    print('500 repetitions of sleeping for 100 milliseconds ten times.')
    print('{}\t{}\t{:.6f}'.format(reps, num, run_trial(reps, num)))
    print('\t\tShould be even closer to 1.0:')
    print()

    reps = 5
    num = 100
    print('5 repetitions of sleeping for 100 milliseconds one hundred times.')
    print('{}\t{}\t{:.6f}'.format(reps, num, run_trial(reps, num)))
    print('\t\tShould be about 10.0:')

#######################################################################
if __name__ == '__main__':
    stages_of_timing()
    print()

    print('Time to add first ten million numbers (seconds)')
    print('{:.6f}'.format(ten_million_addition_trial()))
    print()

    timing_trials()
    print()
