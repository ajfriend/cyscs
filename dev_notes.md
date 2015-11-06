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

## git submodules
`SCS` is contained as a submodule of `scs_python`. When cloning from
github, the submodule doesn't seem to be automatically downloaded.
To do so, use:
- `git clone https://github.com/ajfriend/scs_python`
- `cd scs_python`
- `git submodule init`
- `git submodule update`

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
- good example setup.py: https://github.com/marcelm/cutadapt/blob/master/setup.py
- this guy doesn't like using sys.argv for --cython: http://stackoverflow.com/questions/677577/distutils-how-to-pass-a-user-defined-parameter-to-setup-py
- http://blog.ionelmc.ro/2014/05/25/python-packaging/
- http://blog.ionelmc.ro/2014/06/25/python-packaging-pitfalls/

# Mon Nov  2 15:43:53 2015
- check that all ways to install work
    - github
    - sdist
    - wheel
    - with pip or setup.py
- look at how toolz includes tests..
- good travis example and install from github: https://github.com/dnouri/nolearn
- https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

# Mon Nov  2 23:39:54 2015
- manifest commands: https://docs.python.org/2/distutils/sourcedist.html#commands
- https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
- `travis_wait` and `travis_retry`

# Tue Nov  3 20:48:40 2015
```
In [6]: get_info?
Signature: get_info(name, notfound_action=0)
Docstring:
notfound_action:
  0 - do nothing
  1 - display warning message
  2 - raise error
File:      /usr/local/lib/python3.5/site-packages/numpy/distutils/system_info.py
Type:      function
```

- get_info on different pythons/platforms returns different errors/warnings
- why a problem with linux but not osx?
- inspect the output. see what i can copy over
- everything but `language`?
- look at scikit learn setup.py for tips/tricks
- https://github.com/scikit-learn/scikit-learn/issues/5489
- optimized atlas: http://docs.scipy.org/doc/numpy/user/install.html
- http://scikit-learn.org/stable/modules/computational_performance.html#linear-algebra-libraries
- https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/setup.py
- on linux, be careful about the way you install libraries, because you may get an error like:
```
In [3]: get_info('lapack_opt', 1)
/usr/lib/python2.7/dist-packages/numpy/distutils/system_info.py:1427: UserWarning:
    Atlas (http://math-atlas.sourceforge.net/) libraries not found.
    Directories to search for the libraries can be specified in the
    numpy/distutils/site.cfg file (section [atlas]) or by setting
    the ATLAS environment variable.
  warnings.warn(AtlasNotFoundError.__doc__)
Out[3]:
{'define_macros': [('NO_ATLAS_INFO', 1)],
```
- are these two sufficient on osx, or do i have to go down to blas and lapack without opt?
```
In [6]: get_info('lapack_opt')
Out[6]:
{'define_macros': [('NO_ATLAS_INFO', 3), ('HAVE_CBLAS', None)],
 'extra_compile_args': ['-msse3'],
 'extra_link_args': ['-Wl,-framework', '-Wl,Accelerate']}

In [7]: get_info('blas_opt')
Out[7]:
{'define_macros': [('NO_ATLAS_INFO', 3), ('HAVE_CBLAS', None)],
 'extra_compile_args': ['-msse3',
  '-I/System/Library/Frameworks/vecLib.framework/Headers'],
 'extra_link_args': ['-Wl,-framework', '-Wl,Accelerate']}
```

# Wed Nov  4 15:54:41 2015
- make the sdp test bigger than 2x2
- absolute best travis.yml example: https://github.com/dnouri/nolearn/blob/master/.travis.yml
- try running tests on osx: https://github.com/astropy/astropy/blob/master/.travis.yml
- osx lapack/Accelerate framework weirdness: https://github.com/scikit-learn/scikit-learn/issues/5489
- http://pablissimo.com/381/get-travis-ci-to-do-your-python-packaging-tests-for-you
