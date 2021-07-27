"""Tables and Figures for chapter 06.

   Learning Algorithms:
   A programmer's guide to writing better code
   Chapter 6: Binary Trees: Infinity in the Palm of Your Hand
   (C) 2021, George T. Heineman

"""

import timeit
import math
from algs.table import DataTable, caption, FigureNum, TableNum, process
from ch02.bas import binary_array_search
from ch06.challenge import speaking_tree

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
    stmt = '''
from {0} import PQ 
one_run(PQ({1}), {1}, {2})'''.format(clazz,N,factor)
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def run_trials_pq(clazz, N, factor):
    """Run a single trial."""
    stmt = '''
from {} import PQ 
one_run(PQ(), {}, {})'''.format(clazz,N,factor)
    return min(timeit.repeat(stmt=stmt, setup = 'from ch04.timing import one_run',
                             repeat=5, number=10))/10

def average_performance(max_n=32768, output=True, decimals=2):
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
    high = max_n

    tbl = DataTable([8,8,8], ['N','Heap','BinaryTree'], output=output, decimals=decimals)
    N = 128
    while N <= high:
        binary = 1000000*run_trials_pq('ch06.pq', N, T)/(T*N)
        heap   = 1000000*run_trials_pq_n('ch04.heap', N, T)/(T*N)
        tbl.row([N, heap, binary])
        N *= 2

    if output:
        print('Heap', tbl.best_model('Heap'))
        print('BinaryTree', tbl.best_model('BinaryTree'))

    return tbl

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

    return mult7

def debug_expression():
    """Request evaluation of simple expression."""
    from ch06.expression import Value, Expression, add, mult

    # Sample Recursive Expression
    a = Expression(add, Value(1), Value(5))
    m = Expression(mult, a, Value(9))
    return m

def run_trials_prepend(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    alist.insert(0,i)'''.format(num),
        setup = 'alist=list(range({}))'.format(N), repeat=5, number=1))/10

def run_trials_append(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    alist.append(i)'''.format(num),
        setup = 'alist=list(range({}))'.format(N), repeat=5, number=1))/10

