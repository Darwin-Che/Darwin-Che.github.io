---
blogpost: true
date: 2022-07-25
tags: ["algo","graph"]
category: Blog
author: myself
---

# Graph Algo

## BFS / DFS

For DFS, exists recursive approach (use a boolean array to store the visited nodes to avoid cycles), think about how to adjust for disconnected graph

```c++
DFS (int v) {
  visited[v] = true;
  cout << v << " ";
  
  list<int>::iterator it;
  for (it = adj[v].begin(); it != adj[v].end(); ++it) {
    if (!visited[*it]) DFS(*i);
  }
}
```

For BFS, use iterative approach by applying queue/list

```c++
BFS (int v) {
	bool visited[] = new bool[V];
  for (int i = 0; i < V; ++i) visited[i] = false;
  
  list<int> queue;
  
  visited[v] = true;
  queue.push_back(s);
  list<int>::iterator it;
  
  while (!queue.empty()) {
    v = queue.front();
    cout << v << " ";
    queue.pop_front();
    
    for (it = adj[v].begin(); it != adj[v].end(); ++it) {
      if (!visited[*it]) {
        visited[*it] = true;
        queue.push_back(*it);
      }
    }
  }
}
```

What about DFS iterative approach? just use the back of the list every time.

### DFS Disconnected

```c++
void Graph::DFSUtil(int v)
{
    // Mark the current node as visited and print it
    visited[v] = true;
    cout << v << " ";
 
    // Recur for all the vertices adjacent to this vertex
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i)
        if (!visited[*i])
            DFSUtil(*i);
}
 
// The function to do DFS traversal. It uses recursive
// DFSUtil()
void Graph::DFS()
{
    // Call the recursive helper function to print DFS
    // traversal starting from all vertices one by one
    for (auto i:adj)
        if (visited[i.first] == false)
            DFSUtil(i.first);
}
```



## Topoligical Sort

Topological sorting for Directed Acyclic Graph (DAG) is a linear  ordering of vertices such that for every directed edge u v, vertex u  comes before v in the ordering.  (There can be multiple valid orders)

### Modification of DFS for disconnected

```c++
// A recursive function used by topologicalSort
void Graph::topologicalSortUtil(int v, bool visited[],
                                stack<int>& Stack)
{
    // Mark the current node as visited.
    visited[v] = true;
 
    // Recur for all the vertices
    // adjacent to this vertex
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i)
        if (!visited[*i])
            topologicalSortUtil(*i, visited, Stack);
 
    // Push current vertex to stack
    // which stores result
    Stack.push(v);
}
 
// The function to do Topological Sort.
// It uses recursive topologicalSortUtil()
void Graph::topologicalSort()
{
    stack<int> Stack;
 
    // Mark all the vertices as not visited
    bool* visited = new bool[V];
    for (int i = 0; i < V; i++)
        visited[i] = false;
 
    // Call the recursive helper function
    // to store Topological
    // Sort starting from all
    // vertices one by one
    for (int i = 0; i < V; i++)
        if (visited[i] == false)
            topologicalSortUtil(i, visited, Stack);
 
    // Print contents of stack
    while (Stack.empty() == false) {
        cout << Stack.top() << " ";
        Stack.pop();
    }
}
```

### Kahn’s algorithm

This is iterative algorithm but has same time/space vs DFS

**Algorithm:** Steps involved in finding the topological ordering of a DAG:

**Step-1:** Compute in-degree (number of incoming edges) for each of the vertex  present in the DAG and initialize the count of visited nodes as 0.

**Step-2:** Pick all the vertices with in-degree as 0 and add them into a queue (Enqueue operation)

**Step-3:** Remove a vertex from the queue (Dequeue operation) and then.

1. Increment count of visited nodes by 1.
2. Decrease in-degree by 1 for all its neighboring nodes.
3. If in-degree of a neighboring nodes is reduced to zero, then add it to the queue.

**Step 4:** Repeat Step 3 until the queue is empty.

**Step 5:** If count of visited nodes is **not** equal to the number of nodes in the graph then the topological sort is not possible for the given graph.

**How to find in-degree of each node?**
There are 2 ways to calculate in-degree of every vertex:

1. Take an in-degree array which will keep track of

   Traverse the array of edges and simply increase the counter of the destination node by 1.

   ```c++
   for each node in Nodes
       indegree[node] = 0;
   for each edge(src, dest) in Edges
       indegree[dest]++
   ```

   Time Complexity: O(V+E)

2. Traverse the list for every node and then increment the in-degree of all the nodes connected to it by 1.

   ```c++
       for each node in Nodes
           if (list[node].size()!=0) then
           for each dest in list
               indegree[dest]++;
   ```

   Time Complexity: The outer for  loop will be executed V number of times and the inner for loop will be  executed E number of times, Thus overall time complexity is O(V+E).

   The overall time complexity of the algorithm is O(V+E)

```c++
void Graph::topologicalSort()
{
    // Create a vector to store
    // indegrees of all
    // vertices. Initialize all
    // indegrees as 0.
    vector<int> in_degree(V, 0);
  
    // Traverse adjacency lists
    // to fill indegrees of
    // vertices.  This step
    // takes O(V+E) time
    for (int u = 0; u < V; u++) {
        list<int>::iterator itr;
        for (itr = adj[u].begin();
             itr != adj[u].end(); itr++)
            in_degree[*itr]++;
    }
  
    // Create an queue and enqueue
    // all vertices with indegree 0
    queue<int> q;
    for (int i = 0; i < V; i++)
        if (in_degree[i] == 0)
            q.push(i);
  
    // Initialize count of visited vertices
    int cnt = 0;
  
    // Create a vector to store
    // result (A topological
    // ordering of the vertices)
    vector<int> top_order;
  
    // One by one dequeue vertices
    // from queue and enqueue
    // adjacents if indegree of
    // adjacent becomes 0
    while (!q.empty()) {
        // Extract front of queue
        // (or perform dequeue)
        // and add it to topological order
        int u = q.front();
        q.pop();
        top_order.push_back(u);
  
        // Iterate through all its
        // neighbouring nodes
        // of dequeued node u and
        // decrease their in-degree
        // by 1
        list<int>::iterator itr;
        for (itr = adj[u].begin();
             itr != adj[u].end(); itr++)
  
            // If in-degree becomes zero,
            // add it to queue
            if (--in_degree[*itr] == 0)
                q.push(*itr);
  
        cnt++;
    }
  
    // Check if there was a cycle
    if (cnt != V) {
        cout << "There exists a cycle in the graph\n";
        return;
    }
  
    // Print topological order
    for (int i = 0; i < top_order.size(); i++)
        cout << top_order[i] << " ";
    cout << endl;
}
```



## Floyd cycle detection