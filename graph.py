from copy import deepcopy

class UnionFind:
    """Union Find/Disjoin Set Union data structure."""
    def __init__(self, n):
        self.parent = [0]*n
        self.size = [0]*n
        for i in range(n):
            self.makeSet(i)

    def makeSet(self, v):
        self.parent[v] = v
        self.size[v] = 1

    def findSet(self, v):
        if self.parent[v] == v:
            return v
        self.parent[v] = self.findSet(self.parent[v])
        return self.parent[v]

    def unite(self, a, b):
        a = self.findSet(a)
        b = self.findSet(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            tmp = a
            a = b
            b = tmp
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def getTotalQueryCost(Q):
    res = 0
    for e in Q:
        res += e.cost
    return res

class Graph:
    """Class for storing weighted graphs and finding its minimum spanning tree."""
    def __init__(self, edgeList):
        self.size = 0
        self.edges = []
        for e in edgeList:
            self.size = max(self.size, e.u)
            self.size = max(self.size, e.v)
        self.adj = [[] for i in range(self.size + 1)]
        for e in edgeList:
            self.addEdge(e)

    def addEdge(self, edge):
        self.adj[edge.u].append(edge.v)
        self.adj[edge.v].append(edge.u)
        self.edges.append(edge)

    def kruskalMST(self):
        """Implements kruskal's MST algorithm(assuming that edges were added in the sorted order) and returs the set of edges in the MST."""
        comps = UnionFind(self.size + 1)
        mstEdges = set()
        for e in self.edges:
            if comps.unite(e.u, e.v):
                # print(e)
                mstEdges.add(e)
        return mstEdges


class UncertainEdge:
    """Class for storing uncertain edges."""
    def __init__(self, u, v, lower, upper, actual, index, cost = 1):
        self.u = u
        self.v = v
        self.lower = lower
        self.upper = upper
        self.actual = actual
        self.index = index
        self.trivial = (lower == upper)
        self.cost = cost

    def query(self):
        self.lower = self.upper = self.actual
        self.trivial = True
        return self.actual

    def __str__(self):
        return str(self.u) + ' ' + str(self.v) + ' ' + str(self.lower) + ' ' + str(self.upper) + ' ' + str(self.actual) + ' ' + str(self.cost)

    __repr__ = __str__

    def __eq__(self, other):
        return (self.u, self.v, self.lower, self.upper, self.actual, self.cost, self.index) == (other.u, other.v, other.lower, other.upper, other.actual, other.cost, other.index)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.u, self.v, self.lower, self.upper, self.actual, self.cost, self.index))


class UncertainGraph:
    """Class for storing and manipulating uncertain graphs."""
    def __init__(self):
        self.edges = set()

    def buildFromParameters(self, n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, edgeCost = None):
        self.size = n
        m = len(edgeFrom)
        assert len(edgeTo) == m and len(edgeLo) == m and len(
            edgeHi) == m and len(edgeActual) == m
        for i in range(m):
            self.edges.add(UncertainEdge(
                edgeFrom[i], edgeTo[i], edgeLo[i], edgeHi[i], edgeActual[i], i, edgeCost[i] if edgeCost else 1))

    def buildFromInput(self):
        self.size = int(input("Enter number of nodes: "))
        m = int(input("Enter number of edges: "))
        for i in range(m):
            u, v, lower, upper, actual, cost = list(
                map(int, input("Enter edge " + str(i + 1) + " : ").split()))
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i, cost))

    def buildFromFile(self, s):
        f = open(s, "r")
        self.size, m = map(int, f.readline().split())

        for i in range(m):
            u, v, lower, upper, actual, cost = f.readline().split()
            u, v, cost = map(int, [u, v, cost])
            lower, upper, actual = map(float, [lower, upper, actual])
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i, cost))

    def query(self, edge):
        # self.edges.remove(edge)
        edge.query()
        # self.edges.add(edge)

    def output(self):
        print(self.size)
        print(self.edges)

    def normalize(self):
        edgeCosts = set()
        for edge in self.edges:
            edgeCosts.add(edge.lower)
            edgeCosts.add(edge.upper)
            edgeCosts.add(edge.actual)
        edgeList = list(edgeCosts)
        edgeId = {}
        edgeList.sort()
        id = 1
        for i in edgeList:
            edgeId[i] = id 
            id += 1
        newEdges = set()
        for i in self.edges:
            edge = deepcopy(i)
            edge.lower = edgeId[i.lower]
            edge.upper = edgeId[i.upper]
            edge.actual = edgeId[i.actual]
            newEdges.add(edge)
        self.edges = newEdges

    def __str__(self):
        return str(self.edges)

    __repr__ = __str__


class DynamicForest:
    """Class for storing forests (collection of trees). Supports addition/removal of edges and also allows for generating the unique cycle closed by an edge in the forest."""
    def __init__(self, n):
        self.size = n
        self.edges = set()
        self.adj = [set() for i in range(n + 1)]
        self.comps = UnionFind(n + 1)

    def addEdge(self, edge):
        self.adj[edge.u].add(edge)
        self.adj[edge.v].add(edge)
        self.edges.add(edge)
        self.comps.unite(edge.u, edge.v)

    def removeEdge(self, edge):
        self.adj[edge.u].discard(edge)
        self.adj[edge.v].discard(edge)
        self.edges.discard(edge)
        self.comps = UnionFind(self.size + 1)
        for e in self.edges:
            self.comps.unite(e.u, e.v)

    def cycleCheck(self, edge):
        """Checks if an edge encloses a cycle in the forest or not."""
        return self.comps.findSet(edge.u) == self.comps.findSet(edge.v)

    def dfs(self, node, target, cycleEdges, par):
        """Simple DFS algorithm for finding the unique path between two vertices in the forest."""
        if node == target:
            return 1
        for e in self.adj[node]:
            other = e.v
            if other == node:
                other = e.u
            if other == par:
                continue
            if self.dfs(other, target, cycleEdges, node):
                cycleEdges.append(e)
                return 1
        return 0

    def getCycle(self, edge):
        """Returns the cycle enclosed by the edge in the forest."""
        cycleEdges = [edge]
        self.dfs(edge.u, edge.v, cycleEdges, -1)
        return cycleEdges