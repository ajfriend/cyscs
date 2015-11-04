from __future__ import print_function
from numpy.distutils.system_info import get_info
from collections import defaultdict
from glob import glob
import os

def glober(root, names):
    """ For each relative path name in `names`, add the root directory and
    find files matching the resulting glob pattern.
    """
    out = []
    for name in names:
        out += glob(root + name)
    return out

def from_system_info(names):
    """ Retreive info from `numpy.distutils.system_info.get_info`

    For each name in names, call get_info(name) and add the output
    to a dictionary containing the arguments.

    Expect a dictionary with keys

    define_macros, include_dirs, library_dirs, libraries, extra_link_args, extra_compile_args
    """

    info = defaultdict(set)

    # add blas/lapack info
    for name in names: #'blas_opt', 'lapack_opt': #'blas', 'lapack'
        d = get_info(name, 0)
        for key in d:
            if key in ['libraries', 'library_dirs', 'define_macros', 'include_dirs', 'extra_link_args', 'extra_compile_args']:
                info[key].update(d[key])

    return {k: list(info[k]) for k in info}

def get_blas_lapack_info():
    """ Try three methods for getting blas/lapack info.

    If successful, set LAPACK_LIB_FOUND and return dictionary with the arguments

    If not successful, print error message and return empty dictionary
    """
    info = defaultdict(list)
    
    if not info:
        print("Trying using blas_opt / lapack_opt")
        info = from_system_info(['lapack_opt'])

    if not info:
        print("blas_opt / lapack_opt failed. trying blas / lapack")
        info = from_system_info(['lapack'])

    if info:
        info['define_macros'] += [('LAPACK_LIB_FOUND', None)]
    else:
        print("###############################################################################################")
        print("# failed to find blas/lapack libs, SCS cannot solve SDPs but can solve LPs, SOCPs, ECPs, PCPs #")
        print("# install blas/lapack and run this install script again to allow SCS to solve SDPs            #")
        print("###############################################################################################")

    return info

def add_blas_lapack_info(ext):
    """ Append the output from get_blas_lapack_info() to the given dictionary
    `ext`.

    """
    tmp = get_blas_lapack_info()
    for key in tmp:
        ext[key] += tmp[key]

