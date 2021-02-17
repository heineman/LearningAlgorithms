"""
Data Structure for Binary Tree to implement symbol table data type.

In a symbol table, a (k,v) entry is put into the symbol table, so the value
can be retrieved from its key. Each key in the symbol table is unique.

Apply AVL balancing technique to self-balance.
"""

from ch06.avl import rotate_left, rotate_left_right, rotate_right, rotate_right_left, height_difference, compute_height
from ch06.binary_size import binary_node_size

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
        N - number of nodes in the subtree rooted at node
    """
    def __init__(self, k, v, n=1):
        self.key = k
        self.value = v
        self.left = None
        self.right = None
        self.height = 0
        self.N = n

    def __str__(self):
        return '{} -> {} [{}]'.format(self.key, self.value, self.height)

    def put(self, k, v): 
        """
        Adds a new BinaryNode to the tree containing this value or update
        association of (k, v).
        """
        new_root = self
        if k == self.key:
            self.value = v
            return self

        if k < self.key:
            if self.left:
                self.left = self.left.put(k, v)
            else:
                self.left = BinaryNode(k, v)

            if height_difference(self) == 2:
                if k < self.left.key:
                    new_root = rotate_right(self)
                else:
                    new_root = rotate_left_right(self)
        else:
            if self.right:
                self.right = self.right.put(k, v)
            else:
                self.right = BinaryNode(k, v)

            if height_difference(self) == -2:
                if k > self.right.key:
                    new_root = rotate_left(self)
                else:
                    new_root = rotate_right_left(self)

        compute_height(new_root)
        new_root.N = 1 + binary_node_size(new_root.left) + binary_node_size(new_root.right)
        return new_root

    def remove(self, key):
        """Remove (key, val) from self in BinaryTree and return self."""
        new_root = self

        if key < self.key:
            if self.left:
                self.left = self.left.remove(key)
            if height_difference(self) == -2:
                if height_difference(self.right) <= 0:
                    new_root = rotate_left(self)
                else:
                    new_root = rotate_right_left(self)
        elif key > self.key:
            if self.right:
                self.right = self.right.remove(key)
            if height_difference(self) == 2:
                if height_difference(self.left) >= 0:
                    new_root = rotate_right(self)
                else:
                    new_root = rotate_left_right(self)
        else:
            if self.left is None:
                return self.right
            if self.right is None:
                return self.left

            child = self.left
            while child.right:
                child = child.right

            # replace root value with largest value from left subtree
            child_key,child_value = child.key, child.value
            self.left = self.left.remove(child_key)
            self.key, self.value = child_key, child_value

            if height_difference(self) == -2:
                if height_difference(self.right) <= 0:
                    new_root = rotate_left(self)
                else:
                    new_root = rotate_right_left(self)

        compute_height(new_root)
        new_root.N = 1 + binary_node_size(new_root.left) + binary_node_size(new_root.right)
        return new_root

    def inorder(self):
        """In order traversal generator of tree rooted at given node."""
        # visit every one in the left subtree first
        if self.left:
            for pair in self.left.inorder():
                yield pair

        # then visit self
        yield (self.key, self.value)

        # finally visit every one in the right subtree
        if self.right:
            for pair in self.right.inorder():
                yield pair

class BinaryTree:
    """
    A Binary tree contains the root node, and methods to manipulate the tree.
    """
    def __init__(self):
        self.root = None

    def size(self):
        """Return the number of nodes in Binary Tree."""
        return binary_node_size(self.root)

    def put(self, k, v):
        """Insert (k,v) into Binary Tree."""
        if self.root is None:
            self.root = BinaryNode(k, v)
        else:
            self.root = self.root.put(k, v)

    def remove(self, key):
        """Remove key and associated value from tree."""
        if self.root:
            self.root = self.root.remove(key)

    def __contains__(self, key):
        """Check whether BST contains key value."""
        node = self.root
        while node:
            if key == node.key:
                return True
            if key < node.key:
                node = node.left
            else:
                node = node.right

        return False

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
        if self.root:
            for pair in self.root.inorder():
                yield pair

    def __str__(self):
        if self.root:
            return str(self.root)
