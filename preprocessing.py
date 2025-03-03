from graph import *
from functools import cmp_to_key
from copy import deepcopy

# Base function to do pre-processing for the given graph


class Preprocessor:
    def __init__(self, g):
        self.query = set()
        self.G = deepcopy(g)
        # Find the lower limit tree
        self.Tl = self.lowerLimitTree()
        # Find the upper limit tree
        self.Tu = self.upperLimitTree()
        # Find the intersection set edges
        newEdge = self.findIntersection(self.Tl, self.Tu)
        # Until there is at least one edge common between lower limit tree and upper limit tree
        while len(newEdge):
            # Query for this edge
            for edge in newEdge:
                self.query.add(deepcopy(edge))
                self.G.query(edge)
            # Update lower limit and upper limit trees
            self.Tl = self.lowerLimitTree()
            self.Tu = self.upperLimitTree()
            newEdge = self.findIntersection(self.Tl, self.Tu)

    # Custom coparator function to give total ordering of edge in lower limit tree
    def lowerOrderingComparator(self, e1, e2):
        if e1.lower != e2.lower:
            return e1.lower - e2.lower
        else:
            if e1.trivial and not e2.trivial:
                return 1
            if not e1.trivial and e2.trivial:
                return -1
            if e1.trivial and e2.trivial:
                return e1.index - e2.index
            if e1.upper != e2.upper:
                return e2.upper - e1.upper
        return e1.index - e2.index

    # Custom coparator function to give total ordering of edge in upper limit tree
    def upperOrderingComparator(self, e1, e2):
        if e1.upper != e2.upper:
            return e1.upper - e2.upper
        else:
            if e1.trivial and not e2.trivial:
                return 1
            if not e1.trivial and e2.trivial:
                return -1
            if e1.trivial and e2.trivial:
                return e1.index - e2.index
            if e1.lower != e2.lower:
                return e2.lower - e1.lower
        return e1.index - e2.index

    # Function to find lower limit tree
    def lowerLimitTree(self):
        lowerEdgeOrdering = sorted(
            self.G.edges, key=cmp_to_key(self.lowerOrderingComparator))
        g = Graph(lowerEdgeOrdering)
        return g.kruskalMST()

    # Function to find upper limit tree
    def upperLimitTree(self):
        upperEdgeOrdering = sorted(
            self.G.edges, key=cmp_to_key(self.upperOrderingComparator))
        g = Graph(upperEdgeOrdering)
        return g.kruskalMST()

    # Find the set of edges present in lower limit but not in upper limit tree
    def findIntersection(self, tl, tu):
        ans = set()
        for edge in tl:
            if edge not in tu and not edge.trivial:
                ans.add(edge)
        return ans