---
blogpost: true
date: 2022-07-25
tags: ["algo","combinatorics"]
category: Blog
author: myself
---

# Combinatorics Algorithms

## Finding Power of Factorial Divisor

```cpp
int fact_pow (int n, int k) {
    int res = 0;
    while (n) {
        n /= k;
        res += n;
    }
    return res;
}
```

## Binomial Coefficients

### Calculation

$$
\binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

$$
\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}
$$

### Properties

$$
\binom{n}{k} = \binom{n}{n-k}
$$

$$
\binom{n}{k} = \frac{n}{k} \binom{n-1}{k-1}
$$

$$
\sum_{k=0}^n \binom{n}{k} = 2^n
$$

$$
\sum_{m=0}^n \binom{m}{k} = \binom{n+1}{k+1}
$$

$$
\sum_{k=0}^m \binom{n+k}{k} = \binom{n+m+1}{m}
$$

$$
\binom{n}{0}^2 + \binom{n}{1}^2 + ... + \binom{n}{n}^2 = \binom{2n}{n}
$$

$$
1\binom{n}{1}+2\binom{n}{2}+...+n\binom{n}{n} = n2^{n-1}
$$

$$
\binom{n}{0} + \binom{n-1}{1} + \binom{n-2}{2} + ... + \binom{0}{n} = F_{n+1}
$$

### Calculation

#### Straightforward calculation using analytical formula

