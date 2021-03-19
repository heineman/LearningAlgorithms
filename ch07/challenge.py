"""
Challenge Exercises for Chapter 7.
"""

def path_to_recursive(node_from, src, target):
    """
    Recursive implementation, which appears similar in logic to a pre-order
    search. First yield the path before me, then yield self.
    """
    if target == src:
        yield src
    else:
        if node_from[target] is None:
            raise ValueError('{} is unreachable from {}'.format(target,src))
    
        for n in path_to_recursive(node_from, src, node_from[target]):
            yield n
        yield target
