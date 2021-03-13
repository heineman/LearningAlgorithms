"""Opening example for Chapter 03.

Provides different alternatives to recording the number of days in each
calendar month

  * days_in_month is a standard Python dict. Access as days_in_month[m]
  * days_in_month_mixed uses a list with months in even index locations
    and days in odd index locations. Access as days_mixed(m)
  * s_data and s_num are parallel arrays, sorted alphabetically to
    allow binary array search to be used over s_data. Access
    as days_bas(m)

"""
import calendar
from datetime import date
from algs.sorting import unique

# https://www.oreilly.com/library/view/high-performance-python/9781449361747/ch04.html#:~:text=By%20default%2C%20the%20smallest%20size,will%20still%20allocate%20eight%20elements).
days_in_month = {
    'January'   : 31,    'February'  : 28,   'March'     : 31,
    'April'     : 30,    'May'       : 31,   'June'      : 30,
    'July'      : 31,    'August'    : 31,   'September' : 30,
    'October'   : 31,    'November'  : 30,   'December'  : 31
}

# mixed type arrays can also be used
days_in_month_mixed = [ 'January', 31, 'February', 28, 'March', 31, 'April', 30,
                        'May', 31, 'June', 30, 'July', 31, 'August', 31, 'September', 30,
                        'October', 31, 'November', 30, 'December', 31]

# parallel arrays in alphabetic order suitable for Binary Array Search
s_data = [ 'April', 'August', 'December', 'February', 'January', 'July', 'June',
           'March', 'May', 'November', 'October', 'September']
s_num  = [ 30, 31, 31, 28, 31, 31, 30, 31, 31, 30, 31, 30]

# canonical ordering of months, with lengths in parallel array
key_array = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December' ]
month_length = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def print_month(month, year):
    """Print brief monthly calendar for month, like ('December', 2020)."""
    idx = key_array.index(month)
    day = 1

    wd = date(year,idx + 1,day).weekday()     # Returns Monday as 0, so adjust
    wd = (wd + 1) % 7
    end = month_length[idx]
    if calendar.isleap(year) and idx == 1:    # February LeapYear has one extra day
        end += 1

    print('{} {}'.format(month,year).center(20))
    print('Su Mo Tu We Th Fr Sa')
    print('   ' * wd, end='')                 # Pad spacing
    while day <= end:
        print('{:2d} '.format(day), end='')
        wd = (wd + 1) % 7
        day += 1
        if wd == 0: print()
    print()

def day_of_week(y, m, d):
    """
    There is a formula to compute the week day mathematically, first posted to
    comp.lang.c discussion boards in 1992 by Tomohiko Sakamoto. Further details
    at https://cs.uwaterloo.ca/~alopez-o/math-faq/node73.html. Works for dates
    after 1752 when Gregorian calendar formally adopted. 1 <= m <= 12 and y > 1752.
    """
    y -= m<3
    return (y + y//4 - y//100 + y//400 + ord('-bed=pen+mad.'[m]) + d) % 7

def day_of_week_one_line(y, m, d):
    """Oneliner just for fun."""
    return (y-(m<3)+(y-(m<3))//4-(y-(m<3))//100+(y-(m<3))//400+ord('-bed=pen+mad.'[m])+d)%7

def days_mixed(month):
    """Demonstrate using mixed-type array to compute month length."""
    for i in range(0,24,2):
        if days_in_month_mixed[i] == month:
            return days_in_month_mixed[i+1]
    return 0

def days_bas(month):
    """Use Binary ArraySearch to locate number of days in given month."""
    from ch02.bas import binary_array_search
    idx = binary_array_search(s_data, month)
    if idx < 0:
        return 0
    return s_num[idx]

def sample_search(p1,p2):
    """Check if all hashes are unique for p1 and p2."""
    result = [month_index(k,p1,p2) for k in s_data]
    if (min(result) >= 0) and unique(result):
        data = [-1] * (1+max(result))
        for idx in range(len(s_data)):
            data[result[idx]] = s_num[idx]
        return data
    return None

def month_index(m,p1,p2):
    """"Computed Function to return unique key for month names."""
    ct = 0
    for ch in m:
        ct = (ct*p1 + ord(ch)) % p2
    return ct

def search_for_data():
    """Search prime numbers for suitable constants to use."""
    p1s = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 61, 67, 71]
    best = None
    best_tuple = None
    for p1 in p1s:
        for p2 in p1s:
            data = sample_search(p1, p2)
            if data:
                if best is None:
                    best = data
                    best_tuple = (p1, p2)
                elif len(data) < len(best):
                    best = data
                    best_tuple = (p1, p2)

    return (best_tuple, best)

def search_for_hashes():
    """What is smallest array that stores unique values for months using default hash."""
    N = 12
    while True:
        hashes = [hash(k) % N for k in key_array]
        if len(hashes) == len(set(hashes)):
            tbl = [None] * N
            for idx,key in enumerate(key_array):
                tbl[hash(key) % N] = month_length[idx]
            return tbl
        N += 1

    return []

def craft_table():
    """
    Create a Hashtable from months. Changes each time you run because of
    salted hash strings.
    """
    from ch03.hashtable import Hashtable
    last = 1000
    for M in range(12, last):
        ht = Hashtable(M)
        try:
            for idx,key in enumerate(key_array):
                ht.put(key, month_length[idx])
            return ht
        except RuntimeError:
            pass

    return None

#######################################################################
if __name__ == '__main__':
    # Validate leap years and non-leap years
    print_month('February', 2021)
    print()
    print_month('February', 2024)
    print()

    (best_tuple, best) = search_for_data()
    print('Two constants in monthIndex should be p1 =', best_tuple[0], 'and p2 =', best_tuple[1])

    result = search_for_hashes()
    print('Need hashtable of size', len(result), 'to store months uniquely.')
    print(result)
    ht = craft_table()

    print('created hashtable of size', ht.M)
