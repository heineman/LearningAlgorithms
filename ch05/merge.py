"""""
Merge sort uses auxiliary storage
"""

def merge_sort(A):
    """Merge Sort implementation using auxiliary storage."""
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

        left = lo        # starting index into left sorted sub-array
        right = mid+1    # starting index into right sorted sub-array

        for i in range(lo, hi+1):
            if left > mid:
                A[i] = aux[right]
                right += 1
            elif right > hi:
                A[i] = aux[left]
                left += 1
            elif aux[right] < aux[left]:
                A[i] = aux[right]
                right += 1
            else:
                A[i] = aux[left]
                left += 1

    rsort(0, len(A)-1)

def merge_sort_counting(A):
    """Perform Merge Sort and return #comparisons."""
    aux = [None] * len(A)

    def rsort(lo, hi):
        if hi <= lo:
            return (0,0)

        mid = (lo+hi) // 2
        (lefts, leftc) = rsort(lo, mid)
        (rights, rightc) = rsort(mid+1, hi)
        (nswap, ncomp) = merge(lo, mid, hi)
        return (lefts+rights+nswap, leftc+rightc+ncomp)

    def merge(lo, mid, hi):
        # copy results of sorted sub-problems into auxiliary storage
        aux[lo:hi+1] = A[lo:hi+1]

        i = lo       # starting index into left sorted sub-array
        j = mid+1    # starting index into right sorted sub-array

        numc = 0
        nums = 0
        for k in range(lo, hi+1):
            if i > mid:
                if A[k] != aux[j]: nums += 0.5
                A[k] = aux[j]
                j += 1
            elif j > hi:
                if A[k] != aux[i]: nums += 0.5
                A[k] = aux[i]
                i += 1
            elif aux[j] < aux[i]:
                numc += 1
                if A[k] != aux[j]: nums += 0.5
                A[k] = aux[j]
                j += 1
            else:
                numc += 1
                if A[k] != aux[i]: nums += 0.5
                A[k] = aux[i]
                i += 1
        return (nums, numc)

    return rsort( 0, len(A)-1)
