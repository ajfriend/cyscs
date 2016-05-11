import cyscs as scs
import pytest
import cyscs.examples as ex

import numpy as np


def test_cache():
    data, cone = ex.many_iter_ecp()

    work = scs.Workspace(data, cone)

    sol = work.solve()

def test_settings():
    expected_keys = set(['normalize', 'use_indirect', 'scale', 'verbose',
                        'eps', 'cg_rate', 'max_iters', 'alpha', 'rho_x'])

    data, cone, _ = ex.simple_socp()
    work = scs.Workspace(data, cone)

    assert 'warm_start' not in work.settings
    assert set(work.settings.keys()) == expected_keys

    work.solve()

    assert 'warm_start' not in work.settings
    assert set(work.settings.keys()) == expected_keys


def test_fixed_settings():
    data, cone, _ = ex.simple_socp()
    work = scs.Workspace(data, cone)

    expected_fixed = set(['normalize', 'use_indirect', 'scale', 'rho_x'])

    assert set(work.fixed.keys()) == expected_fixed

    with pytest.raises(Exception):
        work.settings['rho_x'] = 3.14159
        # should raise an exception because we changed a fixed setting
        work.solve()


def test_data_keys():
    data, cone, _ = ex.simple_socp()
    work = scs.Workspace(data, cone)

    assert 'A' not in work.data

    assert set(work.data.keys()) == set(['b','c'])

def test_A():
    data, cone, true_x = ex.simple_socp()
    work = scs.Workspace(data, cone)

    # corrupt the original data (but SCS should have made an internal copy, so this is ok)
    data['A'][:] = 3

    sol = work.solve(eps=1e-6)

    assert np.allclose(sol['x'], true_x)

    # now, solving on corrupted data shouldn't work
    work = scs.Workspace(data, cone)

    sol = work.solve(eps=1e-6)

    assert not np.allclose(sol['x'], true_x)
    

def test_settings_change():
    data, cone, _ = ex.simple_socp()
    work = scs.Workspace(data, cone)

    assert work.settings['eps'] == 1e-3

    work.solve(eps=1e-6)

    assert work.settings['eps'] == 1e-6

def test_warm_start():
    # if warm-starting, the input warm-start vector should not be modified
    data, cone, true_x = ex.simple_socp()
    work = scs.Workspace(data, cone)

    sol = work.solve(eps=1e-2)

    assert np.linalg.norm(sol['x'] - true_x) > 1e-3

    sol2 = work.solve(warm_start=sol, eps=1e-9)

    assert np.linalg.norm(sol2['x'] - true_x) <= 1e-9

    assert np.linalg.norm(sol['x'] - sol2['x']) > 0
    assert sol['x'] is not sol2['x']

def test_many_iter_ecp():
    # warm starting with a solution at a lower tolerance should reduce
    # the number of iterations needed
    data, cone = ex.many_iter_ecp()

    # intially takes ~920 iters for eps 1e-4
    work = scs.Workspace(data, cone, eps=1e-4)
    sol = work.solve()
    assert sol['info']['iter'] >= 800

    # ~640 for eps 1e-3
    sol = work.solve(eps=1e-3)
    assert 500 <= sol['info']['iter'] <= 700

    # use 1e-3 sol as warm start for 1e-4
    # extra digit only takes ~280 iters more
    sol = work.solve(warm_start = sol, eps=1e-4)
    assert sol['info']['iter'] < 300





