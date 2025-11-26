---
blogpost: true
date: 2022-07-25
tags: ["algo"]
category: Blog
author: myself

---
# String Processing

## String Hashing

### Calculation of the hash of a string

$$
hash(s) = \sum_{i=0}^{n-1} s[i] \cdot p^i \mod m
$$

where *p* and *m* are some chosen, positive numbers. It is called a **polynomial rolling hash function**.

It is reasonable to make *p* a prime number roughly equal to the number of characters in the input alphabet. For example, if the input is composed of only lowercase letters of the English alphabet, *p*=31 is a good choice. If the input may contain both uppercase and lowercase letters, then *p*=53 is a possible choice. The code in this article will use *p*=31.

Obviously *m* should be a large number since the probability of two random strings colliding is about ≈1*m*. Sometimes *m*=264 is chosen, since then the integer overflows of 64-bit integers work exactly like the modulo operation. However, there exists a method, which generates colliding strings (which work independently from the choice of *p*). So in practice, *m*=264 is not recommended. A good choice for *m* is some large prime number. The code in this article will just use *m*=109+9. This is a large number, but still small enough so that we can perform multiplication of two values using 64-bit integers.

```cpp
long long compute_hash(string const& s) {
    const int p = 31;
    const int m = 1e9 + 9;
    long long hash_value = 0;
    long long p_pow = 1;
    for (char c : s) {
        hash_value = (hash_value + (c - 'a' + 1) * p_pow) % m;
        p_pow = (p_pow * p) % m;
    }
    return hash_value;
}
```

Precomputing the powers of *p* might give a performance boost.

### Example tasks

#### Search for duplicate strings in an array of strings

Problem: Given a list of *n* strings *s**i*, each no longer than *m* characters, find all the duplicate strings and divide them into groups.

From the obvious algorithm involving sorting the strings, we would get a time complexity of *O*(*n**m*log*n*) where the sorting requires *O*(*n*log*n*) comparisons and each comparison take *O*(*m*) time. However, by using hashes, we reduce the comparison time to *O*(1), giving us an algorithm that runs in *O*(*n**m*+*n*log*n*) time.

```cpp
vector<vector<int>> group_identical_strings(vector<string> const& s) {
    int n = s.size();
    vector<pair<long long, int>> hashes(n);
    for (int i = 0; i < n; i++)
        hashes[i] = {compute_hash(s[i]), i};

    sort(hashes.begin(), hashes.end());

    vector<vector<int>> groups;
    for (int i = 0; i < n; i++) {
        if (i == 0 || hashes[i].first != hashes[i-1].first)
            groups.emplace_back();
        groups.back().push_back(hashes[i].second);
    }
    return groups;
}

```

#### Fast hash calculation of substrings of given string

