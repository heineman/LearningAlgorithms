"""Code for chapter 06."""

import timeit
import math
import random
from algs.table import DataTable, captionx, FigureNum, TableNum, process
from ch02.bas import binary_array_search

def insert_value(A, val):
    """Return new list with val in its proper location."""
    idx = binary_array_search(A, val)
    if idx < 0:
        idx = -idx - 1

    new_A = [None] * (len(A) + 1)
    new_A[:idx] = A[:idx]
    new_A[idx] = val
    new_A[idx+1:] = A[idx:]
    return new_A

def remove_value(A, val):
    """Return new list with val removed if it existed."""
    idx = binary_array_search(A, val)
    if idx < 0:
        return A

    new_A = [None] * (len(A) - 1)
    new_A[:idx] = A[:idx]
    new_A[idx:] = A[idx+1:]
    return new_A

# Executes 3*N/2 add operations and 3*N/2 remove_max operations for a total of 3*N
def run_trials_pq_n(clazz, N, factor):
    """Run a single trial."""
    stmt = f'''
from {clazz} import PQ 
one_run(PQ({N}), {N}, {factor})'''
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def run_trials_pq(clazz, N, factor):
    """Run a single trial."""
    stmt = f'''
from {clazz} import PQ 
one_run(PQ(), {N}, {factor})'''
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def average_performance():
    """
    Generate table of average performance for different PQ implementations.

         N        Heap    BinaryTree
         128        2.38        5.15
         256        2.80        5.75
         512        3.22        6.63
       1,024        3.51        7.60
       2,048        3.89        8.42
       4,096        4.35        9.21
       8,192        4.75       10.24
      16,384        5.23       11.38
      32,768        5.96       12.90
    Heap [(<Model.LOG: 1>, 0.9946069479866522, 0.19032820110187337, 0.3676270723813611)]
    BinaryTree [(<Model.LOG: 1>, 0.9945273325485424, 0.48542129185563554, 0.7892486887139494)]

    While both offer O(Log N) performance, heap is more efficient (a little more than
    twice as efficient).
    """
    T = 3
    high = 32768

    tbl = DataTable([8,8,8], ['N','Heap','BinaryTree'], decimals=2)
    N = 128
    while N <= high:
        binary = 1000000*run_trials_pq('ch06.pq', N, T)/(T*N)
        heap   = 1000000*run_trials_pq_n('ch04.heap', N, T)/(T*N)
        tbl.row([N, heap, binary])
        N *= 2

    print ('Heap', tbl.best_model('Heap'))
    print ('BinaryTree', tbl.best_model('BinaryTree'))

def generate_ch06_old():
    """Generate tables/figures for chapter 06."""
    average_performance()

def expression_tree():
    """Build expression tree."""
    from ch06.expression import Value, Expression, add, mult, sub, divide

    # Sample Recursive Expression
    add1 = Expression(add, Value(3), Value(1))
    div2 = Expression(divide, add1, Value(4))
    add3 = Expression(add, Value(1), Value(5))
    mult4 = Expression(mult, add3, Value(9))
    mult5 = Expression(mult, Value(2), Value(6))
    sub6 = Expression(sub, mult4, mult5)
    mult7 = Expression(mult, div2, sub6)

    print(mult7,'=',mult7.eval())
    print('in postfix:', ' '.join(str(k) for k in mult7.postfix()))

def debug_expression():
    """Request evaluation of simple expression."""
    from ch06.expression import Value, Expression, add, mult

    # Sample Recursive Expression
    add1 = Expression(add, Value(1), Value(5))
    mult2 = Expression(mult, add1, Value(9))
    print(mult2,'=',mult2.eval())

def run_trials_prepend(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt=f'''
for i in range({num}):
    alist.insert(0,i)''', setup = f'alist=list(range({N}))', repeat=5, number=1))/10

def run_trials_append(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt=f'''
for i in range({num}):
    alist.append(i)''', setup = f'alist=list(range({N}))', repeat=5, number=1))/10

def run_trials_remove(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt=f'''
for i in range({num}):
    alist.pop(0)''', setup = f'alist=list(range({N}))', repeat=5, number=1))/10

def run_trials_tree(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt=f'''
for i in range(-1, -{num}, -1):
    bt.remove(i)''', setup = f'''
from ch06.balanced import BinaryTree
bt = BinaryTree()
for i in range({N}):
    bt.insert(i)''', repeat=5, number=1))/10

