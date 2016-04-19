# `scs_python` Cython Interface
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

### Building from source with Cython
Users can also install by
- cloning this GitHub repo with `git clone --recursive https://github.com/ajfriend/scs_python.git`
- installing dependencies `pip install numpy scipy cython`
- (optionally, for tests) `pip install pytest`
- running `python setup.py install --cython` inside the `scs_python` directory
- (optionally) run tests with `make test`

## Basic Usage
The basic usage is almost identical to the existing SCS Python interface: 
```python
import scs
sol = scs.solve(data, cone, warm_start=None, **settings)
```

We describe the arguments to `scs.solve()` briefly below. For more detail, please see the [`SCS README`](https://github.com/cvxgrp/scs/blob/master/README.md).

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
- `warm_start` is an **optional** `dict` of `numpy` arrays (with keys `'x'`, `'y'`, and `'s'`) used to warm-start the solver; if these values are close to the final solution, warm-starting can reduce the number of SCS iterations
- `scs.solve()` also accepts optional keyword arguments for solver settings:
    - `use_indirect`
    - `verbose`
    - `normalize`
    - `max_iters`
    - `scale`
    - `eps`
    - `cg_rate`
    - `alpha`
    - `rho_x`
- settings are passed as keyword arguments:
    - `scs.solve(data, cone, max_iters=100)`
    - `scs.solve(data, cone, alpha=1.4, eps=1e-5, verbose=True)`
    - `scs.solve(data, cone, warm_start, use_indirect=True)`
- default settings can be seen by calling `scs.default_settings()`
- `sol` is a `dict` with keys:
    - `'x'`: `numpy` array
    - `'y'`: `numpy` array
    - `'s'`: `numpy` array
    - `'info'`: `dict` containing solver status information

### Warm-starting
The solver can be warm-started, that is, started from a point close to the final solution in the hope of reducing the solve-time. You must supply `numpy` arrays for for **all** of the warm-started variables `x`, `y`, and `s`. Pass them as dictionary to the `warm_start` parameter in `scs.solve()`:

```python
ws = {'x': x, 'y': y, 's': s}
sol = scs.solve(data, cone, warm_start=ws)
```

Output from previous solves can be used to warm-start future solves:
```python
sol = scs.solve(data, cone, eps=1e-3)
sol = scs.solve(data, cone, warm_start=sol, eps=1e-4)
```


### Data Formats
Below are the integer and floating-point format expectations for input data.
If the formats are not exactly correct, `scs` will attempt to convert the data for you.

`scs` expects `b`, `c`, `x`, `y`, and `s` to be one-dimensional `numpy` arrays with `dtype` `'float64'`.

`scs` also expects `A` to be a `scipy.sparse.csc` matrix such that the values of the matrix have `dtype` `'float64'`, and the attributes `A.indices` and `A.indptr` are `numpy` arrays with `dtype` `'int64'`:

```python
>>> A.dtype
dtype('float64')
>>> A.indices.dtype, A.indptr.dtype
(dtype('int64'), dtype('int64')) 
```

Note that, by default, `scipy.sparse.csc` matrices have `indptr` and `indices` arrays with `dtype` `int32`. If the matrices are not converted ahead of time, `scs` will do the conversion internally, without modifying the original `A` matrix. However, it may be more efficient to construct an `A` with the correct `dtype`s initially, rather than convert.

### Data Immutability
`scs.solve()` will not modify the input data in `data`, `cone`, or `warm_start`. Copies of the data will be made for internal use, and new `numpy` arrays will be created to be returned in `sol`.


## Factorization Caching with `scs.Workspace`
When using the **direct** solver (`use_indirect=False`), a single matrix factorization is performed and used many times in SCS's iterative procedure.
This factorization depends on the input matrix `A` but **not** on the vectors
`b` or `c`. When solving many problems where `A` is fixed, but `b` and `c` change, the `scs.Workspace()` object allows us to cache the initial factorization and reuse it across many solves, without having to re-compute it. This can save time when solving many related problems.

The `Workspace` is instantiated with the same `data` and `cone` dictionaries
as `scs.solve()`, along with optional settings:
```python
work = scs.Workspace(data, cone, **settings)
```

Once the `Workspace` object is created, we can call its solve method
```python
sol = work.solve(new_bc=None, warm_start=None, **settings)
```

which will re-use the matrix factorization that was computed when the `Workspace` was initialized. Note that all of the parameters to `work.solve()` are optional. `new_bc` is a dictionary which can optionally provide
updated `b` or `c` vectors (any other keys, including `A`, are ignored).

The return value, `sol`, is a `dict` with keys `x`, `y`, `s`, and `info`, just as in `scs.solve()`.

### `Workspace` state
`work.solve()` will operate on the data contained in the `work` object:

- `work.data`
- `work.settings`

The user can modify the state of the `Workspace` object between calls to `work.solve`.

#### `work.data`
Note that `work.data` is a `dict` with keys `b` and `c`, but **not** `A`. This is because `A`  is copied and stored internally (along with its factorization) upon initialization, and cannot be modified.

Due to the data copy, the user is now free to delete or modify the `A` matrix that they passed into the `scs.Workspace` constructor, as this will have no effect on the `Workspace` object.

#### `work.settings`
Only some of the values in `work.settings` can be modified between calls to `work.solve()`.

The following settings are **fixed** at `Workspace` initialization time:

- `use_indirect`
- `rho_x`
- `normalize`
- `scale`

A copy of the `dict` of **fixed settings** is given by `work.fixed`. If any of the `work.settings` differ from `work.fixed` when `work.solve()` is called, an `Exception` will be raised. Calling `work.fixed` returns a **copy** of the underlying `dict`, which cannot be modified. XXX: make a test for this

The following settings **can** be modified between calls to `work.solve()`:

- `verbose`
- `max_iters`
- `eps`
- `cg_rate`
- `alpha`

#### `work.info`

When calling `sol = work.solve()`, solver status information is available
through the `sol['info']` dictionary. This same information is also available through the attribute `work.info`.

This attribute is useful, for instance, if you'd like to know the solver setup time after calling `Workspace()` but before calling `work.solve()`, which you can access with `work.info['setupTime']`.

#### Immutable `work` state
Upon initialization, `A` is copied, stored, and factored internally.
Any changes made to the `scipy` sparse input matrix `A` after the fact
will not be reflected in the `work` object.
Similarly, `work.cone` is fixed at initialization and cannot be modified.
To avoid confusion, we do not expose `A` or `cone` to the user
through the `work` object.

### `work.solve()` arguments

#### `new_bc` and `settings`
Passing a `new_bc` dictionary or additional settings to `work.solve()` provides one last chance to modify the problem data before calling the solver. Any changes are written to the `work` object and persist to future calls to `work.solve()`. In fact,
```python
new_b = dict(b=b)
work.solve(new_bc = new_b, eps=1e-5, alpha=1.1)
```

is exactly equivalent to

```python
work.data['b'] = b
work.settings['eps'] = 1e-5
work.settings['alpha'] = 1.1
work.solve()
```

If `new_bc` is passed to `work.solve()`, only the keys `b` and `c` will be used to update `work.data`. If an `A` key exists, it will be ignored.

More commonly, a user might simply update the original `data` dictionary and pass it to `work.solve()`:

```python
work = scs.Workspace(data, cone)
...
data['b'] = b # update the b vector
sol = work.solve(new_bc=data)
```

#### `warm_start`
You can also provide a dictionary of warm-start vectors to the `warm_start` parameter, which may help reduce the solve time.

In the example below, we first solve a problem to a tolerance of `1e-3`, and use that solution as a warm-start for solving the problem to a higher tolerance of `1e-4`. The second call to `work.solve()` will generally take fewer iterations than if we hadn't provided a `warm_start`, and also
benefits from not having to re-compute the matrix factorization.

```python
work = scs.Workspace(data, cone)
sol = work.solve(eps=1e-3)
sol = work.solve(warm_start=sol, eps=1e-4)
```

## Example Library
`SCS` comes with a small examples library,
`scs.examples`, which
demonstrates the proper problem input format,
and can be used to easily test the solver.

For example,
```python
import scs
data, cone = scs.examples.l1(m=100, seed=0)
sol = scs.solve(data, cone)
```

solves a simple least L1-norm problem.

## Python GIL