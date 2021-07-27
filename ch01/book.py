"""Tables and Figures for Chapter 1.

   Learning Algorithms:
   A programmer's guide to writing better code
   Chapter 1: Problem Solving
   (C) 2021, George T. Heineman

"""
import timeit
import itertools
from algs.table import DataTable, TableNum, FigureNum, process, caption
from algs.modeling import Model
from algs.counting import RecordedItem
from ch01.largest import largest, alternate

class Order:
    """Default models used extensively in algorithmic analysis."""
    REVERSED = 1
    SHUFFLED = 2
    ALTERNATING = 3

def run_init_trial(output=True):
    """First Table in chapter 1."""
    n = 100
    tbl = DataTable([12,12,12],['N','Ascending','Descending'], output=output, decimals=3)

    while n <= 1000000:
        # 1 up to but not including N
        m_up = 1000*min(timeit.repeat(stmt='native_largest(up)', setup='''
from ch01.largest import native_largest
up = list(range(1,{}+1))'''.format(n), repeat=10, number=50))/50

        # N down to but not including 0
        m_down = 1000*min(timeit.repeat(stmt='native_largest(down)', setup='''
from ch01.largest import native_largest
down = list(range({}, 0, -1))'''.format(n), repeat=10, number=50))/50

        tbl.row([n, m_up, m_down])
        n *= 10
    return tbl

def flawed(A):
    """Flawed implementation of max()."""
    my_max = 0
    for v in A:
        if my_max < v:
            my_max = v
    return my_max

def visualize_flawed(A):
    """Show values in flawed() visualization."""
    print(' \t ',' | '.join([str(x) for x in A])[:-1], ' |')
    my_max = 0
    print(' \t ', end='')
    for v in A:
        if my_max < v:
            my_max = v
            print('[{}]|'.format(v), end='')
        else:
            print(' {} |'.format(v), end='')
    print()
    print()

def visualize_alternate(A):
    """Show values in alternate() visualization."""
    print('\t ','\t'.join([str(x) for x in A]))

    col = 0
    cols = {}
    done = False
    for v in A:
        if done:
            break
        row = 0
        v_is_largest = True
        for x in A:
            if not row in cols:
                cols[row] = {}
            if not col in cols[row]:
                cols[row][col] = {}
            cols[row][col] = '{} < {}?'.format(v, x)
            if v < x:
                v_is_largest = False
                break
            row += 1

        if v_is_largest:
            done = True
            break
        col += 1
    print()
    for row,v in enumerate(A):
        print('{}\t'.format(v), end='')
        for c in range(col+1):
            if row in cols and c in cols[row]:
                print('{}\t'.format(cols[row][c]), end='')
            else:
                print('\t', end='')

        print()
    print()

def run_largest_alternate(output=True, decimals=3):
    """Generate tables for largest and alternate."""
    n = 8
    tbl = DataTable([8,10,15,10,10],
                   ['N', '#Less', '#LessA', 'largest', 'alternate'],
                   output=output, decimals=decimals)
    tbl.format('#Less', ',d')
    tbl.format('#LessA', ',d')

    while n <= 2048:
        ascending = list(range(n))

        largest_up = 1000*min(timeit.repeat(stmt='largest({})'.format(ascending),
            setup='from ch01.largest import largest', repeat=10, number=50))/50
        alternate_up = 1000*min(timeit.repeat(stmt='alternate({})'.format(ascending),
            setup='from ch01.largest import alternate', repeat=10, number=50))/50

        up_count = [RecordedItem(i) for i in range(n)]
        RecordedItem.clear()
        largest(up_count)
        largest_counts = RecordedItem.report()
        RecordedItem.clear()

        up_count = [RecordedItem(i) for i in range(n)]
        RecordedItem.clear()
        alternate(up_count)
        alternate_counts = RecordedItem.report()
        RecordedItem.clear()

        tbl.row([n, sum(largest_counts), sum(alternate_counts), largest_up, alternate_up])

        n *= 2

    if output:
        print()
        print('largest', tbl.best_model('largest', Model.LINEAR))
        print('Alternate', tbl.best_model('alternate', Model.QUADRATIC))
    return tbl

