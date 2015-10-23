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
