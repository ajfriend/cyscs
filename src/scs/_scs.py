from ._direct import version

import scs._direct
import scs._indirect

from warnings import warn
import scipy.sparse as sp
import numpy as np

"""
## Notes
- cy.Cone, cy.Workspace are Cython classes, wrapping the C structs
- cy.solve is a Cython function, wrapping the C function
"""

# todo: rename to format cone
# this does make a **copy**...
def make_cone(cone_in):
    # only move over the keys we expect
    # don't move over keys not present
    # no empty arrays, just don't move over

    cone_out = {}

    for key in 'f', 'l', 'ep', 'ed':
        if key in cone_in:
            cone_out[key] = cone_in[key]

    for key in 'q', 's':
        if key in cone_in and len(cone_in[key]) > 0:
            cone_out[key] = np.array(cone_in[key], dtype=np.int64)

    if 'p' in cone_in and len(cone_in['p']) > 0:
        cone_out['p'] = np.array(cone_in['p'], dtype=np.float64)

    return cone_out

# not in public interface..
def cone_len(cone):
    total = 0

    if 'f' in cone:
        total += cone['f']

    if 'l' in cone:
        total += cone['l']

    if 'ep' in cone:
        total += 3*cone['ep']

    if 'ed' in cone:
        total += 3*cone['ed']

    if 'q' in cone:
        total += sum(cone['q'])

    if 's' in cone:
        s = cone['s']
        # numpy array operations
        total += sum(s*(s+1)/2)

    if 'p' in cone:
        total += 3*len(cone['p'])

    return total


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
                       #warm_start = False,
                       use_indirect=False)
    return stg_default

"""
python level always 
"""
def solve(data, cone, warm_start=None, **settings):
    stg = default_settings()
    stg.update(settings)

    if stg['use_indirect']:
        cy = scs._indirect
    else:
        cy = scs._direct

    cone = make_cone(cone)

    # todo: decide if we should overwrite data with modified matrices
    # woah! wipes the 'data' dictionary
    data = check_data(data, cone)

    m, n = data['A'].shape
    sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))
    stg['warm_start'] = True

    # copy (and do not modify) warm-start vectors
    if warm_start:
        for key in 'x', 'y', 's':
            sol[key][:] = warm_start[key]

    # updates the sol dict
    cy.solve(data, cone, sol, stg)

    return sol

def not_met(*vargs):
    return not all(vargs)

# todo: does this change the data?
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

    # todo: whats up with this len calcuation?
    if not_met(cone_len(cone) > 0, A.shape[0] == cone_len(cone)):
        raise ValueError('The cones must match the number of rows of A.')

    # return modified data if we needed to convert anything
    data = dict(data) # make a shallow copy of the dictionary

    data.update(A=A,b=b,c=c)
    return data

class Workspace(object):
    """
    responsibility: keep an internal *copy* of cone. underlying Cython layer
    will use numpy memory in C calls.
    """

    _fixed_keys = 'use_indirect', 'rho_x', 'normalize', 'scale'

    def __init__(self, data, cone, sol=None, **settings):
        """ SCS Workspace
        
        """
        self._settings = default_settings()
        self._settings.update(settings)
        self._fixed = {k: self._settings[k] for k in self._fixed_keys}

        # todo: make cone and copy here. internal. can't change
        self._cone = make_cone(cone)

        # todo: why is check data returning something?
        self.data = check_data(data, self._cone)
        
        m, n = data['A'].shape
        if sol is None:
            self.sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))
        else:
            self.sol = sol            
        # todo: fixed parameters: rho, normalize, ...

        # todo: does it make sense to have an indirect workspace?
        # should we only allow `direct` Workspaces
        if self.settings['use_indirect']:
            cy = scs._indirect
        else:
            cy = scs._direct

        self._work = cy.Workspace(self.data, self._cone, self._settings)

    @property
    def fixed(self):
        # return a copy of the fixed dictionary
        return dict(self._fixed)

    @property
    def info(self):
        return self._work.c_info

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
        self._settings.update(settings)
        self.check_settings()

        if data is not None:
            for key in 'b', 'c':
                if key in data:
                    self.data[key] = data[key]

        if sol:
            self.sol = sol

        self._work.solve(self.data['b'], self.data['c'], self._cone, self.sol, self.settings)

        result = dict(self.sol)
        result['info'] = self.info

        return result

