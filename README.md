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

Figure (b) above shows the same situation but in the residual graph, using residual *capacities*. There are no flows shown in the residual graph. Instead, we see capacities, suggesting the potential for flow. In this case, the edge $u→v$ has a capacity 13. There is also capacity 5 in the opposite direction, mirroring the flow we had in figure (a) above.## The challenge

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


If we saturate that edge, the skew symmetry property tells us, we'll reestablish a capacity of 18 from $u$ to $v$, as shown in figure (c) above.## Building it

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
