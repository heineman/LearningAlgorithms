"""Generated from perfect-hash"""
# =======================================================================
# ================= Python code for perfect hash function ===============
# =======================================================================

G = [0, 8, 1, 4, 7, 10, 2, 0, 9, 11, 1, 5]

S1 = [9, 4, 8, 6, 6]
S2 = [2, 10, 6, 3, 5]
assert len(S1) == len(S2) == 5

def hash_f(key, T):
    """Generated helper function."""
    return sum(T[i % 5] * ord(c) for i, c in enumerate(key)) % 12

def perfect_hash(key):
    """Perfect hash for words in K."""
    return (G[hash_f(key, S1)] + G[hash_f(key, S2)]) % 12

# ============================ Sanity check =============================

K = ['a', 'rose', 'by', 'any', 'other', 'name', 'would', 'smell', 'as', 'sweet']
assert len(K) == 10

for h, k in enumerate(K):
    assert perfect_hash(k) == h
