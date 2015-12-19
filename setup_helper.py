from __future__ import print_function
from numpy.distutils.system_info import get_info
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

def get_blas_lapack_info():
    """ Try three methods for getting blas/lapack info.

    If successful, set LAPACK_LIB_FOUND and return dictionary with the arguments

    If not successful, print error message and return empty dictionary
    """
    info = {}
    
    if not info:
        print("Trying 'lapack_opt'")
        info = get_info('lapack_opt')

    if not info:
        print("lapack_opt failed. Trying 'lapack'")
        info = get_info('lapack')

    if info:
        info['define_macros'] = info.get('define_macros', []) + [('LAPACK_LIB_FOUND', None)]
        print('the resulting info is: ', info)
    else:
        print("##########################################################################################")
        print("# failed to find lapack libs, SCS cannot solve SDPs but can solve LPs, SOCPs, ECPs, PCPs #")
        print("# install lapack and run this install script again to allow SCS to solve SDPs            #")
        print("##########################################################################################")

    return info

def add_blas_lapack_info(ext):
    """ Append the output from get_blas_lapack_info() to the given dictionary
    `ext`.

    """
    tmp = get_blas_lapack_info()
    for key in tmp:
        # don't copy over 'language' key (or other unexpedted keys), since its a string and not a list
        if key in ['libraries', 'library_dirs', 'define_macros', 'include_dirs', 'extra_link_args', 'extra_compile_args']:
            ext[key] += tmp[key]

