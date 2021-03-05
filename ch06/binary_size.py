"""
Helper method for safely retrieving size of a binary node.
"""

def binary_node_size(n):
    """Safe method to return size of sub-tree rooted at n, or 0 if None."""
    if n:
        return n.N
    return 0
