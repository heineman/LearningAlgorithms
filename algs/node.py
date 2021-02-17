"""Class represents a node in a linked list."""

class Node:
    """
    Node structure to use in linked list.
    """
    def __init__(self, val):
        self.value = val
        self.next = None

    def __str__(self):
        return '[{}]'.format(self.value)
