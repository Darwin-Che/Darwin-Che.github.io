---
blogpost: true
date: 2022-07-25
tags: ["algo"]
category: Blog
author: myself
---
# Monotonic Queue and similar ideas

https://1e9.medium.com/monotonic-queue-notes-980a019d5793

## Monotonic Queue ADT

"MQ is mostly used as a dynamic programming optimization technique and for some problems where it is applicable we can reduce the reasoning to finding the nearest element. The advantage of MQ is linear time complexity."

https://leetcode.com/problems/daily-temperatures/

"Given a list of daily temperatures `T`, return a list such  that, for each day in the input, tells you how many days you would have  to wait until a warmer temperature.  If there is no future day for which this is possible, put `0` instead.

For example, given the list of temperatures `T = [73, 74, 75, 71, 69, 72, 76, 73]`, your output should be `[1, 1, 4, 2, 1, 1, 0, 0]`."

i.e. Find the next larger element

Maintaining a list of increasing subsequence that starts with index i

```c++
vector<int> dailyTemperatures(vector<int>& T) {
    vector<int> ans(T.size(), 0);
	stack<int> st; // storing the indices
    for (int i = T.size()-1; i >= 0; --i) {
        while (!st.empty() && T[st.top()] <= T[i]) st.pop();
        ans[i] = st.empty() ? 0 : st.top() - i;
        st.emplace(i);
    }
    return ans;
}
```

The code is easy to read. The runtime is O(n) by thinking about the size of stack in amortized workload. A slightly improved but difficult to read version is 

```c++
vector<int> dailyTemperatures(vector<int>& temperatures) {
    vector<int> res(temperatures.size());
    for (int i = temperatures.size() - 1; i >= 0; --i) {
        int j = i+1;
        while (j < temperatures.size() && temperatures[j] <= temperatures[i]) {
            if (res[j] > 0) j = res[j] + j;
            else j = temperatures.size();
        }
        // either j == size || temperatures[j] > temperatures[i]
        if (j < temperatures.size()) res[i] = j - i;
    }
    return res;
}
```

## Abstract idea

Any DP problem where `S[i] = max(A[j:k]) + C` where `j < k <= i` and `C` is a constant.

## Code Tricks

Pay attention to the invariant of of poping an element from the stack

- Elements from `j` to `i - 1` are all greater than `j`.
- Elements after the new top of the stack are all greater than `j`.

This means [new top, i] are the two nearest element bigger than [j].

```c++
int maxSumMinProduct(vector<int>& n) {
    long res = 0;
    n.push_back(0);
    vector<long> dp(n.size() + 1), st;
    for (int i = 0; i < n.size(); ++i)
       dp[i + 1] = dp[i] + n[i];
    for (int i = 0; i < n.size(); ++i) {
        while (!st.empty() && n[st.back()] > n[i]) {
            int j = st.back();
            st.pop_back();
            res = max(res, n[j] * (dp[i] - dp[st.empty() ? 0 : st.back() + 1]));
        }
        st.push_back(i);
    }
    return res % 1000000007;
}
```





