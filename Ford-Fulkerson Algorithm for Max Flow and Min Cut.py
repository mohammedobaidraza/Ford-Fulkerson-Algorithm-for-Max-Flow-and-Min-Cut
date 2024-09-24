# -*- coding: utf-8 -*-
"""Solution of 460 Graphs - Flows and Cuts - assignment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15iy1hwOfs6Ar2dn-5qoInsQYXwnHBQDk

# Flows and cuts

A flow graph is a directed graph $G=(V,E)$ whose edges are characterized by a capacity to carry a flow. In the adjacency matrix representation, $G_{ij}=c(i,j)$, i.e., the capacity of the edge from vertex $i$ to vertex $j$. If there is no edge $i→j$, the capacity is 0 and correspondingly, $G_{ij}=0$.

In a flow graph, our objective is to maximize the flow between two vertices. We label these two special vertices as *source* and *target.*

The **Ford-Fulkerson** method finds the maximum flow that can be pushed through a network, as follows:

```text
initialize max_flow to 0
while there is an augmenting path:
  add augmenting path's min residual capacity to max_flow
return max_flow
```

The technique, as stated above, depends on *augmenting paths*. As long as we figure out what an augmenting path is, we are all set.

## Notation

Instead of a weight, edges in flow graphs have a capacity. We write $u \xrightarrow{10} v$ to show that the capacity of the edge from vertex $u$ to $v$ is 10.

The capacity tells us how much flow this edge can accomodate, at most. For example, if the edge was a road that connected two towns, it can accomodate 10 cars per minute. If we tried to send 11 cars per minute, we'll cause a traffic jam.

Capacities, and flows, are typically expressed in unit time such as seconds, hours, etc. For example, a road has a capacity of 10 cars per minute, an wire has a capacity of $6.24\times 10^8$ electrons per second, and a grocery register has a capacity of 20 clients per hour. In a flow graph, we do not show explicitly the units. We refer to the capacity just by its value, e.g., a "capacity of 10". The assumption is that we are in agreement of what that 10 means in the context of the graph we study (could be 10 cars a minute, 20 clients per hour, etc).

When there is flow across an edge, we show its value too, with a second number: $u \xrightarrow{5/10} v$ indicates that there is a flow of 5 (something per some unit time) across an edge that can accommodate up to 10 somethings per unit time.

If we wish to be dramatic, we could write $u \xrightarrow{0/10} v$ to emphasize that there is no flow over an edge. In desperate situations, we may even write $u \xrightarrow{0} v$ to indicate an edge with 0 capacity; though it may be best if we just admitted there is no edge between $u$ and $v$. Algorists that write $u \xrightarrow{0/0} v$ to indicate there is no flow over a non-existing edge, should not be allowed near computers.

## Augmenting path

An augmenting path is a path from the source vertex to the target vertex, $s\rightsquigarrow t$, in the *residual graph.*

## Residual graph

The residual graph is a copy of the input graph. It is the graph on which we try different paths to determine how much flow we can send from $s$ to $t$ in the actual graph. This process destroys existing edges and creates new ones. We do not want this to happen in the actual graph, and so we operate on a working copy that we call the *residual graph*.

## Residual capacity

The capacity of an edge in the residual graph is called *residual capacity.* The residual capacity is written $c_f(u\rightarrow v)$ for an edge $u\rightarrow v$ in the residual graph. In the beginning, the edges in the residual graph are identical to the edges in the input graph, and so:

$$ c_f(u→v) = c(u→v),\ ∀u→v\ ∈ E$$

As we iterate through the algorithm, the residual capacities are updated according to the flow we can send through the edges of the residual graph. In other words, residual capacity is the available capacity of an edge in the residual graph. Why call it *residual* then and not *available*. Well, we don't want to make algorithms sound too easy, do we?

From iteration to iteration, residual capacities are updated according to

$$
\underbrace{{{}^{t+1}c_f(u,v)}}_{\begin{array}{c}\text{residual}\\ \text{capacity}\\ \text{in next}\\ \text{iteration}\end{array}} =
\underbrace{{{}^{t}c_f(u,v)}}_{\begin{array}{c}\text{total}\\ \text{capacity}\\ \text{in current}\\ \text{iteration}\end{array}} -
\underbrace{{f(u,v)}}_{\begin{array}{c}\text{max. flow}\\ \text{for current}\\ \text{augmenting}\\ \text{path}\end{array}}
$$

The notation $^{t+1}c_f$ indicates the value $c_f$ during the $(t+1)$-th iteration. When the edge $u→v$ is saturated by carrying as much flow as it can, $c_f(u,v)=0$, then the residual capacity becomes $c_f = -f(u,v)$ in the next iteration.

Let's take a minute to illustrate such an iteration. In the input graph, below, we have a path from $A$ to $E$ whose three edges have capacities 20, 5, and 7, respectively. The maximum flow along that path is determined by its edge with the least capacity: in this case $c(B\rightarrow C)=5$. To show that flow along the edges of the input graph, we use the notation $u\xrightarrow{\text{flow}/\text{capacity}} v$. In this example: $A\xrightarrow{15/20}B$, $B\xrightarrow{0/5}C$, and $C\xrightarrow{2/7}E$.

![reverse flow](https://drive.google.com/uc?id=1dzddI-CPAhvcn9myWDyybhfaTgVzlUnQ)

The same information can be shown in the *residual graph*. Initially, the residual graph is identical to the input graph. Once we start sending flow across the input graph, we use the dual notation shown above. **In the residual graph, we use capacities only to describe things;** for example:

$$
\underbrace{A\xrightarrow{5/20}B}_\text{input graph} =
\color{green}{\underbrace{\color{green}{A\xrightarrow{15}B,\ \text{and} \ B\xrightarrow{5}A}}_{\text{residual graph}}}
$$

This is important: we do not show flows in the residual graph. Only capacities. The notation $A\xrightarrow{5/20}B$ in the original graph indicates that across an edge with capacity 20, we are sending a flow of 5. This is effectively leaving a capacity of 15 for further use. This capacity is snown as the residual capacity
$\color{green}{A\xrightarrow{15}B}$
of the corresponding edge in the residual graph. The flow from the input graph is represented as the capacity of a new edge pointing in the opposite direction:
$\color{green}{B\xrightarrow{5}A}$

Knowing that we do not show flows in the residual graph is important because it explains how we find the maximum flow along a path. The maximum flow along a path in the residual graph is the minimum capacity along it. For example, in the path $\color{green}{A\rightarrow B\rightarrow C\rightarrow E}$ at the initialized residual graph, the corresponding capacities are

\begin{align}
  \color{green}{c_f(A\rightarrow B)} &\  \color{green}{= 20}& \\
  \color{green}{c_f(B\rightarrow C)} &\ \color{green}{= 5}& \\
  \color{green}{c_f(C\rightarrow E)} &\ \color{green}{= 7}&
\end{align}

The minimum capacity along the path is 5 and therefore that's as much flow as we can push through this path. When we push that flow along the path (in the actual (input) graph), the capacities in the residual graph are adjusted to indicate the newly available capacities:

\begin{align}
  \color{green}{c_f(A\rightarrow B)} &\  \color{green}{= 15}& \\
  \color{grey}{c_f(B\rightarrow C)} &\ \color{grey}{= 0}& \\
  \color{green}{c_f(C\rightarrow E)} &\ \color{green}{= 2}&
\end{align}

We also add a new edge in the residual graph with capacity that corresponds to the flow that saturated edge $B\rightarrow C$. This new edge has an opposite direction from the saturated edge.
$$
  \color{green}{c_f(C\rightarrow B)}  \color{green}{= 5} \\
$$

A fundemental property of flows, the skew symmetry, defines $f(a,b) = -f(b,a)$, i.e., the flow over an edge $a→b$ is the opposite of the flow in the opposite direction.

Using the skew symmetry, we can write the residual capacity of an edge $u→v$ in the *residual graph,* between successive iterations $t$ and $t+1$ as follows:

\begin{equation}
{}^{t+1}c_f(u,v) = \begin{cases}
{}^{t}c_f(u,v) -f(u,v),\ &\text{if edge}\ u\rightarrow v\ \text{exists} \\
\color{red}{-}f(u,\color{red}{v}) = f(\color{red}{v},u),\ &\text{if edge}\ u\rightarrow v\ \text{does not exist, but edge}\  v\rightarrow u\ \text{exists} \\
0,\ &\text{otherwise}
\end{cases}
\end{equation}

The initial condition above is $^0c_f(u,v) = c(u,v)$.

The first case above is straight-forward. The residual capacity of an edge with a flow, is its initial capacity minus the flow. The middle case appears counter-intuitive: if there is no edge $u\rightarrow v$, but there is an edge in the opposite direction $v\rightarrow u$, the residual capacity $c_f(\color{blue}{u}\rightarrow \color{green}{v})$ is the flow in the opposite direction $f(\color{green}{v}\rightarrow\color{blue}{u})$.

The expression for the capacity of a non-existing edge, when the opposite edge exists, is based on the definition of residual capacity and the skew symmetry. i.e.,

\begin{align}
{}^{t+1}c_f(u,v) & = {}^{t}c(u,v) - f(u,v) && \text{definition of residual flow}  \\
         & = 0 - f(u,v) && u\rightarrow v\ \text{is saturated}  \\
         & = -(-f(v,u)) && \text{skew symmetry}  \\
         & = f(v,u)
\end{align}

It is important to remember that residual capacities exist only in the residual graph. In the original graph, flow and capacity are shown together. For example, in figure (a) below, the edge $u→v$ has a capacity of 18 and currently accomodates a flow of 5. It is up to us to deduce that the remaining capacity along the edge $u→v$ is $18-5$.

![reverse flow](https://drive.google.com/uc?id=1_UHrhQf8S_u3IV6yv7YjdP89okm1vSVc)

Figure (b) above shows the same situation but in the residual graph, using residual *capacities*. There are no flows shown in the residual graph. Instead, we see capacities, suggesting the potential for flow. In this case, the edge $u→v$ has a capacity 13. There is also capacity 5 in the opposite direction, mirroring the flow we had in figure (a) above.

## The challenge

A flow graph is just like any other graph, except that instead of weights edges are characterized by flow capacities. In that respect, a flow graph is represented by an adjacency matrix, where `G[u][v]` is now the capacity of the edge from $u$ to $v$.

The residual graph comprises edges with positive residual capacity. If the original flow network is $G=(V,E)$, the residual network is $G_f=(V,E_f)$. The two networks have the same vertices, and, initially, the same edges.

Next, we focus our attention to the residual graph $G_f = (V, E_f)$. This graph has the same vertices as graph $G$. Therefore, the source $s$ and the target $t$ vertex are present in the residual network. The question, now, is: does a path $s\rightsquigarrow t$ exist in the residual graph? Such a path, from source to target is called an augmenting path (calling it just a path would be boring).

The flow we can send along the augmenting path, is limited by its edge with the least capacity.

## Wrapping up

The Ford-Fulkerson method takes a graph $G=(V, E)$, finds its residual graph $G_f=(V,E_f)$, and determines if there is a path $s\rightsquigarrow t$ in it.

If there is a path $s\rightsquigarrow t$ in the residual graph, the method finds how much flow the path can take. To find that flow, the method needs to find the edge, along the path, with the least capacity. The capacity of that edge is maximum flow of that path. It is added to the maximum flow of the graph. We expect that the edge with the least capacity will be saturated.

The method then recomputes residual capacities in the residual graph, removing edges (such as the one that just got saturated), and looks for a new $s\rightsquigarrow t$ path.

When there is no $s\rightsquigarrow t$ path, the method ends. The maximum flow value we've been computing all along, is the maximum flow that the initial graph $G$ can carry.

## A note on saturated edges

An edge is saturated when it carries as much flow as it can. In the input graph, a saturated edge is shown with a flow equal to its capacity. For example, look at figure (a) below.


![residual capacity](https://drive.google.com/uc?id=1_YbTm3E0viNoLPJMZZgoRIRFnreskPhM)

The same information is shown a bit differently in the residual graph. Remember that the residual graph shows only capacities -- flows are implied but not shown. In figure (b) above, the saturated edge is shown with 0 capacity. However there is a back edge $v→u$ with capacity 18. That back edge essentially indicates what the maximum capacity of edge $u→v$ could be.


If we saturate that edge, the skew symmetry property tells us, we'll reestablish a capacity of 18 from $u$ to $v$, as shown in figure (c) above.

## Building it

Implementing Ford-Fulkerson requires several tasks.

* Determine the presence of a path between two vertices in a graph. This is needed to tell if there is an augmenting path in the residual graph. In other words: is the target vertex reachable from the source vertex in the residual graph?

* In the augmenting path, find the edge with the least capacity. Its capacity determines how much flow can be sent through the augmenting path. This requires that we remember, somehow, the edges in the path. In general, a path $s\rightsquigarrow t$ can be reconstructed if we keep track of each vertices' parent. For example, in the path
$v_0 → v_1 → v_2 → v_3 → v_4$, the parent of $v_4$ is $v_3$, the parent of $v_3$ is $v_2$, and so on. The vertex whose parent is `null` is the first vertex of the path.

* The steps above presuppose that we have a way to assemble and manipulate the residual graph. At the beginning, we assume that the residual graph is the same as the input graph. Then, as long as there is an augmenting path in the residual graph, we adjust its edges to capture available capacities (with back edges used as described earlier).

## Step-by-step example

Consider the following graph, with vertices $A$ and $E$ the source and the target vertices respectively.

![flow network input](https://drive.google.com/uc?id=1_cB9RfxlF1gZbWDovD2MQAk-bu9AH4jU)

Our first step is to create a copy of it, designating it the residual graph. By definition, all capacities shown in the residual graph are called residual capacities.

![flow network step 1](https://drive.google.com/uc?id=1_cYHM-nBJgGUeTBbvSxv0u93ks4ojhX8)

Next, in the residual graph, we find a path (any path) from $A$ to $E$:

![flow network step 2](https://drive.google.com/uc?id=1_d9NyHdNuHebwYR2o-8pvt9zZGbViFxh)

In the path identified above, the smallest residual capacity is 3. That's the maximum flow we can send down the path $A→B→C→D→E$. We make a note of it and adjust the residual capacities accordingly, in step 3. This introduces four new edges in the residual graph: $B→A$, $C→B$, $D→C$, and $E→D$, all with residual capacity 3.

![flow network steps 3 and 4](https://drive.google.com/uc?id=1_m58WQjbqNfDqU3NmOs0vAJFhZ7O6oJ3)

Notice in the revised residual graph of step 3 above, the edge $C→D$ is saturated. The residual capaciy $c_f(C→D)$ is 0.

It is time to find if there is another path from $A$ to $E$ in the residual graph. This is shown in step 4 above. For clarity, I have removed the saturated edge of the previous step. And there is indeed a path, $A→B→C→E$. In this path, the smallest residual capacity is 2. That's the maximum flow we can send down the path. We make a note of it and adjust the residual capacities accordingly, as shown in step 5 below.

![flow network steps 5 and 6](https://drive.google.com/uc?id=1_tnLkeg78MmGhABNU9d_-2mPbMyg3N9-)

Additional capacity (equal to the flow permitted along $A→B→C→E$) is added to the back edges $B\rightarrow A$ and $C→B$. Also, a new edge $E→C$ is introduced with residual capacity 2 (equal the flow we are sending down $A→B→C→E$).

In this residual graph, we must now repeat the search for a path from $A$ to $E$. This is shown in step 6 above where, again, the saturated edge from the previosu step is removed for clarity. The new path we find is $A→B→D→C→E$. The smallest capacity along that path is at the edge $D→C$: 3. This is an edge that does not exist in the actual graph. It was introduced in the *residual graph*, in step 3 earlier.

In step 7, below, we saturate $D\rightarrow C$ and adjust residual capacities accordingly. Then in step 8, we find another path from source ($A$) to target ($E$).

![flow network steps 7 and 8](https://drive.google.com/uc?id=1a489O48OSugEow7a_0wq2ebo3UgTf6TL)

In the path found in step 8 above, the most flow we can accommodate is limited by the capacity of edge $B→D$. We make a note of it and adjust the residual capacities accordingly, as shown in step 9 below.

![flow network steps 5 and 6](https://drive.google.com/uc?id=1a5uxe6MgBiZpFq5fQA5PZ3-BInus24bf)

The resulting residual graph, in step 10, has no more paths from $A$ to $E$, and our process stops. The maximum path flows we found along the way were 3, 2, 3, and 3. Added together, they represent the maximum flow we can send from $A$ to $E$ in the input graph.

## Assignment

Study the code below that computes the maximum flow in a graph using the Ford-Fulkerson process. The input graph is represented by an adjacency matrix.

Then develop a method that identifies the minimum cut for this graph. To accomplish this you need to consider the final state of our example graph above, in step 10.

We arrive to that final state after the `while augmenting_path` loop in method `ff` below ends. At that moment, there is no source-to-target path in the *residual graph.* Effectively the residual graph has been divided into two parts: one with all the vertices reachable from the source vertex and one with all the vertices can are not reachable from it. Any edge across these two parts, is an edge in the minimum cut of the graph. We can find these edges, by finding all the vertices in the residual graph that can be reached from the source vertex.

In the test graph (which represents the graph of the earlier example), the minimum cut comprises edges $B\rightarrow C$ and $B\rightarrow D$. (Identified as `[1,2]` and `[1,3]` using their adjacency matrix indices). Their total capacity is 11 which is also the max flow across the input graph.
"""

