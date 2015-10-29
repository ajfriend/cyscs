from __future__ import print_function

import pytest

import numpy as np
import scipy.sparse as sp

import util


def test_import():
    import scs

def test_cone():
    import scs
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[0,1,4], p=[.1, -.7])
    print(scs.Cone(**d))

def test_version():
    import scs
    import pkg_resources

    print(scs.version())
    print(pkg_resources.require("scs")[0].version)
    assert scs.version() == pkg_resources.require("scs")[0].version

def test_simple():
    import scs
    data, cone = util.simple_lp()

    print('test simple: \n')
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1)

def test_extra_arg():
    data, cone = util.simple_lp()
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, nonsense_arg='nonsense')

def test_simple_indirect():
    data, cone = util.simple_lp()
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=True)

def test_simple_direct():
    data, cone = util.simple_lp()
    import scs
    sol = scs.solve(data, cone, eps=1e-9, alpha=.1, use_indirect=False)

# todo: assert that this raises a value error
def test_cone_size():
    data, cone = util.simple_lp()
    cone['l'] = 5

    import scs

    with pytest.raises(ValueError):
        sol = scs.solve(data, cone)

def test_simple_ecp():
    data, cone = util.simple_ecp()
    import scs
    sol = scs.solve(data, cone)

