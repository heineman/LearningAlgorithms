"""
Functions to work with base26 hash scheme.

    :Example:

    >>> base26('sample')
    214086110

"""
from algs.sorting import unique
from resources.english import english_words
from ch03.months import s_data, s_num, days_in_month, days_bas, days_mixed

def base26(m):
    """Convert string into base26 representation where a=0 and z=25."""
    val = 0
    for ch in m.lower():
        next_digit = ord(ch) - ord('a')
        val  = 26*val + next_digit
    return val

def eval_search_base26(m):
    """
    Check if all hashes are unique for given modulo m for s_data; if
    so, then return array containing -1 in invalid indices, and the
    month length from s_num in valid ones.
    """
    result = [base26(k) % m for k in s_data]
    if (min(result) >= 0) and unique(result):
        data = [-1] * (1+max(result))
        for idx in range(len(s_data)):
            data[result[idx]] = s_num[idx]
        return data
    return None

def search_for_base():
    """
    Search for lowest base that ensures hash(m) modulo base is unique
    for the twelve months stored in s_data
    """
    for m in s_data:
        if days_in_month[m] != days_mixed(m) or days_bas(m) != days_mixed(m):
            print('Inconsistent access for ', m)

    # search for a range of potential bases, starting from 12 which is
    # the lowest it could be
    for m in range(12,1000):
        data = eval_search_base26(m)
        if data:
            return (m, data)

    # failed...
    return (None, None)
