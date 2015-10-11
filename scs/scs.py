from ._indirect import Cone, solve, version


# call either direct or indirect
# make sure matrices and vectors in right format, datatype
# do i need two different versions of Cone and 'version'?

# can i install with 'python setup.py' outside of a virtualenv?
# can i do the numpy install after the fact?
# can i grab the default settings from C?

# issue warnings for having to convert data format?

def check_data(data):
    # data has elements A, b, c
    pass


if not probdata or not cone:
        raise TypeError("Missing data or cone information")

    if not 'A' in probdata or not 'b' in probdata or not 'c' in probdata:
        raise TypeError("Missing one or more of A, b, c from data dictionary")
    A = probdata['A']
    b = probdata['b']
    c = probdata['c']


if A is None or b is None or c is None:
        raise TypeError("Incomplete data specification")
    if not sparse.issparse(A):
        raise TypeError("A is required to be a sparse matrix")
    if not sparse.isspmatrix_csc(A):
        warn("Converting A to a CSC (compressed sparse column) matrix; may take a while.")
        A = A.tocsc()

    if sparse.issparse(b):
        b = b.todense()

    if sparse.issparse(c):
        c = c.todense()
