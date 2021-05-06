"""
Challenge Exercises for Chapter 6.

Randomly generate n values uniformly and insert into a non-balancing BST.
When the BST hits depth K what is the value of (a) the root; (b) and N
"""
import random
from ch06.avl import check_avl_property
from algs.table import DataTable, ExerciseNum, caption
from pandas.util.testing import _network_errno_vals

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

    def size(self):
        """Return number of nodes in subtree rooted at node."""
        ct = 1
        if self.left:  ct += self.left.size()
        if self.right: ct += self.right.size()
        return ct

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

    def max_value(self):
        """Return largest value. Useful for test cases."""
        node = self.root
        if node is None:
            return None

        while node.right:
            node = node.right

        return node.value

    def min_value(self):
        """Return smallest value. Useful for test cases."""
        node = self.root
        if node is None:
            return None

        while node.left:
            node = node.left

        return node.value

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
        bt.insert(random.random())

    return (bt.root.value, bt.root.size())

def produce_height_stats_balanced_integers(max_k=13, output=True):
    """
    Generate statistics on smallest N such that AVL binary search trees increases
    in height, up to (but not including) max_k.
    """
    from ch06.balanced import BinaryTree

    tbl = DataTable([8,10,10],['N', 'height', 'rootValue'], output=output)
    tbl.format('height', 'd')
    tbl.format('rootValue', ',d')
    for k in range(max_k):
        bt = BinaryTree()
        idx = 0
        while height_tree(bt.root) <= k:
            bt.insert(idx)
            idx += 1
        tbl.row([idx, k, bt.root.value])

    return tbl

def produce_table(max_k=15, output=True):
    """
    Generate table with values of k for which a random binary tree with n nodes
    has a height that exceeds k, up to (but not including) heights of max_k.
    """
    from ch06.tree import BinaryTree

    tbl = DataTable([8,10,10], ['Height', 'RootValue', 'N'], output=output, decimals=4)
    tbl.format('N', 'd')
    for k in range(max_k):
        (run, n) = one_run(k, BinaryTree())
        tbl.row([k, run, n])
    return tbl

def worst_heights(max_n=40, output=True):
    """
    Generate random AVL trees of n Nodes to find which ones have greatest height.
    Purely speculative and not definitive exploration of potential trees.
    """
    from ch06.balanced import BinaryTree
    tbl = DataTable([8,8,8],['N', 'WorstHeight', 'NumberFound'], output=output)
    tbl.format('WorstHeight', 'd')
    tbl.format('NumberFound', ',d')
    table_max_height = -1
    for n in range(1,max_n):
        number_found = 0
        max_height = -1
        for _ in range(10001):
            avl = BinaryTree()
            for _ in range(n):
                avl.insert(random.random())
            if avl.root.height > max_height:
                max_height = avl.root.height
                number_found = 0
            elif avl.root.height == max_height:
                number_found += 1

        if max_height > table_max_height:
            tbl.row([n, max_height, number_found])
            table_max_height = max_height
    return tbl

def tree_structure(n):
    """Return structure of binary tree using parentheses to show nodes with left/right subtrees."""
    if n is None:
        return ''

    return '({},{},{})'.format(n.value, tree_structure(n.left), tree_structure(n.right))

def extract(s, start):
    """Given a string and index position to the first '(', extract a full group up to its ')'."""
    level = 1
    for idx in range(start+1, len(s)):
        ch = s[idx]
        if ch == '(':
            level += 1
        if ch == ')':
            level -= 1
        if level == 0:
            return s[start:idx+1]

    # should never get here
    raise ValueError('ill-formed string: {}'.format(s))

def recreate_tree(expr, convert=lambda x: x):
    """
    Recreates Binary Tree from the expression string which was generated by tree_structure().

    Input might look like this: (19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))

    Convert function takes string and reproduces actual value. Use to convert str into numeric
    values.
    """
    # Base case
    if expr[0] == '(' and expr[-1] == ')' and not '(' in expr[1:-1]:
        # (Root, Left-Value, Right-Value)
        elements = expr[1:-1].split(',')
        node = BinaryNode(convert(elements[0]))
        node.left = BinaryNode(convert(elements[1])) if elements[1] else None
        node.right = BinaryNode(convert(elements[2])) if elements[2] else None
        node.compute_height()
        return node

    # More complicated structures... Could either be (Val,(....),(....)) or
    # just (Val, (....),Val) or (Val,Val,(.....))
    comma1 = expr.index(',')
    root_value = expr[1:comma1]
    if expr[comma1+1] == '(':
        # Now we now LEFT needs to be extracted as a group
        subgroup = extract(expr,comma1+1)
        left = recreate_tree(subgroup, convert)
        comma2 = comma1+len(subgroup)+1
        if expr[comma2+1] == '(':
            subgroup = extract(expr,comma2+1)
            right = recreate_tree(subgroup, convert)
        else:
            entry = expr[comma2+1:-1]
            right = BinaryNode(convert(entry)) if entry else None
    else:
        # Left side is a value
        comma2 = expr.index(',', comma1+1)
        left = BinaryNode(expr[comma1+1:comma2]) if comma1+1 < comma2 else None

        if expr[comma2+1] == '(':
            # Right side need to be extracted as a group
            subgroup = extract(expr,comma2+1)
            right = recreate_tree(subgroup, convert)
        else:
            # I have yet to find a case that requires this statement. Might not be necessary?
            right = BinaryNode(convert(expr[comma2+1:-1]))

    node = BinaryNode(convert(root_value))
    node.left = left
    node.right = right
    node.compute_height()
    return node

