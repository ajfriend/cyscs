# TODO notes for Cython interface

## Before Initial release
- initially only support `double` and `int64` data. convert numpy arrays as necessary
- refactor code as cleanly as possible in 3 distinct levels: C, Cython, and pure Python
- `nogil` multithreading working with tests for all aspects of interface 
- setup.py testing on multiple platforms (CI for mac/windows testing?)
- fix setup.py so `pip install scs` works without having to call `pip install numpy` first
- `nogil` multithreading tutorial

## Later changes
- GPU support
- DCOPYAMATRIX
- `float` and `int32` options so CSC matrix conversion not needed
- maybe: 'mutable' data interface to avoid copying and creation of extra numpy arrays
- conda package
- openmp option, and how to make it play nicely with `nogil` multithreading