def generate_list_table():
    """Generate table showing O(N) behavior of Python 'list' structure on insert."""
    tbl = DataTable([8,8,8,8,8], ['N','Prepend','Remove', 'Append', 'Tree'], decimals=3)

    for n in [2**k for k in range(10, 21)]:
        tbl.row([n,run_trials_prepend(n, 1000),
                 run_trials_remove(n, 1000),
                 run_trials_append(n, 1000),
                 run_trials_tree(n,1000)])
    return tbl

def compare_dynamic_build_and_access_time():
    """Generate tables for build and access for AVL trees."""
    repeat = 25
    num = 10

    from ch06.symbol import BinaryTree
    from resources.english import english_words
    bt = BinaryTree()
    for w in english_words():
        bt.put(w,w)
    total = len(english_words())
    
    print('This will take several minutes...')
    print('total number of words =', total)
    print('height of AVL tree for all English words =',bt.root.height)
    print('has to at least be =', math.log(total+1)/math.log(2) - 1)

    # When 'ht = HTLL(...) is inside the STMT, it measures BUILD TIME.
    # When it is included in the setup, we are measuring ACCESS TIME.
    print('build T')
    t_build = min(timeit.repeat(stmt='''
ht = BinaryTree()
for w in words:
    ht.put(w,w)''', setup='''
from ch06.symbol import BinaryTree
from resources.english import english_words
words = english_words()''', repeat=repeat, number=num))/num

    print('Access T')
    t_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch06.symbol import BinaryTree
from resources.english import english_words
ht = BinaryTree()
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

    print('Build-time =', t_build,', Access-time = ', t_access)

def compare_avl_pq_with_heap_pq():
    """Generate times for comparing values."""
    
    tbl = DataTable([8,10,10], ['N','Heap-pq', 'AVL-pq'], decimals=2)
    repeat = 25
    num = 10

    for n in [2**k for k in range(10, 16)]:
        t_heap_pq = min(timeit.repeat(stmt=f'''
random.seed(11)
pq = PQ({n})
for _ in range({n}):
    r = random.random()
    pq.enqueue(r,r)
while pq:
    pq.dequeue()''', setup='''
from ch04.heap import PQ
import random''', repeat=repeat, number=num))/num

        t_avl_pq = min(timeit.repeat(stmt=f'''
random.seed(11)
pq = PQ()
for _ in range({n}):
    r = random.random()
    pq.enqueue(r,r)
while pq:
    pq.dequeue()''', setup='''
from ch06.pq import PQ
import random''', repeat=repeat, number=num))/num

        tbl.row([n, t_heap_pq, t_avl_pq])

def generate_ch06():
    """Generate Tables and Figures for chapter 06."""
    chapter = 6

    with FigureNum(1) as figure_number:
        description  = 'Representing mathematical expressions using expression trees'
        label = captionx(chapter, figure_number)
        expression_tree()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(2) as figure_number:
        description  = 'Visualizing recursive evaluation of ((1+5)*9)'
        label = captionx(chapter, figure_number)
        debug_expression()
        print('{}. {}'.format(label, description))
        print()

    with TableNum(1) as table_number:
        process(generate_list_table(),
                chapter, table_number,
                'Time to prepend or append 1,000 values to list of size N', yaxis="Time (in ms)")

    with FigureNum(3) as figure_number:
        description  = 'Binary Search Tree containing seven values'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(2) as table_number:
        description  = 'Creating a binary search tree by inserting (in order) 19,14,15,53,58,3,26'
        label = captionx(chapter, table_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(4) as figure_number:
        description  = 'Insert 29 into the binary search tree example'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(5) as figure_number:
        description = 'Different binary search trees when same values are inserted in different order'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(6) as figure_number:
        description  = 'Two possible binary search trees afte removing 19 from Figure 6-4'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(7) as figure_number:
        description  = 'Removing minimum value in a subtree'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(3) as table_number:
        description  = 'Demonstrating how node is removed from binary search tree'
        label = captionx(chapter, table_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(8) as figure_number:
        description  = 'Iterating over the values in a binary search tree in ascending order'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(9) as figure_number:
        description  = 'A complete binary tree stores the most values with the least height'
        label = captionx(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    compare_avl_pq_with_heap_pq()
    #compare_dynamic_build_and_access_time()
    #generate_ch06()
