"""
Multiply two n-digit numbers (where n is quite large) of the following form

 1234567891234567 x 9876543219876543
"""
import random

def create_pair(n):
    """Create a pair of n-digit integers, from 1-up and from 9-down."""
    one = 0
    two = 0
    up = 1
    down = 9
    num_digits = 0
    while num_digits < n:
        one = 10*one + up
        two = 10*two + down
        up += 1
        if up == 10: up = 1
        down -= 1
        if down == 0: down = 9
        num_digits += 1

    return [one, two]

def create_random_pair(n):
    """Create a pair of n-digit integers, containing digits from 1-9 only."""
    one = 0
    two = 0
    for _ in range(n):
        one = 10*one + random.randint(1,9)
        two = 10*two + random.randint(1,9)

    return [one, two]

def mult_pair(pair):
    """Return the product of two, potentially large, numbers."""
    return pair[0]*pair[1]
