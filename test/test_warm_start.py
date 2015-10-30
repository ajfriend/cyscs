import scs
import pytest
import util


def test_warm():
    data, cone = util.simple_pcp()
    sol = scs.solve(data, cone, warm_start = False)
    assert sol['info']['iter'] >= 10

    data['sol'] = sol

    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] <= 1

    # change solution a bit
    data['sol']['x'] *= 2

    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] >= 3


    
