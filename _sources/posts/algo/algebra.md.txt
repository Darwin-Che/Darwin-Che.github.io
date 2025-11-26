---
blogpost: true
date: 2022-07-25
tags: ["algo","algebra"]
category: Blog
author: myself
---

# Algebra Algorithms

## Binary Exponentiation

Recursive

```c++
long long binpow(long long a, long long b) {
    if (b == 0)
        return 1;
    long long res = binpow(a, b / 2);
    if (b % 2)
        return res * res * a;
    else
        return res * res;
}
```

Iterative

```c++
long long binpow(long long a, long long b) {
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a;
        a = a * a;
        b >>= 1;
    }
    return res;
}
```

Example Problems:

Compute $x^n \mod m$​. $O(\log n)$

Compute *n*-th Fibonacci number. $O(\log n)$

Applying a permutation *k* times $O(n \log k)$

Number of paths of length *k* in a graph $O(n^3 \log k)$​

## Euclidean Algorithm for GCD and LCM

recursive

```c++
int gcd (int a, int b) {
    return b ? gcd (b, a % b) : a;
}
```

```c++
int lcm (int a, int b) {
    return a / gcd(a, b) * b;
}
```

Binary ops

```c++
int gcd(int a, int b) {
    if (!a || !b)
        return a | b;
    unsigned shift = __builtin_ctz(a | b);
    a >>= __builtin_ctz(a);
    do {
        b >>= __builtin_ctz(b);
        if (a > b)
            swap(a, b);
        b -= a;
    } while (b);
    return a << shift;
}
```

## Extended Euclidean Algorithm and Linear Diophantine Equations

EEA

```c++
int gcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}

int gcd(int a, int b, int& x, int& y) {
    x = 1, y = 0;
    int x1 = 0, y1 = 1, a1 = a, b1 = b;
    while (b1) {
        int q = a1 / b1;
        tie(x, x1) = make_tuple(x1, x - q * x1);
        tie(y, y1) = make_tuple(y1, y - q * y1);
        tie(a1, b1) = make_tuple(b1, a1 - q * b1);
    }
    return a1;
}
```

LDE

```c++
int gcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}

bool find_any_solution(int a, int b, int c, int &x0, int &y0, int &g) {
    g = gcd(abs(a), abs(b), x0, y0);
    if (c % g) {
        return false;
    }

    x0 *= c / g;
    y0 *= c / g;
    if (a < 0) x0 = -x0;
    if (b < 0) y0 = -y0;
    return true;
}
```

The set of all possible solutions are 

$$ x = x_0 + k \frac{b}{g} $$​​

$$ y = y_0 - k \frac{a}{g} $$​​



## Fibonacci Numbers

For the following, $F_0 = 0$, $F_1 = 1$.

### Properties

- Cassini's identity

  $$F_{n-1}F_{n+1} - F_n^2 = (-1)^n$$​​

- The "addition" rule

  $$F_{n+k} = F_k F_{n+1} + F_{k-1}F_n$$

  $$F_{2n} = F_n (F_{n+1} + F_{n-1})$$

  $$F_{nk}$$ is a multiple of $F_n$​, the inverse is also true.

- GCD

  $$GCD(F_n, F_m) = F_{GCD(n,m)}$$

- Lame's Theorem

  Fibonacci numbers are the worst possible inputs for Euclidean algorithm. 

### Binet's formula

$$F_n = \frac{(\frac{1+\sqrt{5}}{2})^n - (\frac{1-\sqrt{5}}{2})^n}{\sqrt{5}} = [ \frac{(\frac{1+\sqrt{5}}{2})^n }{\sqrt{5}} ]$$

### Matrix Recursion

Let $P = \begin{pmatrix}0 & 1 \\ 1 & 1 \end{pmatrix}$​, then

$$ \begin{pmatrix} F_{n-1} & F_{n} \end{pmatrix} =  \begin{pmatrix} F_{n-2} & F_{n-1}\end{pmatrix} \cdot P$$​​

$$ \begin{pmatrix} F_n & F_{n+1} \end{pmatrix} =  \begin{pmatrix} F_0 & F_1 \end{pmatrix} \cdot P^n$$​

### Fast Doubling Method

$$F_{2k} = F_k \cdot (2F_{k+1} - F_k)$$

$$F_{2k+1} = F_{k+1}^2 + F_k^2$$​

