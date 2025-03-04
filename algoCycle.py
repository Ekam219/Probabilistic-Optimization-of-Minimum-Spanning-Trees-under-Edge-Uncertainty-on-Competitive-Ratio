import graph
from preprocessing import Preprocessor
from collections import deque
from copy import deepcopy

# Base class to run the algorithm


class CycleModel:
    # Initialise the class object
    def __init__(self, g):
        self.G = deepcopy(g)
        self.queryCount = 0
        # Do pre-processing and get the initial query set
        p = Preprocessor(g)
        self.Q = deepcopy(p.query)
        # Find the lower limit tree
        self.Tl = deepcopy(p.Tl)
        # Find the upper limit tree
        self.Tu = deepcopy(p.Tu)
        f = self.G.edges
        removed = set()
        for edge in self.Tl:
            removed.add((edge.u, edge.v))
        erased = set()
        for edge in f:
            if (edge.u, edge.v) in removed or (edge.v, edge.u) in removed:
                erased.add(edge)
        for edge in erased:
            f.remove(edge)
        # f is a set of edges not present in lower limit tree
        C = []

        # DFS Function to traverse in the tree
        def dfs(u, par, adj, last, edges):
            if u == last:
                C[:] = edges
            for v in adj[u]:
                if v.u + v.v - u != par:
                    edges.append(v)
                    dfs(v.u + v.v - u, u, adj, last, edges)
                    edges.remove(v)

        # Function to check whether the edgeSet contains in always maximal edge
        def check(edgeSet):
            if len(edgeSet) <= 1:
                return False
            uppers = []
            for edge in edgeSet:
                uppers.append(edge.upper)
            uppers.sort()
            for edge in edgeSet:
                if edge.upper == uppers[-1] and (edge.trivial or edge.lower >= uppers[-2]):
                    return False
            return True

        # Go through each edge in f
        for edge in f:
            # Construct the graph using adjacency list
            adj = [[] for _ in range(self.G.size + 1)]
            for edge2 in self.Tl:
                adj[edge2.u].append(edge2)
                adj[edge2.v].append(edge2)
            C[:] = []
            dfs(edge.u, -1, adj, edge.v, [])
            C.append(edge)
            # C is the set of edges which denote the cycle formed by adding 'edge'
            self.Tl.add(edge)
            # Unless C does not contain always maximal edge
            while check(C):
                uppers = []
                firstUpper = 0
                firstEdge = 0
                # Find the two edges with maximum upper limits
                for i in range(len(C)):
                    if C[i].upper > firstUpper:
                        firstUpper = C[i].upper
                        firstInd = i
                secondUpper = 0
                secondInd = 0
                firstEdge = C[firstInd]
                for i in range(len(C)):
                    if i == firstInd:
                        continue
                    if C[i].upper > secondUpper:
                        secondUpper = C[i].upper
                        secondInd = i
                secondEdge = C[secondInd]
                # If the first edge is not trivial, then query it
                if not firstEdge.trivial:
                    self.Q.add(deepcopy(firstEdge))
                    self.Tl.remove(firstEdge)
                    self.G.query(firstEdge)
                    C.remove(firstEdge)
                    firstEdge.lower = firstEdge.actual
                    firstEdge.upper = firstEdge.actual
                    firstEdge.trivial = True
                    self.Tl.add(firstEdge)
                    C.append(firstEdge)
                # If the second edge is not trivial, then query it
                if not secondEdge.trivial:
                    self.Q.add(deepcopy(secondEdge))
                    self.Tl.remove(secondEdge)
                    self.G.query(secondEdge)
                    C.remove(secondEdge)
                    secondEdge.lower = secondEdge.actual
                    secondEdge.upper = secondEdge.actual
                    secondEdge.trivial = True
                    self.Tl.add(secondEdge)
                    C.append(secondEdge)

            # If an always maximal edge is found, erase it from Lower Limit Tree
            if len(C):
                uppers = []
                for edge in C:
                    uppers.append(edge.upper)
                uppers.sort()
                uCon, vCon = None, None
                for edge in C:
                    if edge.upper == uppers[-1] and (edge.trivial or edge.lower >= uppers[-2]):
                        self.Tl.remove(edge)
                        break