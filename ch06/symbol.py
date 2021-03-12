"""
Data Structure for non-balancing Binary Search Tree.

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
        height - height of the node
        key - key for (key, value) pair
        value - value for (key, value) pair
    """
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.left = None
        self.right = None
        self.height = 0

    def __str__(self):
        return '{} -> {} [{}]'.format(self.key, self.value, self.height)

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

    def put(self, k, v):
        """
        Adds a new BinaryNode to the tree containing this value or update
        association of (k, v). Key cannot be None.
        """
        if k is None:
            raise ValueError('key for symbol table cannot be None.')
        self.root = self._put(self.root, k, v)

    def _put(self, node, k, v):
        """
        Adds a new BinaryNode to the subtree rooted at node or update
        association of (k, v).
        """
        if node is None:
            return BinaryNode(k,v)

        if k == node.key:
            node.value = v
            return node

        if k < node.key:
            node.left = self._put(node.left, k, v)
            node = resolve_left_leaning(node)
        else:
            node.right = self._put(node.right, k, v)
            node = resolve_right_leaning(node)

        node.compute_height()
        return node

    def remove(self, key):
        """Remove (key, val) from self in BinaryTree and return self."""
        self.root = self._remove(self.root, key)

    def _remove_min(self, node):
        """
        Delete minimum value from subtree rooted at node.
        Have to make sure to compute_height on all affected ancestral nodes.
        """
        if node.left is None:
            return node.right

        node.left = self._remove_min(node.left)
        node.compute_height()
        return node

    def _remove(self, node, key):
        """Remove (key,value) from subtree rooted at node and return resulting subtree."""
        if node is None:
            return None

        if key < node.key:
            node.left = self._remove(node.left, key)
            node = resolve_right_leaning(node)
        elif key > node.key:
            node.right = self._remove(node.right, key)
            node = resolve_left_leaning(node)
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

            node = resolve_left_leaning(node)

        node.compute_height()
        return node

    def __contains__(self, key):
        """Check whether BST contains key value."""
        return not self.get(key) is None

    def get(self, key):
        """Symbol table API to retrieve value associated with key."""
        node = self.root
        while node:
            if key == node.key:
                return node.value
            if key < node.key:
                node = node.left
            else:
                node = node.right

        return None

    def __iter__(self):
        """In order traversal of elements in the tree."""
        for pair in self._inorder(self.root):
            yield pair

    def _inorder(self, node):
        """Inorder traversal of tree."""
        if node is None:
            return

        for pair in self._inorder(node.left):
            yield pair

        yield (node.key, node.value)

        for pair in self._inorder(node.right):
            yield pair
