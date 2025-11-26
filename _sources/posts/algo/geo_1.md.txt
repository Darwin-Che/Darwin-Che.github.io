---
blogpost: true
date: 2022-07-25
tags: ["algo","geometry"]
category: Blog
author: myself
---

# Geometry

## Linear operations

```cpp
struct point2d {
    ftype x, y;
    point2d() {}
    point2d(ftype x, ftype y): x(x), y(y) {}
    point2d& operator+=(const point2d &t) {
        x += t.x;
        y += t.y;
        return *this;
    }
    point2d& operator-=(const point2d &t) {
        x -= t.x;
        y -= t.y;
        return *this;
    }
    point2d& operator*=(ftype t) {
        x *= t;
        y *= t;
        return *this;
    }
    point2d& operator/=(ftype t) {
        x /= t;
        y /= t;
        return *this;
    }
    point2d operator+(const point2d &t) const {
        return point2d(*this) += t;
    }
    point2d operator-(const point2d &t) const {
        return point2d(*this) -= t;
    }
    point2d operator*(ftype t) const {
        return point2d(*this) *= t;
    }
    point2d operator/(ftype t) const {
        return point2d(*this) /= t;
    }
};
point2d operator*(ftype a, point2d b) {
    return b * a;
}
```

```cpp
struct point3d {
    ftype x, y, z;
    point3d() {}
    point3d(ftype x, ftype y, ftype z): x(x), y(y), z(z) {}
    point3d& operator+=(const point3d &t) {
        x += t.x;
        y += t.y;
        z += t.z;
        return *this;
    }
    point3d& operator-=(const point3d &t) {
        x -= t.x;
        y -= t.y;
        z -= t.z;
        return *this;
    }
    point3d& operator*=(ftype t) {
        x *= t;
        y *= t;
        z *= t;
        return *this;
    }
    point3d& operator/=(ftype t) {
        x /= t;
        y /= t;
        z /= t;
        return *this;
    }
    point3d operator+(const point3d &t) const {
        return point3d(*this) += t;
    }
    point3d operator-(const point3d &t) const {
        return point3d(*this) -= t;
    }
    point3d operator*(ftype t) const {
        return point3d(*this) *= t;
    }
    point3d operator/(ftype t) const {
        return point3d(*this) /= t;
    }
};
point3d operator*(ftype a, point3d b) {
    return b * a;
}
```

## Dot product

```cpp
ftype dot(point2d a, point2d b) {
    return a.x * b.x + a.y * b.y;
}
ftype dot(point3d a, point3d b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}
```

### Properties

We can define many geometrical properties via the dot product. For example 

Norm : $|a|^2 = a \cdot a$

Projection a onto b: $\frac{a \cdot b}{|b|}$

Angle between vectors : $arccos (\frac{a \cdot b} {|a| \cdot |b|})$

```cpp
ftype norm(point2d a) {
    return dot(a, a);
}
double abs(point2d a) {
    return sqrt(norm(a));
}
double proj(point2d a, point2d b) {
    return dot(a, b) / abs(b);
}
double angle(point2d a, point2d b) {
    return acos(dot(a, b) / abs(a) / abs(b));
}
```

In 2D these vectors will form a line, in 3D they will form a plane. Note that this result allows us to define a line in 2D as **r**⋅**n**=*C* or (**r**−**r**0)⋅**n**=0 where **n** is vector orthogonal to the line and **r**0 is any vector already present on the line and *C*=**r**0⋅**n**. In the same manner a plane can be defined in 3D.

## Cross product

$$
a \cross b = -b \cross a \\
(\alpha \cdot a) \cross b = \alpha \cdot a \cross b \\
a \cdot (b \cross c) = b \cdot (c \cross a) = -a \cdot (c \cross b)
$$

If we will take the sign into consideration then the area will be positive if the rotation from **a** to **b** (i.e. from the view of the point of **e***z*) is performed counter-clockwise and negative otherwise. That defines the pseudo-scalar product. Note that it also equals |**a**|⋅|**b**|sin*θ* where *θ* is angle from **a** to **b** count counter-clockwise (and negative if rotation is clockwise).

```cpp
point3d cross(point3d a, point3d b) {
    return point3d(a.y * b.z - a.z * b.y,
                   a.z * b.x - a.x * b.z,
                   a.x * b.y - a.y * b.x);
}
ftype triple(point3d a, point3d b, point3d c) {
    return dot(a, cross(b, c));
}
ftype cross(point2d a, point2d b) {
    return a.x * b.y - a.y * b.x;
}
```