The first, straightforward formula is very easy to code, but this method is likely to overflow even for relatively small values of *n* and *k* (even if the answer completely fit into some datatype, the calculation  of the intermediate factorials can lead to overflow). Therefore, this  method often can only be used with [long arithmetic](https://cp-algorithms.com/algebra/big-integer.html):

```cpp
int C(int n, int k) {
    int res = 1;
    for (int i = n - k + 1; i <= n; ++i)
        res *= i;
    for (int i = 2; i <= k; ++i)
        res /= i;
    return res;
}
```

#### Improved implementation

Note that in the above implementation numerator and denominator have the same number of factors (*k*), each of which is greater than or equal to 1. Therefore, we can replace our fraction with a product *k* fractions, each of which is real-valued. However, on each step after  multiplying current answer by each of the next fractions the answer will still be integer (this follows from the property of factoring in). C++  implementation:

```cpp
int C(int n, int k) {
    double res = 1;
    for (int i = 1; i <= k; ++i)
        res = res * (n - k + i) / i;
    return (int)(res + 0.01);
}
```

Here we carefully cast the floating point number to an integer, taking  into account that due to the accumulated errors, it may be slightly less than the true value (for example, 2.99999 instead of 3).

#### Pascal's Triangle

By using the recurrence relation we can construct a table of binomial  coefficients (Pascal's triangle) and take the result from it. The  advantage of this method is that intermediate results never exceed the  answer and calculating each new table element requires only one  addition. The flaw is slow execution for large *n* and *k* if you just need a single value and not the whole table. $O(n^2)$

```cpp
const int maxn = ...;
int C[maxn + 1][maxn + 1];
C[0][0] = 1;
for (int n = 1; n <= maxn; ++n) {
    C[n][0] = C[n][n] = 1;
    for (int k = 1; k < n; ++k)
        C[n][k] = C[n - 1][k - 1] + C[n - 1][k];
}
```

If the entire table of values is not necessary, storing only two last rows of it is sufficient (current *n*-th row and the previous *n*−1-th).

#### Calculation in *O*(1)

Finally, in some situations it is beneficial to precompute all the  factorials in order to produce any necessary binomial coefficient with  only two divisions later. This can be advantageous when using [long arithmetic](https://cp-algorithms.com/algebra/big-integer.html), when the memory does not allow precomputation of the whole Pascal's triangle.

### Computing binomial coefficients modulo *m*

#### Binomial coefficient for small *n*

Pascal's triangle $O(n^2)$

#### Binomial coefficient modulo large prime m

$$
\binom{n}{k} \equiv n! \cdot (k!)^{-1} \cdot ((n-k)!)^{-1} \pmod m
$$

First we precompute all factorials modulo *m* up to MAXN! in *O*(MAXN) time.

```cpp
factorial[0] = 1;
for (int i = 1; i <= MAXN; i++) {
    factorial[i] = factorial[i - 1] * i % m;
}
```

And afterwards we can compute the binomial coefficient in *O*(log*m*) time.

```cpp
long long binomial_coefficient(int n, int k) {
    return factorial[n] * inverse(factorial[k] * factorial[n - k] % m) % m;
}
```

We even can compute the binomial coefficient in *O*(1) time if we precompute the inverses of all factorials in *O*(MAXNlog*m*) using the regular method for computing the inverse, or even in *O*(MAXN) time using the congruence (*x*!)−1≡((*x*−1)!)−1⋅*x*−1 and the method for [computing all inverses](https://cp-algorithms.com/algebra/module-inverse.html#mod-inv-all-num) in *O*(*n*).

```cpp
long long binomial_coefficient(int n, int k) {
    return factorial[n] * inverse_factorial[k] % m * inverse_factorial[n - k] % m;
}
```

#### Binomial coefficient modulo prime power  {#mod-prime-pow}

Here we want to compute the binomial coefficient modulo some prime power, i.e. $m = p^b$ for some prime *p*.

If $p > \max(k, n-k)$, then we can use the same method in previous section. But otherwise, at least one of $k!$ and $(n-k)!$ is not coprime with $m$. and therefore we cannot compute the inverses. Nevertheless we can compute the binomial coefficient.

The idea is the following: We compute for each $x!$ the biggest exponent *c* such that $p^c$ divides *x*!, i.e. $p^c | x!$. Let $c(x)$ be that number. And let $g(x) = \frac{x!}{p^c}$. Then we can write the binomial coefficient as:
$$
\binom{n}{k} = \frac{g(n)p^{c(n)}}{g(k)p^{c(k)}g(n-k)p^{c(n-k)}} = \frac{g(n)}{g(k)g(n-k)}p^{c(n)-c(k)-c(n-k)}
$$
The interesting thing is, that *g*(*x*) is now free from the prime divisor *p*. Therefore *g*(*x*) is coprime to m, and we can compute the modular inverses of *g*(*k*) and *g*(*n*−*k*).

After precomputing all values for *g* and *c*, which can be done efficiently using dynamic programming in **(*n*), we can compute the binomial coefficient in *O*(log*m*) time. Or precompute all inverses and all powers of *p*, and then compute the binomial coefficient in *O*(1).

Notice, if *c*(*n*)−*c*(*k*)−*c*(*n*−*k*)≥*b*, than *p**b* | *p**c*(*n*)−*c*(*k*)−*c*(*n*−*k*), and the binomial coefficient is 0.

#### Binomial coefficient modulo an arbitrary number

Apply chinese remainder theorem on previous section

#### Binomial coefficient for large *n* and small modulo

don't understand

## Catalan Numbers

### Application in some combinatorial problems

The Catalan number $C_n$ is the solution for

- Number of correct bracket sequence consisting of *n* opening and *n* closing brackets.
- The number of rooted full binary trees with *n*+1 leaves (vertices are not numbered). A rooted binary tree is full if every vertex has either two children or no children.
- The number of ways to completely parenthesize *n*+1 factors.
- The number of triangulations of a convex polygon with *n*+2 sides (i.e. the number of partitions of polygon into disjoint triangles by using the diagonals).
- The number of ways to connect the 2*n* points on a circle to form *n* disjoint chords.
- The number of [non-isomorphic](https://en.wikipedia.org/wiki/Graph_isomorphism) full binary trees with *n* internal nodes (i.e. nodes having at least one son).
- The number of monotonic lattice paths from point (0,0) to point (*n*,*n*) in a square lattice of size *n*×*n*, which do not pass above the main diagonal (i.e. connecting (0,0) to (*n*,*n*)).
- Number of permutations of length *n* that can be [stack sorted](https://en.wikipedia.org/wiki/Stack-sortable_permutation) (i.e. it can be shown that the rearrangement is stack sorted if and only if there is no such index *i*<*j*<*k*, such that *a**k*<*a**i*<*a**j* ).
- The number of [non-crossing partitions](https://en.wikipedia.org/wiki/Noncrossing_partition) of a set of *n* elements.
- The number of ways to cover the ladder 1…*n* using *n* rectangles (The ladder consists of *n* columns, where *i**t**h* column has a height *i*).

### Calculations

There are two formulas for the Catalan numbers: **Recursive and Analytical**. Since, we believe that all the mentioned above problems are equivalent  (have the same solution), for the proof of the formulas below we will  choose the task which it is easiest to do.

#### Recursive formula

$$
C_0 = C_1 = 1 \\
C_n = \sum_{k=0}^{n-1}C_kC_{n-1-k}
$$

The recurrence formula can be easily deduced from the problem of the correct bracket sequence.

```cpp
const int MOD = ....
const int MAX = ....
int catalan[MAX];
void init() {
    catalan[0] = catalan[1] = 1;
    for (int i=2; i<=n; i++) {
        catalan[i] = 0;
        for (int j=0; j < i; j++) {
            catalan[i] += (catalan[j] * catalan[i-j-1]) % MOD;
            if (catalan[i] >= MOD) {
                catalan[i] -= MOD;
            }
        }
    }
}
```

#### Analytical formula

$$
C_n = \frac{1}{n+1}\binom{2n}{n}
$$

The above formula can be easily concluded from the problem of the monotonic paths in square grid.

## The Inclusion-Exclusion Principle