Problem: Given a string *s* and indices *i* and *j*, find the hash of the substring *s*[*i*…*j*].
$$
p^i \cdot hash(i,j) = hash(0,j) - hash(0,i-1)
$$
So by knowing the hash value of each prefix of the string *s*, we can compute the hash of any substring directly using this formula. The only problem that we face in calculating it is that we must be able to divide hash(*s*[0…*j*])−hash(*s*[0…*i*−1]) by *p**i*. Therefore we need to find the [modular multiplicative inverse](https://cp-algorithms.com/algebra/module-inverse.html) of *p**i* and then perform multiplication with this inverse. We can precompute the inverse of every *p**i*, which allows computing the hash of any substring of *s* in *O*(1) time.

However, there does exist an easier way. In most cases, rather than calculating the hashes of substring exactly,  it is enough to compute the hash multiplied by some power of *p*. Suppose we have two hashes of two substrings, one multiplied by *p**i* and the other by *p**j*. If *i*<*j* then we multiply the first hash by *p**j*−*i*, otherwise, we multiply the second hash by *p**i*−*j*. By doing this, we get both the hashes multiplied by the same power of *p* (which is the maximum of *i* and *j*) and now these hashes can be compared easily with no need for any division.

### Applications of Hashing

Here are some typical applications of Hashing:

[Rabin-Karp algorithm](https://cp-algorithms.com/string/rabin-karp.html) for pattern matching in a string in *O*(*n*) time

Calculating the number of different substrings of a string in *O*(*n*2log*n*) (see below)

Calculating the number of palindromic substrings in a string.

#### Determine the number of different substrings in a string

Problem: Given a string *s* of length *n*, consisting only of lowercase English letters, find the number of different substrings in this string.

To solve this problem, we iterate over all substring lengths *l*=1…*n*. For every substring length *l* we construct an array of hashes of all substrings of length *l* multiplied by the same power of *p*. The number of different elements in the array is equal to the number of distinct substrings of length *l* in the string. This number is added to the final answer.

For convenience, we will use *h*[*i*] as the hash of the prefix with *i* characters, and define *h*[0]=0.

```cpp
int count_unique_substrings(string const& s) {
    int n = s.size();

    const int p = 31;
    const int m = 1e9 + 9;
    vector<long long> p_pow(n);
    p_pow[0] = 1;
    for (int i = 1; i < n; i++)
        p_pow[i] = (p_pow[i-1] * p) % m;

    vector<long long> h(n + 1, 0);
    for (int i = 0; i < n; i++)
        h[i+1] = (h[i] + (s[i] - 'a' + 1) * p_pow[i]) % m;

    int cnt = 0;
    for (int l = 1; l <= n; l++) {
        set<long long> hs;
        for (int i = 0; i <= n - l; i++) {
            long long cur_h = (h[i + l] + m - h[i]) % m;
            cur_h = (cur_h * p_pow[n-i-1]) % m;
            hs.insert(cur_h);
        }
        cnt += hs.size();
    }
    return cnt;
}
```

### Improve no-collision probability

Quite often the above mentioned polynomial hash is good enough, and no collisions will happen during tests. Remember, the probability that collision happens is only ≈1*m*. For *m*=109+9 the probability is ≈10−9 which is quite low. But notice, that we only did one comparison. What if we compared a string *s* with 106 different strings. The probability that at least one collision happens is now ≈10−3. And if we want to compare 106 different strings with each other (e.g. by counting how many unique  strings exists), then the probability of at least one collision  happening is already ≈1. It is pretty much guaranteed that this task will end with a collision and returns the wrong result.

There is a really easy trick to get better probabilities. We can just compute two different hashes for each string (by using two different *p*, and/or different *m*, and compare these pairs instead. If *m* is about 109 for each of the two hash functions than this is more or less equivalent as having one hash function with *m*≈1018. When comparing 106 strings with each other, the probability that at least one collision happens is now reduced to ≈10−6.

## Rabin-Karp Algorithm for string matching

```cpp
vector<int> rabin_karp(string const& s, string const& t) {
    const int p = 31; 
    const int m = 1e9 + 9;
    int S = s.size(), T = t.size();

    vector<long long> p_pow(max(S, T)); 
    p_pow[0] = 1; 
    for (int i = 1; i < (int)p_pow.size(); i++) 
        p_pow[i] = (p_pow[i-1] * p) % m;

    vector<long long> h(T + 1, 0); 
    for (int i = 0; i < T; i++)
        h[i+1] = (h[i] + (t[i] - 'a' + 1) * p_pow[i]) % m; 
    long long h_s = 0; 
    for (int i = 0; i < S; i++) 
        h_s = (h_s + (s[i] - 'a' + 1) * p_pow[i]) % m; 

    vector<int> occurences;
    for (int i = 0; i + S - 1 < T; i++) { 
        long long cur_h = (h[i+S] + m - h[i]) % m; 
        if (cur_h == h_s * p_pow[i] % m)
            occurences.push_back(i);
    }
    return occurences;
}
```

## Prefix function. Knuth–Morris–Pratt algorithm

### Prefix function definition

You are given a string *s* of length *n*. The **prefix function** for this string is defined as an array *π* of length *n*, where *π*[*i*] is the length of the longest proper prefix of the substring *s*[0…*i*] which is also a suffix of this substring. A proper prefix of a string is a prefix that is not equal to the string itself. By definition, *π*[0]=0.

### Trivial Algorithm

```cpp
vector<int> prefix_function(string s) {
    int n = (int)s.length();
    vector<int> pi(n);
    for (int i = 0; i < n; i++)
        for (int k = 0; k <= i; k++)
            if (s.substr(0, k) == s.substr(i-k+1, k))
                pi[i] = k;
    return pi;
}
```

### Efficient Algorithm

#### First optimization

The first important observation is, that the values of the prefix function can only increase by at most one.

Indeed, otherwise, if *π*[*i*+1]>*π*[*i*]+1, then we can take this suffix ending in position *i*+1 with the length *π*[*i*+1] and remove the last character from it. We end up with a suffix ending in position *i* with the length *π*[*i*+1]−1, which is better than *π*[*i*], i.e. we get a contradiction.

Thus when moving to the next position, the value of the prefix function  can either increase by one, stay the same, or decrease by some amount. This fact already allows us to reduce the complexity of the algorithm to *O*(*n*2), because in one step the prefix function can grow at most by one. In total the function can grow at most *n* steps, and therefore also only can decrease a total of *n* steps. This means we only have to perform *O*(*n*) string comparisons, and reach the complexity *O*(*n*2).

#### Second optimization

Let's go further, we want to get rid of the string comparisons. To accomplish this, we have to use all the information computed in the previous steps.

So let us compute the value of the prefix function *π* for *i*+1. If *s*[*i*+1]=*s*[*π*[*i*]], then we can say with certainty that *π*[*i*+1]=*π*[*i*]+1, since we already know that the suffix at position *i* of length *π*[*i*] is equal to the prefix of length *π*[*i*]. 

Indeed, if we find such a length *j*, then we again only need to compare the characters *s*[*i*+1] and *s*[*j*]. If they are equal, then we can assign *π*[*i*+1]=*j*+1. Otherwise we will need to find the largest value smaller than *j*, for which the prefix property holds, and so on. It can happen that this goes until *j*=0. If then *s*[*i*+1]=*s*[0], we assign *π*[*i*+1]=1, and *π*[*i*+1]=0 otherwise.

So we already have a general scheme of the algorithm. The only question left is how do we effectively find the lengths for *j*. Let's recap: for the current length *j* at the position *i* for which the prefix property holds, i.e. *s*[0…*j*−1]=*s*[*i*−*j*+1…*i*], we want to find the greatest *k*<*j*, for which the prefix property holds.

#### Final algorithm

```cpp
vector<int> prefix_function(string s) {
    int n = (int)s.length();
    vector<int> pi(n);
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j])
            j = pi[j-1];
        if (s[i] == s[j])
            j++;
        pi[i] = j;
    }
    return pi;
}
```

### Applications

#### Search for a substring in a string. The Knuth-Morris-Pratt algorithm

#### Counting the number of occurrences of each prefix

#### The number of different substring in a string

Given a string *s* of length *n*. We want to compute the number of different substrings appearing in it.

We will solve this problem iteratively. Namely we will learn, knowing the current number of different  substrings, how to recompute this count by adding a character to the  end.

So let *k* be the current number of different substrings in *s*, and we add the character *c* to the end of *s*. Obviously some new substrings ending in *c* will appear. We want to count these new substrings that didn't appear before.

We take the string *t*=*s*+*c* and reverse it. Now the task is transformed into computing how many prefixes there are that don't appear anywhere else. If we compute the maximal value of the prefix function *π*max of the reversed string *t*, then the longest prefix that appears in *s* is *π*max long. Clearly also all prefixes of smaller length appear in it.

Therefore the number of new substrings appearing when we add a new character *c* is |*s*|+1−*π*max.

So for each character appended we can compute the number of new substrings in *O*(*n*) times, which gives a time complexity of *O*(*n*2) in total.

It is worth noting, that we can also compute the number of different  substrings by appending the characters at the beginning, or by deleting  characters from the beginning or the end.

## Z-function and its calculation

Suppose we are given a string *s* of length *n*. The **Z-function** for this string is an array of length *n* where the *i*-th element is equal to the greatest number of characters starting from the position *i* that coincide with the first characters of *s*.In other words, *z*[*i*] is the length of the longest string that is, at the same time, a prefix of *s* and a prefix of the suffix of *s* starting at *i*.

The first element of Z-function, *z*[0], is generally not well defined. In this article we will assume it is  zero (although it doesn't change anything in the algorithm  implementation).This article presents an algorithm for calculating the Z-function in *O*(*n*) time, as well as various of its applications.

### Trivial algorithm

```cpp
vector<int> z_function_trivial(string s) {
    int n = (int) s.length();
    vector<int> z(n);
    for (int i = 1; i < n; ++i)
        while (i + z[i] < n && s[z[i]] == s[i + z[i]])
            ++z[i];
    return z;
}
```

To obtain an efficient algorithm we will compute the values of *z*[*i*] in turn from *i*=1 to *n*−1 but at the same time, when computing a new value, we'll try to make the best use possible of the previously computed values.

For the sake of brevity, let's call **segment matches** those substrings that coincide with a prefix of *s*. For example, the value of the desired Z-function *z*[*i*] is the length of the segment match starting at position *i* (and that ends at position *i*+*z*[*i*]−1).

To do this, we will keep **the [*l*,*r*]** **indices of the rightmost segment match**. That is, among all detected segments we will keep the one that ends rightmost. In a way, the index *r* can be seen as the "boundary" to which our string *s* has been scanned by the algorithm; everything beyond that point is not yet known.

```cpp
vector<int> z_function(string s) { // O(n)
    int n = (int) s.length();
    vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r)
            z[i] = min (r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]])
            ++z[i];
        if (i + z[i] - 1 > r)
            l = i, r = i + z[i] - 1;
    }
    return z;
}
```

### Applications

#### Search the substring

To avoid confusion, we call *t* the **string of text**, and *p* the **pattern**. The problem is: find all occurrences of the pattern *p* inside the text *t*.

To solve this problem, we create a new string *s*=*p*+⋄+*t*, that is, we apply string concatenation to *p* and *t* but we also put a separator character ⋄ in the middle (we'll choose ⋄ so that it will certainly not be present anywhere in the strings *p* or *t*).

Compute the Z-function for *s*. Then, for any *i* in the interval [0;length(*t*)−1], we will consider the corresponding value *k*=*z*[*i*+length(*p*)+1]. If *k* is equal to length(*p*) then we know there is one occurrence of *p* in the *i*-th position of *t*, otherwise there is no occurrence of *p* in the *i*-th position of *t*.The running time (and memory consumption) is *O*(length(*t*)+length(*p*)).

#### Number of distinct substrings in a string

Given a string *s* of length *n*, count the number of distinct substrings of *s*.

We'll solve this problem iteratively. That is: knowing the current  number of different substrings, recalculate this amount after adding to  the end of *s* one character.

So, let *k* be the current number of distinct substrings of *s*. We append a new character *c* to *s*. Obviously, there can be some new substrings ending in this new character *c* (namely, all those strings that end with this symbol and that we haven't encountered yet).

Take a string *t*=*s*+*c* and invert it (write its characters in reverse order). Our task is now to count how many prefixes of *t* are not found anywhere else in *t*. Let's compute the Z-function of *t* and find its maximum value *z**m**a**x*. Obviously, *t*'s prefix of length *z**m**a**x* occurs also somewhere in the middle of *t*. Clearly, shorter prefixes also occur.

So, we have found that the number of new substrings that appear when symbol *c* is appended to *s* is equal to length(*t*)−*z**m**a**x*.

Consequently, the running time of this solution is *O*(*n*2) for a string of length *n*.

It's worth noting that in exactly the same way we can recalculate, still in *O*(*n*) time, the number of distinct substrings when appending a character in  the beginning of the string, as well as when removing it (from the end  or the beginning).

## Suffix Array

A **suffix array** will contain integers that represent the **starting indexes** of the all the suffixes of a given string, after the aforementioned suffixes are sorted.

### Construction

#### *O*(*n^2*log*n*) approach

This is the most naive approach. Get all the suffixes and sort them using quicksort or mergesort and simultaneously retain their original indices. Sorting uses *O*(*n*log*n*) comparisons, and since comparing two strings will additionally take *O*(*n*) time, we get the final complexity of *O*(*n*2log*n*).

#### *O*(*n*log*n*) approach

Since we are going to sort cyclic shifts, we will consider **cyclic substrings**. We will use the notation *s*[*i*…*j*] for the substring of *s* even if *i*>*j*. In this case we actually mean the string *s*[*i*…*n*−1]+*s*[0…*j*]. In addition we will take all indices modulo the length of *s*, and will omit the modulo operation for simplicity.

The algorithm we discuss will perform ⌈log*n*⌉+1 iterations. In the *k*-th iteration (*k*=0…⌈log*n*⌉) we sort the *n* cyclic substrings of *s* of length 2*k*. After the ⌈log*n*⌉-th iteration the substrings of length 2⌈log*n*⌉≥*n* will be sorted, so this is equivalent to sorting the cyclic shifts altogether.

In each iteration of the algorithm, in addition to the permutation *p*[0…*n*−1], where *p*[*i*] is the index of the *i*-th substring (starting at *i* and with length 2*k*) in the sorted order, we will also maintain an array *c*[0…*n*−1], where *c*[*i*] corresponds to the **equivalence class** to which the substring belongs. Because some of the substrings will be identical, and the algorithm needs to treat them equally. For convenience the classes will be labeled by numbers started from zero. In addition the numbers *c*[*i*] will be assigned in such a way that they preserve information about the order: if one substring is smaller than the other, then it should also have a smaller class label. The number of equivalence classes will be stored in a variable classes.

```cpp
vector<int> sort_cyclic_shifts(string const& s) {
    int n = s.size();
    const int alphabet = 256;
    vector<int> p(n), c(n), cnt(max(alphabet, n), 0);
    for (int i = 0; i < n; i++)
        cnt[s[i]]++;
    for (int i = 1; i < alphabet; i++)
        cnt[i] += cnt[i-1];
    for (int i = 0; i < n; i++)
        p[--cnt[s[i]]] = i;
    c[p[0]] = 0;
    int classes = 1;
    for (int i = 1; i < n; i++) {
        if (s[p[i]] != s[p[i-1]])
            classes++;
        c[p[i]] = classes - 1;
    }
	vector<int> pn(n), cn(n);
    for (int h = 0; (1 << h) < n; ++h) {
        for (int i = 0; i < n; i++) {
            pn[i] = p[i] - (1 << h);
            if (pn[i] < 0)
                pn[i] += n;
        }
        fill(cnt.begin(), cnt.begin() + classes, 0);
        for (int i = 0; i < n; i++)
            cnt[c[pn[i]]]++;
        for (int i = 1; i < classes; i++)
            cnt[i] += cnt[i-1];
        for (int i = n-1; i >= 0; i--)
            p[--cnt[c[pn[i]]]] = pn[i];
        cn[p[0]] = 0;
        classes = 1;
        for (int i = 1; i < n; i++) {
            pair<int, int> cur = {c[p[i]], c[(p[i] + (1 << h)) % n]};
            pair<int, int> prev = {c[p[i-1]], c[(p[i-1] + (1 << h)) % n]};
            if (cur != prev)
                ++classes;
            cn[p[i]] = classes - 1;
        }
        c.swap(cn);
    }
    return p;
}
```

## Aho-Corasick algorithm

### Construction of Trie

```cpp
const int K = 26;

struct Vertex {
    int next[K];
    bool leaf = false;

    Vertex() {
        fill(begin(next), end(next), -1);
    }
};

vector<Vertex> trie(1);
```

```cpp
void add_string(string const& s) {
    int v = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (trie[v].next[c] == -1) {
            trie[v].next[c] = trie.size();
            trie.emplace_back();
        }
        v = trie[v].next[c];
    }
    trie[v].leaf = true;
}
```

### Construction of an automaton

More strictly, let us be in a state *p* corresponding to the string *t*, and we want to transition to a different state with the character *c*. If there is an edge labeled with this letter *c*, then we can simply go over this edge, and get the vertex corresponding to *t*+*c*. If there is no such edge, then we must find the state corresponding to the longest proper suffix of the string *t* (the longest available in the trie), and try to perform a transition via *c* from there.

A **suffix link** for a vertex *p* is a edge that points to the longest proper suffix of the string corresponding to the vertex *p*. The only special case is the root of the trie, the suffix link will  point to itself. Now we can reformulate the statement about the transitions in the  automaton like this: while from the current vertex of the trie there is no transition using  the current letter (or until we reach the root), we follow the suffix  link.

Note that if we want to find a suffix link for some vertex *v*, then we firstly have the base case that the root vertex has its suffix  link as itself, and all nodes that are immediate children of the root  vertex (i.e the vertices associated with prefixes of length one) also  have their suffix links as the root vertex. Moreover, the suffix links  of all deeper vertices can be evaluated as follows: we can go to the  ancestor *p* of this current vertex (let *c* be the letter of the edge from *p* to *v*), then follow its suffix link, and perform the transition with the letter *c* from there.

```cpp
const int K = 26;

struct Vertex {
    int next[K];
    bool leaf = false;
    int p = -1;
    char pch;
    int link = -1;
    int go[K];

    Vertex(int p=-1, char ch='$') : p(p), pch(ch) {
        fill(begin(next), end(next), -1);
        fill(begin(go), end(go), -1);
    }
};

vector<Vertex> t(1);

void add_string(string const& s) {
    int v = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (t[v].next[c] == -1) {
            t[v].next[c] = t.size();
            t.emplace_back(v, ch);
        }
        v = t[v].next[c];
    }
    t[v].leaf = true;
}

int go(int v, char ch);

int get_link(int v) {
    if (t[v].link == -1) {
        if (v == 0 || t[v].p == 0)
            t[v].link = 0;
        else
            t[v].link = go(get_link(t[v].p), t[v].pch);
    }
    return t[v].link;
}

int go(int v, char ch) {
    int c = ch - 'a';
    if (t[v].go[c] == -1) {
        if (t[v].next[c] != -1)
            t[v].go[c] = t[v].next[c];
        else
            t[v].go[c] = v == 0 ? 0 : go(get_link(v), ch);
    }
    return t[v].go[c];
} 
```

### Application

#### Find all strings from a given set in a text

#### Finding the lexicographical smallest string of a given length that doesn't match any given strings

#### Finding the shortest string containing all given strings

#### Finding the lexicographical smallest string of length *L* containing *k* strings

## Suffix Tree. Ukkonen's Algorithm

## Suffix Automaton

## Lyndon factorization

