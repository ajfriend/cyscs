# scs_python
A Python interface, written in Cython, for [SCS](https://github.com/cvxgrp/scs), a numerical optimization package for solving convex cone problems.

## Usage
```
import scs
sol = scs(data, cone, **options)
```