"""
Represents an entry for a Priority Queue stored within a Linked List.
"""
class LinkedEntry:
    """Represents a (v,p) entry in a priority queue using linked lists."""
    def __init__(self, v, p, nxt=None):
        self.value = v
        self.priority = p
        self.next = nxt

    def __str__(self):
        return '[{} p={}]'.format(self.value, self.priority)
