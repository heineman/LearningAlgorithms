"""
Use Binary Tree structure to represent binary expressions.
"""
import re

class Value:
    """
    Represents a Value in an Expression treee, containing a numeric value.

    Has default eval, __str_() methods and supports converting into postfix.
    """
    def __init__(self, e):
        self.value = e

    def __str__(self):
        return str(self.value)

    def eval(self):
        """To evaluate a value, report its value."""
        return self.value

    def postfix(self):
        """A value as postfix is itself."""
        yield self.value

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

# Register operators here.
_operators = { '+' : add, '-' : sub, '*' : mult, '/' : divide }

def add_operator(op, func):
    """Add an operator to the known operators."""
    if op in _operators:
        raise ValueError("Attempting to overwrite existing operator: " + str(op))

    _operators[op] = func

from algs.node import Node
class Stack:
    """
    Implementation of a Stack using linked lists.
    """
    def __init__(self):
        self.top = None

    def is_empty(self):
        """Determine if stack is empty."""
        return self.top is None

    def push(self, val):
        """Push new value to top of stack."""
        self.top = Node(val, self.top)

    def pop(self):
        """Remove and return top item from stack."""
        if self.is_empty():
            raise Exception('Stack is empty')

        val = self.top.value
        self.top = self.top.next
        return val

def build_expression(s):
    """
    Given a string consisting of numeric values, parentheses and
    mathematical operators, return Expression tree using a stack-based
    algorithm developed by Dijskstra.
    """

    # Match open- and close- parens, any sequence of digits, and
    # known operators, using backslash notation. Limited to only special characters
    # but still quite nice...
    pattern = re.compile('(\(|\)|\d+|[{}])'.format('\\'.join(_operators.keys())))

    ops = Stack()
    expressions = Stack()

    for token in pattern.findall(s):
        if token in _operators:
            ops.push(_operators[token])            # Push each operator found for later
        elif token == '(':
            pass                       # You seriously do not need to do anything!
        elif token == ')':
            op = ops.pop()             # Close out most recent expression
            right = expressions.pop()  # Order matters...
            left = expressions.pop()   # And store it for future
            expressions.push(Expression(op, left, right))
        else:                          # If just a numeric value, push it for later
            expressions.push(Value(float(token)))

    return expressions.pop()           # If parens balance, then left with expression

#######################################################################
if __name__ == '__main__':
    # Base case
    num1 = Value(17)
    print(num1)
    print(num1.eval())

    expr = build_expression('(((3 + 1)/4) * (((1 + 5)* 9) - (2*6)))')
    print(expr)
    print(expr.eval())

    def exp(left, right):
        """^"""
        return left ** right

    add_operator('^', exp)

    expr = build_expression('((8^2)*(7/4))')
    print(expr)
    print(expr.eval())

    add1 = Expression(add, Value(1), Value(5))
    mult2 = Expression(mult, add1, Value(9))
    print(mult2,'=',mult2.eval())
