---
blogpost: true
date: 2022-07-25
tags: ["algo","algebra"]
category: Blog
author: myself
---

# Data Structures

## Minimum stack / Minimum queue

In this article we will consider three problems:  first we will modify a stack in a way that allows us to find the smallest element of the stack in *O*(1), then we will do the same thing with a queue, and finally we will use  these data structures to find the minimum in all subarrays of a fixed  length in an array in *O*(*n*)

### Stack modification

To do this, we will not only store the elements in the stack, but we  will store them in pairs: the element itself and the minimum in the  stack starting from this element and below.

```cpp
stack<pair<int, int>> st;

// add element
int new_min = st.empty() ? new_elem : min(new_elem, st.top().second);
st.push({new_elem, new_min});

// remove element
int removed_element = st.top().first;
st.pop();

// find minimum
int minimum = st.top().second;
```

## Queue modification (method 1)

Drawback: 

```cpp
deque<int> q;

// add element
while (!q.empty() && q.back() > new_element)
    q.pop_back();
q.push_back(new_element);

// remove element
if (!q.empty() && q.front() == remove_element)
    q.pop_front();

// find minimum
int minimum = q.front();
```

### Queue modification (method 2)

```cpp
deque<pair<int, int>> q;
int cnt_added = 0;
int cnt_removed = 0;

// add element
while (!q.empty() && q.back().first > new_element)
    q.pop_back();
q.push_back({new_element, cnt_added});
cnt_added++;

// remove element
if (!q.empty() && q.front().second == cnt_removed) 
    q.pop_front();
cnt_removed++;

// find minimum
int minimum = q.front().first;
```

### Queue modification (method 3)

Implement a queue with two stacks

```cpp
stack<pair<int, int>> s1, s2;

// add element
int minimum = s1.empty() ? new_element : min(new_element, s1.top().second);
s1.push({new_element, minimum});

// remove element
if (s2.empty()) {
    while (!s1.empty()) {
        int element = s1.top().first;
        s1.pop();
        int minimum = s2.empty() ? element : min(element, s2.top().second);
        s2.push({element, minimum});
    }
}
int remove_element = s2.top().first;
s2.pop();

// find minimum
if (s1.empty() || s2.empty()) 
    minimum = s1.empty() ? s2.top().second : s1.top().second;
else
    minimum = min(s1.top().second, s2.top().second);
```

### Finding the minimum for all subarrays of fixed length

Can use any of the minimum queue implementations

## Sparse Table

Sparse Table is a data structure, that allows answering range queries. It can answer most range queries in *O*(log*n*), but its true power is answering range minimum queries (or equivalent range maximum queries). For those queries it can compute the answer in *O*(1) time.

The only drawback of this data structure is, that it can only be used on *immutable* arrays. This means, that the array cannot be changed between two queries. If any element in the array changes, the complete data structure has to be recomputed.

The main idea behind Sparse Tables is to precompute all answers for  range queries with power of two length. Afterwards a different range query can be answered by splitting the  range into ranges with power of two lengths, looking up the precomputed  answers, and combining them to receive a complete answer.

### Precomputation

We will use a 2-dimensional array for storing the answers to the precomputed queries. st[*i*][*j*] will store the answer for the range [*i*,*i*+2^*j*−1] of length 2^*j*. The size of the 2-dimensional array will be MAXN×(*K*+1), where MAXN is the biggest possible array length. K has to satisfy K≥⌊log2MAXN⌋, because 2⌊log2MAXN⌋ is the biggest power of two range, that we have to support. For arrays with reasonable length (≤107 elements), *K*=25 is a good value.

Because the range [*i*,*i*+2^*j*−1] of length 2^*j* splits nicely into the ranges [*i*,*i*+2^{*j*−1}−1] and [*i*+2^{*j*−1},*i*+2^*j*−1], both of length 2^{*j*−1}, we can generate the table efficiently using dynamic programming:

```cpp
int st[MAXN][K + 1];

for (int i = 0; i < N; i++)
    st[i][0] = f(array[i]);

for (int j = 1; j <= K; j++)
    for (int i = 0; i + (1 << j) <= N; i++)
        st[i][j] = f(st[i][j-1], st[i + (1 << (j - 1))][j - 1]);
```

### Range Sum Queries

For this type of queries, we want to find the sum of all values in a range. Therefore the natural definition of the function *f* is *f*(*x*,*y*)=*x*+*y*. We can construct the data structure.

To answer the sum query for the range [*L*,*R*], we iterate over all powers of two, starting from the biggest one. As soon as a power of two 2*j* is smaller or equal to the length of the range (=*R*−*L*+1), we process the first the first part of range [*L*,*L*+2*j*−1], and continue with the remaining range [*L*+2*j*,*R*].

```cpp
long long sum = 0;
for (int j = K; j >= 0; j--) {
    if ((1 << j) <= R - L + 1) {
        sum += st[L][j];
        L += 1 << j;
    }
}
```

Time complexity for a Range Sum Query is *O*(*K*)=*O*(logMAXN).

### Range Minimum Queries (RMQ)

These are the queries where the Sparse Table shines. When computing the minimum of a range, it doesn't matter if we process a value in the range once or twice. Therefore instead of splitting a range into multiple ranges, we can also split the range into only two overlapping ranges with power of two  length. E.g. we can split the range [1,6] into the ranges [1,4] and [3,6]. The range minimum of [1,6] is clearly the same as the minimum of the range minimum of [1,4] and the range minimum of [3,6]. So we can compute the minimum of the range [*L*,*R*] with:min(st[*L*][*j*],st[*R*−2*j*+1][*j*]) where *j*=log2(*R*−*L*+1)

```cpp
// precompute logs
int log[MAXN+1];
log[1] = 0;
for (int i = 2; i <= MAXN; i++)
    log[i] = log[i/2] + 1;

// precompute of sparse table
int st[MAXN][K + 1];

for (int i = 0; i < N; i++)
    st[i][0] = array[i];

for (int j = 1; j <= K; j++)
    for (int i = 0; i + (1 << j) <= N; i++)
        st[i][j] = min(st[i][j-1], st[i + (1 << (j - 1))][j - 1]);

// range query O(1)
int j = log[R - L + 1];
int minimum = min(st[L][j], st[R - (1 << j) + 1][j]);
```

