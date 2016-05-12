from __future__ import print_function
import pytest

from cyscs._scs import cone_len, format_and_copy_cone

def test_size_f():
    n = 13
    d = dict(f=n)

    assert cone_len(d) == n

def test_size_l():
    n = 13
    c = dict(l=n)

    assert cone_len(c) == n

def test_size_ep():
    n = 13
    c = dict(ep=n)

    assert cone_len(c) == 3*n

def test_size_ed():
    n = 13
    c = dict(ed=n)

    assert cone_len(c) == 3*n

def test_size_q():
    n = 13
    m = 3
    c = dict(q=[n,m])
    c = format_and_copy_cone(c)

    assert cone_len(c) == n+m

def test_size_s():
    n = 13
    m = 3
    c = dict(s=[n,m])
    c = format_and_copy_cone(c)

    assert cone_len(c) == (n*(n+1))/2 + (m*(m+1))/2

def test_size_p():
    a = [-.4, .7]
    c = dict(p=a)
    c = format_and_copy_cone(c)

    assert cone_len(c) == 3*len(a)

def test_cone():
    d = dict(f=1, l=20, ep=4, ed=7, q=[3,4,9,10], s=[3,2,4], p=[.1, -.7])
    c = format_and_copy_cone(d)

    expected = (d['f'] + d['l'] + 3*d['ep'] + 3*d['ed'] +
                sum(d['q']) + len(d['p'])*3 + sum([i*(i+1)/2 for i in d['s']]))

    assert cone_len(c) == expected