```c++
// return F_n, F_{n+1}
pair<int, int> fib (int n) {
    if (n == 0)
        return {0, 1};

    auto p = fib(n >> 1);
    int c = p.first * (2 * p.second - p.first);
    int d = p.first * p.first + p.second * p.second;
    if (n & 1)
        return {d, c + d};
    else
        return {c, d};
}
```

Consider the Fibonacci sequence modulo *p*. We will prove the sequence is periodic and the period begins with $F_1 = 1$ (that is, the pre-period contains only $F_0$).

## Sieve of Eratosthenes

```c++
int n;
vector<bool> is_prime(n+1, true);
is_prime[0] = is_prime[1] = false;
for (int i = 2; i <= n; i++) {
    if (is_prime[i] && (long long)i * i <= n) {
        for (int j = i * i; j <= n; j += i)
            is_prime[j] = false;
    }
}
```

The algorithm will perform $\frac{n}{p}$ operations for each prime $p \le n$. 

So the runtime is $n \cdot \sum \frac{1}{p}$​

Two helpful facts: 

- The number of prime numbers less than or equal to $n$ is about $\frac{n}{\ln n}$
- The $k$'th prime number is about $k \ln k$

So $$\sum \frac{1}{p} \approx \frac{1}{2} + \sum_{k=2}^{\frac{n}{\ln n}} \frac{1}{k \ln k}$$

And $$\sum_{k=2}^{\frac{n}{\ln n}} \frac{1}{k \ln k} \approx \int_{k=2}^{\frac{n}{\ln n}} \frac{1}{k \ln k} = \ln \ln \frac{n}{\ln n} - \ln \ln 2 \approx \ln \ln n $$

### Different optimizations of the Sieve of Eratosthenes

#### Sieving till root

The biggest weakness of the algorithm is, that it "walks" along the memory multiple times, only manipulating single elements. This is not very cache friendly.

```c++
int n;
vector<bool> is_prime(n+1, true);
is_prime[0] = is_prime[1] = false;
for (int i = 2; i * i <= n; i++) {
    if (is_prime[i]) {
        for (int j = i * i; j <= n; j += i)
            is_prime[j] = false;
    }
}
```

#### Sieving by the odd numbers only

Since all even numbers (except 2) are composite, we can stop checking even numbers at all. Instead, we need to operate with odd numbers only.

First, it will allow us to half the needed memory. Second, it will  reduce the number of operations performing by algorithm approximately in half.

#### Memory consumption and speed of operations

We should notice, that these two implementations of the Sieve of Eratosthenes use *n* bits of memory by using the data structure `vector<bool>`. `vector<bool>` is not a regular container that stores a series of `bool` (as in most computer architectures a `bool` takes one byte of memory). It's a memory-optimization specialization of `vector<T>`, that only consumes *N*8 bytes of memory.

Modern processors architectures work much more efficiently with bytes than with bits as they usually cannot access bits directly. So underneath the `vector<bool>` stores the bits in a  large continuous memory, accesses the memory in blocks of a few bytes,  and extracts/sets the bits with bit operations like bit masking and bit  shifting.

Because of that there is a certain overhead when you read or write bits with a `vector<bool>`, and quite often using a `vector<char>` (which uses 1 byte for each entry, so 8x the amount of memory) is faster.

