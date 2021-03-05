"""Class represents a node in a linked list."""

class Node:
    """
    Node structure to use in linked list.
    """
    def __init__(self, val, rest=None):
        self.value = val
        self.next = rest

    def __str__(self):
        return '[{}]'.format(self.value)

    def __iter__(self):
        """
        Generator to retrieve values in linked list in order.

        Enabled Python code like following, where alist is a Node.

            for v in alist:
                print(v)

        """
        yield self.value

        if self.next:
            for v in self.next:
                yield v
