"""
Home-grown replacement for networkx IN CASE this package is not found.
This implementation is not meant to be production-quality, but simply
a stub object that provides a reasonable implementation.

Note: Doesn't offer capability to draw graphs.
"""

class UndirectedGraph:
    """
    Use Dictionary to store all vertices. Values are lists of neighboring nodes.
    """
    def __init__(self):
        self.adjacency = {}
        self.positions = {}

    def add_node(self, u, pos=None):
        """Add node to graph, if not already there."""
        if u in self.adjacency:
            return
        self.adjacency[u] = []
        self.positions[u] = pos

    def __getitem__(self, u):
        """Get neighboring nodes to this node."""
        for node in self.adjacency[u]:
            yield node

    def nodes(self):
        """Return all nodes."""
        return self.adjacency.keys()
    
    def neighbors(self, u):
        """Return neighboring nodes."""
        for node in self.adjacency[u]:
            yield node
    
    def add_edge(self, u, v):
        if not u in self.adjacency:
            self.adjacency[u] = []
            
        if not v in self.adjacency:
            self.adjacency[u] = []

        # already there
        if v in self.adjacency[u]:
            return
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)

class DirectedGraph:
    """
    Use Dictionary to store all vertices. Values are lists of neighboring nodes.
    """
    def __init__(self):
        self.adjacency = {}
        self.positions = {}
 
    def add_node(self, u, pos=None):
        """Add node to graph, if not already there."""
        if u in self.adjacency:
            return
        self.adjacency[u] = []
        self.positions[u] = pos

    def __getitem__(self, u):
        """Get neighboring nodes to this node."""
        for node in self.adjacency[u]:
            yield node

    def nodes(self):
        """Return all nodes."""
        return self.adjacency.keys()
    
    def add_edge(self, u, v):
        """Add edge from u => v."""
        if not u in self.adjacency:
            self.adjacency[u] = []
            
        if not v in self.adjacency:
            self.adjacency[u] = []

        # already there
        if v in self.adjacency[u]:
            return
        self.adjacency[u].append(v)

class Replacement:
    def __init__(self):
        pass
    
    def Graph(self):
        """Create undirected graph."""
        return UndirectedGraph()
    
    def DiGraph(self):
        """Create directed graph."""
        return DirectedGraph()
    
    def get_node_attributes(self, graph, label):
        """I am not going to provide this capability."""
        return graph.positions
    
    def draw(self, graph, pos, with_labels = True, node_color="w", font_size=8, ax=None):
        """I am not going to provide this capability."""
        pass

