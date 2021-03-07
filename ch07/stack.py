"""
Stack Data Type implemented using linked lists.
"""
from algs.node import Node

class Stack:
    """
    Implementation of a Stack using linked lists.
    """
    def __init__(self):
        self.top = None

    def is_empty(self):
        """Determine if queue is empty."""
        return self.top is None

    def push(self, val):
        """Push new item to the top of the stack."""
        if self.top is None:
            self.top = Node(val)
        else:
            self.top = Node(val, self.top)

    def pop(self):
        """Remove and return top item from stack."""
        if self.is_empty():
            raise Exception('Stack is empty')

        val = self.top.value
        self.top = self.top.next
        return val
