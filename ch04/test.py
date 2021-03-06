"""Test cases for chapter 4."""
import unittest

class Test_Ch04(unittest.TestCase):

    def validate(self, queue):
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
    
    def test_heap_pq(self):
        from ch04.heap import PQ
        from resources.english import english_words
        words = english_words()
        pair = self.priority_queue_stress_test(PQ(len(words)))

        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('formaldehydesulphoxylate'), len('a')), (len(pair[0]), len(pair[1])))
        
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
        words = english_words()
        pair = self.priority_queue_stress_test(PQ(len(words)))
        # Note: we cannot guarantee individual words BUT we can guarantee length
        self.assertEqual((len('formaldehydesulphoxylate'), len('a')), (len(pair[0]), len(pair[1])))
        
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
        
    def test_binary_tree_from_chapter_06(self):
        from ch06.pq import PQ
        from resources.english import english_words
        words = english_words()
        pair = self.priority_queue_stress_test(PQ(), len(words))
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

    def stress_priority(self, queue, ct):
        for i in range(ct//2):    # populate with half, in increasing priority
            queue.enqueue(ct)

        while not queue.is_empty():   # take away 2, add 1
            i += 1
            queue.enqueue(i)

            queue.dequeue()           # will eventually drain
            if queue.is_empty():
                return
            queue.dequeue()

    def test_queue_quick_normal(self):
        from ch04.list_queue import Queue
        q = Queue()
        self.validate(q)

    def test_queue_quick_circular(self):
        from ch04.circular_queue import Queue
        q = Queue(20)
        self.validate(q)

    def test_queue_stress_normal(self):
        from ch04.list_queue import Queue
        queue = Queue()
        result = self.stress(queue, 50)
        self.assertEqual(list(range(50)), result)

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

#######################################################################
if __name__ == '__main__':
    unittest.main()
