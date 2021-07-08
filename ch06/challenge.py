"""
Challenge Exercises for Chapter 6.

Randomly generate n values uniformly and insert into a non-balancing BST.
When the BST hits depth K what is the value of (a) the root; (b) and N
"""
import random
from ch06.avl import check_avl_property
from algs.table import DataTable, ExerciseNum, caption

class ObservableBinaryNode:
    """
    To count rotations, create ObservableBinaryNode class.
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

class ObservableBinaryTree:
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
        """Inserts a new ObservableBinaryNode to the tree containing this value."""
        if node is None:
            return ObservableBinaryNode(val)

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
    Resulting tree is a plain-vanilla non-balancing Binary Search Tree from ch06.tree

    Input might look like this: (19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))

    Convert function takes string and reproduces actual value. Use to convert str into numeric
    values.
    """

    # Base case
    if expr[0] == '(' and expr[-1] == ')' and not '(' in expr[1:-1]:
        # (Root, Left-Value, Right-Value)
        elements = expr[1:-1].split(',')
        node = ObservableBinaryNode(convert(elements[0]))
        node.left = ObservableBinaryNode(convert(elements[1])) if elements[1] else None
        node.right = ObservableBinaryNode(convert(elements[2])) if elements[2] else None
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
            right = ObservableBinaryNode(convert(entry)) if entry else None
    else:
        # Left side is a value
        comma2 = expr.index(',', comma1+1)
        left = ObservableBinaryNode(expr[comma1+1:comma2]) if comma1+1 < comma2 else None

        if expr[comma2+1] == '(':
            # Right side need to be extracted as a group
            subgroup = extract(expr,comma2+1)
            right = recreate_tree(subgroup, convert)
        else:
            # I have yet to find a case that requires this statement. Might not be necessary?
            right = ObservableBinaryNode(convert(expr[comma2+1:-1]))

    node = ObservableBinaryNode(convert(root_value))
    node.left = left
    node.right = right
    node.compute_height()
    return node

def trial_multiple_rotations(output=True, num_attempts=10000):
    """Some trial and error went into these ranges."""
    from ch05.challenge import fib
    tbl = DataTable([6,6,6,6],['NumRot', 'Height', 'N', 'Random Tree'], output=output)
    tbl.format('Random Tree', 's')
    tbl.format('NumRot', 'd')
    tbl.format('Height', 'd')
    tbl.format('N', 'd')

    for extra in range(3):
        (structure, _) = find_multiple_rotations(extra, lo=4, hi=40, num_attempts=num_attempts, output=False)
        n = recreate_tree(structure)

        def count_nodes(n):
            if n is None: return 0
            return 1 + count_nodes(n.left) + count_nodes(n.right)

        tbl.row([extra+1, n.height, count_nodes(n), structure])

    # Now use Fibonacci Trees to accomplish the same result.
    if output:
        print()
    tbl = DataTable([6,6,6,13],['NumRot', 'Height', 'N', 'Fib AVL Trees'], output=output)
    tbl.format('Fib AVL Trees', 's')
    tbl.format('NumRot', 'd')
    tbl.format('Height', 'd')
    tbl.format('N', 'd')
    for n in range(6,14,2):
        root = fibonacci_avl(n)
        root.compute_height()
        check_avl_property(root)             # double-check
        structure = tree_structure(root)
        bt = ObservableBinaryTree()
        height = root.height
        bt.root = root
        count = count_nodes(root)

        num_rotations = rotations[0]
        to_delete = fib(n+1)-1
        bt.remove(to_delete)
        check_avl_property(bt.root)
        num_rotations = rotations[0] - num_rotations

        tbl.row([num_rotations, height, count, structure])

    return (tbl)

def find_multiple_rotations(extra, lo=4, hi=15, num_attempts=10000, output=True):
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
            bt1 = ObservableBinaryTree()
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
    from ch06.speaking import SpeakingBinaryTree
    bt = SpeakingBinaryTree()

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
    bt = SpeakingBinaryTree()
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
        return ObservableBinaryNode(lo)

    val = fib(N)
    n = ObservableBinaryNode(lo+val-1)
    n.left = fibonacci_avl(N-1, lo)
    n.right = fibonacci_avl(N-2, lo+fib(N))
    n.compute_height()
    return n

