from graph import *
from numpy import random
import numpy as np
import random

class GraphGenerator:
    def __init__(self, debug):
        self.debug = debug

    def getEdgeWeightA(self, lo, hi, centre, deviation, trivialProbability):
        probability = random.uniform(0, 1)
        if probability <= trivialProbability:
            weight = random.uniform(lo, hi)
            return (weight, weight, weight)
        left, right = centre, centre
        length = (hi - lo) * deviation
        left = max(lo, left - length)
        right = min(hi, left + length)
        weight = random.uniform(left, right)
        return (lo, hi, weight)

    def getEdgeWeightB(self, lo, hi, trivialProbability):
        probability = random.uniform(0, 1)
        if probability <= trivialProbability:
            weight = random.uniform(lo, hi)
            return (weight, weight, weight)
        left, right = random.uniform(lo, hi), random.uniform(lo, hi)
        if left > right:
            left, right = right, left
        weight = random.uniform(left, right)
        return (left, right, weight)

    def constructGraphA(self, n, m, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        if lo > hi:
            lo, hi = hi, lo
        if centre == None:
            centre = (lo + hi) / 2
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if centre < lo or centre > hi:
            assert False
        if deviation < 0 or deviation > 1:
            assert False
        if trivialProbability < 0 or trivialProbability > 1:
            assert False
        if self.debug:
            print(
                f"Constructing graph with n = {n}, m = {m}, lo = {lo}, hi = {hi}, centre = {centre}, deviation = {deviation} and trivialProbability = {trivialProbability}.")
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            weights = self.getEdgeWeightA(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        # print(edgeSet)
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            weights = self.getEdgeWeightB(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
        return graph

   
    # All the edges are trivial
    def edgeCaseA(self, n, m, weight):
        return self.costructGraph(n, m, weight, weight, weight, 0, 1)

    # Complete Graph
    def edgeCaseC(self, n, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        return self.costructGraph(n, n*(n-1)//2, lo, hi, centre, deviation, trivialProbability)