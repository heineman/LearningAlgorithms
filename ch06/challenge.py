"""
Randomly generate n values uniformly and insert into a non-balancing BST.
When the BST hits depth K what is the value of (a) the root; (b) and N
"""
import random

class BinaryNode:
    """
    To count rotations, have to recreate local BinaryNode class
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

rotations = [0]
def rotate_right(node):
    """Perform right rotation around given node. Update Counts of rotation."""
    rotations[0] += 1
    new_root = node.left
    grandson = new_root.right
    node.left = grandson
    new_root.right = node

    node.compute_height()
    return new_root

def rotate_left(node):
    """Perform left rotation around given node. Update Counts of rotation."""
    rotations[0] += 1
    new_root = node.right
    grandson = new_root.left
    node.right = grandson
    new_root.left = node

    node.compute_height()
    return new_root

def rotate_left_right(node):
    """Perform left, then right rotation around given node. Update Counts of rotation."""
    rotations[0] += 1
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
    """Perform right, then left rotation around given node. Update Counts of rotation."""
    rotations[0] += 1
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

def resolve_right_leaning(node):
    """If node is right-leaning, rebalance and return new root node for subtree."""
    if node.height_difference() == -2:
        if node.right.height_difference() <= 0:
            node = rotate_left(node)
        else:
            node = rotate_right_left(node)
    return node

def resolve_left_leaning(node):
    """If node is right-leaning, rebalance and return new root node for subtree."""
    if node.height_difference() == 2:
        if node.left.height_difference() >= 0:
            node = rotate_right(node)
        else:
            node = rotate_left_right(node)
    return node

class BinaryTree:
    """
    A Binary tree contains the root node, and methods to manipulate the tree.
    Recreated here so we can count rotations
    """
    def __init__(self):
        self.root = None

    def _remove_min(self, node):
        """
        Delete minimum value from subtree rooted at node.
        Have to make sure to compute_height on all affected ancestral nodes.
        """
        if node.left is None:
            return node.right

        node.left = self._remove_min(node.left)

        # Might have made right-leaning, since deleted from left. Deal with it
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

            # Might have made left-leaning. Deal with it
            node = resolve_left_leaning(node)

        node.compute_height()
        return node

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

def height_tree(n):
    """Recursive method to find height of binary node."""
    if n is None:
        return 0

    return 1 + max(height_tree(n.left), height_tree(n.right))

def one_run(k, bt):
    """Add random values to binary tree until height exceeds k."""
    while height_tree(bt.root) <= k:
        bt.add(random.random())

    return (bt.root.value, bt.size())

def produce_height_stats_balanced(k, trials):
    """Generate table showing heights of random AVL binary trees for number of trials."""
    from ch06.balanced import BinaryTree
    for _ in range(trials):
        (run, n) = one_run(k, BinaryTree())
        print('{}\t{}\t{}'.format(k, run, n))

def produce_height_stats_balanced_integers():
    """Generate statistics on smallest N such that AVL binary search trees increases in height."""
    from ch06.balanced import BinaryTree
    for k in range(30):
        bt = BinaryTree()
        idx = 0
        while height_tree(bt.root) <= k:
            bt.insert(idx)
            idx += 1
        print('{}\t{}\t{}'.format(k, bt.root.value, idx))

def produce_table():
    """Generate table showing heights of random non-balancing binary trees for T total."""
    from ch06.tree import BinaryTree
    for k in range(15):
        (run, n) = one_run(k, BinaryTree())
        print(k, run, n)

def worst_heights():
    """Generate random AVL trees of height to see which ones have worst heights."""
    from ch06.balanced import BinaryTree

    max_height = -1
    for n in range(1,50):
        for _ in range(10000):
            avl = BinaryTree()
            for _ in range(n):
                avl.insert(random.random())
            if avl.root.height > max_height:
                max_height = avl.root.height
                print(n, max_height)

def tree_structure(n):
    """Return structure of binary tree using parentheses to show nodes with left/right subtrees."""
    if n is None:
        return ''

    return '({},{},{})'.format(n.value, tree_structure(n.left), tree_structure(n.right))

def recreate_tree(expr):
    """
    Recreates Binary Tree from the expression string which was generated by tree_structure().

    Input might look like this: (19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))
    """
    from ch06.tree import BinaryNode
    if expr == ',':
        return None

    # Go to comma
    comma = expr.index(',')
    val = expr[1:comma]
    if expr[comma:] == ',,)':
        return BinaryNode(val)

    level = 0
    for idx in range(comma+1, len(expr)):
        ch = expr[idx]
        if idx == 0:  # skip opening parentheses
            continue
        if ch == '(':
            level += 1
        if ch == ')':
            level -= 1
        if level == 0:
            break

    left = recreate_tree(expr[comma+1:idx+1])
    start = idx+1
    if expr[start] == ',':    # skip comma
        start += 1

    # skip closing parentheses
    for idx in range(start, len(expr)):
        ch = expr[idx]
        if ch == '(':
            level += 1
        if ch == ')':
            level -= 1
        if level == 0:
            break
    right = recreate_tree(expr[start:-1])

    n = BinaryNode(val)
    n.left = left
    n.right = right
    return n

def find_multiple_rotations():
    """Find the smallest binary-tree that requires multiple rotations upon insert."""
    from ch06.avl import check_avl_property
    

    # Single rotation on remove with four nodes
    # for n=4, found (3,(1,,(3,,)),(3,,)) when removing 3
    #
    # Double rotations on remove?
    # for n=12, found (4,(3,(1,(0,,),(1,,(3,,))),(3,,(4,,))),(9,(6,,(7,,)),(11,,))) when removing 9
    # But I never got it to find a double-rotation on 11
    #
    # Triple rotations on remove?
    # for n=33, found (11,(5,(1,(0,(0,(0,,),),(1,,)),(4,,(5,,))),(7,(6,,),(9,,(10,,)))),(19,(15,(12,(12,,),(13,(13,,),)),(17,,(19,,))),(24,(22,(22,(21,,),),(24,,)),(29,(28,(28,,),),(32,(31,,),(33,(33,,),)))))) when removing 5
    #
    # Four rotations on remove? too computationally expensive, but these
    # numbers (4, 12, 33) suggest a relationship with Fibonacci numbers...
    # Might be related to https://oeis.org/A027941
    random.seed(11)
    for n in range(88,89):
        print('trying {}'.format(n))
        for _ in range(1000000):
            bt1 = BinaryTree()
            keys = []
            for _ in range(n):
                k = random.randint(0,n)
                keys.append(k)
                bt1.insert(k)

            check_avl_property(bt1.root)
            s = tree_structure(bt1.root)
            num_rotations = rotations[0]
            to_delete = random.choice(keys)
            bt1.remove(to_delete)
            check_avl_property(bt1.root)
            if rotations[0] > num_rotations + 3:
                print('for n={}, found {} when removing {}'.format(n, s, to_delete))
                return

    print('{} total rotations encountered: none multiple'.format(rotations[0]))

def speaking_tree():
    """Generate strings representing insert behavior in Binary Tree."""
    from ch06.speaking import BinaryTree
    bt = BinaryTree()

    # Table 6-2
    print(bt.insert(19))
    print(bt.insert(14))
    print(bt.insert(15))
    print(bt.insert(53))
    print(bt.insert(58))
    print(bt.insert(3))
    print(bt.insert(26))
    print(tree_structure(bt.root))

    # Figure 6-4
    print(bt.insert(29))

    # Figure 6-5
    bt = BinaryTree()
    bt.insert(5)
    bt.insert(4)
    bt.insert(6)
    bt.insert(2)
    bt.insert(7)
    bt.insert(1)
    bt.insert(3)
    print(tree_structure(bt.root))
    
def fibonacci_avl(N, lo=1):
    """
    Return root node of an AVL tree corresponding to Fibonacci AVL using Fn as root. 
    Use challenge AVL tree to be able to count # rotations after inserting 0, which
    should force most rotations. Note that this node must be hacked into a BinaryTree.    
    """
    from ch05.challenge import fib
    
    if N < 2:
        return None
    
    if N == 2:
        return BinaryNode(lo)
    
    val = fib(N)
    n = BinaryNode(lo+val-1)
    n.left = fibonacci_avl(N-1, lo)
    n.right = fibonacci_avl(N-2, lo+fib(N))
    n.compute_height()
    return n

def fibonacci_avl_tree(N):
    """Return AVL tree for Fibonacci AVL Binary Tree."""
    tree = BinaryTree()
    tree.root = fibonacci_avl(N)
    return tree

#######################################################################
if __name__ == '__main__':
    n = fibonacci_avl(7)
    bt = BinaryTree()
    bt.root = n
    print('rotations=',rotations[0])
    print(tree_structure(n))
    bt.insert(0)
    print('rotations=',rotations[0])
    print(tree_structure(n))
    
    #find_multiple_rotations()

    bt2 = recreate_tree('(19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))')
    print(tree_structure(bt2))
    produce_height_stats_balanced_integers()
    speaking_tree()

    speaking_tree()
    worst_heights()
