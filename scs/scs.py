from ._indirect import Cone, solve, version

from warnings import warn
import scipy.sparse as sp
import numpy as np


# call either direct or indirect
# make sure matrices and vectors in right format, datatype
# do i need two different versions of Cone and 'version'?

# can i install with 'python setup.py' outside of a virtualenv?
# can i do the numpy install after the fact?
# can i grab the default settings from C?

# issue warnings for having to convert data format?

# todo: add some tests that these checks do the right thing

def not_met(*vargs):
    return not all(vargs)

def check_data(data):
    # data has elements A, b, c
    if not_met('A' in data, 'b' in data, 'c' in data):
        raise TypeError("Missing one or more of A, b, c from data dictionary")

    A = data['A']
    b = data['b']
    c = data['c']

    if A is None or b is None or c is None:
        raise TypeError("Incomplete data specification")

    if not sp.issparse(A):
        raise TypeError("A is required to be a sparse matrix")

    if not sp.isspmatrix_csc(A):
        warn("Converting A to a CSC (compressed sparse column) matrix; may take a while.")
        A = A.tocsc()

    if sp.issparse(b):
        warn("Converting b to a (dense) NumPy ndarray.")
        b = b.todense()

    if sp.issparse(c):
        warn("Converting c to a (dense) NumPy ndarray.")
        c = c.todense()

    m,n = A.shape
    if not_met(b.ndim == 1, c.ndim == 1, b.size == m, c.size == n):
        raise ValueError("b, c must be 1D NumPy ND arrays with sizes matching matrix A.")

    # check that the have the right data type. warn if not and convert
    if not_met(b.dtype == np.float64, c.dtype == np.float64):
        warn("Converting b and c to arrays with dtype = numpy.float64")
        b = b.astype(np.float64)
        c = c.astype(np.float64)

    if not_met(A.indptr.dtype == np.int64, A.indices.dtype == np.int64):
        warn("Converting A.indptr and A.indices to arrays with dtype = numpy.int64")
        A.indptr = A.indptr.astype(np.int64)
        A.indices = A.indices.astype(np.int64)

    if not_met(A.data.dtype == np.float64):
        warn("Converting A.data to array with dtype = numpy.float64")
        A.data = A.data.astype(np.float64)

    # return modified data if we needed to convert anything
    data = dict(A=A,b=b,c=c)
    return data
