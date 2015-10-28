from __future__ import print_function

import numpy as np
import scipy.sparse as sp


def test_import():
    import scs

def test_cone():
    import scs
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[0,1,4], p=[.1, -.7])
    print(scs.Cone(**d))

def test_version():
    import scs
    import pkg_resources

    # pkg_resources.require("scs")[0].version set in setup.py
    # scs.version set in constants.h
    print(scs.version())
    print(pkg_resources.require("scs")[0].version)
    assert scs.version() == pkg_resources.require("scs")[0].version

def test_simple():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    #A.indices = A.indices.astype(np.int64)
    #A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 4}

    data = dict(A=A, b=b, c=c)

    import scs
    print('test simple: \n')
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1)

    print(sol)

    print(sol.keys())
    print(sol['info'].keys())

def test_extra_arg():

    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    #A.indices = A.indices.astype(np.int64)
    #A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 4}

    data = dict(A=A, b=b, c=c)
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, nonsense_arg='nonsense')

def test_simple_indirect():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    #A.indices = A.indices.astype(np.int64)
    #A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 4}

    data = dict(A=A, b=b, c=c)
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=True)

def test_simple_direct():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    #A.indices = A.indices.astype(np.int64)
    #A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 4}

    data = dict(A=A, b=b, c=c)
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=False)

# todo: assert that this raises a value error
def test_cone_size():
    ij = np.array([[0,1,2,3],[0,1,2,3]])
    A = sp.csc_matrix(([-1.,-1.,1.,1.], ij), (4,4))
    #A.indices = A.indices.astype(np.int64)
    #A.indptr = A.indptr.astype(np.int64)
    b = np.array([0.,0.,1,1])
    c = np.array([1.,1.,-1,-1])
    cone = {'l': 5}

    data = dict(A=A, b=b, c=c)
    import scs
    sol = scs.solve(data, cone)
