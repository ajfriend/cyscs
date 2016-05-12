from setuptools import setup, Extension
from platform import system
import copy
from collections import defaultdict
import sys
from setup_helper import glober, add_blas_lapack_info
import os

import numpy

# ext is a dictionary collecting the keyword arguments that will be passed into 
# the Extension module constructor
# We first collect the arguments which are the same between the direct and
# indirection versions of the solver, and later form distinct dictionaries
# for the two versions
ext = defaultdict(list)

# ext['define_macros'] += [('EXTRAVERBOSE', 999)] # for debugging

USE_CYTHON = False
if '--cython' in sys.argv:
    sys.argv.remove('--cython')
    USE_CYTHON = True

file_ext = '.pyx' if USE_CYTHON else '.c'

if system() == 'Linux':
    ext['libraries'] += ['rt']

# location of SCS root directory, containing 'src/' etc.
rootDir = 'c/scs/'

# collect the extension module options common to both direct and indirect versions
ext['sources'] += glober(rootDir, ['src/*.c', 'linsys/*.c'])
ext['include_dirs'] += glober(rootDir, ['', 'include', 'linsys'])
ext['define_macros'] += [('PYTHON', None), ('DLONG', None),
                         ('CTRLC', 1),     ('COPYAMATRIX', None)]
ext['extra_compile_args'] += ["-O3"]

# add the blas and lapack info
add_blas_lapack_info(ext)
ext['include_dirs'] += [numpy.get_include()]

# create the extension module arguments for the direct solver version
# deep copy so that the dictionaries do not point to the same list objects
ext_direct = copy.deepcopy(ext)
# next two names need to match
ext_direct['name'] = 'cyscs._direct'
ext_direct['sources'] += ['cyscs/_direct' + file_ext]
ext_direct['sources'] += glober(rootDir, ['linsys/direct/*.c', 'linsys/direct/external/*.c'])
ext_direct['include_dirs'] += glober(rootDir, ['linsys/direct/', 'linsys/direct/external/'])


ext_indirect = copy.deepcopy(ext)
ext_indirect['name'] = 'cyscs._indirect'
ext_indirect['sources'] += ['cyscs/_indirect' + file_ext]
ext_indirect['sources'] += glober(rootDir, ['linsys/indirect/*.c'])
ext_indirect['include_dirs'] += glober(rootDir, ['linsys/indirect/'])
ext_indirect['define_macros'] += [('INDIRECT', None)]

extensions = [Extension(**ext_direct),
              Extension(**ext_indirect)]

if USE_CYTHON:
    from Cython.Build import cythonize
    # cython compiler directives so that Cython automatically converts C strings to Python strings in python 2/3
    # otherwise, we will get byte strings in Python 3, which is not what CVXPY is expecting
    extensions = cythonize(extensions, compiler_directives={'c_string_type':'unicode', 'c_string_encoding':'utf8'})


setup(name='cyscs',
        version='0.1',
        author = 'AJ Friend',
        author_email = 'ajfriend@gmail.com',
        url = 'http://github.com/ajfriend/cyscs',
        description='CySCS: A Cython wrapper for the SCS convex optimization solver.',
        packages=['cyscs'],
#        py_modules=['scs.examples'],
        package_data={'cyscs': ['test/*.py']},
        zip_safe=False,
        ext_modules=extensions,
        install_requires=["numpy >= 1.7","scipy >= 0.13.2"],
        license = "MIT",
        long_description=(open('README.md').read()
                        if os.path.exists('README.md')
                        else ''))

