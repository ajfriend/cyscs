import cyscs as scs
import pytest
import cyscs.examples as ex
import numpy as np

def test_b():
    data, cone = ex.simple_lp()
    data['b'] = data['b'].astype(np.float32)

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_c():
    data, cone = ex.simple_lp()
    data['c'] = data['c'].astype(np.float32)

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_A_data():
    data, cone = ex.simple_lp()
    data['A'].data = data['A'].data.astype(np.float32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_A_indices():
    data, cone = ex.simple_lp()
    data['A'].indices = data['A'].indices.astype(np.int32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_A_indptr():
    data, cone = ex.simple_lp()
    data['A'].indptr = data['A'].indptr.astype(np.int32)

    with pytest.warns(UserWarning):
        sol = scs.solve(data, cone)

def test_numdim_b():
    data, cone = ex.simple_lp()
    b = data['b']
    b = np.array(b, ndmin=2)
    data['b'] = b

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_numdim_b():
    data, cone = ex.simple_lp()
    b = data['b']
    b = np.array(b, ndmin=2).T
    data['b'] = b

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_b_len():
    data, cone = ex.simple_lp()
    b = data['b']
    b = np.append(b,b)
    data['b'] = b

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_b_len_workspace():
    data, cone = ex.simple_lp()
    work = scs.Workspace(data, cone)

    b = data['b']
    b = np.append(b,b)

    # should go without error
    work.solve()

    # also should go on without error
    data['b'] = b
    work.solve()

    with pytest.raises(ValueError):
        work.data['b'] = b
        work.solve()

def test_b_len_workspace2():
    data, cone = ex.simple_lp()
    work = scs.Workspace(data, cone)

    b = data['b']
    b = np.append(b,b)
    data['b'] = b

    with pytest.raises(ValueError):
        work.solve(new_bc = data)


def test_c_len_workspace():
    data, cone = ex.simple_lp()
    work = scs.Workspace(data, cone)

    c = data['c']
    c = np.append(c,c)

    # should go without error
    work.solve()

    # also should go on without error
    data['c'] = c
    work.solve()

    with pytest.raises(ValueError):
        work.data['c'] = c
        work.solve()

def test_c_len_workspace2():
    data, cone = ex.simple_lp()
    work = scs.Workspace(data, cone)

    c = data['c']
    c = np.append(c,c)
    data['c'] = c

    with pytest.raises(ValueError):
        work.solve(new_bc = data)


def test_xys():
    data, cone = ex.simple_lp()
    m,n = data['A'].shape
    work = scs.Workspace(data, cone)

    with pytest.raises(ValueError):
        ws = dict(x=np.ones(n+1), y=np.ones(m), s=np.ones(m))
        work.solve(warm_start = ws)

    with pytest.raises(ValueError):
        ws = dict(x=np.ones(n), y=np.ones(m+1), s=np.ones(m))
        work.solve(warm_start = ws)

    with pytest.raises(ValueError):
        ws = dict(x=np.ones(n), y=np.ones(m), s=np.ones(m+1))
        work.solve(warm_start = ws)

    ws = dict(x=np.ones(n), y=np.ones(m), s=np.ones(m))
    work.solve(warm_start = ws)

    # no value error because we copy the values to an existing float64 numpy array
    ws = dict(x=np.ones(n,dtype=np.float32), y=np.ones(m), s=np.ones(m))
    work.solve(warm_start = ws)

    # no value error because we copy the list values to an existing float64 array
    ws = dict(x=[1]*n, y=np.ones(m), s=np.ones(m))
    work.solve(warm_start = ws)


