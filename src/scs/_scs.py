from ._direct import Cone, version

from ._direct import Cone as Cone_dir
from ._direct import solve as solve_dir
from ._direct import Workspace as work_dir

from ._indirect import Cone as Cone_indir
from ._indirect import solve as solve_indir
from ._indirect import Workspace as work_indir

from warnings import warn
import scipy.sparse as sp
import numpy as np


def default_settings():
    # todo: note that unrecognized keyword argument settings are silently ignored?
    # todo: would be nice to grab defaults from C, but Cython doesn't
    # actually read C headerfiles, so it can't get the SCS macros
    # however, is possible if defaults are exposed as variables or function
    stg_default = dict(normalize = True,
                       scale = 1.0,
                       rho_x = 1e-3,
                       max_iters = 2500,
                       eps = 1e-3,
                       alpha = 1.5,
                       cg_rate = 2.0,
                       verbose = True,
                       warm_start = False,
                       use_indirect=False)
    return stg_default

def solve(data, cone, sol=None, **settings):
    stg = default_settings()
    stg.update(settings)

    # switch on the direct/indirect solver
    # even though Cone is identical between the two solvers, they compiled to
    # different types, so we get a type mismatch if we try to mix them
    if stg['use_indirect']:
        Cone = Cone_indir
        solve_ = solve_indir
    else:
        Cone = Cone_dir
        solve_ = solve_dir

    cone = Cone(**cone)

    # todo: decide if we should overwrite data with modified matrices
    # woah! wipes the 'data' dictionary
    data = check_data(data, cone)

    # todo: sol prep should be done at python level?
    if sol is None:
        m, n = data['A'].shape
        sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))

    return solve_(data, cone, sol, stg)

def not_met(*vargs):
    return not all(vargs)

def check_data(data, cone):
    # data has elements A, b, c
    if not_met('A' in data, 'b' in data, 'c' in data):
        raise TypeError("Missing one or more of A, b, c from data dictionary")

    A = data['A']
    b = data['b']
    c = data['c']

    if A is None or b is None or c is None:
        raise TypeError("Incomplete data specification")

    if not sp.issparse(A):
        raise TypeError("A is required to be a sparse matrix")

    if not sp.isspmatrix_csc(A):
        warn("Converting A to a CSC (compressed sparse column) matrix; may take a while.")
        A = A.tocsc()

    if sp.issparse(b):
        warn("Converting b to a (dense) NumPy ndarray.")
        b = b.todense()

    if sp.issparse(c):
        warn("Converting c to a (dense) NumPy ndarray.")
        c = c.todense()

    m,n = A.shape
    if not_met(b.ndim == 1, c.ndim == 1, b.size == m, c.size == n):
        raise ValueError("b, c must be 1D NumPy ND arrays with sizes matching matrix A.")

    # check that the have the right data type. warn if not and convert
    if not_met(b.dtype == np.float64, c.dtype == np.float64):
        warn("Converting b and c to arrays with dtype = numpy.float64")
        b = b.astype(np.float64)
        c = c.astype(np.float64)

    if not_met(A.indptr.dtype == np.int64, A.indices.dtype == np.int64):
        warn("Converting A.indptr and A.indices to arrays with dtype = numpy.int64")
        A.indptr = A.indptr.astype(np.int64)
        A.indices = A.indices.astype(np.int64)

    if not_met(A.data.dtype == np.float64):
        warn("Converting A.data to array with dtype = numpy.float64")
        A.data = A.data.astype(np.float64)

    if not_met(len(cone) > 0, A.shape[0] == len(cone)):
        raise ValueError('The cones must match the number of rows of A.')

    # return modified data if we needed to convert anything
    data = dict(data) # make a shallow copy of the dictionary

    data.update(A=A,b=b,c=c)
    return data

class Workspace(object):
    _fixed_keys = 'use_indirect', 'rho_x', 'normalize', 'scale'

    def __init__(self, data, cone, sol=None, **settings):
        """ SCS Workspace
        
        """
        self._settings = default_settings()
        self._settings.update(settings)
        self._fixed = {k: self._settings[k] for k in self._fixed_keys}

        self.cone = cone
        self.data = check_data(data, Cone(**cone))
        
        m, n = data['A'].shape
        if sol is None:
            self.sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))
        else:
            self.sol = sol            
        # todo: fixed parameters: rho, normalize, ...

        if self.settings['use_indirect']:
            self._work = work_indir(self.data, self.cone, self._settings)
        else:
            self._work = work_dir(self.data, self.cone, self._settings)

    @property
    def fixed(self):
        # return a copy of the fixed dictionary
        return dict(self._fixed)

    @property
    def info(self):
        return self._work.info

    @property
    def settings(self):
        self.check_settings()
        return self._settings

    # in fixed, can list (data, 'A') and test that it points to the right numpy array
    # (cone) also fixed
    def check_settings(self):
        for key in self._fixed:
            if not self._fixed[key] == self._settings[key]:
                raise Exception('Setting {} has been changed from Workspace initialization.'.format(key))

    def solve(self, data=None, sol=None, **settings):
        self.settings.update(settings)
        self.check_settings()

        if data is not None:
            for key in 'b', 'c':
                if key in data:
                    self.data[key] = data[key]

        if sol:
            self.sol = sol

        self._work.solve(self.data, self.sol, self.settings)

        result = dict(self.sol)
        result['info'] = self.info

        return result

