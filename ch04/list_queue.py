"""
A queue implemented using linked Lists, storing (value, priority)
pairs to be retrieved in First-in, First-out fashion.
"""
from algs.node import Node

class Queue:
    """
    Implementation of a Queue using a circular buffer.
    """
    def __init__(self):
        self.first = None
        self.last = None

    def is_empty(self):
        """Determine if queue is empty."""
        return self.first is None

    def enqueue(self, val):
        """Enqueue new item to end of queue."""
        if self.first is None:
            self.first = self.last = Node(val)
        else:
            self.last.next = Node(val)
            self.last = self.last.next

    def dequeue(self):
        """Remove and return first item from queue."""
        if self.is_empty():
            raise Exception("Queue is empty")

        val = self.first.value
        self.first = self.first.next
        return val
