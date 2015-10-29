import numpy as np
import scipy.sparse as sp

def simple_lp():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1], dtype=np.float64)
    c = np.array([1.,1.,-1,-1], dtype=np.float64)
    cone = {'l': 4}

    return dict(A=A,b=b,c=c), cone

def simple_socp():
    pass

def simple_sdp():
    pass

def simple_ecp():
    A = sp.csc_matrix([[ 1.,  0.],
                       [ 0., -1.],
                       [ 0.,  0.],
                       [-1.,  0.]])
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    c = np.array([ 0., -1.], dtype=np.float64)
    b = np.array([ 1., -0.,  1., -0.], dtype=np.float64)
    cone = {'l': 1, 'ep': 1}

    return dict(A=A,b=b,c=c), cone