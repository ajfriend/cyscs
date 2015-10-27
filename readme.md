# scs_python
Cython interface for SCS
- `source env/bin/activate` virtual environment
- `deactivate` virtual environment
- `make clean` to pip uninstall and remove Cython build files
- `make test` to run nosetests
- `make` to clean, install, and test
- [SCS C library](https://github.com/cvxgrp/scs) is incorporated as a submodule
in `src/scs`
- update the SCS submodule by going to `src/scs` and running `git pull`


# TODO
- i get an error with `python setup.py` having to do with numpy includes; maybe I should be catching it and continue on...
- check and convert scipy sparse matrices for input
- do memory checks
- check that options works as expected
- how to package: `setup.py` can't import cython without adding cython as dependency? sub command?
- python module structure?
    - local imports
    - hidden modules
    - `__init__.py`
    - figure out and simplify