def just_compare_sort_tournament_two(max_k=25, output=True, decimals=2):
    """Very large data sets to investigate whether crossover occurs (no it does not)."""
    tbl = DataTable([15,10,15],
        ['N','sorting_two','tournament_two'],
        output=output, decimals=decimals)

    trials = [2**k for k in range(10,max_k)]
    num = 5
    for n in trials:
        m_tt = timeit.timeit(stmt='random.shuffle(x)\ntournament_two(x)', setup='''
import random
from ch01.largest_two import tournament_two
x=list(range({}))'''.format(n), number=num)

        m_st = timeit.timeit(stmt='random.shuffle(x)\nsorting_two(x)', setup='''
import random
from ch01.largest_two import sorting_two
x=list(range({}))'''.format(n), number=num)

        tbl.row([n, m_st, m_tt])

    if output:
        print()
        for header in tbl.labels[1:]:
            print(header, tbl.best_model(header))
    return tbl

def run_largest_two_trials(mode, max_k=22, output=True, decimals=2):
    """Mode is either Order.REVERSED or Order.SHUFFLED for 2**k up to (but not including) max_k."""
    tbl = DataTable([10,15,15,10,10,15],
        ['N','double_two','mutable_two','largest_two','sorting_two','tournament_two'],
        output=output, decimals=decimals)

    if mode is Order.REVERSED:
        prepare = 'list(reversed(x))'
    if mode is Order.SHUFFLED:
        prepare = 'random.shuffle(x)'

    trials = [2**k for k in range(10,max_k)]
    num = 100
    for n in trials:
        if mode is Order.ALTERNATING:
            prepare = '''
up_down = zip(range(0,{0},2),range({0}-1,0,-2))
x=[i for i in itertools.chain(*up_down)]
'''.format(n)
        m_dt = timeit.timeit(stmt='double_two(x)', setup='''
import random
from ch01.largest_two import double_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_mt = timeit.timeit(stmt='mutable_two(x)', setup='''
import random
from ch01.largest_two import mutable_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_lt = timeit.timeit(stmt='largest_two(x)', setup='''
import random
from ch01.largest_two import largest_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        # hard-code these values since take too long to compute...
        if n > 1048576:
            m_tt = None
        else:
            m_tt = timeit.timeit(stmt='tournament_two(x)', setup='''
import random
from ch01.largest_two import tournament_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        m_st = timeit.timeit(stmt='sorting_two(x)', setup='''
import random
from ch01.largest_two import sorting_two
x=list(range({}))
{}'''.format(n,prepare), number=num)

        # Skip runs that are going to be too expensive
        if m_tt:
            tbl.row([n, m_dt, m_mt, m_lt, m_st, m_tt])
        else:
            tbl.row([n, m_dt, m_mt, m_lt, m_st ])

    return tbl

def run_best_worst(max_n=525288, output=True, decimals=2):
    """Perform best and worst case analysis for largest."""
    n = 4096
    tbl = DataTable([8,10,10,10,10],['N', 'LargestW', 'MaxW', 'LargestB', 'MaxB'],
                    output=output, decimals=decimals)

    while n <= max_n:    ###  524288:
        ups = list(range(1,n+1))         # 1 up to n
        downs = list(range(n, 0, -1))    # n down to 1

        m_up = 1000*min(timeit.repeat(stmt='largest({})'.format(ups),
            setup='from ch01.largest import largest', repeat=10, number=50))/50
        max_up = 1000*min(timeit.repeat(stmt='max({})'.format(ups),
            setup='from ch01.largest import largest', repeat=10, number=50))/50

        m_down = 1000*min(timeit.repeat(stmt='largest({})'.format(downs),
            setup='from ch01.largest import largest', repeat=10, number=50))/50
        max_down = 1000*min(timeit.repeat(stmt='max({})'.format(downs),
            setup='from ch01.largest import largest', repeat=10, number=50))/50

        tbl.row([n, m_up, max_up, m_down, max_down])
        n *= 2

    return tbl

def performance_different_approaches(output=True):
    """Produce results on # less-than for different algorithms and data sets."""
    headers = ['Algorithm', 'Ascending', 'Descending', 'Alternating']
    n = 524288

    tbl = DataTable([15,10,10,10], headers, output=output)
    for hdr in headers:
        tbl.format(hdr, ',d')
    tbl.format('Algorithm', 's')

    # Ascending / Descending / Weave
    from ch01.largest_two import largest_two, sorting_two, double_two, mutable_two, tournament_two
    funcs = [largest_two, sorting_two, double_two, mutable_two, tournament_two]
    algs  = ['largest_two', 'sorting_two', 'double_two', 'mutable_two', 'tournament_two']

    for label,func in zip(algs,funcs):
        RecordedItem.clear()
        func([RecordedItem(i) for i in range(n)])
        up_count = sum(RecordedItem.report())

        RecordedItem.clear()
        func([RecordedItem(i) for i in range(n,0,-1)])
        down_count = sum(RecordedItem.report())

        RecordedItem.clear()
        up_down = zip(range(0,n,2),range(n-1,0,-2))
        func([RecordedItem(i) for i in itertools.chain(*up_down)])
        weave_count = sum(RecordedItem.report())

        tbl.row([label, up_count, down_count, weave_count])
    return tbl

def count_operations(output=True):
    """Generate statistics on some functions."""
    def f0(_):
        ct = 0
        ct = ct + 1
        ct = ct + 1
        return ct

    def f1(N):
        ct = 0
        for _ in range(N):
            ct = ct + 1
        return ct

    def f2(N):
        ct = 0
        for _ in range(N):
            ct = ct + 1
            ct = ct + 1
            ct = ct + 1
            ct = ct + 1
            ct = ct + 1
            ct = ct + 1
            ct = ct + 1
        return ct

    def f3(N):
        ct = 0
        for _ in range(N):
            for _ in range(N):
                ct = ct + 1
        return ct

    n = 512
    tbl = DataTable([8,4,10,10,10], ['N', 'f0', 'f1', 'f2', 'f3'], output=output)
    for func in ['f0', 'f1', 'f2', 'f3']:
        tbl.format(func, ',d')

    while n <= 2048:
        tbl.row([n, f0(n), f1(n), f2(n), f3(n)])
        n = n*2
    print()
    return tbl

def visualize_tournament_two(A):
    """Visualize execution of tournament."""
    print('        |' + '|'.join([str(x) for x in A]) + '|')

    N = len(A)
    winner = [None] * (N-1)
    loser = [None] * (N-1)
    prior = [-1] * (N-1)

    # populate N/2 initial winners/losers
    idx = 0
    for i in range(0, N, 2):
        if A[i] < A[i+1]:
            winner[idx] = A[i+1]
            loser[idx] = A[i]
        else:
            winner[idx] = A[i]
            loser[idx] = A[i+1]
        idx += 1

    def output(m,i, step):
        print('winner\t|', end='')
        for v in winner:
            if v is None:
                print(' |', end='')
            else:
                print('{}|'.format(v), end='')

        print('\t{}\nloser\t|'.format(step), end='')
        for v in loser:
            if v is None:
                print(' |', end='')
            else:
                print('{}|'.format(v), end='')
        print('\n\t ', end='')
        print('  ' * m, end='')
        print('m', end='')
        print('  ' * (i-m-1), end='')
        print(' i')

    # pair up subsequent winners and record priors
    m = 0
    output(m,idx, 'Initialize step')
    print()
    while idx < N-1:
        if winner[m] < winner[m+1]:
            winner[idx] = winner[m+1]
            loser[idx]  = winner[m]
            prior[idx]  = m+1
        else:
            winner[idx] = winner[m]
            loser[idx]  = winner[m+1]
            prior[idx]  = m
        m += 2
        idx += 1
        output(m,idx, 'Advance step {}'.format(m//2))
    # Find where second is hiding!
    largest = winner[m]
    second = loser[m]
    m = prior[m]
    while m >= 0:
        if second < loser[m]:
            second = loser[m]
        m = prior[m]

    return (largest, second)

def generate_ch01():
    """Generate Tables and Figures for chapter 01."""
    chapter = 1

    with FigureNum(1) as figure_number:
        pi1 = [13, 2, 18, 7, 50]
        pi2 = [-19, -236, -17, -204, -97, -20, -928, -454, -92, -19]
        pi3 = list(range(1, 1000001))
        print(pi1, '->', max(pi1))
        print(pi2, '->', max(pi2))
        print(pi3[:5]+['...'] + pi3[-3:], '->', max(pi3))
        print(caption(chapter, figure_number),
              'Three different problem instances processed by an algorithm')
        print()

    with TableNum(1) as table_number:
        process(run_init_trial(),
                chapter, table_number,
                'Executing max() on two kinds of problem instances of size N (time in ms)',
                yaxis = 'Time (in ms)')

    with FigureNum(2) as figure_number:
        visualize_flawed([1, 5, 2, 9, 3, 4])
        print(caption(chapter, figure_number),
              'Visualizing the execution of flawed()')

    with FigureNum(3) as figure_number:
        visualize_alternate([1, 5, 2, 9, 3, 4])
        print(caption(chapter, figure_number),
              'Visualizing the execution of alternate()')

    with FigureNum(4) as figure_number:
        visualize_alternate([9, 5, 2, 1, 3, 4])
        visualize_alternate([1, 2, 3, 4, 5, 9])
        print(caption(chapter, figure_number),
              'Visualizing the execution of alternate() on best and worst cases')

    # TODO: Option for secondary axis specification
    with TableNum(2) as table_number:
        process(run_largest_alternate(),
                chapter, table_number,
                'Comparing largest() with alternate() on worst case problem instances')

    # Take results and plot #LessA on left-axis as line, and TimesA on right axis as column
    with FigureNum(5) as figure_number:
        print(caption(chapter, figure_number),
              'Relationship between #Less-Than and runtime performance')

    with TableNum(3) as table_number:
        process(run_best_worst(),
                chapter, table_number,
                'Performance of largest() and max() on best and worst cases')

    with TableNum(4) as table_number:
        process(performance_different_approaches(),
                chapter, table_number,
                'Performance of different approached on 524,288 values in different orders',
                create_image = False)

    with FigureNum(6) as figure_number:
        print('by hand')
        print(caption(chapter, figure_number),
              'A tournament with eight initial values')

    with FigureNum(7) as figure_number:
        print('by hand')
        print(caption(chapter, figure_number),
              'A tournament with 32 values')

    with FigureNum(8) as figure_number:
        visualize_tournament_two([3,1,4,1,5,9,2,6])
        print(caption(chapter, figure_number),
              'Step-by-step execution of tournament algorithm')

    with TableNum(5) as table_number:
        process(run_largest_two_trials(Order.SHUFFLED),
                chapter, table_number,
                'Comparing runtime performance (in ms) of all four algorithms',
                yaxis = 'Time (in ms)')

    # Taken from table
    with FigureNum(9) as figure_number:
        print(caption(chapter, figure_number),
              'Runtime performance comparison')

    with TableNum(6) as table_number:
        process(count_operations(),
                chapter, table_number,
                'Counting operations in four different functions',
                yaxis = 'Number of times ct is incremented')

#######################################################################
if __name__ == '__main__':
    generate_ch01()