# Test graph, expect max flow = 11

G = [#  A   B   C   D   E
     [  0, 20,  0,  0,  0], # A
     [  0,  0,  5,  6,  0], # B
     [  0,  0,  0,  3,  7], # C
     [  0,  0,  0,  0,  8], # D
     [  0,  0,  0,  0,  0]  # E
]

import copy # to make deep copy


def find_path(graph, source, target, path):
  """Finds a path between two vertices in a directed acyclic graph.

  Inputs
  ------
  graph : list
    adjacency matrix of the graph to search
  source, target : int
    The two vertices at both ends of the path
  path : list
    path from previous recursive call; [] for initial call

  Returns
  -------
  path : list
    vertices along the path from source to vertex; None if path doesn't exist.
  """
  # The source is always part of the path
  path.append(source)

  # Base case
  if source == target:
    return path

  # Consider every vertex adjacent to the source; because we use adjacency
  # matrix representation, we examine the row corresponding to the source
  # vertex: graph[source]. Every element in that row that is not zero represents
  # an edge. If the vertex on the other side of that edge is not already in the
  # path, we add it to the path. Then we ask if there is a parth from that
  # vertex to the target vertex.
  for v in range(len(graph)):
    if graph[source][v] > 0:
      if v not in path:
        possible_path = find_path(graph, v, target, path)
        if possible_path:
          return path
  return None


