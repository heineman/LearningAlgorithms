"""
Priority Queue implementation using Symbol Tree Binary Tree implementation.

Cannot use symbol table implementation "as is" because there may be multiple
values with the same priority.

"""
from ch06.avl import rotate_left, rotate_left_right, rotate_right, rotate_right_left
from ch06.avl import height_difference, compute_height

from ch06.binary_size import binary_node_size

class BinaryNode:
    """
    Node structure to use in a binary tree.
    """
    def __init__(self, k, v, n=1):
        self.key = k
        self.value = v
        self.left = None
        self.right = None
        self.height = 0
        self.N = n

    def __str__(self):
        return '{} -> {}'.format(self.key, self.value)

    def add(self, k, v):
        """Adds a new BinaryNode to the tree containing this (k, v) pair."""
        new_root = self

        if k <= self.key:
            if self.left:
                self.left = self.left.add(k, v)
            else:
                self.left = BinaryNode(k, v)

            if self.height_difference() == 2:
                if k <= self.left.key:
                    new_root = rotate_right(self)
                else:
                    new_root = rotate_left_right(self)
        else:
            if self.right:
                self.right = self.right.add(k, v)
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

            if self.height_difference() == -2:
                if self.right.height_difference() <= 0:
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
        return BinaryNode.size(self.root)

    def put(self, k, v):
        """Insert (k,v) into Binary Tree."""
        if self.root is None:
            self.root = BinaryNode(k, v)
        else:
            self.root = self.root.add(k, v)

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

class PQ:
    """
    Binary Tree storage for a MAX priority queue.
    """
    def __init__(self):
        self.tree = BinaryTree()
        self.N = 0

    def __len__(self):
        """Return number of values in priority queue."""
        return self.N

    def is_empty(self):
        """Returns whether priority queue is empty."""
        return self.N == 0

    def is_full(self):
        """Priority queue using a Binary Tree is never full."""
        return False

    def enqueue(self, v, p):
        """Enqueue (v, p) entry into priority queue."""
        self.N += 1
        self.tree.put(p, v)

    def peek(self):
        """Return the value at the top of the priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        return self.tree.root.value

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        # Find the maximum
        node = self.tree.root
        if node:
            if node.right:
                while node.right:
                    node = node.right

        val = node.value
        self.tree.remove(node.key)
        self.N -= 1
        return val

    def __iter__(self):
        """In order traversal of elements in the PQ."""
        if self.tree:
            for pair in self.tree:
                yield pair

#######################################################################
if __name__ == '__main__':
    pq = PQ()

    pq.enqueue('apple', 5)
    pq.enqueue('ball', 8)
    print(pq.dequeue())
    pq.enqueue('alternate', 5)
    pq.enqueue('car', 11)
    pq.enqueue('desk', 7)
    print(pq.dequeue())
    print(pq.dequeue())
    print(pq.dequeue())
    print(pq.dequeue())
