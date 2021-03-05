"""
Algorithms to locate top two values in an arbitrary list.
"""

def largest_two(A):
    """
    Return two largest values in A. In worst case, 2N-3 invocations of
    less-than will determine answer. In best case, N-1.
    """
    if len(A) < 2:
        raise ValueError('Must have at least two values')

    my_max,second = A[:2]
    if my_max < second:
        my_max,second = second,my_max

    for i in range(2, len(A)):
        if my_max < A[i]:
            my_max,second = A[i],my_max
        elif second < A[i]:
            second = A[i]
    return (my_max, second)

def sorting_two(A):
    """Sorts A in descending order and retrieve first two values."""
    if len(A) < 2:
        raise ValueError('Must have at least two values')
    
    return tuple(sorted(A, reverse=True)[:2])

def double_two(A):
    """Uses built-in max() method and duplicated list."""
    if len(A) < 2:
        raise ValueError('Must have at least two values')
    
    my_max = max(A)
    copy = list(A)
    copy.remove(my_max)
    return (my_max, max(copy))

def mutable_two(A):
    """Uses built-in max() method and extra storage."""
    if len(A) < 2:
        raise ValueError('Must have at least two values')
    
    index_max = max(range(len(A)), key=A.__getitem__)
    my_max = A[index_max]
    del A[index_max]
    second = max(A)
    A.insert(index_max, my_max)
    return (my_max, second)

class Match:
    """
    Match class used during Tournament algorithm to determine first and
    second largest values in list. Only supports an even-number of
    initial values.

    Attributes
    ----------
    larger : Comparable
        largest value in the match (i.e., the winner)
    smaller : Comparable
        Smaller value in the match (or could be equal to larger)

    Methods
    -------
    advance(m1, m2)
        returns new Match using larger values from matches m1 and m2
    """

    def __init__(self, val1, val2):
        self.prior = None
        if val1 < val2:
            self.larger = val2
            self.smaller = val1
        else:
            self.larger = val1
            self.smaller = val2

    @classmethod
    def advance(cls, match1, match2) -> 'Match':
        """Return Match that resulting from winners of two matches."""
        m = Match(match1.larger, match2.larger)
        if m.larger == match1.larger:
            m.prior = match1
        else:
            m.prior = match2
        return m

def tournament_two_object(A):
    """"
    Returns two largest values in A. Only works for lists whose length
    is a power of 2. This implementation is much slower because it
    instantiates Match objects.
    """
    if len(A) < 2:
        raise ValueError('Must have at least two values')
    if len(A) % 2 == 1:
        raise ValueError('Only works for lists with even number of values.')

    tourn = []
    for i in range(0, len(A), 2):
        tourn.append(Match(A[i], A[i+1]))

    while len(tourn) > 1:
        tourn.append(Match.advance(tourn[0], tourn[1]))
        del tourn[0:2]

    # Find where second is hiding!
    m = tourn[0]
    largest = m.larger
    second = m.smaller
    while m.prior:
        m = m.prior
        if second < m.smaller:
            second = m.smaller

    return (largest,second)

def tournament_two(A):
    """"
    Returns two largest values in A. Only works for lists whose length
    is a power of 2.
    """
    N = len(A)
    winner = [None] * (N-1)
    loser = [None] * (N-1)
    prior = [-1] * (N-1)

    # populate N/2 initial winners/losers
    idx = 0
    for i in range(0, N, 2):
        if A[i] < A[i+1]:
            winner[idx] = A[i+1]
            loser[idx] = A[i]
        else:
            winner[idx] = A[i]
            loser[idx] = A[i+1]
        idx += 1

    # pair up subsequent winners and record priors
    m = 0
    while idx < N-1:
        if winner[m] < winner[m+1]:
            winner[idx] = winner[m+1]
            loser[idx]  = winner[m]
            prior[idx]  = m+1
        else:
            winner[idx] = winner[m]
            loser[idx]  = winner[m+1]
            prior[idx]  = m
        m += 2
        idx += 1

    # Find where second is hiding!
    largest = winner[m]
    second = loser[m]
    m = prior[m]
    while m >= 0:
        if second < loser[m]:
            second = loser[m]
        m = prior[m]

    return (largest, second)
