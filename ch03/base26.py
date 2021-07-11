"""
Functions to work with base26 hash scheme.

    :Example:

    >>> base26('sample')
    214086110

"""
from algs.sorting import unique
from ch03.months import s_data, s_num, days_in_month, days_bas, days_mixed

def base26(w):
    """Convert string into base26 representation where a=0 and z=25."""
    val = 0
    for ch in w.lower():
        next_digit = ord(ch) - ord('a')
        val = 26*val + next_digit
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
            raise RuntimeError('Inconsistent access for {}'.format(m))

    # search for a range of potential bases, starting from 12 which is
    # the lowest it could be
    for m in range(12,1000):
        data = eval_search_base26(m)
        if data:
            return (m, data)

    # failed...
    raise RuntimeError('search_for_base() failed')

#######################################################################
if __name__ == '__main__':
    print('base26 of june is {:,d}'.format(base26('june')))
    print('base26 of january is {:,d}'.format(base26('january')))
    print('base26 of august is {0:,d} with {0:,d} % 34 = {1}'.format(base26('august'), base26('august') % 34))
    print('base26 of abbreviated is {0:,d} and for march is {1:,d}'.format(base26('abbreviated') % 34, base26('march') % 34))
