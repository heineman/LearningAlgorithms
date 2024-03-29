"""Tables and Figures for Chapter 4

   Learning Algorithms:
   A programmer's guide to writing better code
   Chapter 4: Heaping It On
   (C) 2021, George T. Heineman

"""
import timeit

from algs.table import DataTable, FigureNum, TableNum, process, caption

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_trials(clazz, N, factor):
    """Run a single trial."""
    stmt = '''
from {0} import PQ 
one_run(PQ({1}), {1}, {2})'''.format(clazz,N,factor)
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def average_performance(max_n=65536, output=True, decimals=1):
    """Generate table of average performance for different PQ implementations."""
    T = 3
    base = 256
    cutoff = 16384
    high = max_n

    heap = {}
    order_ar = {}
    order_ll = {}
    N = base
    while N <= high:
        order_ll[N] = 1000000*run_trials('ch04.ordered_list', N, T)/(T*N)
        heap[N]     = 1000000*run_trials('ch04.heap', N, T)/(T*N)
        N *= 2

    N = base
    array = {}
    linked = {}
    builtin = {}
    while N <= cutoff:
        order_ar[N]  = 1000000*run_trials('ch04.ordered', N, T)/(T*N)
        linked[N]    = 1000000*run_trials('ch04.linked', N, T)/(T*N)
        array[N]     = 1000000*run_trials('ch04.array', N, T)/(T*N)
        builtin[N]   = 1000000*run_trials('ch04.builtin', N, T)/(T*N)

        N *= 2

    N = base
    tbl = DataTable([8,8,8,8,8,8,8],
                    ['N','Heap','OrderL','Linked','OrderA','Built-in','Array'],
                    output=output, decimals=decimals)
    while N <= high:
        if N <= cutoff:
            tbl.row([N, heap[N], order_ll[N], linked[N], order_ar[N], builtin[N], array[N]])
        else:
            #tbl.set_output(False)
            tbl.row([N, heap[N], order_ll[N]])
        N *= 2

    if output:
        print()
        print('Heap', tbl.best_model('Heap'))
        print('OrderL', tbl.best_model('OrderL'))
        print('Linked', tbl.best_model('Linked'))
        print('OrderA', tbl.best_model('OrderA'))
        print('Built-in', tbl.best_model('Built-in'))
        print('Array', tbl.best_model('Array'))
    return tbl

def output_heap(h):
    """Output a heap, roughly in ASCII with rows."""
    idx = 1
    offset = 16
    level = 0
    while idx < h.N:
        print('level {}\t'.format(level) + '|'.join([' {:>3} '.format(e.priority) for e in h.storage[idx:min(h.N+1,2*idx)]]))
        idx *= 2
        level += 1
        offset //= 2

def initial_heap():
    """Construct initial heap for figures."""
    from ch04.heap import PQ

    h = PQ(31)
    for i in [15, 13, 14, 9, 11, 12, 14, 8, 2, 1, 10, 8, 6, 9, 7, 4, 5]:
        h.enqueue(i, i)

    return h

