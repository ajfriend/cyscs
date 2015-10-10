import numpy as np
import scipy.sparse as sp

def test_import():
    import scs

def test_cone():
    import scs
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[0,1,4], p=[.1, -.7])
    print scs.Cone(**d)

def test_version():
    import scs
    import pkg_resources

    # pkg_resources.require("scs")[0].version set in setup.py
    # scs.version set in constants.h
    assert scs.version() == pkg_resources.require("scs")[0].version

def test_simple():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    A.indices = A.indices.astype(np.int64)
    A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 4}

    data = dict(A=A, b=b, c=c, cones=cone)

    import scs
    print 'test simple: \n'
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1)

    print sol

    print sol.keys()
    print sol['info'].keys()
