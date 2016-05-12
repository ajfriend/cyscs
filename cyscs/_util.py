""" Internal utilities for checking that input data is valid.
"""

from warnings import warn
import scipy.sparse as sp
import numpy as np


def check_xys(x,y,s,m,n):
    """ Check that x, y, s are dense numpy arrays of the right shape, length
    and dtype.

    Raise a value error otherwise.

    """
    if sp.issparse(x):
        raise ValueError("x must be a (dense) NumPy ndarray.")

    if sp.issparse(y):
        raise ValueError("y must be a (dense) NumPy ndarray.")

    if sp.issparse(s):
        raise ValueError("s must be a (dense) NumPy ndarray.")

    if not_met(x.ndim == 1, y.ndim == 1, s.ndim == 1,
               x.size == n, y.size == m, s.size == m):
        raise ValueError("x, y, s must be 1D NumPy ND arrays with sizes matching matrix A.")

    # check that they have the right data type. warn if not and convert
    if not_met(x.dtype == np.float64, y.dtype == np.float64, s.dtype == np.float64):
        raise ValueError("x, y, s must be numpy arrays with dtype = numpy.float64")

def check_bc(b,c,m,n):
    """ Check that b, c are dense numpy arrays of the right shape, length
    and dtype.

    Raise a value error otherwise.

    """
    if sp.issparse(b):
        raise ValueError("b must be a (dense) NumPy ndarray.")

    if sp.issparse(c):
        raise ValueError("c must be a (dense) NumPy ndarray.")

    if not_met(b.ndim == 1, c.ndim == 1, b.size == m, c.size == n):
        raise ValueError("b, c must be 1D NumPy ND arrays with sizes matching matrix A.")

    # check that they have the right data type. warn if not and convert
    if not_met(b.dtype == np.float64, c.dtype == np.float64):
        raise ValueError("b, c must be numpy arrays with dtype = numpy.float64")



def default_settings():
    """ Return a *copy* of the dictionary of the default CySCS solver settings.
    """
    # todo: note that unrecognized keyword argument settings are silently ignored?
    # todo: would be nice to grab defaults from C, but Cython doesn't
    # actually read C headerfiles, so it can't get the SCS macros
    # however, is possible if defaults are exposed as variables or function
    stg_default = dict(normalize = True,
                       scale = 1.0,
                       rho_x = 1e-3,
                       max_iters = 2500,
                       eps = 1e-3,
                       alpha = 1.5,
                       cg_rate = 2.0,
                       verbose = True,
                       use_indirect=False)
    return stg_default


def format_and_copy_cone(cone_in):
    """ Make a cone dictionary with the proper keys and numpy arrays.

    Converts from cones with q,s,p as lists or numpy arrays with improper type.

    Makes a *deep* copy, creating and copying data for numpy arrays.

    Only contains nontrivial keys. (No empty arrays or zero values.)
    """
    cone_out = {}

    for key in 'f', 'l', 'ep', 'ed':
        if key in cone_in:
            cone_out[key] = cone_in[key]

    for key in 'q', 's':
        if key in cone_in and len(cone_in[key]) > 0:
            cone_out[key] = np.array(cone_in[key], dtype=np.int64)

    if 'p' in cone_in and len(cone_in['p']) > 0:
        cone_out['p'] = np.array(cone_in['p'], dtype=np.float64)

    return cone_out

def cone_len(cone):
    total = 0

    if 'f' in cone:
        total += cone['f']

    if 'l' in cone:
        total += cone['l']

    if 'ep' in cone:
        total += 3*cone['ep']

    if 'ed' in cone:
        total += 3*cone['ed']

    if 'q' in cone:
        total += sum(cone['q'])

    if 's' in cone:
        s = cone['s']
        # numpy array operations
        total += sum(s*(s+1)/2)

    if 'p' in cone:
        total += 3*len(cone['p'])

    return total

def not_met(*vargs):
    return not all(vargs)


def check_data(data, cone):
    """ Check the correctness of input data.
    A is CSC with int64 indices and float64 values
    b,c are float64 vectors, with correct sizes

    If all datatypes are OK, returns *new* dictionary with *same* A, b, c objects.

    Raises an *error* if b, or c are incorrectly formatted.

    If A is incorrect, but can be converted, returns a *new* dict with the
    same b,c arrays, but a *new* A matrix, so as not to modify the original A
    matrix.
    """
    # data has elements A, b, c
    if not_met('A' in data, 'b' in data, 'c' in data):
        raise TypeError("Missing one or more of A, b, or c from data dictionary.")

    A = data['A']
    b = data['b']
    c = data['c']

    if A is None or b is None or c is None:
        raise TypeError("Incomplete data specification.")

    if not sp.issparse(A):
        raise TypeError("A is required to be a scipy sparse matrix.")

    if not sp.isspmatrix_csc(A):
        warn("Converting A to a scipy CSC (compressed sparse column) matrix; may take a while.")
        A = A.tocsc()

    m,n = A.shape
    check_bc(b,c,m,n)

    if not_met(A.indptr.dtype == np.int64, A.indices.dtype == np.int64):
        warn("Converting A.indptr and A.indices to arrays with dtype = numpy.int64")
        # copy the matrix to avoid modifying original
        A = sp.csc_matrix(A)
        A.indptr = A.indptr.astype(np.int64)
        A.indices = A.indices.astype(np.int64)

    if not_met(A.data.dtype == np.float64):
        warn("Converting A.data to array with dtype = numpy.float64")
        # copy the matrix to avoid modifying original
        A = sp.csc_matrix(A)
        A.data = A.data.astype(np.float64)

    if not_met(cone_len(cone) > 0, A.shape[0] == cone_len(cone)):
        raise ValueError('The cones must match the number of rows of A.')


    # return a dict of (possibly modified) problem data
    # we do not modify the original dictionary or the original numpy arrays or matrices
    # if no modifications are needed, these are the *same* A, b, c matrices
    return dict(A=A,b=b,c=c)
