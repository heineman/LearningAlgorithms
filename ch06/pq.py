"""
Priority Queue implementation using Symbol Tree Binary Tree implementation.

Cannot use symbol table implementation "as is" because there may be multiple
values with the same priority. It is for this reason that the remove() is more
complicated since you have to be careful not to lose values when there happen
to be multiple values with the same priority.

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
        value - value for (value, priority) pair
        priority - key for (value, priority) pair
    """
    def __init__(self, v, p):
        self.value = v
        self.priority = p
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

    def insert(self, v, p):
        """Insert (value, priority) entry into Binary Tree."""
        self.root = self._insert(self.root, v, p)

    def _insert(self, node, v, p):
        """Inserts a new BinaryNode to the tree containing (value, priority) pair."""
        if node is None:
            return BinaryNode(v, p)

        if p <= node.priority:
            node.left = self._insert(node.left, v, p)
            node = resolve_left_leaning(node)
        else:
            node.right = self._insert(node.right, v, p)
            node = resolve_right_leaning(node)

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
        for p in self._inorder(self.root):
            yield p

    def _inorder(self, node):
        """Inorder traversal of tree."""
        if node is None:
            return

        for pair in self._inorder(node.left):
            yield pair

        yield (node.value, node.priority)

        for pair in self._inorder(node.right):
            yield pair

class PQ:
    """
    PriorityQueue using a Binary Tree to store entries, although this stored N.
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
        """Enqueue (v, p) entry into priority queue. Priority cannot be None."""
        if p is None:
            raise ValueError('key for symbol table cannot be None.')

        self.N += 1
        self.tree.insert(v, p)

    def peek(self):
        """Return value associated with node with maximum priority in queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        node = self.tree.root
        while node.right:
            node = node.right

        return node.value

    def _remove_max(self, node):
        """
        Remove max and unwind, addressing AVL property on way back. Return 
        pair (value, new root)
        """
        if node.right is None:
            return (node.value, node.left)

        (value, node.right) = self._remove_max(node.right)
        node = resolve_left_leaning(node)
        node.compute_height()
        return (value, node)

    def dequeue(self):
        """Remove and return value with highest priority in priority queue."""
        if self.N == 0:
            raise RuntimeError('PriorityQueue is empty!')

        (value, self.tree.root) = self._remove_max(self.tree.root)
        self.N -= 1
        return value

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
