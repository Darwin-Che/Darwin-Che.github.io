---
blogpost: true
date: 2022-07-25
tags: ["algo","dp"]
category: Blog
author: myself
---

# DP

## Divide and Conquer DP

Some dynamic programming problems have a recurrence of this form: 
$$
dp(i,j) = \min_{0\le k \le j} dp(i-1, k-1) + C(k,j)
$$
Say 0≤*i*<*m* and 0≤*j*<*n*, and evaluating *C* takes *O*(1) time. Then the straightforward evaluation of the above recurrence is *O*(*m**n*2). There are *m*×*n* states, and *n* transitions for each state.

Let $opt(i,j)$ be the value of *k* that minimizes the above expression. If $opt(i,j) \le opt(i, j+1)$ for all *i*,*j*, then we can apply divide-and-conquer DP. This is known as the *monotonicity condition*. The optimal "splitting point" for a fixed *i* increases as *j* increases.

To minimize the runtime, we apply the idea behind divide and conquer. First, compute *o**p**t*(*i*,*n*/2). Then, compute *o**p**t*(*i*,*n*/4), knowing that it is less than or equal to *o**p**t*(*i*,*n*/2) and *o**p**t*(*i*,3*n*/4) knowing that it is greater than or equal to *o**p**t*(*i*,*n*/2). By recursively keeping track of the lower and upper bounds on *o**p**t*, we reach a *O*(*m**n*log*n*) runtime. Each possible value of *o**p**t*(*i*,*j*) only appears in log*n* different nodes.

Note that it doesn't matter how "balanced" *o**p**t*(*i*,*j*) is. Across a fixed level, each value of *k* is used at most twice, and there are at most log*n* levels.

### Generic implementation

```cpp
int m, n;
vector<long long> dp_before(n), dp_cur(n);

long long C(int i, int j);

// compute dp_cur[l], ... dp_cur[r] (inclusive)
void compute(int l, int r, int optl, int optr) {
    if (l > r)
        return;

    int mid = (l + r) >> 1;
    pair<long long, int> best = {LLONG_MAX, -1};

    for (int k = optl; k <= min(mid, optr); k++) {
        best = min(best, {(k ? dp_before[k - 1] : 0) + C(k, mid), k});
    }

    dp_cur[mid] = best.first;
    int opt = best.second;

    compute(l, mid - 1, optl, opt);
    compute(mid + 1, r, opt, optr);
}

int solve() {
    for (int i = 0; i < n; i++)
        dp_before[i] = C(0, i);

    for (int i = 1; i < m; i++) {
        compute(0, n - 1, 0, n - 1);
        dp_before = dp_cur;
    }

    return dp_before[n - 1];
}
```

#### Things to look out for

The greatest difficulty with Divide and Conquer DP problems is proving the monotonicity of *o**p**t*. Many Divide and Conquer DP problems can also be solved with the Convex Hull trick or vice-versa. It is useful to know and understand both!

## Zero Matrix

```cpp
int zero_matrix(vector<vector<int>> a) {
    int n = a.size();
    int m = a[0].size();

    int ans = 0;
    vector<int> d(m, -1), d1(m), d2(m);
    stack<int> st;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (a[i][j] == 1)
                d[j] = i;
        }

        for (int j = 0; j < m; ++j) {
            while (!st.empty() && d[st.top()] <= d[j])
                st.pop();
            d1[j] = st.empty() ? -1 : st.top();
            st.push(j);
        }
        while (!st.empty())
            st.pop();

        for (int j = m - 1; j >= 0; --j) {
            while (!st.empty() && d[st.top()] <= d[j])
                st.pop();
            d2[j] = st.empty() ? m : st.top();
            st.push(j);
        }
        while (!st.empty())
            st.pop();

        for (int j = 0; j < m; ++j)
            ans = max(ans, (i - d[j]) * (d2[j] - d1[j] - 1));
    }
    return ans;
}
```

