import scs
import pytest
import util

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