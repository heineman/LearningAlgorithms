"""
Helper method for safely retrieving size of a binary node.
"""

def binary_node_size(n):
    """Safe method to return size of sub-tree rooted at n, or 0 if None."""
    return n.N if n else 0