def ff(graph, source, target):
  """Finds the maximum flow across a flow graph and identifies the minimum cuts
  that will disable the flow between a source and a target vertex in the graph.

  Inputs
  ------
  graph : list
    adjacency matrix of the input graph
  source : int
    label of the source vertex
  target : int
    label of the target vertex

  Returns
  -------
  max_flow : int
    The max flow can can travel from source to target in the input graph
  min_cuts : list
    The small set of edges that can reduce the graph's flow to 0.
  """

  # Variable to return
  max_flow = 0

  # Initially, the residual graph is identical to the input graph
  residual_graph = copy.deepcopy(graph)

  # Find an augmenting path; any such path is fine, to get the iteration loop
  # started. The loop continues as long as there is an augmenting path in the
  # residual graph. (Reminder: an augmenting path in the residual graph is a
  # path from the source to the target vertex).
  augmenting_path = find_path(residual_graph, source, target, [])

  while augmenting_path:

    # Find the edge with the least capacity along this path. Edges can be
    # identified by the elements of augmenting_path: adjacent elements of the
    # list are the vertices on that edge, e.g., an edge u --> v in the path will
    # have u = augmenting_path[i] and
    #      v = augmenting_path[i+1]
    # This is a standard search for a min value in a collection of values. It
    # begins by assuming that the first edge in the augmenting path has the least
    # capacity of the path. That edge is between the vertices in positions [0]
    # and [1] in the augmenting_path list. The weight of their edge is obtained
    # by referencing the residual_graph list for these two vertices. Then we
    # traverse the remaining edges in the augmenting path in to see if there is
    # one with less capacity.
    min_capacity = residual_graph[augmenting_path[0]][augmenting_path[1]]
    i = 1
    while i < len(augmenting_path)-1: # -1 to compensate for [i+1] below
      # Obtain vertices u, v for edge u --> v in augmenting path
      u = augmenting_path[i]
      v = augmenting_path[i+1]
      if residual_graph[u][v] < min_capacity:
        min_capacity = residual_graph[u][v]
      i += 1

    # Now that we know the bottleneck of the augmenting path, we can add its
    # capacity to the max flow of the graph, because that's as much flow as we
    # can push through this path.
    max_flow += min_capacity

    # Update residual capacities along the augmenting path. This is done by
    # traversing the augmenting path (yes, again), subtracting the path's
    # minimum capacity from its existing edges, and adding back-edges where
    # necessary based on the skew symmetry property.
    i = 0
    while i < len(augmenting_path)-1: # -1 to compensate for [i+1] below
      # Obtain vertices u, v for edge u --> v in augmenting path
      u = augmenting_path[i]
      v = augmenting_path[i+1]
      residual_graph[u][v] -= min_capacity # existing edge
      residual_graph[v][u] += min_capacity # back-edge due to skew symmetry
      i += 1

    # Now that the residual graph has been updated let's see if there is another
    # path between source and target. If None, the while loop ends.
    augmenting_path = find_path(residual_graph, source, target, [])

  # Done
  return max_flow

