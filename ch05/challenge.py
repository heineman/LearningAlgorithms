"""Challenge questions for chapter 5"""

def num_swaps(A):
    """Given an array of integers from 0 to N-1, return number of swaps to sort."""
    N = len(A)
    seen = [False] * N

    ct = 0
    for i in range(N):
        if not seen[i]:
            idx = i
            num = 0
            while not seen[idx]:
                num += 1
                seen[idx] = True
                idx = A[idx]

            ct += (num - 1)       # number of swaps is one less than size

    return ct

def num_swaps_hashable(A):
    """Given an array of distinct strings, return minimum number of swaps."""
    N = len(A)
    seen = {}
    final = {}
    original = list(A)

    # Selection sort and remember locations
    for i in range(N-1):
        min_index = i
        for j in range(i+1, N):
            if A[j] < A[min_index]:
                min_index = j

        final[A[min_index]] = i
        A[i],A[min_index] = A[min_index],A[i]
    final[A[N-1]] = N-1    # TRICKY can't forget this one

    ct = 0
    for i in range(N):
        if not original[i] in seen:
            idx = i
            num = 0
            while original[idx] not in seen:
                num += 1
                seen[original[idx]] = True
                idx = final[original[idx]]    # move to where final location will be

            ct += (num - 1)       # number of swaps is one less than size

    return ct

def slice_merge_sort(A):
    """Merge Sort where merge uses Python slice."""
    aux = [None] * len(A)

    def rsort(lo, hi):
        if hi <= lo:
            return

        mid = (lo+hi) // 2
        rsort(lo, mid)
        rsort(mid+1, hi)
        merge(lo, mid, hi)

    def merge(lo, mid, hi):
        # copy results of sorted sub-problems into auxiliary storage
        aux[lo:hi+1] = A[lo:hi+1]

        i = lo       # starting index into left sorted sub-array
        j = mid+1    # starting index into right sorted sub-array

        for k in range(lo, hi+1):
            if i > mid:
                A[k:hi+1] = aux[j:j+hi+1-k]
                return
            if j > hi:
                A[k:hi+1] = aux[i:i+hi+1-k]
                return
            if aux[j] < aux[i]:
                A[k] = aux[j]
                j += 1
            else:
                A[k] = aux[i]
                i += 1

    rsort(0, len(A)-1)
    
def recursive_two(A):
    """Return two largest values in A, using recursive approach."""

    def rtwo(lo, hi):
        # Base case: 1 or two values
        if lo == hi: return (A[lo], None)
        if lo+1 == hi:
            if A[lo] < A[hi]:
                return (A[hi], A[lo])
            return (A[lo], A[hi])

        mid = (lo+hi) // 2
        L = rtwo(lo, mid)
        R = rtwo(mid+1, hi)

        # Recursive case: Find largest of the possible four values.
        if L[0] < R[0]:
            if R[1] is None:
                return (R[0], L[0])
            return (R[0], R[1]) if L[0] < R[1] else (R[0], L[0])
        else:
            if L[1] is None:
                return (L[0], R[0])
            return (L[0], L[1]) if R[0] < L[1] else (L[0], R[0])

    return rtwo(0, len(A)-1)

#######################################################################
if __name__ == '__main__':
    print(num_swaps_hashable(['15', '21', '20', '2', '15', '24', '5', '19']))

    # Construct an array with UP-DOWN-UP structure.
    VALS = list(range(137))
    VALS.extend(list(range(300,200,-1)))
    VALS.extend(range(400,500))

    from algs.sorting import check_sorted
    slice_merge_sort(VALS)
    print('VALS should is sorted:', check_sorted(VALS))