def run_trials_remove(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    alist.pop(0)'''.format(num),
        setup = 'alist=list(range({}))'.format(N), repeat=5, number=1))/10

def run_trials_tree(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt='''
for i in range(-1, -{}, -1):
    bt.remove(i)'''.format(num), setup = '''
from ch06.balanced import BinaryTree
bt = BinaryTree()
for i in range({}):
    bt.insert(i)'''.format(N), repeat=5, number=1))/10

def generate_list_table(max_k=21, output=True, decimals=3):
    """
    Generate table showing O(N) behavior of Python 'list' structure on insert for
    lists up to (but not including) 2**max_k
    """
    tbl = DataTable([8,8,8,8,8], ['N','Prepend','Remove', 'Append', 'Tree'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        tbl.row([n,run_trials_prepend(n, 1000),
                 run_trials_remove(n, 1000),
                 run_trials_append(n, 1000),
                 run_trials_tree(n,1000)])
    return tbl

def compare_dynamic_build_and_access_time(repeat=25, num=10, output=True):
    """Generate tables for build and access for AVL trees."""
    from ch06.symbol import BinaryTree
    from resources.english import english_words
    bt = BinaryTree()
    for w in english_words():
        bt.put(w,w)
    total = len(english_words())

    if output:
        print('This will take several minutes...')
        print('total number of words =', total)
        print('height of AVL tree for all English words =',bt.root.height)
        print('has to at least be =', math.log(total+1)/math.log(2) - 1)

    # When 'ht = HTLL(...) is inside the STMT, it measures BUILD TIME.
    # When it is included in the setup, we are measuring ACCESS TIME.
    t_build = min(timeit.repeat(stmt='''
ht = BinaryTree()
for w in words:
    ht.put(w,w)''', setup='''
from ch06.symbol import BinaryTree
from resources.english import english_words
words = english_words()''', repeat=repeat, number=num))/num

    t_access = min(timeit.repeat(stmt='''
for w in words:
    ht.get(w)''', setup='''
from ch06.symbol import BinaryTree
from resources.english import english_words
ht = BinaryTree()
words = english_words()
for w in words:
    ht.put(w,w)''', repeat=repeat, number=num))/num

    if output:
        print('Build-time =', t_build,', Access-time = ', t_access)
    return (t_build, t_access)

def compare_avl_pq_with_heap_pq(max_k=16, output=True, decimals=2):
    """Generate times for comparing values."""
    tbl = DataTable([8,10,10], ['N','Heap-pq', 'AVL-pq'], output=output, decimals=decimals)
    repeat = 25
    num = 10

    for n in [2**k for k in range(10, max_k)]:
        t_heap_pq = min(timeit.repeat(stmt='''
random.seed(11)
pq = PQ({0})
for _ in range({0}):
    r = random.random()
    pq.enqueue(r,r)
while pq:
    pq.dequeue()'''.format(n), setup='''
from ch04.heap import PQ
import random''', repeat=repeat, number=num))/num

        t_avl_pq = min(timeit.repeat(stmt='''
random.seed(11)
pq = PQ()
for _ in range({0}):
    r = random.random()
    pq.enqueue(r,r)
while pq:
    pq.dequeue()'''.format(n), setup='''
from ch06.pq import PQ
import random''', repeat=repeat, number=num))/num

        tbl.row([n, t_heap_pq, t_avl_pq])

    return tbl

def sample_binary_tree_as_symbol():
    """Create BST as symbol structure."""
    from ch06.symbol import BinaryTree

    def structure(n):
        """Return structure of binary tree using parentheses to show nodes with left/right subtrees."""
        if n is None:
            return ''

        return '({} => {},{},{})'.format(n.key, n.value, structure(n.left), structure(n.right))

    # priorities from the Chapter 4 max binary heap example, in some random order.
    entries = [(53, 'Iodine'), (20, 'Calcium'), (76, 'Osmium'), (5, 'Boron'),
               (58, 'Cerium'), (79, 'Gold')]

    symbol = BinaryTree()
    for num,element in entries:
        symbol.put(num, element)

    # (9,(5,(2,(1,,),(4,,)),(8,(7,(6,,),(8,,)),(9,,))),(12,(10,,(11,,)),(14,(13,,),(14,,(15,,)))))
    return structure(symbol.root)

def sample_binary_tree_as_pq():
    """Create BST as priority queue structure."""
    from ch06.pq import PQ

    def structure(n):
        """Return structure of binary tree using parentheses to show nodes with left/right subtrees."""
        if n is None:
            return ''

        return '({},{},{})'.format(n.priority, structure(n.left), structure(n.right))

    # priorities from the Chapter 4 max binary heap example, in some random order.
    priorities = [9, 13, 4, 10, 8, 12, 14, 2, 11, 5, 9, 14, 7, 6, 15, 1, 8]
    pq = PQ()
    for p in priorities:
        pq.enqueue('some_value{}'.format(p), p)

    # (9,(5,(2,(1,,),(4,,)),(8,(7,(6,,),(8,,)),(9,,))),(12,(10,,(11,,)),(14,(13,,),(14,,(15,,)))))
    return structure(pq.tree.root)

def show_unbalanced_result():
    """Show tree resulting from two insertions that unbalances it."""
    from ch06.tree import BinaryTree

    def height(n):
        """Compute height for node."""
        if n is None:
            return -1
        return 1 + max(height(n.left), height(n.right))

    def survey(n, result):
        """Produce map of heights for all nodes."""
        if n is None:
            return

        ht = height(n)
        if ht in result:
            result[ht].append(n.value)
        else:
            result[ht] = [n.value]

        survey(n.left, result)
        survey(n.right, result)

    def report(result):
        """Format results properly."""
        for ht in sorted(result.keys()):
            print(ht, result[ht])
        print()

    bt = BinaryTree()
    for i in [19, 14, 53, 3, 15, 26, 58]:
        bt.insert(i)

    result = {}
    survey(bt.root, result)
    report(result)

    result = {}
    bt.insert(29)
    survey(bt.root, result)
    report(result)

    result = {}
    bt.insert(27)
    survey(bt.root, result)
    report(result)

def fibonacci_tree_sample():
    """Produce the 12-node Fibonacci tree in challenge exercise."""
    from ch06.challenge import fibonacci_avl, tree_structure

    node = fibonacci_avl(6)
    print(tree_structure(node))

def generate_ch06():
    """Generate Tables and Figures for chapter 06."""
    chapter = 6

    with FigureNum(1) as figure_number:
        description  = 'Representing mathematical expressions using expression trees'
        label = caption(chapter, figure_number)
        mult7 = expression_tree()
        print(mult7,'=',mult7.eval())
        print('in postfix:', ' '.join(str(k) for k in mult7.postfix()))
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(2) as figure_number:
        description  = 'Visualizing recursive evaluation of ((1+5)*9)'
        label = caption(chapter, figure_number)
        mult2 = debug_expression()
        print(mult2,'=',mult2.eval())
        print('{}. {}'.format(label, description))
        print()

    with TableNum(1) as table_number:
        process(generate_list_table(),
                chapter, table_number,
                'Comparing insert and remove performance of lists against binary search tree (time in ms)', yaxis="Time (in ms)")

    with FigureNum(3) as figure_number:
        description  = 'Binary Search Tree containing seven values'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(2) as table_number:
        description  = 'Creating a binary search tree by inserting (in order) 19,14,15,53,58,3,26'
        speaking_tree()
        label = caption(chapter, table_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(4) as figure_number:
        description  = 'Insert 29 into the binary search tree example'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(5) as figure_number:
        description = 'Different binary search trees when same values are inserted in different order'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(6) as figure_number:
        description  = 'Two possible binary search trees after removing 19 from Figure 6-4'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(7) as figure_number:
        description  = 'Removing minimum value in a subtree'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(3) as table_number:
        description  = 'Demonstrating how node is removed from binary search tree'
        label = caption(chapter, table_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(8) as figure_number:
        description  = 'Iterating over the values in a binary search tree in ascending order'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(9) as figure_number:
        description  = 'A complete binary tree stores the most values with the least height'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(10) as figure_number:
        description = 'Unbalanced tree after two insertions.'
        label = caption(chapter, figure_number)
        show_unbalanced_result()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(11) as figure_number:
        description = 'Recursive invocation when inserting a value.'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(12) as figure_number:
        description = 'Rebalancing this binary search tree by rotating the root node to the right'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(13) as figure_number:
        description = 'Four different node rotations'
        label = caption(chapter, figure_number)
        print('{}. {}'.format(label, description))
        print()

    with TableNum(4) as table_number:
        description = 'Implementation of rotate left-right'
        label = caption(chapter, table_number)
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(14) as figure_number:
        description = 'Binary search tree as symbol table: keys are atomic numbers; values are element names'
        label = caption(chapter, figure_number)
        sample_binary_tree_as_symbol()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(15) as figure_number:
        description = 'Binary search tree as priority queue: priorities are atomic numbers; values are element names'
        label = caption(chapter, figure_number)
        sample_binary_tree_as_pq()
        print('{}. {}'.format(label, description))
        print()

    with FigureNum(16) as figure_number:
        description = 'A Fibonacci tree with twelve nodes'
        label = caption(chapter, figure_number)
        fibonacci_tree_sample()
        print('{}. {}'.format(label, description))
        print()

#######################################################################
if __name__ == '__main__':
    generate_ch06()
