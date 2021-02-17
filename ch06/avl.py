"""
Helper methods to support AVL re-balancing.

These depend on having a Binary node that computes its height
and automatically recomputes N attributes.
"""

from ch06.binary_size import binary_node_size

def height_difference(self):
    """
    Compute height difference of node's children in BST. Can return
    a negative number or positive number.
    """
    left_target  = 0
    right_target = 0
    if self.left:
        left_target = 1 + self.left.height
    if self.right:
        right_target = 1 + self.right.height

    return left_target - right_target

def compute_height(self):
    """Compute height of node in BST."""
    height = -1
    if self.left:
        height = max(height, self.left.height)
    if self.right:
        height = max(height, self.right.height)

    self.height = height + 1
    self.N = 1 + binary_node_size(self.left) + binary_node_size(self.right)

def rotate_right(self):
    """Perform right rotation around given node."""
    new_root = self.left
    grandson = new_root.right
    self.left = grandson
    new_root.right = self

    compute_height(self)
    return new_root

def rotate_left(self):
    """Perform left rotation around given node."""
    new_root = self.right
    grandson = new_root.left
    self.right = grandson
    new_root.left = self

    compute_height(self)
    return new_root

def rotate_left_right(self):
    """Perform left, then right rotation around given node."""
    child = self.left
    new_root = child.right
    grand1  = new_root.left
    grand2  = new_root.right
    child.right = grand1
    self.left = grand2

    new_root.left = child
    new_root.right = self

    compute_height(child)
    compute_height(self)
    return new_root

def rotate_right_left(self):
    """Perform right, then left rotation around given node."""
    child = self.right
    new_root = child.left
    grand1  = new_root.left
    grand2  = new_root.right
    child.left = grand2
    self.right = grand1

    new_root.left = self
    new_root.right = child

    compute_height(child)
    compute_height(self)
    return new_root
