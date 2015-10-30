import scs
import pytest
import util


def test_warm():
    data, cone = util.simple_pcp()
    sol = scs.solve(data, cone, warm_start = False)
    assert sol['info']['iter'] >= 20

    data['sol'] = sol

    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] <= 1

    data['sol']['x'] *= 2

    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] >= 3
    
