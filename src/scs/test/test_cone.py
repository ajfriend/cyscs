from __future__ import print_function
import scs
import pytest

def test_cone():
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[3,2,4], p=[.1, -.7])
    print(scs.Cone(**d))

def test_repr():
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[3,2,4], p=[.1, -.7])
    c = scs.Cone(**d)

    c2 = eval('scs.' + str(c))

    assert c == c2

def test_eq():
    c = scs.Cone(f=1,l=3)
    c2 = scs.Cone(f=1,l=4)

    assert c != c2

def test_invalid_leq():
    c = scs.Cone(f=1,l=3)
    c2 = scs.Cone(f=1,l=4)

    with pytest.raises(SyntaxError):
        c < c2

def test_invalid_eq():
    c = scs.Cone(f=1,l=3)

    with pytest.raises(SyntaxError):
        c >= 4

def test_diff_cones():
    c = scs.Cone(f=1,l=3)
    c2 = scs.Cone(f=1,l=4,p=[.1,.4])

    assert c != c2

def test_diff_cones():
    c = scs.Cone(f=1,l=3, p=[.10001, .4])
    c2 = scs.Cone(f=1,l=4,p=[.1,.4])

    assert c != c2

def test_size_f():
    n = 13
    c = scs.Cone(f=n)

    assert len(c) == n

def test_size_l():
    n = 13
    c = scs.Cone(l=n)

    assert len(c) == n

def test_size_ep():
    n = 13
    c = scs.Cone(ep=n)

    assert len(c) == 3*n

def test_size_ed():
    n = 13
    c = scs.Cone(ed=n)

    assert len(c) == 3*n

def test_size_q():
    n = 13
    m = 3
    c = scs.Cone(q=[n,m])

    assert len(c) == n+m

def test_size_s():
    n = 13
    m = 3
    c = scs.Cone(s=[n,m])

    assert len(c) == (n*(n+1))/2 + (m*(m+1))/2

def test_size_p():
    a = [-.4, .7]
    c = scs.Cone(p=a)

    assert len(c) == 3*len(a)
