""" Data for example problems that can be solved with SCS.

Demonstrates proper input format (particularly for SDP).
Also used for testing and benchmarking.

Functions return cone, data, and (possibly) the known solution.
"""

import numpy as np
import scipy.sparse as sp

def simple_lp():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    b = np.array([0,0,1,1], dtype=np.float64)
    c = np.array([1,1,-1,-1], dtype=np.float64)
    cone = {'l': 4}

    return dict(A=A,b=b,c=c), cone

def simple_socp():
    """
    from model:

    ```
    x = cvx.Variable(2)
    prob = cvx.Problem(cvx.Minimize(cvx.norm(x)), [x >= 1])
    ```
    """
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

    true_x = np.array([1,1, np.sqrt(2)], dtype=np.float64)

    return dict(A=A,b=b,c=c), cone, true_x

def simple_sdp():
    """
    from model:
    ```
    X = cvx.Semidef(3)
    prob = cvx.Problem(cvx.Minimize(X[0,1] + X[0,2]), [X[0,0] <= 1, X[1,1] <= 1, X[2,2] <= 1])
    prob.get_problem_data('SCS')
    ```
    """
    sq = -np.sqrt(2)
    A = sp.csc_matrix([[ 1,  0,  0,  0,  0,  0],
                       [ 0,  0,  0,  1,  0,  0],
                       [ 0,  0,  0,  0,  0,  1],
                       [-1,  0,  0,  0,  0,  0],
                       [ 0, sq,  0,  0,  0,  0],
                       [ 0,  0, sq,  0,  0,  0],
                       [ 0,  0,  0, -1,  0,  0],
                       [ 0,  0,  0,  0, sq,  0],
                       [ 0,  0,  0,  0,  0, -1]], dtype=np.float64)
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    c = np.array([0, 1, 1, 0, 0, 0], dtype=np.float64)
    b = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0], dtype=np.float64)
    cone = {'l': 3, 's': [3]}

    true_x = np.array([ 1, -1, -1, 1, 1, 1], dtype=np.float64)

    return dict(A=A,b=b,c=c), cone, true_x

def simple_ecp():
    """
    From model:
    ```
    a = .3
    x = cvx.Variable()
    prob = cvx.Problem(cvx.Minimize(cvx.exp(a*x)-x))
    prob.solve(solver='SCS')
    true_x = -np.log(a)/a
    ```
    """

    a = .4 # can vary a > 0
    A = sp.csc_matrix([ [-a,  0. ],
                        [ 0. ,  0. ],
                        [ 0. , -1. ]])
    b = np.array([-0.,  1., -0.])
    c = np.array([-1.,  1.])
    cone = dict(ep=1)
    data = dict(A=A,b=b,c=c)

    true_x = np.array([-np.log(a)/a, 1.0/a])

    return data, cone, true_x


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

    true_x = np.array([5, -4], dtype=np.float64)

    return dict(A=A,b=b,c=c), cone

def simple_pcp():
    A = sp.csc_matrix([[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]], dtype=np.float64)
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    b = np.array([1,-2,0,0,0], dtype=np.float64)
    c = np.array([1,0,0], dtype=np.float64)
    cone = dict(f=1,l=1,p=[.3])

    true_x = np.array([2**(1/.3), 1, -2])

    return dict(A=A,b=b,c=c), cone, true_x

def l1(m=100, seed=0):
    """ Solve random least-l1 norm problem.

    Data is for problem:

    min. ||x||_1
    s.t. Cx = d

    C is m by n, with n = 2*m
    C is sparse, with each element 10 percent chance of nonzero

    Note: if m is too small, C may have a row of all zeros, making the problem infeasible

    todo: why does normalization seem to hurt?
    """
    n = 2*m
    np.random.seed(seed)

    C = sp.rand(m, n, 0.1, format='csc')
    Ae = sp.hstack([C, sp.csc_matrix((m, n))], format="csc")
    h = np.zeros(2 * n)
    d = np.random.randn(m)
    bt = np.hstack([d, h])  # in cone formulation
    c = np.hstack([np.zeros(n), np.ones(n)])
    I = sp.eye(n)
    G = sp.vstack([sp.hstack([I, -I]), sp.hstack([-I, -I])], format="csc")
    At = sp.vstack([Ae, G], format="csc")  # in cone formulation
    At.indices = At.indices.astype(np.int64)
    At.indptr = At.indptr.astype(np.int64)

    data = {'A': At, 'b': bt, 'c': c}
    cone = {'l': 2 * n, 'f': m}
    #opts = {'normalize': True}

    # the unstuffed problem data
    extra = dict(C=C,d=d)

    return data, cone
