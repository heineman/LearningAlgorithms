"""Test cases for Chapter 04."""

import unittest

class Item:
    """Represents an item that is comparable by priority."""
    def __init__(self, v, p):
        """An entry in priority queue."""
        self.val = v
        self.priority = p

    def __lt__(self, other):
        """Needed for Item to be in a heap."""
        return self.priority < other.priority

    def __str__(self):
        """return string representation."""
        return '[value={}, priority={}]'.format(self.val, self.priority)

class TimeSpecifiedItem:
    """
    Build in timestamp when an item is enqueued to be able to break
    ties by oldest timestamp.
    """
    ctr = [0]

    def __init__(self, v, p):
        """
        An entry in priority queue with counter since timestamp is
        not precise enough, even with nanosec.
        """
        self.val = v
        self.priority = p
        self.timestamp = TimeSpecifiedItem.ctr[0]
        TimeSpecifiedItem.ctr[0] += 1

    def __lt__(self, other):
        """Needed for Item to be in a heap."""
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority < other.priority

    def __str__(self):
        """return string representation."""
        return '[value={}, priority={}]'.format(self.val, self.priority)

class TestChapter4(unittest.TestCase):

    def validate(self, queue):
        """For a queue validates a few simple operations."""
        self.assertTrue(queue.is_empty())
        queue.enqueue(10)
        self.assertFalse(queue.is_empty())
        queue.enqueue(20)
        self.assertEqual(10, queue.dequeue())
        self.assertFalse(queue.is_empty())
        queue.enqueue(30)
        queue.enqueue(40)
        self.assertEqual(20, queue.dequeue())
        self.assertEqual(30, queue.dequeue())
        self.assertEqual(40, queue.dequeue())

    def priority_queue_stress_test(self, pq, max_length=None):
        """
        Given an empty Priority queue, add words from English dictionary where
        priority is length of word. Because some PQ implementations are so
        inefficient, allow a caller to restrict
        """
        from resources.english import english_words
        words = english_words()
        if max_length:
            words = words[:max_length]
        for w in words:
            pq.enqueue(w, len(w))

        # First word out is longest... / Last one out is smallest
        first = pq.dequeue()
        while pq:
            last = pq.dequeue()

        # Should be drained
        with self.assertRaises(RuntimeError):
            pq.dequeue()

        return (first, last)

    def test_dynamic_heap_pq_status(self):
        from ch04.dynamic_heap import PQ
        pq = PQ(5)
        self.assertTrue(pq.is_empty())
        for v,p in [('a',1), ('b',2), ('c', 3), ('d',4), ('e',5)]:
            pq.enqueue(v, p)
        self.assertTrue(pq.is_full())

    def test_heap_pq(self):
        from ch04.heap import PQ
        from resources.english import english_words
        words = english_words()[:1000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))

        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('abdominohysterectomy'), len('a')), (len(pair[0]), len(pair[1])))

    def test_array_pq(self):
        from ch04.array import PQ
        from resources.english import english_words
        words = english_words()[:1000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('abdominohysterectomy'), len('a')), (len(pair[0]), len(pair[1])))

    def test_ordered_list_pq(self):
        from ch04.ordered_list import PQ
        from resources.english import english_words
        words = english_words()[:10000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('acetylphenylhydrazine'), len('a')), (len(pair[0]), len(pair[1])))

    def test_just_ordered(self):
        from ch04.ordered import PQ
        pq = PQ(4)
        for i in range(4):
            pq.enqueue(i,i)
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_just_array(self):
        from ch04.array import PQ
        pq = PQ(4)
        for i in range(4):
            pq.enqueue(i,i)
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_just_builtin(self):
        from ch04.builtin import PQ
        pq = PQ(4)
        for i in range(4):
            pq.enqueue(i,i)
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_just_ordered_list(self):
        from ch04.ordered_list import PQ
        pq = PQ(4)
        for i in range(4):
            pq.enqueue(i,i)
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_ordered_pq(self):
        from ch04.ordered import PQ
        from resources.english import english_words
        words = english_words()[:10000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('acetylphenylhydrazine'), len('a')), (len(pair[0]), len(pair[1])))

    def test_factorial_heap_pq(self):
        from ch04.factorial_heap import PQ
        from resources.english import english_words
        words = english_words()[:1000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('abdominohysterectomy'), len('a')), (len(pair[0]), len(pair[1])))

    def test_validate_factorial_heap_pq(self):
        """Validate levels for factorial heap after enqueue and dequeue."""
        from ch04.factorial_heap import PQ, validate

        end = 10000
        pq = PQ(end)
        for i in range(end):
            pq.enqueue(i, i)
            validate(pq)

        last = end-1
        while pq:
            self.assertEqual(last, pq.dequeue())
            last -= 1
            validate(pq)

    def test_builtin_heap_pq(self):
        from ch04.builtin import PQ
        from resources.english import english_words
        words = english_words()[:1000]
        pair = self.priority_queue_stress_test(PQ(len(words)), len(words))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('abdominohysterectomy'), len('a')), (len(pair[0]), len(pair[1])))

    def test_dynamic_heap_pq(self):
        from ch04.dynamic_heap import PQ
        pair = self.priority_queue_stress_test(PQ(625))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('formaldehydesulphoxylate'), len('a')), (len(pair[0]), len(pair[1])))

    def stress(self, queue, ct):
        """Stress test queue with valid sequence of operations."""
        result = []
        for i in range(ct//2):    # populate with half
            queue.enqueue(i)

        while not queue.is_empty():   # take away 2, add 1
            i += 1
            queue.enqueue(i)

            result.append(queue.dequeue())  # will eventually drain
            if queue.is_empty():
                return result
            result.append(queue.dequeue())
        return result

    def test_queue_quick_normal(self):
        from ch04.list_queue import Queue
        q = Queue()
        self.validate(q)

    def test_queue_quick_circular(self):
        from ch04.circular_queue import Queue
        q = Queue(20)
        self.validate(q)
        with self.assertRaises(RuntimeError):
            q.dequeue()

    def test_queue_ordered_list(self):
        from ch04.ordered_list import PQ
        pq = PQ(5)
        self.assertFalse(pq.is_full())
        for v,p in [(1,1), (2,2), (3, 3), (4,4), (5,5)]:
            pq.enqueue(v, p)
        val = 5
        while pq:
            self.assertEqual(val, pq.dequeue())
            val -= 1
        with self.assertRaises(RuntimeError):
            pq.dequeue()

    def test_queue_ordered(self):
        from ch04.ordered import PQ
        pq = PQ(5)
        self.assertFalse(pq.is_full())
        for v,p in [(1,1), (2,2), (3, 3), (4,4), (5,5)]:
            pq.enqueue(v, p)
        val = 5
        while pq:
            self.assertEqual(val, pq.dequeue())
            val -= 1
        with self.assertRaises(RuntimeError):
            pq.dequeue()

    def test_queue_array(self):
        from ch04.array import PQ
        pq = PQ(5)
        self.assertFalse(pq.is_full())
        for v,p in [(1,1), (2,2), (3, 3), (4,4), (5,5)]:
            pq.enqueue(v, p)
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)
        val = 5
        while pq:
            self.assertEqual(val, pq.dequeue())
            val -= 1
        with self.assertRaises(RuntimeError):
            pq.dequeue()

    def test_queue_stress_normal(self):
        from ch04.list_queue import Queue
        queue = Queue()
        result = self.stress(queue, 50)
        self.assertEqual(list(range(50)), result)
        with self.assertRaises(RuntimeError):
            queue.dequeue()

    def test_queue_stress_circular(self):
        from ch04.circular_queue import Queue
        queue = Queue(20)
        result = self.stress(queue, 20)
        expect = list(range(20))

        self.assertEqual(expect, result)

        queue = Queue(20)
        for i in range(20):
            queue.enqueue(i)
        try:
            queue.enqueue(99999)
            self.fail('should have detected full queue')
        except RuntimeError:
            pass

    def test_heap(self):
        from ch04.heap import PQ

        pq = PQ(5)
        for i in range(5):
            pq.enqueue(i, i)

        self.assertEqual(4, pq.dequeue())
        self.assertEqual(3, pq.dequeue())
        self.assertEqual(2, pq.dequeue())
        self.assertEqual(1, pq.dequeue())
        self.assertEqual(0, pq.dequeue())

    def test_linked_entry(self):
        from ch04.linked_entry import LinkedEntry
        e = LinkedEntry('99', 101)
        self.assertEqual('[99 p=101]', str(e))

    def test_linked_pq(self):
        from ch04.linked import PQ
        pq = PQ(3)
        self.assertFalse(pq.is_full())
        with self.assertRaises(RuntimeError):
            pq.dequeue()
        for i in range(3):
            pq.enqueue(i,i)
        self.assertTrue(pq.is_full())
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_heap_pq_edge_cases(self):
        from ch04.heap import PQ
        pq = PQ(3)
        with self.assertRaises(RuntimeError):
            pq.peek()
        self.assertFalse(pq.is_full())
        with self.assertRaises(RuntimeError):
            pq.dequeue()
        for i in range(3):
            pq.enqueue(i,i)
        self.assertTrue(pq.is_full())
        with self.assertRaises(RuntimeError):
            pq.enqueue(99,99)

    def test_entry(self):
        from ch04.entry import Entry
        e = Entry('99', 101)
        self.assertEqual('[99 p=101]', str(e))

    def test_trial_factorial_heap(self):
        from ch04.timing import trial_factorial_heap

        tbl = trial_factorial_heap(max_n=2048, output=False)
        self.assertTrue(tbl.entry(1024, 'Heap') <= tbl.entry(1024, 'FactHeap'))

    def test_native(self):
        """
        Heapq is min heap provided by Python libraries.

        In some Heap implementations, two elements with the same priority are
        removed from the PQ in the order in which they had been inserted,
        but this is not the case for Python Heapq. You actually have to do
        the work yourself, which is commonly done by adding an incrementing
        counter to the item so it can be used for comparison.
        """
        import heapq
        X = []
        heapq.heappush(X, Item('A', 5))
        heapq.heappush(X, Item('B', 5))
        heapq.heappush(X, Item('C', 5))
        heapq.heappush(X, Item('D', 5))
        heapq.heappush(X, Item('E', 5))
        heapq.heappush(X, Item('F', 5))
        item_ordered = []
        while X:
            item_ordered.append(heapq.heappop(X).val)
        self.assertEqual(['A', 'C', 'F', 'E', 'B', 'D'], item_ordered)

        X = []
        heapq.heappush(X, TimeSpecifiedItem('A', 5))
        heapq.heappush(X, TimeSpecifiedItem('B', 5))
        heapq.heappush(X, TimeSpecifiedItem('C', 5))
        heapq.heappush(X, TimeSpecifiedItem('D', 5))
        heapq.heappush(X, TimeSpecifiedItem('E', 5))
        heapq.heappush(X, TimeSpecifiedItem('F', 5))
        ordered = []
        while X:
            ordered.append(heapq.heappop(X).val)
        self.assertEqual(['A', 'B', 'C', 'D', 'E', 'F'], ordered)

#######################################################################
if __name__ == '__main__':
    unittest.main()