As for the cross product, it equals to the zero vector iff the vectors **a** and **b** are collinear (they form a common line, i.e. they are parallel). The same thing holds for the triple product, it is equal to zero iff the vectors **a**, **b** and **c** are coplanar (they form a common plane).

From this we can obtain universal equations defining lines and planes. A line can be defined via its direction vector **d** and an initial point **r**0 or by two points **a** and **b**. It is defined as (**r**−**r**0)×**d**=0 or as (**r**−**a**)×(**b**−**a**)=0. As for planes, it can be defined by three points **a**, **b** and **c** as (**r**−**a**)⋅((**b**−**a**)×(**c**−**a**))=0 or by initial point **r**0 and two direction vectors lying in this plane **d**1 and **d**2: (**r**−**r**0)⋅(**d**1×**d**2)=0.

In 2D the pseudo-scalar product also may be used to check the  orientation between two vectors because it is positive if the rotation  from the first to the second vector is clockwise and negative otherwise. And, of course, it can be used to calculate areas of polygons, which is  described in a different article. A triple product can be used for the same purpose in 3D space.

## Exercises

### Line intersection

```cpp
point2d intersect(point2d a1, point2d d1, point2d a2, point2d d2) {
    return a1 + cross(a2 - a1, d2) / cross(d1, d2) * d1;
}
```

### Planes intersection

Don't understand

## Finding the equation of a line for a segment

### Two-dimensional case

Given $P_x, P_y, Q_x, Q_y$.

It is necessary to construct **the equation of a line in the plane** passing through this segment, i.e. find the coefficients *A*,*B*,*C* in the equation of a line: $Ax + By + C = 0$.
$$
A = P_y - Q_y \\
B = Q_x - P_x \\
C = -A P_x - B P_y
$$

### Integer case

An important advantage of this method of constructing a straight line is that if the coordinates of the ends were integer, then the  coefficients obtained will also be **integer** . In some cases, this allows one to perform geometric operations without resorting to real numbers at all.

