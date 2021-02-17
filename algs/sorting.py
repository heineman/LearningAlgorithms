"""Utility methods for validating sorting algorithms."""

def is_sorted(a):
    """Determines if list is sorted, throwing exception if not."""
    if not check_sorted(a):
        raise Exception('Not sorted!')

def check_sorted(a):
    """Determines if list is sorted."""
    for i, val in enumerate(a):
        if i > 0 and val < a[i-1]:
            return False
    return True

def unique(A):
    """Determine if A contains any duplicate values."""
    ascending = sorted(A)

    for i in range(len(ascending)-1):
        if ascending[i] == ascending[i+1]:
            return False

    return True