However, for the simple implementations of the Sieve of Eratosthenes using a `vector<bool>` is faster. You are limited by how fast you can load the data into the cache, and therefore using less memory gives a big advantage. A benchmark ([link](https://gist.github.com/jakobkogler/e6359ea9ced24fe304f1a8af3c9bee0e)) shows, that using a `vector<bool>` is between 1.4x and 1.7x faster than using a `vector<char>`.

### Segmented Sieve

```c++
int count_primes(int n) {
    const int S = 10000;

    vector<int> primes;
    int nsqrt = sqrt(n);
    vector<char> is_prime(nsqrt + 2, true);
    for (int i = 2; i <= nsqrt; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (int j = i * i; j <= nsqrt; j += i)
                is_prime[j] = false;
        }
    }

    int result = 0;
    vector<char> block(S);
    for (int k = 0; k * S <= n; k++) {
        fill(block.begin(), block.end(), true);
        int start = k * S;
        for (int p : primes) {
            int start_idx = (start + p - 1) / p;
            int j = max(start_idx, p) * p - start;
            for (; j < S; j += p)
                block[j] = false;
        }
        if (k == 0)
            block[0] = block[1] = false;
        for (int i = 0; i < S && start + i <= n; i++) {
            if (block[i])
                result++;
        }
    }
    return result;
}
```

### Find primes in range

Sometimes we need to find all prime numbers in a range [*L*,*R*] of small size (e.g. *R*−*L*+1≈1*e*7), where *R* can be very large (e.g. 1*e*12).

To solve such a problem, we can use the idea of the Segmented sieve. We pre-generate all prime numbers up to $\sqrt(R)$​​, and use those primes to mark all composite numbers in the segment [*L*,*R*].

```c++
// (R-L+1) log log R + sqrt(R) log log sqrt(R)
vector<char> segmentedSieve(long long L, long long R) {
    // generate all primes up to sqrt(R)
    long long lim = sqrt(R);
    vector<char> mark(lim + 1, false);
    vector<long long> primes;
    for (long long i = 2; i <= lim; ++i) {
        if (!mark[i]) {
            primes.emplace_back(i);
            for (long long j = i * i; j <= lim; j += i)
                mark[j] = true;
        }
    }

    vector<char> isPrime(R - L + 1, true);
    for (long long i : primes)
        for (long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}

```

It's also possible that we don't pre-generate all prime numbers:

```c++
// (R-L+1) log R + \sqrt(R)
vector<char> segmentedSieveNoPreGen(long long L, long long R) {
    vector<char> isPrime(R - L + 1, true);
    long long lim = sqrt(R);
    for (long long i = 2; i <= lim; ++i)
        for (long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}
```

## Sieve of Eratosthenes Having Linear Time Complexity

This will also calculate the factorization of all numbers smaller than $N$, which is useful in many cases.

```cpp
const int N = 10000000;
int lp[N+1];
vector<int> pr;

for (int i=2; i<=N; ++i) {
    if (lp[i] == 0) {
        lp[i] = i;
        pr.push_back (i);
    }
    for (int j=0; j<(int)pr.size() && pr[j]<=lp[i] && i*pr[j]<=N; ++j)
        lp[i * pr[j]] = pr[j];
}
```

We can speed it up a bit by replacing vector *p**r* with a simple array and a counter, and by getting rid of the second multiplication in the nested `for` loop (for that we just need to remember the product in a variable).

### Correctness Proof

We need to prove that the algorithm sets all values $l p[]$ correctly, and that every value will be set exactly once. Hence, the  algorithm will have linear runtime, since all the remaining actions of  the algorithm, obviously, work for *O*(*n*).

Notice that every number $i$ has exactly one representation in form: $i= lp[i] * x$,

where $lp[i]$ is the minimal prime factor of *i*, and the number *x* doesn't have any prime factors less than *l**p*[*i*] , i.e.$lp[i] \le x$.

Now, let's compare this with the actions of our algorithm: in fact, for every $x$  it goes through all prime numbers it could be multiplied by, i.e. all prime numbers up to $lp[x]$​​  inclusive, in order to get the numbers in the form given above.

Hence, the algorithm will go through every composite number exactly once, setting the correct values $lp[]$​​ there. Q.E.D.



## Primality tests

### Trial division

```c++
bool isPrime(int x) {
    for (int d = 2; d * d <= x; d++) {
        if (x % d == 0)
            return false;
    }
    return true;
}
```

### Fermat primality test

This is a probabilistic test.

$$a^{p-1} \equiv 1 \mod p$$ if p is prime. If inequality discovered for $a$, call it *Fermat witness*. If equality discovered for $a$, but p is not prime, then call it *Fermat liar*.

```c++
bool probablyPrimeFermat(int n, int iter=5) {
    if (n < 4)
        return n == 2 || n == 3;

    for (int i = 0; i < iter; i++) {
        int a = 2 + rand() % (n - 3);
        if (binpower(a, n - 1, n) != 1)
            return false;
    }
    return true;
}
```

Use binary exponentiation to obtain runtime $c \log n$.

There is one bad news though: there exist some composite numbers where $$a^{p-1} \equiv 1 \mod p$$​ holds for holds for all *a* coprime to *n*, called *Carmichael numbers*. The Fermat primality test can identify these numbers only, if we have immense luck and choose a base *a* with gcd(*a*,*n*)≠1.

### Miller-Rabin primality test

For an odd number *n*, *n*−1 is even and we can factor out all powers of 2. We can write:

$$n-1=2^s \cdot d$$, with $d$​ odd.

This allows us to factorize the equation of Fermat's little theorem:

$$(a^{2^{s-1}d}+1)(a^{2^{s-2}d}+1) \cdots (a^d + 1)(a^d - 1) \equiv 0 \mod n$$​​

If *n* is prime, then *n* has to divide one of these factors. And in the Miller-Rabin primality test we check exactly that statement,  which is a more stricter version of the statement of the Fermat test. For a base 2≤*a*≤*n*−2 we check if either

$$a^d \equiv 1 \mod n$$ 

$$a^{2^r d} \equiv -1 \mod n$$ for some $0 \le r \le s-1$​.

If we found a base *a* which doesn't satisfy any of the above equalities, than we found a *witness* for the compositeness of *n*. In this case we have proven that *n* is not a prime number.

Similar to the Fermat test, it is also possible that the set of equations is satisfied for a composite number. In that case the base *a* is called a *strong liar*. If a base *a* satisfies the equations (one of them), *n* is only *strong probable prime*. However, there are no numbers like the Carmichael numbers, where all non-trivial bases lie. In fact it is possible to show, that at most 1/4 of the bases can be strong liars. If *n* is composite, we have a probability of ≥75% that a random base will tell us that it is composite. By doing multiple iterations, choosing different random bases, we can  tell with very high probability if the number is truly prime or if it is composite.

Miller showed that it is possible to make the algorithm deterministic by only checking all bases $≤O(( \ln n)^2)$​​​. Bach later gave a concrete bound, it is only necessary to test all bases $a \le 2 ( \ln n )^2$​​​​

This is still a pretty large number of bases. So people have invested quite a lot of computation power into finding lower bounds. It turns out, for testing a 32 bit integer it is only necessary to check the first 4 prime bases: 2, 3, 5 and 7. The smallest composite number that fails this test is 3,215,031,751=151⋅751⋅28351

. And for testing 64 bit integer it is enough to check the first 12 prime bases: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, and 37.

```c++
using u64 = uint64_t;
using u128 = __uint128_t;

u64 binpower(u64 base, u64 e, u64 mod) {
    u64 result = 1;
    base %= mod;
    while (e) {
        if (e & 1)
            result = (u128)result * base % mod;
        base = (u128)base * base % mod;
        e >>= 1;
    }
    return result;
}

bool check_composite(u64 n, u64 a, u64 d, int s) {
    u64 x = binpower(a, d, n);
    if (x == 1 || x == n - 1)
        return false;
    for (int r = 1; r < s; r++) {
        x = (u128)x * x % n;
        if (x == n - 1)
            return false;
    }
    return true;
};

// deterministic version
bool MillerRabin(u64 n) { // returns true if n is prime, else returns false.
    if (n < 2)
        return false;

    int r = 0;
    u64 d = n - 1;
    while ((d & 1) == 0) {
        d >>= 1;
        r++;
    }

    for (int a : {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}) {
        if (n == a)
            return true;
        if (check_composite(n, a, d, r))
            return false;
    }
    return true;
}
```

## Integer factorization

Notice, if the number that you want to factorize is actually a prime  number, most of the algorithms, especially Fermat's factorization  algorithm, Pollard's p-1, Pollard's rho algorithm will run very slow. So it makes sense to perform a probabilistic (or a fast deterministic) primality test before trying to factorize the number.

### Trial division

```c++
vector<long long> trial_division1(long long n) {
    vector<long long> factorization;
    for (long long d = 2; d * d <= n; d++) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

### Wheel factorization

This is an optimization of the trial division. The idea is the following. Once we know that the number is not divisible by 2, we don't need to check every other even number. This leaves us with only 50% of the numbers to check. After checking 2, we can simply start with 3 and skip every other number.

```c++
vector<long long> trial_division2(long long n) {
    vector<long long> factorization;
    while (n % 2 == 0) {
        factorization.push_back(2);
        n /= 2;
    }
    for (long long d = 3; d * d <= n; d += 2) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

This method can be extended. If the number is not divisible by 3, we can also ignore all other multiples of 3 in the future computations. So we only need to check the numbers 5,7,11,13,17,19,23,…. We can observe a pattern of these remaining numbers. We need to check all numbers with *d*mod6=1 and *d*mod6=5. So this leaves us with only 33.3%

 percent of the numbers to check. We can implement this by checking the primes 2 and 3 first, and then  start checking with 5 and alternatively skip 1 or 3 numbers.

We can extend this even further. Here is an implementation for the prime number 2, 3 and 5. It's convenient to use an array to store how much we have to skip.

```cpp
vector<long long> trial_division3(long long n) {
    vector<long long> factorization;
    for (int d : {2, 3, 5}) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    static array<int, 8> increments = {4, 2, 4, 2, 4, 6, 2, 6};
    int i = 0;
    for (long long d = 7; d * d <= n; d += increments[i++]) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
        if (i == 8)
            i = 0;
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

### Precomputed primes

Extending the wheel factorization with more and more primes will leave exactly the primes to check. So a good way of checking is just to precompute all prime numbers with the [Sieve of Eratosthenes](https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html) until $\sqrt{n}$ and test them individually.

```c++
vector<long long> primes;

vector<long long> trial_division4(long long n) {
    vector<long long> factorization;
    for (long long d : primes) {
        if (d * d > n)
            break;
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

### Fermat's factorization method

We can write an odd composite number *n*=*p*⋅*q* as the difference of two squares $$n = (\frac{p+q}{2})^2 - (\frac{p-q}{2})^2$$.

```c++
int fermat(int n) {
    int a = ceil(sqrt(n));
    int b2 = a*a - n;
    int b = round(sqrt(b2));
    while (b * b != b2) {
        a = a + 1;
        b2 = a*a - n;
        b = round(sqrt(b2));
    }
    return a - b;
}
```

Notice, this factorization method can be very fast, if the difference between the two factors *p* and *q* is small. The algorithm runs in *O*(|*p*−*q*|) time. However since it is very slow, once the factors are far apart, it is rarely used in practice.

### Pollard's *p*−1 method

not understanded

## Pollard's rho algorithm

Generate sudo random sequence $\{x_0, x_1, ...\}$, and take $\mod n$​​. We try to find two $g = gcd(x_s - x_t , n) > 0$​​. Equivalently, we have found a cycle in the sequence $\mod g$​. This gives $g$ If $< n$​​ a factor. The expected run-time before a cycle appears is $O(n^{1/4})$.

### Floyd's cycle-finding algorithm

If the cycle length is *λ* and the *μ* is the first index at which the cycle starts, then the algorithm will run in *O*(*λ*+*μ*) time.

```c++
long long mult(long long a, long long b, long long mod) {
    return (__int128)a * b % mod;
}

long long f(long long x, long long c, long long mod) {
    return (mult(x, x, mod) + c) % mod;
}
// expected time O(n^{1/4} * log n)
long long rho(long long n, long long x0=2, long long c=1) {
    long long x = x0;
    long long y = x0;
    long long g = 1;
    while (g == 1) {
        x = f(x, c, n);
        y = f(y, c, n);
        y = f(y, c, n);
        g = gcd(abs(x - y), n);
    }
    return g;
}
```

### Brent's algorithm

```c++
long long brent(long long n, long long x0=2, long long c=1) {
    long long x = x0;
    long long g = 1;
    long long q = 1;
    long long xs, y;

    int m = 128;
    int l = 1;
    while (g == 1) {
        y = x;
        for (int i = 1; i < l; i++)
            x = f(x, c, n);
        int k = 0;
        while (k < l && g == 1) {
            xs = x;
            for (int i = 0; i < m && i < l - k; i++) {
                x = f(x, c, n);
                q = mult(q, abs(y - x), n);
            }
            g = gcd(q, n);
            k += m;
        }
        l *= 2;
    }
    if (g == n) {
        do {
            xs = f(xs, c, n);
            g = gcd(abs(xs - y), n);
        } while (g == 1);
    }
    return g;
}
```

The combination of a trial division for small prime numbers together  with Brent's version of Pollard's rho algorithm will make a very  powerful factorization algorithm.

## Euler's totient function

```c++
int phi(int n) {
    int result = n;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            while (n % i == 0)
                n /= i;
            result -= result / i;
        }
    }
    if (n > 1)
        result -= result / n;
    return result;
}
```

```c++
void phi_1_to_n(int n) {
    vector<int> phi(n + 1);
    phi[0] = 0;
    phi[1] = 1;
    for (int i = 2; i <= n; i++)
        phi[i] = i;

    for (int i = 2; i <= n; i++) {
        if (phi[i] == i) {
            for (int j = i; j <= n; j += i)
                phi[j] -= phi[j] / i;
        }
    }
}
```

### Divisor sum property

$$\sum_{d | n} \phi(d) = n$$

### Euler's Theorem

If a and m are relatively prime, then $a^{\phi(m)} \equiv 1 \pmod{m}$​

Results

$a^n = a^{n \mod{\phi(m)}} \pmod m$

For arbitrary x,m (not coprime), $x^n \equiv x^{\phi(m) + [n \mod \phi(m)]} \pmod m$​

## Find Modulo Inverse

### Extended Euclidean Algo

$ax+my=1$

```c++
int x, y;
int g = extended_euclidean(a, m, x, y);
if (g != 1) {
    cout << "No solution!";
}
else {
    x = (x % m + m) % m;
    cout << x << endl;
}
```

### Fermat's / Euclid Thm

$a^{\phi(m)} \equiv 1 \pmod m$

$a^{\phi(m)-1} \equiv a^{-1} \pmod m$​

Both of the above are $O(\log n)$.

### Find all number's modulo inverse from 1 to m in $O(m)$​

$inv(i) = - \lfloor \frac{m}{i} \rfloor \cdot inv(m \mod i) \pmod m$​

```c++
inv[1] = 1;
for(int i = 2; i < m; ++i)
    inv[i] = m - (m/i) * inv[m%i] % m;
```

## Linear Congruence Equation

$ax \equiv b \pmod m$

### Inverse

let $g = gcd(a,m)$

if g does not divides b, no solution. 

Otherwise, obtain $a'x' \equiv b' \pmod m'$​ where $gcd(a',m') = 1$​​.​

$x'$ will be a solution, but there are other solutions, $x_i = x' + i \cdot n'$ for $i = 0, ..., g-1$.

### Extended Euclidean Algorithm

$ax + my = b$​​



## Chinese Remainder Theorem

let $p = p_1 p_2 ... p_k$​, where $p_i$​ are relatively prime, and $a \equiv a_i \pmod p_i$​​. Then, there is exactly one solution $a \pmod p$.

### Garner's Algorithm

mixed radix representation of a is 

$a = x_1 + x_2 p_1 + x_3 p_1 p_2 + ... + x_k p_1 ...p_{k-1}$

Let $r_{ij} = (p_i)^{-1} \pmod p_j$ by prev algorithm, thus

$a_1 \equiv x_1 \pmod {p_1}$​

$a_2 \equiv x_1+x_1p_1 \pmod {p_2}$​

$x_2 \equiv (a_2 - x_1)r_{12} \pmod {p_2}$

Thus $x_3 \equiv ((a_3-x_1)r_{13} - x_2)r_{23} \pmod {p_3}$

```java
for (int i = 0; i < k; ++i) {
    x[i] = a[i];
    for (int j = 0; j < i; ++j) {
        x[i] = r[j][i] * (x[i] - x[j]);

        x[i] = x[i] % p[i];
        if (x[i] < 0)
            x[i] += p[i];
    }
}
```

## Discrete Logarithm

The discrete logarithm is an integer *x* satisfying the equation $a^x \equiv b \pmod m$, where $a$ and $m$ are relatively prime. 

Let $x = np-q$. then any number $x \in [0,m)$ can be represented in this form, $p \in [1, \lceil \frac{m}{n} \rceil]$, $q \in [0,n]$

So $a^{np} \equiv b a^{q} \pmod m$. 

This problem can be solved using the meet-in-the-middle method as follows:

- Calculate *f*1 for all possible arguments *p*. Sort the array of value-argument pairs.

- For all possible arguments *q*, calculate *f*2 and look for the corresponding *p* in the sorted array using binary search.

First step : $O(\frac{m}{n} \log m)$, Second Step : $O(n \log m)$. We can choose $n = \sqrt m$ to minimize this to get $O(\sqrt m \log m)$.

### The simplest implementation

```c++
int powmod(int a, int b, int m) {
    int res = 1;
    while (b > 0) {
        if (b & 1) {
            res = (res * 1ll * a) % m;
        }
        a = (a * 1ll * a) % m;
        b >>= 1;
    }
    return res;
}

int solve(int a, int b, int m) {
    a %= m, b %= m;
    int n = sqrt(m) + 1;
    map<int, int> vals;
    for (int p = 1; p <= n; ++p)
        vals[powmod(a, p * n, m)] = p;
    for (int q = 0; q <= n; ++q) {
        int cur = (powmod(a, q, m) * 1ll * b) % m;
        if (vals.count(cur)) {
            int ans = vals[cur] * n - q;
            return ans;
        }
    }
    return -1;
}
```

### Improved implementation

A possible improvement is to get rid of binary exponentiation. This can be done by keeping a variable that is multiplied by *a* each time we increase *q* and a variable that is multiplied by *a**n* each time we increase *p*. With this change, the complexity of the algorithm is still the same, but now the log factor is only for the `map`. Instead of a `map`, we can also use a hash table (`unordered_map` in C++) which has the average time complexity *O*(1) for inserting and searching.

Problems often ask for the minimum *x* which satisfies the solution. It is possible to get all answers and take the minimum, or reduce the first found answer using [Euler's theorem](https://cp-algorithms.com/algebra/phi-function.html#toc-tgt-2), but we can be smart about the order in which we calculate values and ensure the first answer we find is the minimum.

```c++
// Returns minimum x for which a ^ x % m = b % m, a and m are coprime.
int solve(int a, int b, int m) {
    a %= m, b %= m;
    int n = sqrt(m) + 1;

    int an = 1;
    for (int i = 0; i < n; ++i)
        an = (an * 1ll * a) % m;

    unordered_map<int, int> vals;
    for (int q = 0, cur = b; q <= n; ++q) {
        vals[cur] = q;
        cur = (cur * 1ll * a) % m;
    }

    for (int p = 1, cur = 1; p <= n; ++p) {
        cur = (cur * 1ll * an) % m;
        if (vals.count(cur)) {
            int ans = n * p - vals[cur];
            return ans;
        }
    }
    return -1;
}
```

### When *a* and *m* are not coprime

```c++
// Returns minimum x for which a ^ x % m = b % m.
int solve(int a, int b, int m) {
    a %= m, b %= m;
    int k = 1, add = 0, g;
    while ((g = gcd(a, m)) > 1) {
        if (b == k)
            return add;
        if (b % g)
            return -1;
        b /= g, m /= g, ++add;
        k = (k * 1ll * a / g) % m;
    }

    int n = sqrt(m) + 1;
    int an = 1;
    for (int i = 0; i < n; ++i)
        an = (an * 1ll * a) % m;

    unordered_map<int, int> vals;
    for (int q = 0, cur = b; q <= n; ++q) {
        vals[cur] = q;
        cur = (cur * 1ll * a) % m;
    }

    for (int p = 1, cur = k; p <= n; ++p) {
        cur = (cur * 1ll * an) % m;
        if (vals.count(cur)) {
            int ans = n * p - vals[cur] + add;
            return ans;
        }
    }
    return -1;
}
```

## Primitive Root

In modular arithmetic, a number *g* is called a `primitive root modulo n` if every number coprime to *n* is congruent to a power of *g* modulo *n*. Mathematically, *g* is a `primitive root modulo n` if and only if for any integer *a* such that gcd(*a*,*n*)=1, there exists an integer *k* such that:*g**k*≡*a*(mod*n*).*k* is then called the `index` or `discrete logarithm` of *a* to the base *g* modulo *n*. *g* is also called the `generator` of the multiplicative group of integers modulo *n*.

In particular, for the case where *n* is a prime, the powers of primitive root runs through all numbers from 1 to *n*−1.

### Existence

Primitive root modulo *n* exists if and only if:

- *n* is 1, 2, 4, or
- *n* is power of an odd prime number (*n*=*p**k*), or
- *n* is twice power of an odd prime number (*n*=2⋅*p**k*).

### Relation with the Euler function

Let *g* be a primitive root modulo *n*. Then we can show that the smallest number *k* for which *g**k*≡1(mod*n*) is equal *ϕ*(*n*). Moreover, the reverse is also true, and this fact will be used in this article to find a primitive root.

Furthermore, the number of primitive roots modulo *n*, if there are any, is equal to *ϕ*(*ϕ*(*n*)).

### Computation

don't understand

## Discrete Root

don't understand

## Montgomery Multiplication

The **Montgomery (modular) multiplication** is a method that allows computing such multiplications $ab \mod n$​ faster. Instead of dividing the product and subtracting *n* multiple times, it adds multiples of *n* to cancel out the lower bits and then just discards the lower bits.



## References 

https://cp-algorithms.com/

