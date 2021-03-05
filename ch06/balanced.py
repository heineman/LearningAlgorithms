"""
Data Structure for self-balancing AVL Binary Search Tree.

The tree can contain duplicate values.
"""
from ch06.avl import resolve_left_leaning, resolve_right_leaning

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
        self.height = 0

    def height_difference(self):
        """
        Compute height difference of node's children in BST. Can return
        a negative number or positive number.
        """
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height

    def compute_height(self):
        """Compute height of node in BST."""
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)

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
            node = resolve_left_leaning(node)
        else:
            node.right = self._insert(node.right, val)
            node = resolve_right_leaning(node)

        node.compute_height()
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
        """
        Delete minimum value from subtree rooted at node.
        Have to make sure to compute_height on all affected ancestral nodes.
        """
        if node.left is None:
            return node.right

        # Might have made right-leaning, since deleted from left. Deal with it
        node.left = self._remove_min(node.left)
        node = resolve_right_leaning(node)
        node.compute_height()
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
            node = resolve_right_leaning(node)
        elif val > node.value:
            node.right = self._remove(node.right, val)
            node = resolve_left_leaning(node)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # replace self value with node containing smallest value from right subtree
            original = node

            # find SMALLEST child in right subtree and remove it
            node = node.right
            while node.left:
                node = node.left

            node.right = self._remove_min(original.right)
            node.left = original.left

            # Might have made left-leaning by shrinking right side
            node = resolve_left_leaning(node)

        node.compute_height()
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
