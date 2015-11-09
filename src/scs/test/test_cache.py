import scs
import pytest
import scs.examples as ex

import scipy.sparse as sp
import numpy as np

def test_cache():
    data, cone = ex.many_iter_ecp()

    work = scs.Workspace(data, cone)

    work.solve({})