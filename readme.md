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
- inside virtualenv, run cvxpy tests with `nosetests cvxpy`, making sure both nose and scs are pointing to the proper locations


# TODO
- do memory checks
- check that options works as expected
- how to package: `setup.py` can't import cython without adding cython as dependency? sub command?
- python module structure?
    - local imports
    - hidden modules
    - `__init__.py`
    - figure out and simplify
- memory checks
- installer

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
- organize dir structure
- building without cython
- fix numpy order
- sdists/wheels?
- clean up check_data function

# packaging
- [do i need manifest.ini](http://stackoverflow.com/questions/24727709/i-dont-understand-python-manifest-in)
- [package structure and testpypi](http://pymbook.readthedocs.org/en/latest/projectstructure.html)
- http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
- [sdist distutils notes](https://docs.python.org/2/distutils/sourcedist.html)
- [setuptools](https://pythonhosted.org/setuptools/setuptools.html)
- [distutils setup script](https://docs.python.org/3.5/distutils/setupscript.html)
- [config file](https://docs.python.org/2/distutils/configfile.html)
- [distributing python modules](https://docs.python.org/2.7/distutils/index.html)
- [parameter into setup.py](http://stackoverflow.com/questions/677577/distutils-how-to-pass-a-user-defined-parameter-to-setup-py)
- [pip docs](https://pip.readthedocs.org/en/stable/)

# Sun Nov  1 15:36:07 2015
- If pip does not find a wheel to install, it will locally build a wheel and cache it for future installs, instead of rebuilding the source distribution in the future
- [packaging directory structure example](https://docs.python.org/2.7/distutils/examples.html#pure-python-distribution-by-package)
- [single extension module example](https://docs.python.org/2.7/distutils/examples.html#single-extension-module)
- [listing packages](https://docs.python.org/2.7/distutils/setupscript.html#listing-whole-packages)
- [extension package structure](https://docs.python.org/2.7/distutils/setupscript.html#extension-names-and-packages)

## plan
- so i think I can build the extension modules wherever I want by [prepending the package name](https://docs.python.org/2/distutils/setupscript.html#extension-names-and-packages)
- will that work with cython
- can I then hide the internal extension modules with __all__?
- 10.1 in the cookbook
- should i change the inner scs name to hide the implementation details?
- this is the way to do it <https://github.com/cmcqueen/simplerandom/blob/master/python/setup.py>
- looks like cythonize automatically includes the C files
- header files aren't included: manifest?
- just need to fix the setup.py to use the included C files
- http://pymbook.readthedocs.org/en/latest/projectstructure.html
- zip safe flag?
- i think my `packages` listing of just `[scs]` is ok in setup.py
- good article: <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>
    - i like how he tests sdists with pip inside a virtualenv: `pip install dist/attrs-15.1.0.tar.gz`
    - also good code on testing from pypi test server
- move test into package folder hopefully lets us run `py.test scs` after installing
- not sure why it isn't finding extension modules...
- when i run setup.py with pyhton or pip and use cython, see where it puts everything in the virtualenv. see if the tests are there. what other files. see if i can run tests. make sure that a 'github' install will work for people