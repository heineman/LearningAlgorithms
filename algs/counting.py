"""An Item that can be used to count the number of times <, = or > is invoked.

Clear the statistics by invoking RecordedItem.clear()
"""
class RecordedItem:
    """
    When used in a list, this class records the number of times that each
    of the (eq, lt, gt) operations are called.
    """
    num_eq = 0
    num_lt = 0
    num_gt = 0

    def __init__(self, val):
        self.val = val

    @classmethod
    def range(cls, n):
        """Return list of RecordItem(i) for i from 0 to n-1."""
        return [RecordedItem(i) for i in range(n)]

    @classmethod
    def header(cls):
        """Terms in the report."""
        return ('eq', 'lt', 'gt')

    @classmethod
    def clear(cls):
        """Reset the counters."""
        RecordedItem.num_eq = RecordedItem.num_lt = RecordedItem.num_gt = 0

    @classmethod
    def report(cls):
        """Return the resulting statistics for EQ, LT, GT."""
        return (RecordedItem.num_eq, RecordedItem.num_lt, RecordedItem.num_gt)

    def __eq__(self, other):
        RecordedItem.num_eq += 1
        return self.val == other.val

    def __lt__(self, other):
        RecordedItem.num_lt += 1
        return self.val < other.val

    def __gt__(self, other):
        RecordedItem.num_gt += 1
        return self.val > other.val
