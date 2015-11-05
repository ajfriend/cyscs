import scs
import pytest
import util
import numpy as np

def test_b():
    data, cone = util.simple_lp()
    data['b'] = data['b'].astype(np.float32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_c():
    data, cone = util.simple_lp()
    data['c'] = data['c'].astype(np.float32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_A_data():
    data, cone = util.simple_lp()
    data['A'].data = data['A'].data.astype(np.float32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_A_indices():
    data, cone = util.simple_lp()
    data['A'].indices = data['A'].indices.astype(np.int32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_A_indptr():
    data, cone = util.simple_lp()
    data['A'].indptr = data['A'].indptr.astype(np.int32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_numdim_b():
    data, cone = util.simple_lp()
    b = data['b']
    b = np.array(b, ndmin=2)
    data['b'] = b

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_numdim_b():
    data, cone = util.simple_lp()
    b = data['b']
    b = np.array(b, ndmin=2).T
    data['b'] = b

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

