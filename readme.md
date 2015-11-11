# scs_python
[![Build Status](https://travis-ci.org/ajfriend/scs_python.svg?branch=master)](https://travis-ci.org/ajfriend/scs_python)

A Python interface, written in Cython, for [SCS](https://github.com/cvxgrp/scs), a numerical optimization package in C for solving convex cone problems.

SCS solves convex cone programs via operator splitting.
It can solve: linear programs (LPs), second-order cone programs (SOCPs),
semidefinite programs (SDPs), exponential cone programs (ECPs), and
power cone programs (PCPs), or problems with any combination of these
cones.

Most users will not interact with SCS directly. The most common use-case is as
a back-end to a convex optimization modeling tool like [CVXPY](http://www.cvxpy.org).

Advanced users can consult the interface notes below or the [tutorial IPython notebook](tutorial.ipynb). For more complete definitions of the input data format, convex cones, and output variables, please see the [`SCS README`](https://github.com/cvxgrp/scs/blob/master/README.md).

## Installation
### Pip
- XXX: not yet uploaded to PyPI, so `pip` won't work
- `pip install scs`

### `setup.py`
Users can also install via by cloning this GitHub repo and running
`python setup.py install --cython`. This method requires that the user
has Cython installed (`pip install cython`).

## Usage
The usage is almost identical to the existing SCS Python interface: 
```python
import scs
result = scs(data, cone, sol=None, **settings)
```

- `data` is a Python `dict` with keys:
    - `'A'`: `scipy.sparse.csc` matrix, i.e., a matrix in Compressed Sparse Column format with `m` rows and `n` columns
    - `'b'`: 1D `numpy` array of length `m`
    - `'c'`: 1D `numpy` array of lenth `n`
- `cone` is a Python `dict` with potential keys:
    - `'f'`: `int` of linear equality constraints
    - `'l'`: `int` of linear inequality constraints
    - `'q'`: `list` of `int`s giving second-order cone sizes
    - `'s'`: `list` of `int`s giving semidefinite cone sizes
    - `'ep'`: `int` of primal exponential cones
    - `'ed'`: `int` of dual exponential cones
    - `'p'`: `list` of `float`s of primal/dual power cone parameters 
- `sol` is an **optional** `dict` of `numpy` arrays where the solution vectors (corresponding to keys `'x'`, `'y'`, and `'s'`) will be written. If `sol` is `None`, new `numpy` arrays will be created automatically. These are the starting-points used if `warm_start=True`.
- `scs` also accepts optional keyword arguments for solver settings:
    - `use_indirect`
    - `verbose`
    - `normalize`
    - `max_iters`
    - `scale`
    - `eps`
    - `cg_rate`
    - `alpha`
    - `rho_x`
    - `warm_start`
- settings are passed as keyword arguments:
    - `scs(data, cone, sol, max_iters=100)`
    - `scs(data, cone, alpha=1.4, eps=1e-5, verbose=True)`
    - `scs(data, cone, sol=None, use_indirect=True)`
- the default settings can be seen by calling `scs.default_settings()`
- `result` is a `dict` with keys:
    - `'x'`
    - `'y'`
    - `'s'`
    - `'info'`: `dict` containing solver status information

## Warm-starting
The solver can be warm-started, that is, started from a point close to the final solution in the hope of reducing the solve-time. You must supply warm-start vectors for **all** of the variables `x`, `y`, and `s`. Pass them via the `sol` parameter in the `scs()` function with the setting `warm_start=True`:

```python
sol = {'x': x, 'y': y, 's': s}
result = scs(data, cone, sol, warm_start=True)
```

## Factorization Caching
```
work = scs.Workspace(data, cone, sol=None, **settings)
result = work.solve(data=None, sol=None, **settings)
```

- call `work.solve()` many times, benefit from a one-time cost of factorization (time can be seen in info[setuptime])
- `data`, `cone`, `settings`, `sol`, `result` are the same as above
- once initialized, **some** settings for the `Workspace` cannot be modified:
    - `'use_indirect'`
    - `'rho_x'`
    - `'normalize'`
    - `'scale'`
- if `sol` is `None`, solution vectors will be created for you automatically
- the `Workspace` data can be inspected once created
    - `data`
    - `cone`
    - `sol`
    - `info`
    - `settings`
- the user can modify `data['b']` and `data['c']` between calls to `work.solve()`
- `data['A']` should never be modified or replaced
- `cone` cannot be modified
- `work.solve()` will solve the sytem using whatever state the `work` object is currently in, including `sol`, `data['b']`, `data['c']`, and `settings`
- `work.solve(data, sol, **settings)` will modify the object state one last time before calling the solve method
    - note that the `'A'` key in `data` will be ignored in updating the state
    - some of the `settings` are not allowed to change
- solve method checks the settings for unallowed changes before solving (and maybe just overwrites them)
