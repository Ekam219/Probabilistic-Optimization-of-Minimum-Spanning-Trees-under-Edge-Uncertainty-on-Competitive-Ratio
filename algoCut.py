import graph
from preprocessing import Preprocessor
from copy import deepcopy

# Base class to run the algorithm
class CutModel:
    # Initialise the class object
    def __init__(self, g):
        self.G = deepcopy(g)
        self.queryCount = 0
        # Do pre-processing and get the initial query set
        p = Preprocessor(self.G)
        self.Q = deepcopy(p.query)
        # Find the lower limit tree
        self.Tl = deepcopy(p.Tl)
        # Find the upper limit tree
        self.Tu = deepcopy(p.Tu)
        g = list(deepcopy(self.Tu))
        g.sort(key=lambda x: -x.upper)
        # g is the set of edges in upper limit tree sorted in descending order of upper limits
        component = {}

        # DFS Function to traverse in the tree
        def dfs(u, par, adj, c):
            component[u] = c
            for v in adj[u]:
                if v.u + v.v - u != par:
                    dfs(v.u + v.v - u, u, adj, c)

        # Function to check whether the edgeSet contains in always minimal edge
        def check(edgeSet):
            if len(edgeSet) <= 1:
                return False
            lowers = []
            for edge in edgeSet:
                lowers.append(edge.lower)
            lowers.sort()
            for edge in edgeSet:
                if edge.lower == lowers[0] and (edge.trivial or edge.upper <= lowers[1]):
                    return False
            return True

        # Go through each edge in g
        for edge in g:
            # Construct the graph in adjacency list
            adj = [[] for _ in range(self.G.size + 1)]
            erased = None
            for edge2 in self.Tu:
                if {edge2.u, edge2.v} == {edge.u, edge.v}:
                    erased = edge2
            self.Tu.remove(erased)
            for edge2 in self.Tu:
                adj[edge2.u].append(edge2)
                adj[edge2.v].append(edge2)
            # Do two DFS - once from each component
            component.clear()
            dfs(edge.u, -1, adj, 0)
            dfs(edge.v, -1, adj, 1)
            # C stores the edge set denoting the "cut" created
            C = []
            for edge2 in self.G.edges:
                if component[edge2.u] != component[edge2.v]:
                    C.append(edge2)
            # While C does not have always mininal edge
            while check(C):
                firstLower = 1e9
                firstInd = 0
                # Find the two edges with minimum lower limits
                for i in range(len(C)):
                    if C[i].lower < firstLower:
                        firstLower = C[i].lower
                        firstInd = i
                secondLower = 1e9
                secondInd = 0
                firstEdge = C[firstInd]
                for i in range(len(C)):
                    if i == firstInd:
                        continue
                    if C[i].lower < secondLower:
                        secondLower = C[i].lower
                        secondInd = i
                secondEdge = C[secondInd]
                assert secondEdge.lower <= firstEdge.upper
                # If the first edge is not trivial, then query it
                if not firstEdge.trivial:
                    self.Q.add(deepcopy(firstEdge))
                    self.G.query(firstEdge)
                    C.remove(firstEdge)
                    firstEdge.lower = firstEdge.actual
                    firstEdge.upper = firstEdge.actual
                    firstEdge.trivial = True
                    C.append(firstEdge)
                # If the second edge is not trivial, then query it
                if not secondEdge.trivial:
                    self.Q.add(deepcopy(secondEdge))
                    self.G.query(secondEdge)
                    C.remove(secondEdge)
                    secondEdge.lower = secondEdge.actual
                    secondEdge.upper = secondEdge.actual
                    secondEdge.trivial = True
                    C.append(secondEdge)

            # If an always minimal edge is found, erase it from Upper Limit Tree
            if len(C):
                if len(C) == 1:
                    self.Tu.add(C[0])
                else:
                    lowers = []
                    for edge in C:
                        lowers.append(edge.lower)
                    lowers.sort()
                    for edge in C:
                        if edge.lower == lowers[0] and (edge.trivial or edge.upper <= lowers[1]):
                            self.Tu.add(edge)
                            break