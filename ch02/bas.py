"""Binary Array Search implementation"""

def binary_array_search(A, target):
    """
    Use Binary Array Search to search for target in ordered list A.
    If target is found, a non-negative value is returned marking the
    location in A; if a negative number, x, is found then -x-1 is the
    location where target would need to be inserted.
    """
    lo = 0
    hi = len(A) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if target < A[mid]:
            hi = mid-1
        elif target > A[mid]:
            lo = mid+1
        else:
            return mid

    return -(1+lo)
