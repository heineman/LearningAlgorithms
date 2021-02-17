"""
Represents an entry in a Hashtable.

There are two flavors. Entry is meant for array-based storage while
LinkedEntry is meant for linked-list storage.

MarkedEntry is designed to support `remove()` in an open addressing
hashtable, as described in a challenge question for this chapter.

"""
class Entry:
    """Standard (k, v) entry for a hashtable."""
    def __init__(self, k, v):
        self.key = k
        self.value = v

    def __str__(self):
        return '{} -> {}'.format(self.key, self.value)

class LinkedEntry:
    """An (k, v) entry for a hashtable using linked lists, via next."""
    def __init__(self, k, v, nxt=None):
        self.key = k
        self.value = v
        self.next = nxt

    def __str__(self):
        return '{} -> {}'.format(self.key, self.value)

class MarkedEntry:
    """
    Entry (k, v) that can be marked. An open addressing hashtable can support
    removal by marking entries, and throwing them away upon resize.
    """
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.marked = False

    def is_marked(self):
        """Determines if entry is marked."""
        return self.marked

    def mark(self):
        """Mark entry."""
        self.marked = True

    def unmark(self):
        """Unmark entry."""
        self.marked = False

    def __str__(self):
        """Return entry as a string."""
        marks = '[Marked]' if self.marked else ''
        return '{} -> {} {}'.format(self.key, self.value, marks)
