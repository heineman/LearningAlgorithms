"""
Data Structure for non-balancing Binary Search Tree.

The tree can contain duplicate values.
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

    def size(self):
        """Return number of nodes in subtree rooted at node."""
        ct = 1
        if self.left:  ct += self.left.size() 
        if self.right: ct += self.right.size() 
        return ct

class BinaryTree:
    """
    A Binary tree contains the root node, and methods to manipulate the tree.
    """
    def __init__(self):
        self.root = None

    def is_empty(self):
        """Returns whether tree is empty."""
        return self.root is None

    def insert(self, val):
        """Insert value into Binary Tree."""
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        """Inserts a new BinaryNode to the tree containing this value."""
        if node is None:
            return BinaryNode(val)

        if val <= node.value:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return node

    def min(self):
        """Return minimum value in tree without causing any changes."""
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.value

    def _remove_min(self, node):
        """Delete minimum value from subtree rooted at node."""
        if node.left is None:
            return node.right

        node.left = self._remove_min(node.left)
        return node

    def remove(self, val):
        """Remove value from tree."""
        self.root = self._remove(self.root, val)

    def _remove(self, node, val):
        """Remove val from subtree rooted at node and return resulting subtree."""
        if node is None:
            return None

        if val < node.value:
            node.left = self._remove(node.left, val)
        elif val > node.value:
            node.right = self._remove(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # replace self value with largest value from left subtree
            original = node

            # find SMALLEST child in right subtree and remove it
            node = node.right
            while node.left:
                node = node.left

            node.right = self._remove_min(original.right)
            node.left = original.left

        return node

    def __contains__(self, target):
        """Check whether BST contains target value."""
        node = self.root
        while node:
            if target == node.value:
                return True
            if target < node.value:
                node = node.left
            else:
                node = node.right

        return False

    def __iter__(self):
        """In order traversal of elements in the tree."""
        for v in self._inorder(self.root):
            yield v

    def _inorder(self, node):
        """Inorder traversal of tree."""
        if node is None:
            return

        for v in self._inorder(node.left):
            yield v

        yield node.value

        for v in self._inorder(node.right):
            yield v
