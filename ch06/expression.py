"""
Use Binary Tree structure to represent binary expressions.
"""
import re

class Value:
    """
    Represents a Value in an Expression tree, containing a numeric value.

    Has default eval, __str_() methods and supports converting into postfix.
    """
    def __init__(self, e):
        self.value = e

    def __str__(self):
        return str(self.value)

    def eval(self):
        """To evaluate a value, report its value."""
        return self.value

    def references(self):
        """A Value has no references."""
        yield None

    def postfix(self):
        """A value as postfix is itself."""
        yield self.value

class Reference:
    """
    Represents a Value in an Expression tree, containing a reference to a value.

    Has default eval, __str_() methods and supports converting into postfix.
    """
    def __init__(self, e, environment=None):
        self.reference = e
        self.environment = {} if environment is None else environment

    def __str__(self):
        return str(self.reference)

    def eval(self):
        """To evaluate a reference, report its value from the environment (or 0 if not found)."""
        try:
            return self.environment[self.reference]
        except KeyError:
            return 0

    def references(self):
        """Yield this reference."""
        yield self.reference

    def postfix(self):
        """A reference as postfix is itself."""
        yield self.reference

class Expression:
    """
    Node structure to use in a binary expression tree.

    Attributes
    ----------
        left - left child (or None)
        right - right child (or None)
        element - A function to perform a binary operation
    """
    def __init__(self, func, left, right):
        self.left  = left
        self.right = right
        self.func = func

    def __str__(self):
        return '({} {} {})'.format(
                self.left,
                self.func.__doc__,
                self.right)

    def eval(self):
        """Evaluate expression."""
        return self.func(self.left.eval(),
                         self.right.eval())

    def references(self):
        """Return generator for all references, if any exist."""
        for v in self.left.references():
            if v:
                yield v

        for v in self.right.references():
            if v:
                yield v

    def postfix(self):
        """Return generator containing postfix representation of expression."""
        for v in self.left.postfix():
            yield v

        for v in self.right.postfix():
            yield v

        yield self.func.__doc__

# Pre-loaded operations
def add(left, right):
    """+"""
    return left + right

def mult(left, right):
    """*"""
    return left * right

def divide(left, right):
    """/"""
    return left / right

def sub(left, right):
    """-"""
    return left - right

# Built in operators here.
_operators = { '+' : add, '-' : sub, '*' : mult, '/' : divide }

def build_expression(s, new_operators=None, environment=None):
    """
    Given a string consisting of numeric values, parentheses and
    mathematical operators, return Expression tree using a stack-based
    algorithm developed by Dijkstra. To parse new operations, simply
    pass them in as a dict where key is the symbol for the new operator and
    its value is a function that takes in two arguments (left, right) for
    the operands to the binary function.
    """

    # Match open- and close- parens, any sequence of digits, and
    # known operators, using backslash notation. Limited to only special characters
    # but still quite nice...
    known_operators = {}
    for op in _operators:
        known_operators[op] = _operators[op]

    if new_operators:
        for op in new_operators:
            if op in _operators:
                raise ValueError('Attempting to overwrite existing operator: {}'.format(op))

            known_operators[op] = new_operators[op]

    # In Python 3.3, this regular expression generates a Deprecation Warning and yields a unit
    # test failure in test_baseline_expression for the "^" operator representing exponentiation
    pattern = re.compile('(\(|\)|[a-zA-Z.0-9_]+|[{}])'.format('\\'.join(known_operators.keys())))

    # A bit out of place, but the stack was introduced in Chapter 07
    from ch07.list_stack import Stack
    ops = Stack()
    expressions = Stack()

    for token in pattern.findall(s):
        if token in known_operators:
            ops.push(known_operators[token])            # Push each operator found for later
        elif token == '(':
            pass                       # You seriously do not need to do anything!
        elif token == ')':
            op = ops.pop()             # Close out most recent expression
            right = expressions.pop()  # Order matters...
            left = expressions.pop()   # And store it for future
            expressions.push(Expression(op, left, right))
        else:                          # If just a numeric value, push it for later
            try:
                expressions.push(Value(float(token)))
            except ValueError:
                # If it cannot be evaluated, leave untouched for post processing, perhaps?
                expressions.push(Reference(token, environment))

    return expressions.pop()           # If parens balance, then left with expression
