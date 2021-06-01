""" Algorithms to find largest value in unordered array.
"""

def largest(A):
    """
    Requires N-1 invocations of less-than to determine max of N>0 elements.
    """
    my_max = A[0]
    for idx in range(1, len(A)):
        if my_max < A[idx]:
            my_max = A[idx]
    return my_max

def native_largest(A):
    """Simply access built-in max() method."""
    return max(A)

def alternate(A):
    """
    In worst case, requires (1/2)*(N^2 + 3N - 2) invocations of less-than.
    In best case requires N.
    """
    for v in A:
        v_is_largest = True             # When iterating over A, each value, v, could be largest
        for x in A:
            if v < x:                   # If v is smaller than some x, stop and record not largest
                v_is_largest = False
                break
        if v_is_largest:                # If largest, return v since it is maximum value.
            return v

    return None                         # If A is empty, return None

def just_three(A):
    """
    Returns largest in A when given exactly three elements. Won't work on
    all problem instances.
    """
    if len(A) != 3:
        raise ValueError('I only work on lists of size 3.')

    if A[1] < A[0]:
        if A[2] < A[1]:
            return A[0]
        if A[2] < A[0]:
            return A[0]
        return A[2]
    if A[1] < A[2]:
        return A[2]
    return A[1]
