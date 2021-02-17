"""
Use Binary Tree structure to represent expression.
"""
class Expression:
    """
    Node structure to use in a binary expression tree.
    
    Attributes
    ----------
        left - left child (or None)
        right - right child (or None)
        element - either a value or a string representing operation
    """
    def __init__(self, e, left=None, right=None):
        self.element = e
        self.left  = left
        self.right = right

    def __str__(self):
        if isinstance(self.element, str):
            L = str(self.left)
            R = str(self.right)
            return '({} {} {})'.format(L, self.element, R)
        return str(self.element)

    def eval(self):
        """Evaluate expression."""
        if isinstance(self.element, str):
            left = self.left.eval() if isinstance(self.left, Expression) else self.left
            right = self.right.eval() if isinstance(self.right, Expression) else self.right

            if self.element == '*':
                return left * right
            if self.element == '/':
                return left / right
            if self.element == '-':
                return left - right
            if self.element == '+':
                return left + right

            raise ValueError('Unknown operation:', self.element)

        # just the value
        return self.element

# Sample Recursive Expression
add1 = Expression('+', 3, 1)
div2 = Expression('/', add1, 4)
print(str(div2))
add3 = Expression('+', 1, 5)
mult4 = Expression('*', add3, 9)
mult5 = Expression('*', 2, 6)
sub6 = Expression("-", mult4, mult5)
mult7 = Expression("*", div2, sub6)

print(str(mult7))
print(mult7.eval())

# Base case
num1 = Expression(17)
print(str(num1))
print(num1.eval())