def bfs_reachable_nodes(graph, source):
    """Find all nodes reachable from the source in a residual graph."""
    visited = [False] * len(graph)  # Track visited nodes
    queue = [source]  # Start with the source node
    visited[source] = True  # Mark source as visited

    while queue:
        u = queue.pop(0)  # Get the next node
        for v in range(len(graph)):  # Check all edges from u
            if graph[u][v] > 0 and not visited[v]:  # If capacity exists and v not visited
                queue.append(v)  # Add v to the queue
                visited[v] = True  # Mark v as visited

    return visited  # Return all reachable nodes

def find_min_cut(graph, residual_graph, source):
    """Find the edges in the minimum cut after the max flow is computed."""
    reachable = bfs_reachable_nodes(residual_graph, source)  # Get reachable nodes
    min_cut = []  # Store min cut edges

    for u in range(len(graph)):  # For every node u
        for v in range(len(graph)):  # Check all edges from u
            # If u is reachable and v is not, it's a min-cut edge
            if reachable[u] and not reachable[v] and graph[u][v] > 0:
                min_cut.append((u, v))  # Add edge to min cut

    return min_cut  # Return the min cut edges

def ff_with_min_cut(graph, source, target):
    """Finds max flow and minimum cut in a flow network."""
    max_flow = 0  # Initialize max flow

    residual_graph = copy.deepcopy(graph)  # Start with the same graph for residuals

    augmenting_path = find_path(residual_graph, source, target, [])  # Find first path

    while augmenting_path:  # While a path exists
        # Find the minimum capacity in the augmenting path
        min_capacity = residual_graph[augmenting_path[0]][augmenting_path[1]]
        i = 1
        while i < len(augmenting_path) - 1:  # Traverse the path
            u = augmenting_path[i]
            v = augmenting_path[i + 1]
            if residual_graph[u][v] < min_capacity:
                min_capacity = residual_graph[u][v]  # Update min capacity
            i += 1

        max_flow += min_capacity  # Add flow

        # Update residual capacities and add back-edges
        i = 0
        while i < len(augmenting_path) - 1:
            u = augmenting_path[i]
            v = augmenting_path[i + 1]
            residual_graph[u][v] -= min_capacity  # Reduce capacity on forward edge
            residual_graph[v][u] += min_capacity  # Increase capacity on backward edge
            i += 1

        augmenting_path = find_path(residual_graph, source, target, [])  # Find new path

    min_cut = find_min_cut(graph, residual_graph, source)  # Find the min cut

    return max_flow, min_cut  # Return max flow and min cut

# Example Test Graph (same as in the assignment)
G = [  # A   B   C   D   E
     [  0, 20,  0,  0,  0],  # A
     [  0,  0,  5,  6,  0],  # B
     [  0,  0,  0,  3,  7],  # C
     [  0,  0,  0,  0,  8],  # D
     [  0,  0,  0,  0,  0]   # E
]

# Run the function
max_flow, min_cut = ff_with_min_cut(G, 0, 4)  # A is 0, E is 4
print("Max Flow:", max_flow)
print("Min Cut:", min_cut)