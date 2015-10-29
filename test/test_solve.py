import scs
import pytest
import util

def test_simple():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1)

def test_extra_arg():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, nonsense_arg='nonsense')

def test_simple_indirect():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=True)

def test_simple_direct():
    data, cone = util.simple_lp()
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=False)

# todo: assert that this raises a value error
def test_cone_size():
    data, cone = util.simple_lp()
    cone['l'] = 5

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_simple_ecp():
    data, cone = util.simple_ecp()
    sol = scs.solve(data, cone)