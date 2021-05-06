"""Recursive implementations."""

def find_max(A):
    """invoke recursive function to find maximum value in A."""

    def rmax(lo, hi):
        """Use recursion to find maximum value in A[lo:hi+1]."""
        if lo == hi: return A[lo]

        mid = (lo+hi)//2
        left = rmax(lo, mid)
        right = rmax(mid+1, hi)
        return max(left, right)

    return rmax(0, len(A)-1)

def find_max_with_count(A):
    """Count number of comparisons."""

    def frmax(lo, hi):
        """Use recursion to find maximum value in A[lo:hi+1] incl. count"""
        if lo == hi: return (0, A[lo])

        mid = (lo+hi)//2
        ctleft,left = frmax(lo, mid)
        ctright,right = frmax(mid+1, hi)
        return (1+ctleft+ctright, max(left, right))

    return frmax(0, len(A)-1)

def count(A,target):
    """invoke recursive function to return number of times target appears in A."""

    def rcount(lo, hi, target):
        """Use recursion to find maximum value in A[lo:hi+1]."""
        if lo == hi:
            return 1 if A[lo] == target else 0

        mid = (lo+hi)//2
        left = rcount(lo, mid, target)
        right = rcount(mid+1, hi, target)
        return left + right

    return rcount(0, len(A)-1, target)