def heap_enqueue_animation():
    """Show changes to storage with each swim()."""
    from ch04.entry import Entry

    heap = initial_heap()
    heap.N += 1
    heap.storage[heap.N] = Entry(12, 12)
    fig_num = 8
    print('Fig. 4-{:<2d} : '.format(fig_num),' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap.storage[1:heap.N+1]]))
    print()
    child = heap.N
    while child > 1 and heap.less(child//2, child):
        heap.swap(child, child//2)
        child = child // 2
        fig_num += 1
        print('Fig. 4-{:<2d} : '.format(fig_num),' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap.storage[1:heap.N+1]]))

def heap_dequeue_animation():
    """Show changes to storage with each sink()."""
    heap = initial_heap()
    heap.enqueue(12, 12)
    heap.enqueue(16, 16)
    print('Fig. 4-11 : ',' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap.storage[1:heap.N+1]]))
    heap.storage[1] = heap.storage[heap.N]
    heap.storage[heap.N] = None
    heap.N -= 1
    fig_num = 13
    print('Fig. 4-{} : '.format(fig_num),' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap.storage[1:heap.N+1]]))
    print()
    parent = 1
    while 2*parent <= heap.N:
        child = 2*parent
        if child < heap.N and heap.less(child, child+1):
            child += 1
        if not heap.less(parent, child):
            break
        heap.swap(child, parent)
        fig_num += 1
        print('Fig. 4-{} : '.format(fig_num),' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap.storage[1:heap.N+1]]))

        parent = child

def generate_ch04():
    """Generate tables/figures for chapter 04."""
    chapter = 4

    with FigureNum(1) as figure_number:
        description  = 'Waiting in a queue at a nightclub'
        label = caption(chapter, figure_number)
        print('Redrawn by artist')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(2) as figure_number:
        description  = 'modeling a nightclub queue with three nodes'
        label = caption(chapter, figure_number)
        print('Redrawn by artist')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(3) as figure_number:
        description  = 'Patrons can advance quicker with a purchased pass'
        label = caption(chapter, figure_number)
        print('Redrawn by artist')
        print('{}. {}'.format(label, description))
        print()

    # For full book output, remove "max_n=16384". Added to reduce time to generate all.
    with TableNum(1) as table_number:
        process(average_performance(max_n=16384),
                chapter, table_number,
                'Average operation performance (time in ns) on problem instances of size N',
                yaxis='Time (in nanoseconds)')

    with FigureNum(4) as figure_number:
        description  = 'O(log N) behavior of Heap outperforms O(N) behavior for other approaches'
        label = caption(chapter, figure_number)
        print('Generated by Excel')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(5) as figure_number:
        description  = 'A sample max binary heap'
        label = caption(chapter, figure_number)
        heap = initial_heap()
        output_heap(heap)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(6) as figure_number:
        description  = 'Determining levels needed for a binary heap with N entries'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(7) as figure_number:
        description  = 'Which of these are valid binary max heaps?'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(8) as figure_number:
        description  = 'The first step to inserting an entry is to place it in the next available position'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(9) as figure_number:
        description  = 'The second step is to swim the entry up one level as needed'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(10) as figure_number:
        description  = 'Third step swims the entry up one level as needed'
        label = caption(chapter, figure_number)
        heap2 = initial_heap()
        heap2.enqueue(12, 12)
        output_heap(heap2)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(11) as figure_number:
        description  = 'Adding an entry with priority 16 swims up to the top'
        label = caption(chapter, figure_number)
        heap3 = initial_heap()
        heap3.enqueue(12, 12)
        heap3.enqueue(16, 16)
        output_heap(heap3)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(12) as figure_number:
        description  = 'The first step is to remove bottommost entry'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(13) as figure_number:
        description  = 'Broken heap resulting from swapping last entry with level 0'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(14) as figure_number:
        description  = 'Swap top entry with its left child which had a higher priority'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(15) as figure_number:
        description  = 'Sink down an additional level'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(16) as figure_number:
        description  = 'Resulting heap after sinking entry to its proper location'
        label = caption(chapter, figure_number)
        heap4 = initial_heap()
        heap4.enqueue(12, 12)
        heap4.enqueue(16, 16)
        heap4.dequeue()
        output_heap(heap4)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(17) as figure_number:
        description  = 'Storing a max binary heap in an array'
        label = caption(chapter, figure_number)
        heap4 = initial_heap()
        heap4.enqueue(12, 12)
        print(' -- |' + '|'.join([' {:>3} '.format(e.priority) for e in heap4.storage[1:heap4.N+1]]))
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(18) as figure_number:
        description  = 'Changes to storage after enqueue in Figure 4-8'
        label = caption(chapter, figure_number)
        heap_enqueue_animation()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(19) as figure_number:
        description  = 'Changes to storage after dequeue in Figure 4-11'
        label = caption(chapter, figure_number)
        heap_dequeue_animation()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(20) as figure_number:
        description  = 'Using an array as a circular queue'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(21) as figure_number:
        description  = 'A novel factorial heap structure'
        label = caption(chapter, figure_number)
        print('Hand drawn')
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    generate_ch04()
