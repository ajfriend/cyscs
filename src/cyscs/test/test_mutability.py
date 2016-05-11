import cyscs as scs
import pytest
import cyscs.examples as ex
import numpy as np


def test_workspace():
    data, cone = ex.simple_lp()
    m,n = data['A'].shape
    work = scs.Workspace(data, cone)

    ws = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))

    sol = work.solve(warm_start = ws)

    # make sure sol and ws contain *different* numpy arrays
    assert any(ws['x'] != sol['x'])
    assert any(ws['y'] != sol['y'])
    assert any(ws['s'] != sol['s'])

def test_solve():
    data, cone = ex.simple_lp()
    m,n = data['A'].shape
    
    ws = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))

    sol = scs.solve(data, cone, warm_start = ws)

    # make sure sol and ws contain *different* numpy arrays
    assert any(ws['x'] != sol['x'])
    assert any(ws['y'] != sol['y'])
    assert any(ws['s'] != sol['s'])

