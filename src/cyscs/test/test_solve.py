import cyscs as scs
import pytest
import cyscs.examples as ex

import scipy.sparse as sp
import numpy as np

def test_simple_lp():
    data, cone = ex.simple_lp()
    sol = scs.solve(data, cone)

def test_extra_arg():
    data, cone = ex.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, nonsense_arg='nonsense')

def test_simple_indirect():
    data, cone = ex.simple_lp()
    sol = scs.solve(data, cone, use_indirect=True)

def test_simple_direct():
    data, cone = ex.simple_lp()
    sol = scs.solve(data, cone, use_indirect=False)

def test_cone_size():
    # test that the solve method recognizes that the length of the cone
    # does not match the number of rows of A
    data, cone = ex.simple_lp()
    cone['l'] = 5

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_simple_ecp():
    data, cone, true_x = ex.simple_ecp()
    sol = scs.solve(data, cone, eps=1e-6)

    assert np.allclose(sol['x'], true_x)

def test_simple_socp():
    data, cone, true_x = ex.simple_socp()
    sol = scs.solve(data, cone, eps=1e-6)

    assert np.allclose(sol['x'], true_x)

def test_simple_sdp():
    data, cone, true_x = ex.simple_sdp()
    sol = scs.solve(data, cone, eps=1e-6)

    assert np.allclose(sol['x'], true_x)

def test_simple_pcp():
    data, cone, true_x = ex.simple_pcp()
    sol = scs.solve(data, cone, eps=1e-6)

    assert np.allclose(sol['x'], true_x)


def test_str_output():
    data, cone = ex.simple_lp()
    sol = scs.solve(data, cone)

    assert sol['info']['status'] == 'Solved'