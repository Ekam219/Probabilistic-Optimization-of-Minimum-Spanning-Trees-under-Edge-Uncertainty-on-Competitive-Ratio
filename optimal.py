from graph import *
from functools import cmp_to_key
from copy import deepcopy
from collections import deque

def compareEdges(e, f):
    if e.lower != f.lower:
        return e.lower - f.lower
    elif e.upper != f.upper:
        return e.upper - f.upper
    else:
        return 0

def optimalQuerySet(g):
    # PHASE 1: Preprocessing with Kruskal's algorithm
    sortedEdges = sorted(g.edges, key=cmp_to_key(compareEdges))
    common = []
    choices = []
    curgraph = DynamicForest(g.size)
    
    while sortedEdges:
        e = sortedEdges.pop(0)
        if not curgraph.cycleCheck(e):
            curgraph.addEdge(e)
            continue
        
        cycle = curgraph.getCycle(e)
        curgraph.addEdge(e)
        candidate = max(cycle, key=lambda x: x.upper)
        
        # Check if candidate is always maximal
        has_maximal = all(e.upper <= candidate.lower for e in cycle)
        if has_maximal:
            curgraph.removeEdge(candidate)
            continue
        
        # Check if candidate must be queried
        flag = any(e.actual > candidate.actual for e in cycle)
        if not flag:
            for e in cycle:
                if e != candidate and e.upper > candidate.actual:
                    flag = True
                    candidate = e
                    break
        
        if not flag:
            flag = any(e.actual > candidate.lower and e != candidate for e in cycle)
        
        if flag:
            curgraph.removeEdge(candidate)
            common.append(candidate)
            candidate.query()
            sortedEdges.append(candidate)
            sortedEdges.sort(key=cmp_to_key(compareEdges))
            continue
        
        # Handle remaining case
        B = [e for e in cycle if e != candidate and e.upper > candidate.lower]
        choices.append((candidate, B))
        curgraph.removeEdge(max(cycle, key=lambda x: x.actual))

    # PHASE 2: Direct minimum vertex cover implementation
    leftEdges = [d for d, _ in choices]
    rightEdges = list({e for _, B in choices for e in B})
    
    # Create adjacency list and mappings
    adj = [[] for _ in range(len(leftEdges))]
    right_to_index = {e: i for i, e in enumerate(rightEdges)}
    
    for i, (d, B) in enumerate(choices):
        for e in B:
            adj[i].append(right_to_index[e])

    # Maximum Bipartite Matching using integrated implementation
    match_to = [-1] * len(rightEdges)
    match_from = [-1] * len(leftEdges)
    
    def bfs():
        layer = [0] * len(leftEdges)
        q = deque()
        for u in range(len(leftEdges)):
            if match_from[u] == -1:
                layer[u] = 0
                q.append(u)
            else:
                layer[u] = -1
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                if match_to[v] == -1:
                    found = True
                elif layer[match_to[v]] == -1:
                    layer[match_to[v]] = layer[u] + 1
                    q.append(match_to[v])
        return found
    
    def dfs(u, label):
        for v in adj[u]:
            if match_to[v] == -1 or (layer[match_to[v]] == label + 1 and dfs(match_to[v], label + 1)):
                match_from[u] = v
                match_to[v] = u
                return True
        layer[u] = -1
        return False
    
    result = 0
    while bfs():
        for u in range(len(leftEdges)):
            if match_from[u] == -1:
                result += dfs(u, 0)
    
    # Find minimum vertex cover using Konig's theorem
    visited_from = [False] * len(leftEdges)]
    visited_to = [False] * len(rightEdges)]
    
    # Mark unmatched left nodes
    q = deque()
    for u in range(len(leftEdges)):
        if match_from[u] == -1:
            visited_from[u] = True
            q.append(u)
    
    # BFS to mark alternating paths
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited_to[v] and match_to[v] != u:
                visited_to[v] = True
                if match_to[v] != -1 and not visited_from[match_to[v]]:
                    visited_from[match_to[v]] = True
                    q.append(match_to[v])
    
    # Select vertices for minimum cover
    min_cover = []
    for u in range(len(leftEdges)):
        if not visited_from[u]:
            min_cover.append(('left', u))
    for v in range(len(rightEdges)):
        if visited_to[v]:
            min_cover.append(('right', v))
    
    # Convert to edges
    for side, idx in min_cover:
        if side == 'left':
            common.append(leftEdges[idx])
        else:
            common.append(rightEdges[idx])
    
    return list(set(common))