"""
Provides English descriptions for operations as they happen.

Used for Table 6-2 in the book.
"""
class BinaryNode:
    """
    Node structure to use in a binary tree.

    Attributes
    ----------
        left - left child (or None)
        right - right child (or None)
    """
    def __init__(self, val):
        self.value = val
        self.left  = None
        self.right = None

class BinaryTree:
    """
    A Binary tree contains the root node, and methods to manipulate the tree.
    """
    def __init__(self):
        self.root = None

    def insert(self, val):
        """Insert value into Binary Tree."""
        (self.root,explanation) = self._insert(self.root, val, 'To insert `{}`, '.format(val))
        return explanation

    def _insert(self, node, val, sofar):
        """Inserts a new BinaryNode to the tree containing this value."""
        if node is None:
            return (BinaryNode(val), sofar + 'create a new subtree with root of `{}`.'.format(val))

        if val <= node.value:
            sofar += '`{1}` is smaller than or equal to `{0}`, so insert `{1}` into the left subtree of `{0}` '.format(node.value, val)
            if node.left is None:
                sofar += 'but there is no left subtree, so '
            else:
                sofar += 'rooted at `{}`. Now '.format(node.left.value)
            (node.left, expl) = self._insert(node.left, val, sofar)
            return (node, expl)

        sofar += '`{1}` is larger than `{0}`, so insert `{1}` into the right subtree of `{0}` '.format(node.value, val)
        if node.right is None:
            sofar += 'but there is no right subtree, so '
        else:
            sofar += 'rooted at `{}`. Now '.format(node.right.value)
        (node.right, expl) = self._insert(node.right, val, sofar)
        return (node, expl)