def find_multiple_rotations(extra, lo=2, hi=1000, num_attempts=100000, output=True):
    """Find the smallest binary-tree that requires extra rotations upon insert."""

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
    for n in range(lo, hi):
        if output:
            print('trying {}'.format(n))
        for _ in range(num_attempts):
            bt1 = BinaryTree()
            keys = []
            for _ in range(n):
                k = random.randint(0,n)
                keys.append(k)
                bt1.insert(k)

            check_avl_property(bt1.root)
            s = tree_structure(bt1.root)

            # Try to force max # of rotations on deletion...
            num_rotations = rotations[0]
            to_delete = random.choice(keys)
            bt1.remove(to_delete)
            check_avl_property(bt1.root)
            if rotations[0] > num_rotations + extra:
                if output:
                    print('for extra={} and after n={} tries, found {} when removing {}'.format(extra, n, s, to_delete))
                return (s, to_delete)

    if output:
        print('{} total rotations encountered: none in [{}, {}] with extra={}'.format(rotations[0], lo, hi, extra))
    return (None, None)

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

def fibonacci_avl_tree_up_to_2k(N):
    """
    Return AVL tree for Fibonacci AVL Binary Tree that was extended to add
    nodes up to 2*height-1, which simulates, in a way, an attempt to structurally
    recreate a complete tree. Resulting heights are just one greater than what
    you would have in a completed tree, with |Left| + |Right-Grandchild| = |left-child-of-Right|
    """
    from ch05.challenge import fib
    tree = BinaryTree()
    tree.root = fibonacci_avl(N)

    for i in range(fib(N+1), 2**(tree.root.height+1)):     # up to a complete tree...
        tree.insert(i)

    check_avl_property(tree.root)
    return tree

def count(n, target):
    """Count # of times non-None target exists in linked list, n."""
    ct = 0
    if n is None:
        return 0
    if n.value == target:
        ct = 1
    return ct + count(n.next, target)

class RankBinaryNode:
    """
    Demonstration of challenge exercise
    """
    def __init__(self, key):
        self.key = key
        self.left  = None
        self.right = None
        self.N = 1
        self.height = 0

class RankBinaryTree:
    """
    Demonstration of challenge exercise. Only supports insert
    """
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        """Insert value into Binary Tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Inserts a new BinaryNode to the tree containing this key."""
        if node is None:
            return RankBinaryNode(key)

        if key <= node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.N = 1
        ht = -1
        if node.left:  
            node.N += node.left.N
            ht = max(ht, node.left.height)
        if node.right: 
            node.N += node.right.N
            ht = max(ht, node.right.height)
        node.height = ht + 1
        return node

    def _count(self, node):
        """Return count of the nodes in the subtree rooted at node or 0 if None."""
        return 0 if node is None else node.N

    def select(self, k):
        """Return kth smallest value in the tree."""
        return self._select(self.root, k)

    def _select(self, node, k):
        if node is None:
            return None
        leftN = self._count(node.left)

        if leftN > k:
            return self._select(node.left, k)
        if leftN < k:
            return self._select(node.right, k - leftN - 1)
        return node.key

    def rank(self, key):
        """Return rank (or -1 if it doesn't exist) of key in the tree. min() = 0"""
        return self._rank(self.root, key)

    def _rank(self, node, key):
        if node is None:
            return 0

        if key == node.key:
            return self._count(node.left)
        if key < node.key:
            return self._rank(node.left, key)
        return 1 + self._count(node.left) + self._rank(node.right, key)

def manually_build(vals, height):
    """
    Manually produce permutations of vals to build tree. Count how many have given height.
    Only call with vals <= 7, since 15 requires 1,307,674,368,000 possible arrangements.
    """
    import itertools
    count = 0
    for val in itertools.permutations(vals):
        rbt = RankBinaryTree()
        for v in val:
            rbt.insert(v)
        if rbt.root.height == height:
            count += 1
    return count

def compute_perfect_tree(total):
    """
    Determine # of ways complete tree would be constructed from 2^k - 1 values.
    Still waiting for confirmation.
    """
    import math
    if total == 1:
        return 1
    half = total // 2
    return (math.factorial(2*half) / (2 * math.factorial(half))) * 2*compute_perfect_tree(half)

#######################################################################
if __name__ == '__main__':
    chapter = 6

    with ExerciseNum(1) as exercise_number:
        print('find count() in ch05.challenge')
        print(caption(chapter, exercise_number), 'Recursive count method')
        print()

    with ExerciseNum(2) as exercise_number:
        print('A binary tree that only has right children.')
        print(caption(chapter, exercise_number), 'What binary tree has O(N) to find two largest?')
        print()

    with ExerciseNum(3) as exercise_number:
        print('RankBinaryTree in ch06.challenge')
        print(caption(chapter, exercise_number), 'select() and rank() methods')
        print()

    with ExerciseNum(4) as exercise_number:
        compute_perfect_tree(3)
        print(caption(chapter, exercise_number), 'select() and rank() methods')
        print()

    worst_heights()

    #find_multiple_rotations()
    bt2 = recreate_tree('(19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))')
    #print(tree_structure(bt2))
    #produce_height_stats_balanced_integers()
