"""
Code showing how to work with Linked Lists as recursive structures.
"""
from algs.node import Node

def create_linked_list(alist):
    """Given a Python list, create linked list in same order."""
    if len(alist) == 0:
        return None

    first = Node(alist[0])
    first.next = create_linked_list(alist[1:])
    return first

def sum_list(node):
    """Given a Python list, sum its values recursively."""
    if node is None:
        return 0

    return node.value + sum_list(node.next)

def iterate_list(node):
    """
    Python Generator for a linked list.

    The following will print all elements in a linked list:

        for v in iterate_list(alist):
            print(v)

    """
    if node is None:
        return

    yield node.value

    for v in iterate_list(node.next):
        yield v

def sum_iterative(node):
    """Given a Python list, sum its values iteratively."""
    total = 0
    while node:
        total += node.value
        node = node.next

    return total

def reverse(node):
    """
    Given the first node in a linked list, return (R, L) where R is the
    linked list in reverse, and L points to last node in that list.
    """
    if node.next is None:
        return (node, node)

    (flipped, tail) = reverse(node.next)

    # Append to tail and return
    tail.next = node
    node.next = None
    return (flipped, node)