def fibonacci_avl_tree(N):
    """Return AVL tree for Fibonacci AVL Binary Tree."""
    tree = ObservableBinaryTree()
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

    tree = ObservableBinaryTree()
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

    def contains(self, target):
        """Recursive implementation of contains. Must prevent calls on missing children."""
        if target == self.key:
            return True

        if target < self.key:
            if self.left is None:
                return False
            return self.left.contains(target)

        if self.right is None:
            return False
        return self.right.contains(target)

class RankBinaryTree:
    """
    Demonstration of challenge exercise. Only supports insert.
    Has the recursive contains() method, as well as rank() and select()
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

    def __contains__(self, target):
        """Recursive contains method."""
        if self.root is None:
            return False
        return self.root.contains(target)

def manually_build(vals, height):
    """
    Manually produce permutations of vals to build tree. Count how many have given height.
    Only call with vals <= 7, since 15 requires 1,307,674,368,000 possible arrangements.
    """
    import itertools
    ct = 0
    for val in itertools.permutations(vals):
        rbt = RankBinaryTree()
        for v in val:
            rbt.insert(v)
        if rbt.root.height == height:
            ct += 1
    return ct

def demonstrate_tree_structure():
    """compute tree_structure for a sample tree."""
    from ch06.tree import BinaryTree
    bt9 = BinaryTree()
    for i in [19, 14, 53, 3, 15, 26, 58]:
        bt9.insert(i)
    result = tree_structure(bt9.root)
    print(result)
    print(tree_structure(recreate_tree(result)))     # must be same as result
    bt10 = recreate_tree('(19,(14,(3,,),(15,,)),(53,(26,,(29,,)),(58,,)))')
    print('another one', tree_structure(bt10))

def speaking_tree_demonstration():
    """Small example of inserting three values into Speaking Tree."""
    from ch06.speaking import SpeakingBinaryTree
    bt = SpeakingBinaryTree()
    print(bt.insert(5))
    print(bt.insert(3))
    print(bt.insert(1))

def compute_perfect_tree(total):
    """
    Determine # of ways complete tree would be constructed from 2^k - 1 values.
    This is a really subtle problem to solve. One hopes for a recursive solution,
    because it is binary trees, and the surprisingly simple equation results
    from the fact that it is a complete tree. It comes down to the number of
    ways you can independently interleave the sequential values from two subsequences.
    The total of the subsequences is (total - 1), because you leave out the subtree root.
    Each of the (total // 2) half sequences are then interleaved. To properly count
    the number of possibilities, you need to multiply by the ways you can create
    subtrees of half the side (one for the left and one for the right).

    https://stackoverflow.com/questions/17119116/how-many-ways-can-you-insert-a-series-of-values-into-a-bst-to-form-a-specific-tr
    """
    import math
    if total == 1:
        return 1
    half = total // 2
    return (math.factorial(total-1) / (math.factorial(half) * math.factorial(half))) * compute_perfect_tree(half) * compute_perfect_tree(half)

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
        print(7, compute_perfect_tree(7))
        print(15, compute_perfect_tree(15))
        print(31, compute_perfect_tree(31))
        print(caption(chapter, exercise_number), 'select() and rank() methods')
        print()

    with ExerciseNum(5) as exercise_number:
        print('RankBinaryTree in ch06.challenge')
        print(caption(chapter, exercise_number), 'recursive contains() method')
        print()

    with ExerciseNum(6) as exercise_number:
        worst_heights()
        print(caption(chapter, exercise_number), 'AVL tree heights change in specific pattern')
        print()

    with ExerciseNum(7) as exercise_number:
        speaking_tree_demonstration()
        print(caption(chapter, exercise_number), 'Speaking binary tree after inserting three values')
        print()

    with ExerciseNum(8) as exercise_number:
        print('Review ch06.avl')
        print(caption(chapter, exercise_number), 'check_avl_property')
        print()

    with ExerciseNum(9) as exercise_number:
        demonstrate_tree_structure()
        print(caption(chapter, exercise_number), 'tree_structure')
        print()

    with ExerciseNum(10) as exercise_number:
        trial_multiple_rotations(num_attempts=10000)   # doesn't always find one...
        print('Experiment with different values of these parameters to explore larger deltas')
        print(caption(chapter, exercise_number), 'counting rotations upon delete.')
        print()

    with ExerciseNum(11) as exercise_number:
        print(tree_structure(fibonacci_avl(6)))
        print(caption(chapter, exercise_number), 'Fibonacci trees')
        print()
