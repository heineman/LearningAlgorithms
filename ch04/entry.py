"""Represents an entry in a Priority Queue."""
class Entry:
    """Represents a (v,p) entry in a priority queue."""
    def __init__(self, v, p):
        self.value = v
        self.priority = p

    def __str__(self):
        return '[{} p={}]'.format(self.value, self.priority)
