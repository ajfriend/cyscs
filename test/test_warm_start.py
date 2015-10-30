import scs
import pytest
import util


def test_warm():
    data, cone = util.simple_pcp()

    # computing a fresh solution takes some number of iters
    sol = scs.solve(data, cone, warm_start = False)
    assert sol['info']['iter'] >= 10

    # use the solution to the problem as the warm start
    data['sol'] = sol

    # should take 0 iterations
    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] == 0

    # change solution a bit
    data['sol']['x'] *= 2

    # perturbing the solution should take a few iterations to correct
    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] >= 3


def test_many_iter_ecp():
    # warm starting with the previously found solution should take 0 iterations
    data, cone = util.many_iter_ecp()
    sol = scs.solve(data, cone, warm_start = False)
    assert sol['info']['iter'] >= 500

    data['sol'] = sol

    sol = scs.solve(data, cone, warm_start = True)
    assert sol['info']['iter'] == 0

def test_many_iter_ecp_tol():
    # warm starting with a solution at a lower tolerance should reduce
    # the number of iterations needed
    data, cone = util.many_iter_ecp()

    # intially takes ~920 iters for eps 1e-4
    sol = scs.solve(data, cone, warm_start = False, eps=1e-4)
    assert sol['info']['iter'] >= 800

    # ~640 for eps 1e-4
    sol = scs.solve(data, cone, warm_start = False, eps=1e-3)
    assert 500 <= sol['info']['iter'] <= 700

    # use 1e-3 sol as warm start for 1e-4
    data['sol'] = sol

    # extra digit only takes ~280 iters more
    sol = scs.solve(data, cone, warm_start = True, eps=1e-4)
    assert sol['info']['iter'] < 300



    
