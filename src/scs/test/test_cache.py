import scs
import pytest
import util

import scipy.sparse as sp
import numpy as np

def test_cache():
    data, cone = util.many_iter_ecp()

    work = scs.Workspace(data, cone)

    work.solve({})