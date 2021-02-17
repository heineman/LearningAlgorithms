"""
Data Structure for non-balancing Binary Search Tree.

The tree can contain duplicate values.
"""
from ch06.binary_size import binary_node_size

class BinaryNode:
    """
    Node structure to use in a binary tree.
    
    Attributes
    ----------
        left - left child (or None)
        right - right child (or None)
        N - number of nodes in the subtree rooted at node
    """
    def __init__(self, val, n=1):
        self.value = val
        self.left  = None
        self.right = None
        self.N = n

    def __str__(self):
        return str(self.value)

    def add(self, val):
        """Adds a new BinaryNode to the tree containing this value."""
        if val <= self.value:
            if self.left:
                self.left.add(val)
            else:
                self.left = BinaryNode(val)
        else:
            if self.right:
                self.right.add(val)
            else:
                self.right = BinaryNode(val)
                
        self.N = 1 + binary_node_size(self.left) + binary_node_size(self.right)

    def remove(self, val):
        """Remove val from self in BinaryTree and return resulting sub-tree."""
        if val < self.value:
            if self.left:
                self.left = self.left.remove(val)
        elif val > self.value:
            if self.right:
                self.right = self.right.remove(val)
        else:
            if self.left is None:
                return self.right
            if self.right is None:
                return self.left

            # find LARGEST child in left subtree and remove it
            child = self.left
            while child.right:
                child = child.right

            # replace self value with largest value from left subtree
            child_value = child.value
            self.left = self.left.remove(child_value)
            self.value = child_value

        self.N = 1 + binary_node_size(self.left) + binary_node_size(self.right)
        return self

    def inorder(self):
        """In order traversal generator of tree rooted at given node."""
        # visit every one in the left subtree first
        if self.left:
            for v in self.left.inorder():
                yield v

        # then visit self
        yield self.value

        # finally visit every one in the right subtree
        if self.right:
            for v in self.right.inorder():
                yield v

class BinaryTree:
    """
    A Binary tree contains the root node, and methods to manipulate the tree.
    """
    def __init__(self):
        self.root = None

    def add(self, val):
        """Insert value into Binary Tree."""
        if self.root is None:
            self.root = BinaryNode(val)
        else:
            self.root.add(val)
            
    def size(self):
        """Return the number of nodes in Binary Tree."""
        return binary_node_size(self.root)

    def remove(self, value):
        """Remove value from tree."""
        if self.root:
            self.root = self.root.remove(value)

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
        if self.root:
            for val in self.root.inorder():
                yield val

    def __str__(self):
        if self.root:
            return str(self.root)