One of the main weakness of the *O*(1) approach discussed in the previous section is, that this approach only supports queries of [idempotent functions](https://en.wikipedia.org/wiki/Idempotence). I.e. it works great for range minimum queries, but it is not possible to answer range sum queries using this approach.

There are similar data structures that can handle any type of associative functions and answer range queries in *O*(1). One of them is called is called [Disjoint Sparse Table](https://discuss.codechef.com/questions/117696/tutorial-disjoint-sparse-table). Another one would be the [Sqrt Tree](https://cp-algorithms.com/data_structures/sqrt-tree.html).

This node stores precomputed values of

$F(A[i…M])∣i∈[L,M]$ and 

$F(A[M+1…i])∣i∈[M+1,R) $​

So size of node is equal to R−L. If its size>1 then it has two children corresponding to [L,M) and [M,R).

## Disjoint Set Union

This article discusses the data structure **Disjoint Set Union** or **DSU**. Often it is also called **Union Find** because of its two main operations.

This data structure provides the following capabilities. We are given several elements, each of which is a separate set. A DSU will have an operation to combine any two sets, and it will be able to tell in which set a specific element is. The classical version also introduces a third operation, it can create a set from a new element.

### Naive implementation $O(n)$

```cpp
void make_set(int v) {
    parent[v] = v;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return find_set(parent[v]);
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b)
        parent[b] = a;
}
```

### Path compression optimization $O(\log n)$

```cpp
int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}
```

### Union by size / rank $O(\log n)$

```cpp
void make_set(int v) {
    parent[v] = v;
    size[v] = 1;
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (size[a] < size[b])
            swap(a, b);
        parent[b] = a;
        size[a] += size[b]; // rank[a] ++; if rank[a] = rank[b]
    }
}
```

Combining we get $O(\alpha(n))$.

### Linking by index / coin-flip linking

You can find a proof of the complexity and even more union techniques [here](http://www.cis.upenn.edu/~sanjeev/papers/soda14_disjoint_set_union.pdf).

```cpp
void make_set(int v) {
    parent[v] = v;
    index[v] = rand();
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (index[a] < index[b])
            swap(a, b);
        parent[b] = a;
    }
}
```

It's a common misconception that just flipping a coin, to decide which set we attach to the other, has the same complexity. However that's not true. And in benchmarks it performs a lot worse than union by size/rank or linking by index.

### Applications

#### Connected components in a graph

Formally the problem is defined in the following way: Initially we have an empty graph. We have to add vertices and undirected edges, and answer queries of the form (*a*,*b*) - "are the vertices *a* and *b* in the same connected component of the graph?"

$O(m \log n)$

#### Search for connected components in an image

#### Store additional information for each set

DSU allows you to easily store additional information in the sets.

A simple example is the size of the sets: storing the sizes was already described in the Union by size section  (the information was stored by the current representative of the set).

In the same way - by storing it at the representative nodes - you can also store any other information about the sets.

#### Compress jumps along a segment / Painting subarrays offline

One common application of the DSU is the following: There is a set of vertices, and each vertex has an outgoing edge to  another vertex. With DSU you can find the end point, to which we get after following all edges from a given starting point, in almost constant time.

#### Compress jumps along a segment / Painting subarrays offline

One common application of the DSU is the following: There is a set of vertices, and each vertex has an outgoing edge to  another vertex. With DSU you can find the end point, to which we get after following all edges from a given starting point, in almost constant time.

A good example of this application is the **problem of painting subarrays**. We have a segment of length *L*, each element initially has the color 0. We have to repaint the subarray [*l*,*r*] with the color *c* for each query (*l*,*r*,*c*). At the end we want to find the final color of each cell. We assume that we know all the queries in advance, i.e. the task is offline.

For the solution we can make a DSU, which for each cell stores a link to the next unpainted cell. Thus initially each cell points to itself. After painting one requested repaint of a segment, all cells from that segment will point to the cell after the segment.

Now to solve this problem, we consider the queries **in the reverse order**: from last to first. This way when we execute a query, we only have to paint exactly the unpainted cells in the subarray [*l*,*r*]. All other cells already contain their final color. To quickly iterate over all unpainted cells, we use the DSU. We find the left-most unpainted cell inside of a segment, repaint it,  and with the pointer we move to the next empty cell to the right.

Here we can use the DSU with path compression, but we cannot use  union by rank / size (because it is important who becomes the leader  after the merge). Therefore the complexity will be *O*(log*n*) per union (which is also quite fast).

```cpp
for (int i = 0; i <= L; i++) {
    make_set(i);
}

for (int i = m-1; i >= 0; i--) {
    int l = query[i].l;
    int r = query[i].r;
    int c = query[i].c;
    for (int v = find_set(l); v <= r; v = find_set(v)) {
        answer[v] = c;
        parent[v] = v + 1;
    }
}
```

There is one optimization: We can use **union by rank**, if we store the next unpainted cell in an additional array `end[]`. Then we can merge two sets into one ranked according to their heuristics, and we obtain the solution in *O*(*α*(*n*)).

#### Support distances up to representative

## Fenwick Tree

Fenwick tree is a data structure which:

- calculates the value of function *f* in the given range [*l*,*r*] (i.e. *f*(*A**l*,*A**l*+1,…,*A**r*)) in *O*(log*n*) time;
- updates the value of an element of *A* in *O*(log*n*) time;requires *O*(*N*) memory, or in other words, exactly the same memory required for *A*;
- is easy to use and code, especially, in the case of multidimensional arrays.

Fenwick tree is also called **Binary Indexed Tree**, or just **BIT** abbreviated.

$T_i = \sum_{g(i)}^i A[i]$

```python
def sum(int r):
    res = 0
    while (r >= 0):
        res += t[r]
        r = g(r) - 1
    return res

def increase(int i, int delta):
    for all j with g(j) <= i <= j:
        t[j] += delta
```

If $g(i) = i$, $T = A$, so sum will be slow. 

If $g(i) = 0$, $T$ is presum, so update will be slow.

### Definition

replace all trailing 1 bits in the binary representation of *i* with 0 bits.

$g(i) = i\ \&\ (i+1)$​

flipping the last unset bit

$h(i) = i \ \|\ (i+1)$

### Implementation

```cpp
struct FenwickTree {
    vector<int> bit;  // binary indexed tree
    int n;

    FenwickTree(int n) {
        this->n = n;
        bit.assign(n, 0);
    }

    FenwickTree(vector<int> a) : FenwickTree(a.size()) {
        for (size_t i = 0; i < a.size(); i++)
            add(i, a[i]);
    }

    int sum(int r) {
        int ret = 0;
        for (; r >= 0; r = (r & (r + 1)) - 1)
            ret += bit[r];
        return ret;
    }

    int sum(int l, int r) {
        return sum(r) - sum(l - 1);
    }

    void add(int idx, int delta) {
        for (; idx < n; idx = idx | (idx + 1))
            bit[idx] += delta;
    }
};
```

```cpp
struct FenwickTreeMin {
    vector<int> bit;
    int n;
    const int INF = (int)1e9;

    FenwickTreeMin(int n) {
        this->n = n;
        bit.assign(n, INF);
    }

    FenwickTreeMin(vector<int> a) : FenwickTreeMin(a.size()) {
        for (size_t i = 0; i < a.size(); i++)
            update(i, a[i]);
    }

    int getmin(int r) {
        int ret = INF;
        for (; r >= 0; r = (r & (r + 1)) - 1)
            ret = min(ret, bit[r]);
        return ret;
    }

    void update(int idx, int val) {
        for (; idx < n; idx = idx | (idx + 1))
            bit[idx] = min(bit[idx], val);
    }
};
```

Note: it is possible to implement a Fenwick tree that can handle arbitrary minimum range queries and arbitrary updates. The paper [Efficient Range Minimum Queries using Binary Indexed Trees](http://ioinformatics.org/oi/pdf/v9_2015_39_44.pdf) describes such an approach. However with that approach you need to maintain a second binary indexed  trees over the data, with a slightly different structure, since you one  tree is not enough to store the values of all elements in the array. The implementation is also a lot harder compared to the normal  implementation for sums.

```cpp
struct FenwickTree2D {
    vector<vector<int>> bit;
    int n, m;

    // init(...) { ... }

    int sum(int x, int y) {
        int ret = 0;
        for (int i = x; i >= 0; i = (i & (i + 1)) - 1)
            for (int j = y; j >= 0; j = (j & (j + 1)) - 1)
                ret += bit[i][j];
        return ret;
    }

    void add(int x, int y, int delta) {
        for (int i = x; i < n; i = i | (i + 1))
            for (int j = y; j < m; j = j | (j + 1))
                bit[i][j] += delta;
    }
};

```

### One-based indexing approach

For this approach we change the requirements and definition for *T*[] and *g*() a little bit. We want *T*[*i*] to store the sum of [*g*(*i*)+1;*i*]. This changes the implementation a little bit, and allows for a similar nice definition for *g*(*i*):

```cpp
def sum(int r):
    res = 0
    while (r > 0):
        res += t[r]
        r = g(r)
    return res

def increase(int i, int delta):
    for all j with g(j) < i <= j:
        t[j] += delta
```

toggling of the last set 1 bit in the binary representation of *i*.

$g(i) = i - (i \& -i)$

$h(i) = i + (i \& -i)$

```cpp
struct FenwickTreeOneBasedIndexing {
    vector<int> bit;  // binary indexed tree
    int n;

    FenwickTreeOneBasedIndexing(int n) {
        this->n = n + 1;
        bit.assign(n + 1, 0);
    }

    FenwickTreeOneBasedIndexing(vector<int> a)
        : FenwickTreeOneBasedIndexing(a.size()) {
        for (size_t i = 0; i < a.size(); i++)
            add(i, a[i]);
    }

    int sum(int idx) {
        int ret = 0;
        for (++idx; idx > 0; idx -= idx & -idx)
            ret += bit[idx];
        return ret;
    }

    int sum(int l, int r) {
        return sum(r) - sum(l - 1);
    }

    void add(int idx, int delta) {
        for (++idx; idx < n; idx += idx & -idx)
            bit[idx] += delta;
    }
};
```

### Range operations

A Fenwick tree can support the following range operations:

1. Point Update and Range Query
2. Range Update and Point Query
3. Range Update and Range Query

#### 1. Point Update and Range Query

This is just the ordinary Fenwick tree as explained above.

#### 2. Range Update and Point Query

Suppose that we want to increment the interval [*l*,*r*] by *x*. We make two point update operations on Fenwick tree which are `add(l, x)` and `add(r+1, -x)`.

```cpp
// one index
void add(int idx, int val) {
    for (++idx; idx < n; idx += idx & -idx)
        bit[idx] += val;
}

void range_add(int l, int r, int val) {
    add(l, val);
    add(r + 1, -val);
}

int point_query(int idx) {
    int ret = 0;
    for (++idx; idx > 0; idx -= idx & -idx)
        ret += bit[idx];
    return ret;
}
```

#### 3. Range Updates and Range Queries

```python
def add(b, idx, x):
    while idx <= N:
        b[idx] += x
        idx += idx & -idx

def range_add(l,r,x):
    add(B1, l, x)
    add(B1, r+1, -x)
    add(B2, l, x*(l-1))
    add(B2, r+1, -x*r)

def sum(b, idx):
    total = 0
    while idx > 0:
        total += b[idx]
        idx -= idx & -idx
    return total

def prefix_sum(idx):
    return sum(B1, idx)*idx -  sum(B2, idx)

def range_sum(l, r):
    return prefix_sum(r) - prefix_sum(l-1)
```

## Sqrt Decomposition

simplest implementation

```cpp
// input data
int n;
vector<int> a (n);

// preprocessing
int len = (int) sqrt (n + .0) + 1; // size of the block and the number of blocks
vector<int> b (len);
for (int i=0; i<n; ++i)
    b[i / len] += a[i];

// answering the queries
for (;;) {
    int l, r;
  // read input data for the next query
    int sum = 0;
    for (int i=l; i<=r; )
        if (i % len == 0 && i + len - 1 <= r) {
            // if the whole block starting at i belongs to [l, r]
            sum += b[i / len];
            i += len;
        }
        else {
            sum += a[i];
            ++i;
        }
}
```

```cpp
int sum = 0;
int c_l = l / len,   c_r = r / len;
if (c_l == c_r)
    for (int i=l; i<=r; ++i)
        sum += a[i];
else {
    for (int i=l, end=(c_l+1)*len-1; i<=end; ++i)
        sum += a[i];
    for (int i=c_l+1; i<=c_r-1; ++i)
        sum += b[i];
    for (int i=c_r*len; i<=r; ++i)
        sum += a[i];
}
```

### Mo's algorithm

A similar idea, based on sqrt decomposition, can be used to answer range queries (*Q*) offline in *O*((*N*+*Q*)*\sqrtN*). This might sound like a lot worse than the methods in the previous  section, since this is a slightly worse complexity than we had earlier  and cannot update values between two queries. But in a lot of situations this method has advantages. During a normal sqrt decomposition, we have to precompute the answers  for each block, and merge them during answering queries. In some problems this merging step can be quite problematic. E.g. when each queries asks to find the **mode** of its  range (the number that appears the most often). For this each block would have to store the count of each number in it  in some sort of data structure, and we cannot longer perform the merge  step fast enough any more. **Mo's algorithm** uses a completely different approach,  that can answer these kind of queries fast, because it only keeps track  of one data structure, and the only operations with it are easy and  fast.

The idea is to answer the queries in a special order based on the  indices. We will first answer all queries which have the left index in block 0,  then answer all queries which have left index in block 1 and so on. And also we will have to answer the queries of a block is a special  order, namely sorted by the right index of the queries.

As already said we will use a single data structure. This data structure will store information about the range. At the beginning this range will be empty. When we want to answer the next query (in the special order), we simply  extend or reduce the range, by adding/removing elements on both sides of the current range, until we transformed it into the query range. This way, we only need to add or remove a single element once at a time, which should be pretty easy operations in our data structure.

Since we change the order of answering the queries, this is only  possible when we are allowed to answer the queries in offline mode.

```cpp
void remove(idx);  // TODO: remove value at idx from data structure
void add(idx);     // TODO: add value at idx from data structure
int get_answer();  // TODO: extract the current answer of the data structure

int block_size;

struct Query {
    int l, r, idx;
    bool operator<(Query other) const
    {
        return make_pair(l / block_size, r) <
               make_pair(other.l / block_size, other.r);
    }
};

vector<int> mo_s_algorithm(vector<Query> queries) {
    vector<int> answers(queries.size());
    sort(queries.begin(), queries.end());

    // TODO: initialize data structure

    int cur_l = 0;
    int cur_r = -1;
    // invariant: data structure will always reflect the range [cur_l, cur_r]
    for (Query q : queries) {
        while (cur_l > q.l) {
            cur_l--;
            add(cur_l);
        }
        while (cur_r < q.r) {
            cur_r++;
            add(cur_r);
        }
        while (cur_l < q.l) {
            remove(cur_l);
            cur_l++;
        }
        while (cur_r > q.r) {
            remove(cur_r);
            cur_r--;
        }
        answers[q.idx] = get_answer();
    }
    return answers;
}
```

Based on the problem we can use a different data structure and modify the `add`/`remove`/`get_answer` functions accordingly. For example if we are asked to find range sum queries then we use a simple integer as data structure, which is 0 at the beginning. The `add` function will simply add the value of the position and subsequently update the answer variable. On the other hand `remove` function will subtract the value at position and subsequently update the answer variable. And `get_answer` just returns the integer.

For answering mode-queries, we can use a binary search tree (e.g. `map<int, int>`) for storing how often each number appears in the current range, and a second binary search tree (e.g. `set<pair<int, int>>`) for keeping counts of the numbers (e.g. as count-number pairs) in order. The `add` method removes the current number from the second  BST, increases the count in the first one, and inserts the number back  into the second one. `remove` does the same thing, it only decreases the count. And `get_answer` just looks at second tree and returns the best value in *O*(1).

#### Complexity

Sorting all queries will take *O*(*Q*log*Q*).

How about the other operations? How many times will the `add` and `remove` be called?

Let's say the block size is *S*.

If we only look at all queries having the left index in the same block, the queries are sorted by the right index. Therefore we will call `add(cur_r)` and `remove(cur_r)` only *O*(*N*) times for all these queries combined. This gives *O*(*N**S**N*) calls for all blocks.

The value of `cur_l` can change by at most *O*(*S*) during between two queries. Therefore we have an additional *O*(*S**Q*) calls of `add(cur_l)` and `remove(cur_l)`.

For *S*≈*N*‾‾√ this gives *O*((*N*+*Q*)*N*‾‾√) operations in total. Thus the complexity is *O*((*N*+*Q*)*F**N*‾‾√) where *O*(*F*)  is the complexity of `add` and `remove` function.

#### Tips for improving runtime

- Block size of precisely *N*‾‾√ doesn't always offer the best runtime.  For example, if *N*‾‾√=750 then it may happen that block size of 700 or 800

-  may run better. More importantly, don't compute the block size at runtime - make it `const`. Division by constants is well optimized by compilers.
- In odd blocks sort the right index in ascending order and in even  blocks sort it in descending order. This will minimize the movement of  right pointer, as the normal sorting will move the right pointer from  the end back to the beginning at the start of every block. With the  improved version this resetting is no more necessary.

```cpp
bool cmp(pair<int, int> p, pair<int, int> q) {
    if (p.first / BLOCK_SIZE != q.first / BLOCK_SIZE)
        return p < q;
    return (p.first / BLOCK_SIZE & 1) ? (p.second < q.second) : (p.second > q.second);
}
```

You can read about even faster sorting approach [here](https://codeforces.com/blog/entry/61203).

## Segment Tree

### Simplest Form

```cpp
int n, t[4*MAXN];

void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = a[tl];
    } else {
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        t[v] = t[v*2] + t[v*2+1];
    }
}

int sum(int v, int tl, int tr, int l, int r) {
    if (l > r) 
        return 0;
    if (l == tl && r == tr) {
        return t[v];
    }
    int tm = (tl + tr) / 2;
    return sum(v*2, tl, tm, l, min(r, tm))
           + sum(v*2+1, tm+1, tr, max(l, tm+1), r);
}

void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        t[v] = new_val;
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
        t[v] = t[v*2] + t[v*2+1];
    }
}
```

### More complex queries

#### Finding the maximum

#### Finding the maximum and the number of times it appears

```cpp
pair<int, int> t[4*MAXN];

pair<int, int> combine(pair<int, int> a, pair<int, int> b) {
    if (a.first > b.first) 
        return a;
    if (b.first > a.first)
        return b;
    return make_pair(a.first, a.second + b.second);
}

void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = make_pair(a[tl], 1);
    } else {
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}

pair<int, int> get_max(int v, int tl, int tr, int l, int r) {
    if (l > r)
        return make_pair(-INF, 0);
    if (l == tl && r == tr)
        return t[v];
    int tm = (tl + tr) / 2;
    return combine(get_max(v*2, tl, tm, l, min(r, tm)), 
                   get_max(v*2+1, tm+1, tr, max(l, tm+1), r));
}

void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        t[v] = make_pair(new_val, 1);
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}
```

#### Counting the number of zeros, searching for the *k*-th zero

```cpp
int find_kth(int v, int tl, int tr, int k) {
    if (k > t[v])
        return -1;
    if (tl == tr)
        return tl;
    int tm = (tl + tr) / 2;
    if (t[v*2] >= k)
        return find_kth(v*2, tl, tm, k);
    else 
        return find_kth(v*2+1, tm+1, tr, k - t[v*2]);
}
```

#### Compute the greatest common divisor / least common multiple

In this problem we want to compute the GCD / LCM of all numbers of given ranges of the array. 

This interesting variation of the Segment Tree can be solved in  exactly the same way as the Segment Trees we derived for sum / minimum / maximum queries: it is enough to store the GCD / LCM of the corresponding vertex in each  vertex of the tree.  Combining two vertices can be done by computing the GCM / LCM of both  vertices.

#### Searching for an array prefix with a given amount

#### Searching for the first element greater than a given amount

```cpp
int get_first(int v, int lv, int rv, int l, int r, int x) {
    if(lv > r || rv < l) return -1;
    if(l <= lv && rv <= r) {
        if(t[v] <= x) return -1;
        while(lv != rv) {
            int mid = lv + (rv-lv)/2;
            if(t[2*v] > x) {
                v = 2*v;
                rv = mid;
            }else {
                v = 2*v+1;
                lv = mid+1;
            }
        }
        return lv;
    }

    int mid = lv + (rv-lv)/2;
    int rs = get_first(2*v, lv, mid, l, r, x);
    if(rs != -1) return rs;
    return get_first(2*v+1, mid+1, rv, l ,r, x);
}
```

#### Finding subsegments with the maximal sum

Here again we receive a range *a*[*l*…*r*] for each query, this time we have to find a subsegment *a*[*l*′…*r*′] such that *l*≤*l*′ and *r*′≤*r* and the sum of the elements of this segment is maximal.  As before we also want to be able to modify individual elements of the array.  The elements of the array can be negative, and the optimal subsegment can be empty (e.g. if all elements are negative).

This problem is a non-trivial usage of a Segment Tree. This time we will store four values for each vertex:  the sum of the segment, the maximum prefix sum, the maximum suffix sum,  and the sum of the maximal subsegment in it. In other words for each segment of the Segment Tree the answer is  already precomputed as well as the answers for segments touching the  left and the right boundaries of the segment.

```cpp
struct data {
    int sum, pref, suff, ans;
};

data combine(data l, data r) {
    data res;
    res.sum = l.sum + r.sum;
    res.pref = max(l.pref, l.sum + r.pref);
    res.suff = max(r.suff, r.sum + l.suff);
    res.ans = max(max(l.ans, r.ans), l.suff + r.pref);
    return res;
}
```

```cpp
data make_data(int val) {
    data res;
    res.sum = val;
    res.pref = res.suff = res.ans = max(0, val);
    return res;
}

void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = make_data(a[tl]);
    } else {
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}

void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        t[v] = make_data(new_val);
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}
```

```cpp
data query(int v, int tl, int tr, int l, int r) {
    if (l > r) 
        return make_data(0);
    if (l == tl && r == tr) 
        return t[v];
    int tm = (tl + tr) / 2;
    return combine(query(v*2, tl, tm, l, min(r, tm)), 
                   query(v*2+1, tm+1, tr, max(l, tm+1), r));
}
```

#### Saving the entire subarrays in each vertex

This is a separate subsection that stands apart from the others,  because at each vertex of the Segment Tree we don't store information  about the corresponding segment in compressed form (sum, minimum,  maximum, ...), but store all elements of the segment. Thus the root of the Segment Tree will store all elements of the array,  the left child vertex will store the first half of the array, the right  vertex the second half, and so on.

In its simplest application of this technique we store the elements  in sorted order. In more complex versions the elements are not stored in lists, but more  advanced data structures (sets, maps, ...).  But all these methods have the common factor, that each vertex requires  linear memory (i.e. proportional to the length of the corresponding  segment).

The first natural question, when considering these Segment Trees, is about memory consumption. Intuitively this might look like *O*(*n*2) memory, but it turns out that the complete tree will only need *O*(*n*log*n*) memory. Why is this so? Quite simply, because each element of the array falls into *O*(log*n*) segments (remember the height of the tree is *O*(log*n*)). So in spite of the apparent extravagance of such a Segment Tree, it  consumes only slightly more memory than the usual Segment Tree. 

Several typical applications of this data structure are described  below. It is worth noting the similarity of these Segment Trees with 2D data  structures (in fact this is a 2D data structure, but with rather limited capabilities).

#### Find the smallest number greater or equal to a specified number. No modification queries.

Merge Sort Tree

```cpp
vector<int> t[4*MAXN];

void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = vector<int>(1, a[tl]);
    } else { 
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        merge(t[v*2].begin(), t[v*2].end(), t[v*2+1].begin(), t[v*2+1].end(),
              back_inserter(t[v]));
    }
}
```

We already know that the Segment Tree constructed in this way will require *O*(*n*log*n*) memory. And thanks to this implementation its construction also takes *O*(*n*log*n*) time, after all each list is constructed in linear time in respect to its size. 

Now consider the answer to the query.  We will go down the tree, like in the regular Segment Tree, breaking our segment *a*[*l*…*r*] into several subsegments (into at most *O*(log*n*) pieces).  It is clear that the answer of the whole answer is the minimum of each  of the subqueries. So now we only need to understand, how to respond to a query on one such subsegment that corresponds with some vertex of the tree.

We are at some vertex of the Segment Tree and we want to compute the  answer to the query, i.e. find the minimum number greater that or equal  to a given number *x*.  Since the vertex contains the list of elements in sorted order, we can  simply perform a binary search on this list and return the first number, greater than or equal to *x*.Thus the answer to the query in one segment of the tree takes *O*(log*n*) time, and the entire query is processed in *O*(log2*n*).

```cpp
int query(int v, int tl, int tr, int l, int r, int x) {
    if (l > r)
        return INF;
    if (l == tl && r == tr) {
        vector<int>::iterator pos = lower_bound(t[v].begin(), t[v].end(), x);
        if (pos != t[v].end())
            return *pos;
        return INF;
    }
    int tm = (tl + tr) / 2;
    return min(query(v*2, tl, tm, l, min(r, tm), x), 
               query(v*2+1, tm+1, tr, max(l, tm+1), r, x));
}
```

#### Find the smallest number greater or equal to a specified number. With modification queries.

The solution is similar to the solution of the previous problem, but  instead of lists at each vertex of the Segment Tree, we will store a  balanced list that allows you to quickly search for numbers, delete  numbers, and insert new numbers.  Since the array can contain a number repeated, the optimal choice is the data structure multiset. 

The construction of such a Segment Tree is done in pretty much the same  way as in the previous problem, only now we need to combine multisets and not sorted lists. This leads to a construction time of *O*(*n*log2*n*) (in general merging two red-black trees can be done in linear time, but the C++ STL doesn't guarantee this time complexity).

```cpp
void update(int v, int tl, int tr, int pos, int new_val) {
    t[v].erase(t[v].find(a[pos]));
    t[v].insert(new_val);
    if (tl != tr) {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
    } else {
        a[pos] = new_val;
    }
}
```

Processing of this modification query also takes *O*(log^2*n*) time.

#### Find the smallest number greater or equal to a specified number. Acceleration with "fractional cascading".

We have the same problem statement, we want to find the minimal number greater than or equal to *x* in a segment, but this time in *O*(log*n*) time. We will improve the time complexity using the technique "fractional cascading".

Fractional cascading is a simple technique that allows you to improve the running time of multiple binary searches, which are conducted at  the same time.  Our previous approach to the search query was, that we divide the task  into several subtasks, each of which is solved with a binary search.  Fractional cascading allows you to replace all of these binary searches  with a single one.

The simplest and most obvious example of fractional cascading is the following problem: there are *k* sorted lists of numbers, and we must find in each list the first number greater than or equal to the given number.Instead of performing a binary search for each list, we could merge all lists into one big sorted list. Additionally for each element *y* we store a list of results of searching for *y* in each of the *k* lists. Therefore if we want to find the smallest number greater than or equal to *x*, we just need to perform one single binary search, and from the list of  indices we can determine the smallest number in each list. This approach however requires *O*(*n*⋅*k*) (*n* is the length of the combined lists), which can be quite inefficient. 

Fractional cascading reduces this memory complexity to *O*(*n*) memory, by creating from the *k* input lists *k* new lists, in which each list contains the corresponding list and  additionally also every second element of the following new list. Using this structure it is only necessary to store two indices, the  index of the element in the original list, and the index of the element  in the following new list. So this approach only uses *O*(*n*) memory, and still can answer the queries using a single binary search. 

But for our application we do not need the full power of fractional  cascading. In our Segment Tree a vertex will contain the sorted list of all  elements that occur in either the left or the right subtrees (like in  the Merge Sort Tree).  Additionally to this sorted list, we store two positions for each  element. For an element *y* we store the smallest index *i*, such that the *i*th element in the sorted list of the left child is greater or equal to *y*. And we store the smallest index *j*, such that the *j*th element in the sorted list of the right child is greater or equal to *y*. These values can be computed in parallel to the merging step when we build the tree.

How does this speed up the queries?

Remember, in the normal solution we did a binary search in ever node. But with this modification, we can avoid all except one.

To answer a query, we simply to a binary search in the root node. This gives as the smallest element *y*≥*x* in the complete array, but it also gives us two positions. The index of the smallest element greater or equal *x* in the left subtree, and the index of the smallest element *y* in the right subtree. Notice that ≥*y* is the same as ≥*x*, since our array doesn't contain any elements between *x* and *y*. In the normal Merge Sort Tree solution we would compute these indices  via binary search, but with the help of the precomputed values we can  just look them up in *O*(1). And we can repeat that until we visited all nodes that cover our query interval.

To summarize, as usual we touch *O*(log*n*) nodes during a query. In the root node we do a binary search, and in all other nodes we only do constant work. This means the complexity for answering a query is *O*(log*n*).

But notice, that this uses three times more memory than a normal Merge Sort Tree, which already uses a lot of memory (*O*(*n*log*n*)).

It is straightforward to apply this technique to a problem, that doesn't require any modification queries. The two positions are just integers and can easily be computed by counting when merging the two sorted sequences.

It it still possible to also allow modification queries, but that complicates the entire code. Instead of integers, you need to store the sorted array as `multiset`, and instead of indices you need to store iterators. And you need to work very carefully, so that you increment or decrement the correct iterators during a modification query.

#### Range updates (Lazy Propagation)

All problems in the above sections discussed modification queries  that only effected a single element of the array each. However the Segment Tree allows applying modification queries to an  entire segment of contiguous elements, and perform the query in the same time *O*(log*n*). 

## Treap

A treap provides the following operations:

- insert $\log n$
- search $\log n$
- erase $\log n$
- Build $O(n)$
- union $O(M \log (n/m))$
- Intersection $O(M \log (n/m))$

In addition, due to the fact that a treap is a binary search tree, it can implement other operations, such as finding the K-th largest  element or finding the index of an element.

### Implementation

By Split(T,X) and Merge(T1, T2)

```cpp
struct item {
    int key, prior;
    item *l, *r;
    item () { }
    item (int key) : key(key), prior(rand()), l(NULL), r(NULL) { }
};
typedef item* pitem;

void split (pitem t, int key, pitem & l, pitem & r) {
    if (!t)
        l = r = NULL;
    else if (t->key <= key)
        split (t->r, key, t->r, r),  l = t;
    else
        split (t->l, key, l, t->l),  r = t;
}

void merge (pitem & t, pitem l, pitem r) {
    if (!l || !r)
        t = l ? l : r;
    else if (l->prior > r->prior)
        merge (l->r, l->r, r),  t = l;
    else
        merge (r->l, l, r->l),  t = r;
}

void insert (pitem & t, pitem it) {
    if (!t)
        t = it;
    else if (it->prior > t->prior)
        split (t, it->key, it->l, it->r),  t = it;
    else
        insert (t->key <= it->key ? t->r : t->l, it);
}

void erase (pitem & t, int key) {
    if (t->key == key) {
        pitem th = t;
        merge (t, t->l, t->r);
        delete th;
    }
    else
        erase (key < t->key ? t->l : t->r, key);
}

pitem unite (pitem l, pitem r) {
    if (!l || !r)  return l ? l : r;
    if (l->prior < r->prior)  swap (l, r);
    pitem lt, rt;
    split (r, l->key, lt, rt);
    l->l = unite (l->l, lt);
    l->r = unite (l->r, rt);
    return l;
}

int cnt (pitem t) {
    return t ? t->cnt : 0;
}

void upd_cnt (pitem t) {
    if (t)
        t->cnt = 1 + cnt(t->l) + cnt (t->r);
}
```

### Implicit Treaps

All in $\log n$

- Inserting an element in the array in any location
- Removal of an arbitrary element
- Finding sum, minimum / maximum element etc. on an arbitrary interval
- Addition, painting on an arbitrary interval
- Reversing elements on an arbitrary interval

The idea is that the keys should be **indices** of the elements in the array. But we will not store these values explicitly.

More specifically, the **implicit key** for some node T is the number of vertices *c**n**t*(*T*→*L*) in the left subtree of this node plus similar values *c**n**t*(*P*→*L*)+1 for each ancestor P of the node T, if T is in the right subtree of P.

```cpp
void merge (pitem & t, pitem l, pitem r) {
    if (!l || !r)
        t = l ? l : r;
    else if (l->prior > r->prior)
        merge (l->r, l->r, r),  t = l;
    else
        merge (r->l, l, r->l),  t = r;
    upd_cnt (t);
}

void split (pitem t, pitem & l, pitem & r, int key, int add = 0) {
    if (!t)
        return void( l = r = 0 );
    int cur_key = add + cnt(t->l); //implicit key
    if (key <= cur_key)
        split (t->l, l, t->l, key, add),  r = t;
    else
        split (t->r, t->r, r, key, add + 1 + cnt(t->l)),  l = t;
    upd_cnt (t);
}

```

**Insert element**.  Suppose we need to insert an element at position `pos`. We divide the treap into two parts, which correspond to arrays `[0..pos-1]` and `[pos..sz]`; to do this we call `split` (T, *T*1, *T*2, pos). Then we can combine tree *T*1 with the new vertex by calling `merge` (*T*1, *T*1, new_item) (it is easy to see that all preconditions are met). Finally, we combine trees *T*1 and *T*2 back into T by calling `merge` (T, *T*1, *T*2).

**Delete element**.  This operation is even easier: find the element to be deleted T,  perform merge of its children L and R, and replace the element T with  the result of merge. In fact, element deletion in the implicit treap is  exactly the same as in the regular treap.

**Find sum / minimum, etc. on the interval.** First, create an additional field F in the `item` structure  to store the value of the target function for this node's subtree. This  field is easy to maintain similarly to maintaining sizes of subtrees:  create a function which calculates this value for a node based on values for its children and add calls of this function in the end of all  functions which modify the tree. Second, we need to know how to process a query for an arbitrary interval [A; B]. To get a part of tree which corresponds to the interval [A; B], we need to call `split` (T, *T*1, *T*2, A), and then `split` (*T*2, *T*2, *T*3, B - A + 1): after this *T*2 will consist of all the elements in the interval [A; B], and only of  them. Therefore, the response to the query will be stored in the field F of the root of *T*2. After the query is answered, the tree has to be restored by calling `merge` (T, *T*1, *T*2) and `merge` (*T*, *T*, *T*3).

**Addition / painting** on the interval. We act similarly to the previous paragraph, but instead of the field F we will store a field `add` which will contain the added value for the subtree (or the value to  which the subtree is painted). Before performing any operation we have  to "push" this value correctly - i.e. change *T*→*L*→*a**d**d* and *T*→*R*→*a**d**d*, and to clean up `add` in the parent node. This way after any changes to the tree the information will not be lost.

**Reverse** on the interval. This is again similar to the previous operation: we have to add boolean flag ‘rev’ and set it to true when the subtree of the current node has  to be reversed. "Pushing" this value is a bit complicated - we swap  children of this node and set this flag to true for them.

```cpp
typedef struct item * pitem;
struct item {
    int prior, value, cnt;
    bool rev;
    pitem l, r;
};

int cnt (pitem it) {
    return it ? it->cnt : 0;
}

void upd_cnt (pitem it) {
    if (it)
        it->cnt = cnt(it->l) + cnt(it->r) + 1;
}

void push (pitem it) {
    if (it && it->rev) {
        it->rev = false;
        swap (it->l, it->r);
        if (it->l)  it->l->rev ^= true;
        if (it->r)  it->r->rev ^= true;
    }
}

void merge (pitem & t, pitem l, pitem r) {
    push (l);
    push (r);
    if (!l || !r)
        t = l ? l : r;
    else if (l->prior > r->prior)
        merge (l->r, l->r, r),  t = l;
    else
        merge (r->l, l, r->l),  t = r;
    upd_cnt (t);
}

void split (pitem t, pitem & l, pitem & r, int key, int add = 0) {
    if (!t)
        return void( l = r = 0 );
    push (t);
    int cur_key = add + cnt(t->l);
    if (key <= cur_key)
        split (t->l, l, t->l, key, add),  r = t;
    else
        split (t->r, t->r, r, key, add + 1 + cnt(t->l)),  l = t;
    upd_cnt (t);
}

void reverse (pitem t, int l, int r) {
    pitem t1, t2, t3;
    split (t, t1, t2, l);
    split (t2, t2, t3, r-l+1);
    t2->rev ^= true;
    merge (t, t1, t2);
    merge (t, t, t3);
}

void output (pitem t) {
    if (!t)  return;
    push (t);
    output (t->l);
    printf ("%d ", t->value);
    output (t->r);
}
```

## Sqrt Tree

Process range query on associative functions with run-time $O(1)$, and preprocess and memory $O(n \log \log n)$.

Prefix array $O(\sqrt n)$, Suffix array$O(\sqrt n)$, block range array $O(n)$

It's obvious to see that these arrays can be easily calculated in *O*(*n*) time and memory.

But if we have queries that entirely fit into one block, we cannot  process them using these three arrays. So, we need to do something.

So, we get a tree. Each node of the tree represents some segment of the array. Node that represents array segment with size *k* has *k*√ children -- for each block. Also each node contains the three arrays  described above for the segment it contains. The root of the tree  represents the entire array. Nodes with segment lengths 1 or 2 are leaves.

Height of the tree is $O(\log \log n)$.

Now we can answer the queries in *O*(loglog*n*). We can go down on the tree until we meet a segment with length 1 or 2 (answer for it can be calculated in *O*(1) time) or meet the first segment in which our query doesn't fit entirely into one block. See the first section on how to answer the query in  this case.OK, now we can do *O*(loglog*n*) per query. Can it be done faster?

### Optimizing the query complexity

One of the most obvious optimization is to binary search the tree node we need. Using binary search, we can reach the *O*(logloglog*n*) complexity per query. Can we do it even faster?

The answer is yes. Let's assume the following two things:

1. Each block size is a power of two.
2. All the blocks are equal on each layer.

Using this observation, we can find a layer that is suitable to answer the query quickly. How to do this:

1. For each *i* that doesn't exceed the array size, we find the highest bit that is equal to 1. To do this quickly, we use DP and a precalculated array.

2. Now, for each *q*(*l*,*r*) we find the highest bit of *l* xor *r* and, using this information, it's easy to choose the layer on which we  can process the query easily. We can also use a precalculated array  here.

### Updating a single element

#### Naive approach

O(n)

#### An sqrt-tree inside the sqrt-tree

Note that the bottleneck of updating is rebuilding between of the root node. To optimize the tree, let's get rid of this array! Instead of between array, we store another sqrt-tree for the root node. Let's call it index. It plays the same role as between— answers the queries on segments of blocks. Note that the rest of the tree nodes don't have index, they keep their between arrays.

A sqrt-tree is *indexed*, if its root node has index. A sqrt-tree with between array in its root node is *unindexed*. Note that index **is \*unindexed\* itself**.

So, we have the following algorithm for updating an *indexed* tree:

Update prefixOp and suffixOp in *O*(*n*‾√).Update index. It has length *O*(*n*‾√) and we need to update only one item in it (that represents the changed block). So, the time complexity for this step is *O*(*n*‾√). We can use the algorithm described in the beginning of this section (the "slow" one) to do it.

Go into the child node that represents the changed block and update it in *O*(*n*‾√) with the "slow" algorithm.Note that the query complexity is still *O*(1): we need to use index in query no more than once, and this will take *O*(1) time.

So, total time complexity for updating a single element is *O*(*n*‾√). Hooray! :)

#### Updating a segment

Read Later

```cpp
SqrtTreeItem op(const SqrtTreeItem &a, const SqrtTreeItem &b);

inline int log2Up(int n) {
    int res = 0;
    while ((1 << res) < n) {
        res++;
    }
    return res;
}

class SqrtTree {
private:
    int n, lg, indexSz;
    vector<SqrtTreeItem> v;
    vector<int> clz, layers, onLayer;
    vector< vector<SqrtTreeItem> > pref, suf, between;

    inline void buildBlock(int layer, int l, int r) {
        pref[layer][l] = v[l];
        for (int i = l+1; i < r; i++) {
            pref[layer][i] = op(pref[layer][i-1], v[i]);
        }
        suf[layer][r-1] = v[r-1];
        for (int i = r-2; i >= l; i--) {
            suf[layer][i] = op(v[i], suf[layer][i+1]);
        }
    }

    inline void buildBetween(int layer, int lBound, int rBound, int betweenOffs) {
        int bSzLog = (layers[layer]+1) >> 1;
        int bCntLog = layers[layer] >> 1;
        int bSz = 1 << bSzLog;
        int bCnt = (rBound - lBound + bSz - 1) >> bSzLog;
        for (int i = 0; i < bCnt; i++) {
            SqrtTreeItem ans;
            for (int j = i; j < bCnt; j++) {
                SqrtTreeItem add = suf[layer][lBound + (j << bSzLog)];
                ans = (i == j) ? add : op(ans, add);
                between[layer-1][betweenOffs + lBound + (i << bCntLog) + j] = ans;
            }
        }
    }

    inline void buildBetweenZero() {
        int bSzLog = (lg+1) >> 1;
        for (int i = 0; i < indexSz; i++) {
            v[n+i] = suf[0][i << bSzLog];
        }
        build(1, n, n + indexSz, (1 << lg) - n);
    }

    inline void updateBetweenZero(int bid) {
        int bSzLog = (lg+1) >> 1;
        v[n+bid] = suf[0][bid << bSzLog];
        update(1, n, n + indexSz, (1 << lg) - n, n+bid);
    }

    void build(int layer, int lBound, int rBound, int betweenOffs) {
        if (layer >= (int)layers.size()) {
            return;
        }
        int bSz = 1 << ((layers[layer]+1) >> 1);
        for (int l = lBound; l < rBound; l += bSz) {
            int r = min(l + bSz, rBound);
            buildBlock(layer, l, r);
            build(layer+1, l, r, betweenOffs);
        }
        if (layer == 0) {
            buildBetweenZero();
        } else {
            buildBetween(layer, lBound, rBound, betweenOffs);
        }
    }

    void update(int layer, int lBound, int rBound, int betweenOffs, int x) {
        if (layer >= (int)layers.size()) {
            return;
        }
        int bSzLog = (layers[layer]+1) >> 1;
        int bSz = 1 << bSzLog;
        int blockIdx = (x - lBound) >> bSzLog;
        int l = lBound + (blockIdx << bSzLog);
        int r = min(l + bSz, rBound);
        buildBlock(layer, l, r);
        if (layer == 0) {
            updateBetweenZero(blockIdx);
        } else {
            buildBetween(layer, lBound, rBound, betweenOffs);
        }
        update(layer+1, l, r, betweenOffs, x);
    }

    inline SqrtTreeItem query(int l, int r, int betweenOffs, int base) {
        if (l == r) {
            return v[l];
        }
        if (l + 1 == r) {
            return op(v[l], v[r]);
        }
        int layer = onLayer[clz[(l - base) ^ (r - base)]];
        int bSzLog = (layers[layer]+1) >> 1;
        int bCntLog = layers[layer] >> 1;
        int lBound = (((l - base) >> layers[layer]) << layers[layer]) + base;
        int lBlock = ((l - lBound) >> bSzLog) + 1;
        int rBlock = ((r - lBound) >> bSzLog) - 1;
        SqrtTreeItem ans = suf[layer][l];
        if (lBlock <= rBlock) {
            SqrtTreeItem add = (layer == 0) ? (
                query(n + lBlock, n + rBlock, (1 << lg) - n, n)
            ) : (
                between[layer-1][betweenOffs + lBound + (lBlock << bCntLog) + rBlock]
            );
            ans = op(ans, add);
        }
        ans = op(ans, pref[layer][r]);
        return ans;
    }
public:
    inline SqrtTreeItem query(int l, int r) {
        return query(l, r, 0, 0);
    }

    inline void update(int x, const SqrtTreeItem &item) {
        v[x] = item;
        update(0, 0, n, 0, x);
    }

    SqrtTree(const vector<SqrtTreeItem>& a)
        : n((int)a.size()), lg(log2Up(n)), v(a), clz(1 << lg), onLayer(lg+1) {
        clz[0] = 0;
        for (int i = 1; i < (int)clz.size(); i++) {
            clz[i] = clz[i >> 1] + 1;
        }
        int tlg = lg;
        while (tlg > 1) {
            onLayer[tlg] = (int)layers.size();
            layers.push_back(tlg);
            tlg = (tlg+1) >> 1;
        }
        for (int i = lg-1; i >= 0; i--) {
            onLayer[i] = max(onLayer[i], onLayer[i+1]);
        }
        int betweenLayers = max(0, (int)layers.size() - 1);
        int bSzLog = (lg+1) >> 1;
        int bSz = 1 << bSzLog;
        indexSz = (n + bSz - 1) >> bSzLog;
        v.resize(n + indexSz);
        pref.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
        suf.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
        between.assign(betweenLayers, vector<SqrtTreeItem>((1 << lg) + bSz));
        build(0, 0, n, 0);
    }
};
```

## Randomized Heap

### Operations

It is not difficult to see, that all operations can be reduced to a single one: **merging** two heaps into one. Indeed, adding a new value to the heap is equivalent to merging the heap with a heap consisting of a single vertex with that value.  Finding a minimum doesn't require any operation at all - the minimum is  simply the value at the root. Removing the minimum is equivalent to the result of merging the left and right children of the root vertex. And removing an arbitrary element is similar. We merge the children of the vertex and replace the vertex with the  result of the merge.

So we actually only need to implement the operation of merging two heaps. All other operations are trivially reduced to this operation.

Let two heaps *T*1 and *T*2 be given. It is clear that the root of each of these heaps contains its minimum. So the root of the resulting heap will be the minimum of these two values. So we compare both values, and use the smaller one as the new root. Now we have to combine the children of the selected vertex with the remaining heap. For this we select one of the children, and merge it with the remaining heap. Thus we again have the operation of merging two heaps. Sooner of later this process will end (the number of such steps is limited by the sum of the heights of the two heaps)

To achieve logarithmic complexity on average, we need to specify a  method for choosing one of the two children so that the average path  length is logarithmic. It is not difficult to guess, that we will make this decision **randomly**. Thus the implementation of the merging operation is as follows:

```cpp
Tree* merge(Tree* t1, Tree* t2) {
    if (!t1 || !t2)
        return t1 ? t1 : t2;
    if (t2->value < t1->value)
        swap(t1, t2);
    if (rand() & 1)
        swap(t1->l, t1->r);
    t1->l = merge(t1->l, t2);
    return t1;
}
```

### Complexity

We introduce the random variable *h*(*T*) which will denote the **length of the random path** from the root to the leaf (the length in the number of edges). It is clear that the algorithm `merge` performs *O*(*h*(*T*1)+*h*(*T*2)) steps. Therefore to understand the complexity of the operations, we must look into the random variable *h*(*T*).

#### Expected value

$O(\log n)$ by induction. 

#### Exceeding the expected value

Read later.

## Deleting from a data structure in *O*(*T*(*n*)log*n*)

Suppose you have a data structure which allows adding elements in **true***O*(*T*(*n*)). This article will describe a technique that allows deletion in *O*(*T*(*n*)log*n*) offline.

### Algorithm

Each element lives in the data structure for some segments of time between additions and deletions. Let's build a segment tree over the queries. Each segment when some element is alive splits into *O*(log*n*) nodes of the tree. Let's put each query when we want to know something about the structure into the corresponding leaf. Now to process all queries we will run a DFS on the segment tree. When entering the node we will add all the elements that are inside this node. Then we will go further to the children of this node or answer the queries (if the node is a leaf). When leaving the node, we must undo the additions. Note that if we change the structure in *O*(*T*(*n*)) we can roll back the changes in *O*(*T*(*n*)) by keeping a stack of changes. Note that rollbacks break amortized complexity.

