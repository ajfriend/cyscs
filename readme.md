# scs_python
Cython interface for SCS
- `source env/bin/activate` virtual environment
- make sure `nosetests` points to the virtualenv
- `deactivate` virtual environment
- `make clean` to pip uninstall and remove Cython build files
- `make test` to run nosetests
- `make` to clean, install, and test
- [SCS C library](https://github.com/cvxgrp/scs) is incorporated as a submodule
in `src/scs`
- update the SCS submodule by going to `src/scs` and running `git pull`


# TODO
- do memory checks
- check that options works as expected
- how to package: `setup.py` can't import cython without adding cython as dependency? sub command?
- python module structure?
    - local imports
    - hidden modules
    - `__init__.py`
    - figure out and simplify
- tests for proper exceptions
- memory checks
- python 3
- installer
- add power cone support

# blas warning
I get this when i run `python setup.py install`:

```
/Users/ajfriend/Dropbox/work/scs_python/env/lib/python2.7/site-packages/numpy/distutils/system_info.py:635: UserWarning: Specified path  is invalid.
  warnings.warn('Specified path %s is invalid.' % d)
```

# CVXPY tests
- test simple problems with each type of cone:
- this one below spotted a bug that the exp cone has size 3
```
x = cvx.Variable()
prob = cvx.Problem(cvx.Maximize(cvx.log(x)), [x >= 1, x <= 10])
```

# scipy/cython C integer types
https://github.com/scikit-learn/scikit-learn/wiki/C-integer-types:-the-missing-manual

# packaging/distributing/compilation/building
- http://docs.cython.org/src/userguide/source_files_and_compilation.html
- http://docs.cython.org/src/reference/compilation.html
- http://docs.cython.org/src/quickstart/build.html
- http://stackoverflow.com/questions/4505747/how-should-i-structure-a-python-package-that-contains-cython-code

# profiling
- http://docs.cython.org/src/tutorial/profiling_tutorial.html
- [memory allocation](http://docs.cython.org/src/tutorial/memory_allocation.html)

# Wed Oct 28 15:25:22 2015
- tests
- organize dir structure
- building without cython
- ask brendan about numpy
- fix numpy order
- sdists/wheels?
