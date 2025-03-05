# Probabilistic Optimization of Spanning Tree under Edge Uncertainty Based on Competitive Ratio

> Efficient MST construction under edge uncertainty leveraging combinatorial optimization and competitive analysis.  

---

## Abstract  

In real-world graph-based applications (e.g., **sensor networks, logistics planning**), **edge weights are inherently uncertain**, often represented as **interval values** rather than absolute scalars. This project explores the challenge of constructing a **Minimum Spanning Tree (MST) while minimizing edge querying costs** in an **uncertain-weight model**.  

We propose and analyze **two approximation algorithms**, `CutModel` and `CycleModel`, which exploit **MST properties** to **reduce redundant queries**. Additionally, we implement an **optimal approach** leveraging **Kruskal’s Algorithm** and **König’s Theorem-based edge-selection minimization** to achieve **minimal query complexity**.  

Our analysis benchmarks these strategies against **randomly generated test cases**, demonstrating **theoretical and empirical efficiency**.  
---

## Problem Statement  

Given a connected, undirected graph **\( G = (V, E) \)**, where each edge **\( e \in E \)** has an **uncertain weight** represented as an **interval**:

- The **true edge weight** remains **unknown** until explicitly queried.  
- Querying an edge **reveals its exact weight**, making it **trivial** \( (\text{lower} = \text{upper}) \).  
- The goal is to compute an **MST** while minimizing **the number of queries required** to determine exact edge weights.  

### Constraints:  
✔ Queries **incur a cost**, so they should be **strategically minimized**.  
✔ The constructed **MST must be correct**, despite uncertainty.  
✔ The competitive ratio **should be bounded** for approximation methods.  

---

## Algorithmic Approach  

### **1. CutModel (Cut-Based 2-Approximation Algorithm)**  

#### Theory:
The **cut property** of an MST states that for any partition of the vertices into two disjoint sets, the **lightest edge** crossing the partition must be included in the MST. The CutModel algorithm exploits this property to strategically query edges in partitions (or cuts) of the graph until the **lightest edge** in the cut is identified.

#### Strategy:
- **Identify uncertain edges spanning cut-sets**. A cut-set is a collection of edges that, when removed, separate the graph into two disconnected components.
- **Query edges** **until** an **always minimal** edge is found in the cut.
- Construct the **MST incrementally** while ensuring minimal queries by focusing only on edges that are relevant to the current cut.
  
#### Competitive Bound:  
The algorithm guarantees that the number of queries made will be at most **twice** the optimal number of queries, which results in a **2-approximation**.
---

### **2. CycleModel (Cycle-Based 2-Approximation Algorithm)**  

#### Theory:
The **cycle property** of an MST states that for any cycle in the graph, the MST must contain the lightest edge in the cycle, and exclude all others. The CycleModel algorithm uses this property to iteratively identify cycles with uncertain edges and eliminate non-MST edges (i.e., the heavier ones) from the graph.

#### Strategy:
- **Identify cycles** containing uncertain edges. A cycle is a path that starts and ends at the same vertex.
- **Query edges** until an **always maximal** edge is identified. The maximal edge in the cycle is the one with the highest weight, and it is determined that it will not be in the MST.
- Iteratively **eliminate heavier edges** to refine the MST by querying the edges of the cycle one at a time and removing edges that are not part of the MST.

#### Competitive Bound:  
Similar to the CutModel algorithm, CycleModel guarantees a **2-approximation**.

---

### **3. Optimal Solution (Kruskal + König’s Theorem)**  

#### Theory:
The **optimal solution** is based on a **two-phase approach**. First, a candidate MST is constructed using a modified version of **Kruskal's Algorithm**, which greedily adds edges to the tree based on their weights (assuming that edge weights are known). After this, **König’s Theorem** from **graph theory** is applied to minimize the number of queries required to determine which edges are part of the MST.

- **Phase 1:** Use a **modified Kruskal’s Algorithm** to construct an MST candidate. This step assumes that edge weights are known and processes the edges in increasing order of their weights.
- **Phase 2:** Once the MST candidate is constructed, apply **König’s Theorem** (a **graph matching theorem**) to identify a minimal set of edges that must be queried to confirm the MST. This theorem is particularly useful in **bipartite graphs** and helps identify **maximum matching** between edge sets, leading to the optimal query set.

#### Query Complexity:
The optimal approach guarantees the **minimal query complexity** but at the cost of **increased computational time** for edge selection and analysis.

---

### **Execution Workflow**  

1. **Step 1:** Generate **random graphs** with uncertain edge weights.  
2. **Step 2:** Execute **CutModel**, **CycleModel**, and **Optimal MST Construction** on the graph.  
3. **Step 3:** Compute and compare **query efficiency metrics** across all algorithms.  
4. **Step 4:** Visualize **query sequences** and the **MST formation** to understand the progression of edge queries and construction.  

---

