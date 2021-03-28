"""
Code to blindly search through a Graph in Depth First and Breadth First strategies. Also
contains a rudimentary Smart Search for undirected graphs when there is a metric showing
how far a node is from the target.
"""

def recover_cycle(DG):
    """Use recursive Depth First Search to detect cycle."""
    marked = {}
    in_stack = {}
    node_from = {}
    cycle = []

    def recover_cycle(w, v):
        n = v
        while n != w:
            yield n
            n = node_from[n]
        yield w
        yield v

    def dfs(v):
        in_stack[v] = True
        marked[v] = True

        if cycle: return        # Leave if cycle detected

        for w in DG[v]:
            if not w in marked:
                node_from[w] = v
                dfs(w)
            else:
                # Check to make sure it's not in stack -- CYCLE if so!
                if w in in_stack and in_stack[w]:
                    cycle.extend(reversed(list(recover_cycle(w, v))))

        in_stack[v] = False

    for v in DG.nodes():
        if not v in marked and not cycle:
            dfs(v)
    return cycle

def has_cycle(DG):
    """Use recursive Depth First Search to detect cycle."""
    marked = {}
    in_stack = {}

    def dfs(v):
        in_stack[v] = True
        marked[v] = True

        for w in DG[v]:
            if not w in marked:
                if dfs(w):
                    return True
            else:
                # Check to make sure it's not in stack -- CYCLE if so!
                if w in in_stack and in_stack[w]:
                    return True

        in_stack[v] = False
        return False

    for v in DG.nodes():
        if not v in marked:
            if dfs(v):
                return True
    return False

def topological_sort(DG):
    """
    Use recursive Depth First Search to generate a topological sort of nodes.
    Only call when no cycle exists!
    """
    marked = {}
    postorder = []

    def dfs(v):
        marked[v] = True

        for w in DG[v]:
            if not w in marked:
                dfs(w)

        postorder.append(v)

    for v in DG.nodes():
        if not v in marked:
            dfs(v)

    return reversed(postorder)

def has_cycle_nr(DG):
    """Conduct non-recursive cycle detection over directed graph."""
    from ch07.list_stack import Stack
    marked = {}
    in_stack = {}
    node_from = {}
    stack = Stack()

    for s in DG.nodes():
        if not s in marked:
            stack.push(s)

            while not stack.is_empty():
                v = stack.pop()
                if v in marked:
                    in_stack[v] = False
                else:
                    marked[v] = True
                    stack.push(v)
                    in_stack[v] = True

                for w in DG[v]:
                    if not w in marked:
                        stack.push(w)
                        node_from[w] = v
                    else:
                        # Check to make sure it's not in stack -- CYCLE if so!
                        if w in in_stack and in_stack[w]:
                            return True
    return False

def return_cycle_nr(DG):
    """Conduct non-recursive cycle detection over directed graph and return cycle."""
    from ch07.list_stack import Stack
    marked = {}
    in_stack = {}
    node_from = {}
    stack = Stack()

    for s in DG.nodes():
        if not s in marked:
            stack.push(s)

            while not stack.is_empty():
                v = stack.pop()
                if v in marked:
                    in_stack[v] = False
                else:
                    marked[v] = True
                    stack.push(v)
                    in_stack[v] = True

                for w in DG[v]:
                    if not w in marked:
                        stack.push(w)
                        node_from[w] = v
                    else:
                        # Check to make sure it's not in stack -- CYCLE if so!
                        if w in in_stack and in_stack[w]:
                            cycle = []
                            n = v
                            while n != w:
                                cycle.append(n)
                                n = node_from[n]

                            cycle.append(w)
                            cycle.append(v)
                            cycle.reverse()
                            return cycle

    return None

#######################################################################
if __name__ == '__main__':
    from ch07.book import make_sample_directed_graph
    DG = make_sample_directed_graph()
    #DG.add_edge('B2', 'C5')
    print('well:',has_cycle(DG))
