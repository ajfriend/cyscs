from ._direct import version

import scs._direct
import scs._indirect

import numpy as np

from .util import default_settings, make_cone, cone_len, not_met, check_data

"""
## Notes
- cy.Cone, cy.Workspace are Cython classes, wrapping the C structs
- cy.solve is a Cython function, wrapping the C function
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
    
    # copy (and do not modify) warm-start vectors
    if warm_start:
        for key in 'x', 'y', 's':
            sol[key][:] = warm_start[key]

    stg['warm_start'] = True
    # updates the sol dict
    cy.solve(data, cone, sol, stg)

    return sol



class Workspace(object):
    """
    responsibility: keep an internal *copy* of cone. underlying Cython layer
    will use numpy memory in C calls.
    """

    _fixed_keys = 'use_indirect', 'rho_x', 'normalize', 'scale'

    def __init__(self, data, cone, **settings):
        """ SCS Workspace
        
        """
        self._settings = default_settings()
        self._settings.update(settings)

        self._fixed = {k: self._settings[k] for k in self._fixed_keys}

        # todo: make cone and copy here. internal. can't change
        self._cone = make_cone(cone)

        # todo: why is check data returning something?
        self.data = check_data(data, self._cone)

        self._m, self._n = data['A'].shape

        # todo: does it make sense to have an indirect workspace?
        # should we only allow `direct` Workspaces
        if self._settings['use_indirect']:
            cy = scs._indirect
        else:
            cy = scs._direct

        # todo: wwaaaa
        self._settings['warm_start'] = True
        self._work = cy.Workspace(self.data, self._cone, self._settings)
        del self._settings['warm_start']

        del self.data['A']

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

    def solve(self, new_bc=None, warm_start=None, **settings):
        self._settings.update(settings)
        self.check_settings()

        if new_bc is not None:
            for key in 'b', 'c':
                if key in new_bc:
                    self.data[key] = new_bc[key]

        sol = dict(x=np.zeros(self._n), y=np.zeros(self._m), s=np.zeros(self._m))
        
        # copy (and do not modify) warm-start vectors
        if warm_start:
            for key in 'x', 'y', 's':
                sol[key][:] = warm_start[key]

        self._settings['warm_start'] = True
        self._work.solve(self.data['b'], self.data['c'], self._cone, sol, self._settings)
        del self._settings['warm_start']

        
        sol['info'] = self.info

        return sol

