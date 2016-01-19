# TODO notes for Cython interface

## Before Initial release
- simplified interface
    - treat input data as immutable
    - initially only support `double` and `int64` data. convert numpy arrays as necessary
    - optional `warm_start` dictionary
- refactor code as cleanly as possible in 3 distinct levels: C, Cython, and pure Python
- `nogil` multithreading working with tests for all aspects of interface 
- setup.py testing on multiple platforms (CI for mac/windows testing?)
- fix setup.py so `pip install scs` works without having to call `pip install numpy` first
- `nogil` multithreading tutorial
- think about how mutable warm-starting would work with a given `sol` dict. would a future change be very different from initial interface? I liked the ability to re-solve a problem to a higher tolerance (and benefit from warm starting and caching) just by resetting one `settings` parameter.

## Later changes
- GPU support
- DCOPYAMATRIX
- `float` and `int32` options so CSC matrix conversion not needed
- maybe: 'mutable' data interface to avoid copying and creation of extra numpy arrays
- conda package
- openmp option, and how to make it play nicely with `nogil` multithreading