However, there is a small drawback: for the same straight line different triples of coefficients can be obtained. To avoid this, but do not go away from the integer coefficients, you can apply the following technique, often called **rationing**. Find the [greatest common divisor](https://cp-algorithms.com/algebra/euclid-algorithm.html) of numbers |*A*|,|*B*|,|*C*| , we divide all three coefficients by it, and then we make the normalization of the sign: if *A*<0 or *A*=0,*B*<0 then multiply all three coefficients by −1 . As a result, we will come to the conclusion that for identical straight  lines, identical triples of coefficients will be obtained, which makes  it easy to check straight lines for equality.

### Real case

When working with real numbers, you should always be aware of errors.

The coefficients *A* and *B* will have the order of the original coordinates, the coefficient *C* is of the order of the square of them. This may already be quite large numbers, and, for example, when we [intersect straight lines](https://cp-algorithms.com/geometry/lines-intersection.html), they will become even larger, which can lead to large rounding errors  already when the coordinates of the end points are of order 103.

Therefore, when working with real numbers, it is desirable to produce the so-called **normalization**, this is straightforward: namely, to make the coefficients such that *A*^2+*B*^2=1 .

Finally, we mention the **comparison** of straight lines -  in fact, after such a normalization, for the same straight line, only  two triples of coefficients can be obtained: up to multiplication by −1. Accordingly, if we make an additional normalization taking into account the sign (if *A*<−*ε*  or |*A*|<*ε*, *B*<−*ε* then multiply by −1 ), the resulting coefficients will be unique.

### Three-dimensional and multidimensional case

Already in the three-dimensional case there is **no simple equation** describing a straight line (it can be defined as the intersection of  two planes, that is, a system of two equations, but this is an  inconvenient method).

Consequently, in the three-dimensional and multidimensional cases we must use the **parametric method of defining a straight line** , $p + vt, t \in \R$.

## Intersection Point of Lines

You are given two lines, described via the equations *a*1*x*+*b*1*y*+*c*1=0 and  *a*2*x*+*b*2*y*+*c*2=0. We have to find the intersection point of the lines, or determine that the lines are parallel.

### Solution

If two lines are not parallel, they intersect. To find their intersection point, we need to solve the system of linear equations.

Using Cramer's rule, we can immediately write down the solution for the  system, which will give us the required intersection point of the lines:
$$
x = - \frac{c_1b_2-c_2b_1} {a_1b_2 - a_2b_1}\\
y = - \frac{a_1c_2 - a_2c_1} {a_1b_2-a_2b_1}
$$
If the denominator equals 0, then either the system has no solutions (the lines are parallel and  distinct) or there are infinitely many solutions (the lines overlap). If $a_1c_2-a_2c_1 = 0 = c_1b_2-c_2b_1$, then overlap.

Notice, a different approach for computing the intersection point is explained in the article [Basic Geometry](https://cp-algorithms.com/geometry/basic-geometry.html).

### Implementation

```cpp
struct pt {
    double x, y;
};

struct line {
    double a, b, c;
};

const double EPS = 1e-9;

double det(double a, double b, double c, double d) {
    return a*d - b*c;
}

bool intersect(line m, line n, pt & res) {
    double zn = det(m.a, m.b, n.a, n.b);
    if (abs(zn) < EPS)
        return false;
    res.x = -det(m.c, m.b, n.c, n.b) / zn;
    res.y = -det(m.a, m.c, n.a, n.c) / zn;
    return true;
}

bool parallel(line m, line n) {
    return abs(det(m.a, m.b, n.a, n.b)) < EPS;
}

bool equivalent(line m, line n) {
    return abs(det(m.a, m.b, n.a, n.b)) < EPS
        && abs(det(m.a, m.c, n.a, n.c)) < EPS
        && abs(det(m.b, m.c, n.b, n.c)) < EPS;
}
```

## Check if two segments intersect

You are given two segments (*a*,*b*) and (*c*,*d*). You have to check if they intersect. Of course, you may find their intersection and check if it isn't empty,  but this can't be done in integers for segments with integer  coordinates. The approach described here can work in integers.

### Algorithm

Firstly, consider the case when the segments are part of the same line. In this case it is sufficient to check if their projections on *O**x* and *O**y* intersect. In the other case *a* and *b* must not lie on the same side of line (*c*,*d*), and *c* and *d* must not lie on the same side of line (*a*,*b*). It can be checked with a couple of cross products.

```cpp
struct pt {
    long long x, y;
    pt() {}
    pt(long long _x, long long _y) : x(_x), y(_y) {}
    pt operator-(const pt& p) const { return pt(x - p.x, y - p.y); }
    long long cross(const pt& p) const { return x * p.y - y * p.x; }
    long long cross(const pt& a, const pt& b) const { return (a - *this).cross(b - *this); }
};

int sgn(const long long& x) { return x >= 0 ? x ? 1 : 0 : -1; }

bool inter1(long long a, long long b, long long c, long long d) {
    if (a > b)
        swap(a, b);
    if (c > d)
        swap(c, d);
    return max(a, c) <= min(b, d);
}

bool check_inter(const pt& a, const pt& b, const pt& c, const pt& d) {
    if (c.cross(a, d) == 0 && c.cross(b, d) == 0)
        return inter1(a.x, b.x, c.x, d.x) && inter1(a.y, b.y, c.y, d.y);
    return sgn(a.cross(b, c)) != sgn(a.cross(b, d)) &&
           sgn(c.cross(d, a)) != sgn(c.cross(d, b));
}
```

## Finding Intersection of Two Segments

### Solution

We can find the intersection point of segments in the same way as [the intersection of lines](https://cp-algorithms.com/geometry/lines-intersection.html):  reconstruct line equations from the segments' endpoints and check whether they are parallel. 

If the lines are not parallel, we need to find their point of intersection and check whether it belongs to both segments (to do this it's sufficient to verify that the intersection point belongs to each segment projected on X and Y axes).  In this case the answer will be either "no intersection" or the single point of lines' intersection.

The case of parallel lines is slightly more complicated (the case of  one or more segments being a single point also belongs here). In this case we need to check that both segments belong to the same  line. If they don't, the answer is "no intersection". If they do, the answer is the intersection of the segments belonging to  the same line, which is obtained by  ordering the endpoints of both segments in the increasing order of  certain coordinate and taking the rightmost of left endpoints and the  leftmost of right endpoints.

If both segments are single points, these points have to be identical, and it makes sense to perform this check separately.

In the beginning of the algorithm let's add a bounding box check - it is necessary for the case when the segments belong to the same line,  and (being a lightweight check) it allows the algorithm to work faster  on average on random tests.

### Implementation

Here is the implementation, including all helper functions for lines and segments processing.

The main function `intersect` returns true if the segments have a non-empty intersection,  and stores endpoints of the intersection segment in arguments `left` and `right`.  If the answer is a single point, the values written to `left` and `right` will be the same.

```cpp
const double EPS = 1E-9;

struct pt {
    double x, y;

    bool operator<(const pt& p) const
    {
        return x < p.x - EPS || (abs(x - p.x) < EPS && y < p.y - EPS);
    }
};

struct line {
    double a, b, c;

    line() {}
    line(pt p, pt q)
    {
        a = p.y - q.y;
        b = q.x - p.x;
        c = -a * p.x - b * p.y;
        norm();
    }

    void norm()
    {
        double z = sqrt(a * a + b * b);
        if (abs(z) > EPS)
            a /= z, b /= z, c /= z;
    }

    double dist(pt p) const { return a * p.x + b * p.y + c; }
};

double det(double a, double b, double c, double d)
{
    return a * d - b * c;
}

inline bool betw(double l, double r, double x)
{
    return min(l, r) <= x + EPS && x <= max(l, r) + EPS;
}

inline bool intersect_1d(double a, double b, double c, double d)
{
    if (a > b)
        swap(a, b);
    if (c > d)
        swap(c, d);
    return max(a, c) <= min(b, d) + EPS;
}

bool intersect(pt a, pt b, pt c, pt d, pt& left, pt& right)
{
    if (!intersect_1d(a.x, b.x, c.x, d.x) || !intersect_1d(a.y, b.y, c.y, d.y))
        return false;
    line m(a, b);
    line n(c, d);
    double zn = det(m.a, m.b, n.a, n.b);
    if (abs(zn) < EPS) {
        if (abs(m.dist(c)) > EPS || abs(n.dist(a)) > EPS)
            return false;
        if (b < a)
            swap(a, b);
        if (d < c)
            swap(c, d);
        left = max(a, c);
        right = min(b, d);
        return true;
    } else {
        left.x = right.x = -det(m.c, m.b, n.c, n.b) / zn;
        left.y = right.y = -det(m.a, m.c, n.a, n.c) / zn;
        return betw(a.x, b.x, left.x) && betw(a.y, b.y, left.y) &&
               betw(c.x, d.x, left.x) && betw(c.y, d.y, left.y);
    }
}
```

## Circle-Line Intersection

```cpp
double r, a, b, c; // given as input
double x0 = -a*c/(a*a+b*b), y0 = -b*c/(a*a+b*b);
if (c*c > r*r*(a*a+b*b)+EPS)
    puts ("no points");
else if (abs (c*c - r*r*(a*a+b*b)) < EPS) {
    puts ("1 point");
    cout << x0 << ' ' << y0 << '\n';
}
else {
    double d = r*r - c*c/(a*a+b*b);
    double mult = sqrt (d / (a*a+b*b));
    double ax, ay, bx, by;
    ax = x0 + b * mult;
    bx = x0 - b * mult;
    ay = y0 - a * mult;
    by = y0 + a * mult;
    puts ("2 points");
    cout << ax << ' ' << ay << '\n' << bx << ' ' << by << '\n';
}
```

## Circle-Circle Intersection

Let's reduce this problem to the [circle-line intersection problem](https://cp-algorithms.com/geometry/circle-line-intersection.html).

Assume first circle is at origin, subtract second circle equation by first circle equation.

The number of common tangents to two circles can be **0,1,2,3,4** and **infinite**. Look at the images for different cases.

Here, we won't be considering **degenerate** cases, i.e *when the circles coincide (in this case they have infinitely many common  tangents), or one circle lies inside the other (in this case they have  no common tangents, or if the circles are tangent, there is one common  tangent).*

In most cases, two circles have **four** common tangents.

If the circles **are tangent** , then they will have three common tangents, but this can be understood as a degenerate case: as if the two tangents coincided.

Moreover, the algorithm described below will work in the case when  one or both circles have zero radius: in this case there will be,  respectively, two or one common tangent.

Summing up, we will always look for **four tangents**  for all cases except infinite tangents case (The infinite tangents case  needs to be handled separately and it is not discussed here). In  degenerate cases, some of tangents will coincide, but nevertheless,  these cases will also fit into the big picture.

### Algorithm

