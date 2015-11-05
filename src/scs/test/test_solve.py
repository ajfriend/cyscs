import scs
import pytest
import util

import scipy.sparse as sp
import numpy as np

def test_simple_lp():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone)

def test_extra_arg():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, nonsense_arg='nonsense')

def test_simple_indirect():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, use_indirect=True)

def test_simple_direct():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, use_indirect=False)

def test_cone_size():
    # test that the solve method recognizes that the length of the cone
    # does not match the number of rows of A
    data, cone = util.simple_lp()
    cone['l'] = 5

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_simple_ecp():
    data, cone = util.simple_ecp()
    sol = scs.solve(data, cone)

def test_simple_socp():
    data, cone = util.simple_socp()
    sol = scs.solve(data, cone)

def test_simple_sdp():
    data, cone = util.simple_sdp()
    sol = scs.solve(data, cone)

def test_simple_pcp():
    data, cone = util.simple_pcp()
    sol = scs.solve(data, cone)


def test_str_output():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone)

    assert sol['info']['status'] == 'Solved'

def test_ecp():
    """ From problem:

    a = .3
    x = cvx.Variable()
    prob = cvx.Problem(cvx.Minimize(cvx.exp(a*x)-x))
    prob.solve(solver='SCS')
    true_x = -np.log(a)/a

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
    sol = scs.solve(data, cone, verbose=False, eps=1e-6)

    assert np.allclose(sol['x'], true_x)