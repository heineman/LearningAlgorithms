"""
Timing results for Chapter 08.
"""
import timeit
from algs.table import DataTable

def list_enqueue(N, num):
    """Run a single trial of num enqueue requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.append(i)'''.format(num),
        setup = 'q = list(range({}))'.format(N), repeat=5, number=1))

def list_dequeue(N, num):
    """Run a single trial of num dequeue requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.pop(0)'''.format(num),
        setup = 'q = list(range({}))'.format(N), repeat=5, number=1))

def dequeue_enqueue(N, num):
    """Run a single trial of num enqueue requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.append(i)'''.format(num),
        setup = '''
from collections import deque
q = deque()
for i in range({}):
    q.append(i)'''.format(N), repeat=5, number=1))

def dequeue_dequeue(N, num):
    """Run a single trial of num dequeue requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.popleft()'''.format(num),
        setup = '''
from collections import deque
q = deque()
for i in range({}):
    q.append(i)'''.format(N), repeat=5, number=1))
    
def queue_enqueue(N, num):
    """Run a single trial of num enqueue requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.put(i)'''.format(num),
        setup = '''
from queue import Queue
q = Queue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def queue_dequeue(N, num):
    """Run a single trial of num dequeue requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.get()'''.format(num),
        setup = '''
from queue import Queue
q = Queue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def simple_queue_enqueue(N, num):
    """Run a single trial of num enqueue requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.put(i)'''.format(num),
        setup = '''
from queue import SimpleQueue
q = SimpleQueue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def simple_queue_dequeue(N, num):
    """Run a single trial of num dequeue requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.get()'''.format(num),
        setup = '''
from queue import SimpleQueue
q = SimpleQueue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def run_trials_dequeue(N, num):
    """Run a single trial."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    alist.append(i)'''.format(num),
        setup = 'alist=list(range({}))'.format(N), repeat=5, number=1))

def generate_queue_table(max_k=18, output=True, decimals=3):
    """
    Generate table showing different queue behaviors.
    """
    # Enqueue table first
    enq_tbl = DataTable([8,8,8,8,8], ['N','list','Dequeue', 'SimpleQueue', 'Queue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        enq_tbl.row([n,list_enqueue(n, 1000),
                 dequeue_enqueue(n, 1000),
                 queue_enqueue(n, 1000),
                 simple_queue_enqueue(n, 1000)])
        
    deq_tbl = DataTable([8,8,8,8,8], ['N','list','Dequeue', 'SimpleQueue', 'Queue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        enq_tbl.row([n,list_dequeue(n, 1000),
                 dequeue_dequeue(n, 1000),
                 queue_dequeue(n, 1000),
                 simple_queue_dequeue(n, 1000)])
           
    return (enq_tbl, deq_tbl)

def list_push(N, num):
    """Run a single trial of num push requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    st.append(i)'''.format(num),
        setup = 'st = list(range({}))'.format(N), repeat=5, number=1))

def list_pop(N, num):
    """Run a single trial of num dequeue requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    st.pop()'''.format(num),
        setup = 'st = list(range({}))'.format(N), repeat=5, number=1))

def dequeue_push(N, num):
    """Run a single trial of num push requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.append(i)'''.format(num),
        setup = '''
from collections import deque
q = deque()
for i in range({}):
    q.append(i)'''.format(N), repeat=5, number=1))

def dequeue_pop(N, num):
    """Run a single trial of num pop requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.pop()'''.format(num),
        setup = '''
from collections import deque
q = deque()
for i in range({}):
    q.append(i)'''.format(N), repeat=5, number=1))

def queue_push(N, num):
    """Run a single trial of num push requests."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.put(i)'''.format(num),
        setup = '''
from queue import LifoQueue
q = LifoQueue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def queue_pop(N, num):
    """Run a single trial of num pop requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for i in range({}):
    q.get()'''.format(num),
        setup = '''
from queue import LifoQueue
q = LifoQueue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def generate_stack_table(max_k=18, output=True, decimals=3):
    """
    Generate table showing different stack behaviors.
    """
    # Enqueue table first
    push_tbl = DataTable([8,8,8,8], ['N','list','Dequeue', 'LifoQueue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        push_tbl.row([n,list_push(n, 1000),
                 dequeue_push(n, 1000),
                 queue_push(n, 1000)])
        
    pop_tbl = DataTable([8,8,8,8], ['N','list','Dequeue', 'LifoQueue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        pop_tbl.row([n,list_pop(n, 1000),
                 dequeue_pop(n, 1000),
                 queue_pop(n, 1000)])
           
    return (push_tbl, pop_tbl)

def heap_add(N, num):
    """Run a single trial of num heap add requests."""
    return 1000*min(timeit.repeat(stmt='''
v = 0
for i in range({}):
    q.put(v)
    v = (v + 137)%{}'''.format(num, N),
        setup = '''
from queue import LifoQueue
q = LifoQueue()
for i in range({}):
    q.put(i)'''.format(N), repeat=5, number=1))

def heap_remove(N, num):
    """Run a single trial of num heap remove requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for _ in range({}):
    heapq.heappop(h)'''.format(num),
        setup = '''
import heapq
h = []
for i in range(0,2*{},2):
    heapq.heappush(h, i)'''.format(N), repeat=5, number=1))
    
def pq_add(N, num):
    """Run a single trial of num heap add requests."""
    return 1000*min(timeit.repeat(stmt='''
v = 0
for i in range({}):
    pq.put(v)
    v = (v + 137)%{}'''.format(num, N),
        setup = '''
import queue
pq = queue.PriorityQueue()
for i in range(0,{},2):
    pq.put(i, i)'''.format(N), repeat=5, number=1))

def pq_remove(N, num):
    """Run a single trial of num heap remove requests. Make sure that num < N."""
    return 1000*min(timeit.repeat(stmt='''
for _ in range({}):
    pq.get()'''.format(num),
        setup = '''
import queue
pq = queue.PriorityQueue()
for i in range(0,2*{},2):
    pq.put(i, i)'''.format(N), repeat=5, number=1))

def generate_heap_table(max_k=18, output=True, decimals=3):
    """
    Generate table showing different stack behaviors.
    """
    # Enqueue table first
    add_tbl = DataTable([8,8,8], ['N','heapq','PriorityQueue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        add_tbl.row([n,heap_add(n, 1000),
                 pq_add(n, 1000)])
        
    remove_tbl = DataTable([8,8,8], ['N','heapq','PriorityQueue'],
                    output=output, decimals=decimals)

    for n in [2**k for k in range(10, max_k)]:
        remove_tbl.row([n,heap_remove(n, 1000),
                 pq_remove(n, 1000)])
           
    return (add_tbl, remove_tbl)

#######################################################################
if __name__ == '__main__':
    print('Stack Tables')
    generate_stack_table()
    
    print('Queue Tables')
    generate_queue_table
    
    print('Heap Tables')
    generate_heap_table()
    
