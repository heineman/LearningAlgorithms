"""
Helper functions to support AVL re-balancing.

These depend on having a binary tree structure with a
compute_height() method to maintain height information.
"""

def rotate_right(node):
    """Perform right rotation around given node."""
    new_root = node.left
    grandson = new_root.right
    node.left = grandson
    new_root.right = node

    node.compute_height()
    return new_root

def rotate_left(node):
    """Perform left rotation around given node."""
    new_root = node.right
    grandson = new_root.left
    node.right = grandson
    new_root.left = node

    node.compute_height()
    return new_root

def rotate_left_right(node):
    """Perform left, then right rotation around given node."""
    child = node.left
    new_root = child.right
    grand1  = new_root.left
    grand2  = new_root.right
    child.right = grand1
    node.left = grand2

    new_root.left = child
    new_root.right = node

    child.compute_height()
    node.compute_height()
    return new_root

def rotate_right_left(node):
    """Perform right, then left rotation around given node."""
    child = node.right
    new_root = child.left
    grand1  = new_root.left
    grand2  = new_root.right
    child.left = grand2
    node.right = grand1

    new_root.left = node
    new_root.right = child

    child.compute_height()
    node.compute_height()
    return new_root

def resolve_left_leaning(node):
    """If node is right-leaning, rebalance and return new root node for subtree."""
    if node.height_difference() == 2:
        if node.left.height_difference() >= 0:
            node = rotate_right(node)
        else:
            node = rotate_left_right(node)
    return node

def resolve_right_leaning(node):
    """If node is right-leaning, rebalance and return new root node for subtree."""
    if node.height_difference() == -2:
        if node.right.height_difference() <= 0:
            node = rotate_left(node)
        else:
            node = rotate_right_left(node)
    return node

def check_avl_property(n):
    """
    Validates that the height for each node in the tree rooted at 'n' is correct, and that
    the AVL property regarding height difference is correct. This is a helpful debugging tool.
    """
    if n is None:
        return -1

    left_height = check_avl_property(n.left)
    right_height = check_avl_property(n.right)

    if n.height != 1 + max(left_height, right_height):
        raise ValueError('AVL height incorrect at {}'.format(n.value))

    if left_height - right_height < -1 or left_height - right_height > 1:
        raise ValueError('AVL tree property invalidated at {}'.format(n.value))

    return n.height
