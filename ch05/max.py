"""Recursive implementation of max."""

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
