# scs_python
[![Build Status](https://travis-ci.org/ajfriend/scs_python.svg?branch=master)](https://travis-ci.org/ajfriend/scs_python)

`scs_python` is a Python interface, written in Cython, for [SCS](https://github.com/cvxgrp/scs), a numerical optimization package in C for solving convex cone problems.

SCS solves convex cone programs via operator splitting.
It can solve: linear programs (LPs), second-order cone programs (SOCPs),
semidefinite programs (SDPs), exponential cone programs (ECPs), and
power cone programs (PCPs), or problems with any combination of these
cones.

Most users will not interact with SCS directly. The most common use-case is as
a back-end to a convex optimization modeling framework like [CVXPY](http://www.cvxpy.org).

Advanced users can consult the interface notes below or the [tutorial IPython notebook](tutorial.ipynb). For more complete definitions of the input data format, convex cones, and output variables, please see the [`SCS README`](https://github.com/cvxgrp/scs/blob/master/README.md) or the [SCS Paper](http://web.stanford.edu/~boyd/papers/scs.html).

## Installation
### Pip
- XXX: not yet uploaded to PyPI, so `pip` won't work
- `pip install scs`

### Building from source
Users can also install by cloning this GitHub repo and running
`python setup.py install --cython`. This method requires that the user
has Cython installed (`pip install cython`).

## Usage
The basic usage is almost identical to the existing SCS Python interface: 
```python
import scs
result = scs.solve(data, cone, sol=None, **settings)
```

We describe the arguments briefly below. For more detail, please see the [`SCS README`](https://github.com/cvxgrp/scs/blob/master/README.md).

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
- default settings can be seen by calling `scs.default_settings()`
- `result` is a `dict` with keys:
    - `'x'`: `numpy` array
    - `'y'`: `numpy` array
    - `'s'`: `numpy` array
    - `'info'`: `dict` containing solver status information

## Warm-starting
The solver can be warm-started, that is, started from a point close to the final solution in the hope of reducing the solve-time. You must supply `numpy` arrays for for **all** of the warm-started variables `x`, `y`, and `s`. Pass them via the `sol` parameter in the `scs.solve()` function with the setting `warm_start=True`:

```python
sol = {'x': x, 'y': y, 's': s}
result = scs.solve(data, cone, sol, warm_start=True)
```

## Factorization Caching with `scs.Workspace`
When using the **direct** solver (`use_indirect=False`), a single matrix factorization is performed and used many times in the iterative procedure.
This factorization depends on the input matrix `A` but **not** on the vectors
`b` or `c`. The `scs.Workspace()` object allows us to cache this factorization
and call the iterative solve procedure many times where `b` and `c` are allowed to vary, but `A` is fixed.

The `Workspace` is instantiated with the same `data` and `cone` dictionaries
as `scs.solve()`, optional solution vectors, and optional settings:
```python
work = scs.Workspace(data, cone, sol=None, **settings)
```
(If `sol` is `None` or is omitted, `SCS` will create appropriately-sized `numpy` arrays automatically.)

Once the `Workspace` object is created, we can call its solve method
```
result = work.solve(data=None, sol=None, **settings)
```

which will re-use the matrix factorization that was computed when the `Workspace` was initialized. `result` is a `dict` with keys `x`, `y`, `s`, and `info`, just as in `scs.solve()`.

### `Workspace` state
`work.solve()` will operate on the data contained in the `work` object:

- `work.data`
- `work.cone`
- `work.settings`
- `work.sol` (these are used for warm-starting if `warm_start=True`)

Some of these data and settings **cannot** be modified between calls to `work.solve()`. They are fixed at `Workspace` initialization time:

- the `settings`: `use_indirect`, `rho_x`, `normalize`, `scale`
- `data['A']`

A copy of the `dict` of **fixed settings** is given by `work.fixed`. If any of the `work.settings` differ from `work.fixed` when `work.solve()` is called, an `Exception` will be raised.

Some of these data and settings **can** be modified between calls to `work.solve()`:
- `data['b']` and `data['c']`
- `work.sol`
- any of the `work.settings` **not** in `work.fixed`

In addition to being returned by `result = work.solve()`, the solver return status can be inspected through the `dict` `work.info`, and the solution vectors can be found in `work.sol`.

### `work.sol()` arguments
Passing `data`, `sol`, or `settings` to `work.solve()` provides one last chance to change the problem data before calling the solver. These changes persist between calls to `work.solve()`. In fact,
```
work.solve(eps=1e-5, alpha=1.1)
```

is exactly equivalent to

```
work.settings['eps'] = 1e-5
work.settings['alpha'] = 1.1
work.solve()
```

If `data` is passed to `work.solve()`, only the keys `b` and `c` will be used to update `work.data`. The `A` key will be ignored.


