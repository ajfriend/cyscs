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
    A = sp.csc_matrix([[-1.,  0.,  0.],
                       [ 0., -1.,  0.],
                       [ 0.,  0., -1.],
                       [-1.,  0.,  0.],
                       [ 0., -1.,  0.]])
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    c = np.array([ 0.,  0.,  1.], dtype=np.float64)
    b = np.array([-1., -1., -0., -0., -0.], dtype=np.float64)
    cone = {'l': 2, 'q': [3]}

    return dict(A=A,b=b,c=c), cone

def simple_sdp():
    A = sp.csc_matrix([[ 1.,  0.        ,  0.],
                       [ 0.,  0.        ,  1.],
                       [-1.,  0.        ,  0.],
                       [ 0., -np.sqrt(2),  0.],
                       [ 0.,  0.        , -1.]])
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    c = np.array([0, 1, 0], dtype=np.float64)
    b = np.array([1, 1, 0, 0, 0], dtype=np.float64)
    cone = {'l': 2, 's': [2]}

    return dict(A=A,b=b,c=c), cone

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

def many_iter_ecp():
    """ ECP that should take ~640 iters to solve at default settings

    from model:
    ```
    x = cvx.Variable(2)
    obj = cvx.Minimize(cvx.sum_entries(cvx.exp(x)))
    prob = cvx.Problem(obj, [cvx.sum_entries(x) == 1, x[0] >= 5])
    ```

    """
    A = sp.csc_matrix([ [ 1.,  1.,  0.,  0.],
                        [-1.,  0.,  0.,  0.],
                        [-1.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0., -1.,  0.],
                        [ 0., -1.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0., -1.]])
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    c = np.array([ 0.,  0.,  1.,  1.], dtype=np.float64)
    b = np.array([ 1., -5., -0.,  1., -0., -0.,  1., -0.], dtype=np.float64)
    cone = {'f':1, 'l': 1, 'ep': 2}

    return dict(A=A,b=b,c=c), cone

def simple_pcp():
    A = sp.csc_matrix([[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]], dtype=np.float64)
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    b = np.array([1,-2,0,0,0], dtype=np.float64)
    c = np.array([1,0,0], dtype=np.float64)
    cone = dict(f=1,l=1,p=[.3])

    expected_x = np.array([2**(1/.3), 1, -2])

    return dict(A=A,b=b,c=c), cone