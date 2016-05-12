import cyscs as scs
import pytest
import cyscs.examples as ex


def test_warm():
    data, cone, true_x = ex.simple_pcp()

    # computing a fresh solution takes some number of iters
    sol = scs.solve(data, cone)
    assert sol['info']['iter'] >= 10

    # should take 0 iterations
    sol = scs.solve(data, cone, warm_start = sol)
    assert sol['info']['iter'] == 0

    # change solution a bit
    sol['x'] *= 2

    # perturbing the solution should take a few iterations to correct
    sol = scs.solve(data, cone, warm_start = sol)
    assert sol['info']['iter'] >= 3


def test_many_iter_ecp():
    # warm starting with the previously found solution should take 0 iterations
    data, cone = ex.many_iter_ecp()
    sol = scs.solve(data, cone)
    assert sol['info']['iter'] >= 500

    sol = scs.solve(data, cone, warm_start = sol)
    assert sol['info']['iter'] == 0

def test_many_iter_ecp_tol():
    # warm starting with a solution at a lower tolerance should reduce
    # the number of iterations needed
    data, cone = ex.many_iter_ecp()

    # intially takes ~920 iters for eps 1e-4
    sol = scs.solve(data, cone, eps=1e-4)
    assert sol['info']['iter'] >= 800

    # ~640 for eps 1e-3
    sol = scs.solve(data, cone, eps=1e-3)
    assert 500 <= sol['info']['iter'] <= 700

    # use 1e-3 sol as warm start for 1e-4
    # extra digit only takes ~280 iters more
    sol = scs.solve(data, cone, warm_start = sol, eps=1e-4)
    assert sol['info']['iter'] < 300



    
