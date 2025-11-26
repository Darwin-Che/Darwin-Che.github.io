---
blogpost: true
date: 2022-07-25
tags: ["algo","algebra"]
category: Blog
author: myself
---

# Linear Algebra Algorithms

## Gauss method for solving system of linear equations

The input to the function `gauss` is the system matrix *a*. The last column of this matrix is vector *b*.

Implementation notes:

The function uses two pointers - the current column *c**o**l* and the current row *r**o**w*.

For each variable *x**i*, the value *w**h**e**r**e*(*i*) is the line where this column is not zero. This vector is needed because some variables can be independent.

In this implementation, the current *i*th line is not divided by *a**i**i* as described above, so in the end the matrix is not identity matrix (though apparently dividing the *i*th line can help reducing errors).

After finding a solution, it is inserted back into the matrix - to  check whether the system has at least one solution or not. If the test  solution is successful, then the function returns 1 or inf, depending on whether there is at least one independent variable.

```cpp
const double EPS = 1e-9;
const int INF = 2; // it doesn't actually have to be infinity or a big number

int gauss (vector < vector<double> > a, vector<double> & ans) {
    int n = (int) a.size();
    int m = (int) a[0].size() - 1;

    vector<int> where (m, -1);
    for (int col=0, row=0; col<m && row<n; ++col) {
        int sel = row;
        for (int i=row; i<n; ++i)
            if (abs (a[i][col]) > abs (a[sel][col]))
                sel = i;
        if (abs (a[sel][col]) < EPS)
            continue;
        for (int i=col; i<=m; ++i)
            swap (a[sel][i], a[row][i]);
        where[col] = row;

        for (int i=0; i<n; ++i)
            if (i != row) {
                double c = a[i][col] / a[row][col];
                for (int j=col; j<=m; ++j)
                    a[i][j] -= a[row][j] * c;
            }
        ++row;
    }

    ans.assign (m, 0);
    for (int i=0; i<m; ++i)
        if (where[i] != -1)
            ans[i] = a[where[i]][m] / a[where[i]][i];
    for (int i=0; i<n; ++i) {
        double sum = 0;
        for (int j=0; j<m; ++j)
            sum += ans[j] * a[i][j];
        if (abs (sum - a[i][m]) > EPS)
            return 0;
    }

    for (int i=0; i<m; ++i)
        if (where[i] == -1)
            return INF;
    return 1;
}
```

## Calculating the determinant of a matrix by Gauss

We will perform the same steps as in the solution of systems of linear  equations, excluding only the division of the current line to *a**i**j*. These operations will not change the absolute value of the determinant  of the matrix. When we exchange two lines of the matrix, however, the  sign of the determinant can change.

```cpp
const double EPS = 1E-9;
int n;
vector < vector<double> > a (n, vector<double> (n));

double det = 1;
for (int i=0; i<n; ++i) {
    int k = i;
    for (int j=i+1; j<n; ++j)
        if (abs (a[j][i]) > abs (a[k][i]))
            k = j;
    if (abs (a[k][i]) < EPS) {
        det = 0;
        break;
    }
    swap (a[i], a[k]);
    if (i != k)
        det = -det;
    det *= a[i][i];
    for (int j=i+1; j<n; ++j)
        a[i][j] /= a[i][i];
    for (int j=0; j<n; ++j)
        if (j != i && abs (a[j][i]) > EPS)
            for (int k=i+1; k<n; ++k)
                a[j][k] -= a[i][k] * a[j][i];
}

cout << det;
```

