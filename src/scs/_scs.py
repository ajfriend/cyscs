from ._direct import version

import scs._direct
import scs._indirect

import numpy as np

from .util import default_settings, format_and_copy_cone, cone_len, not_met, check_data, check_xys, check_bc


def solve(data, cone, warm_start=None, **settings):
    stg = default_settings()
    stg.update(settings)

    if stg['use_indirect']:
        cy = scs._indirect
    else:
        cy = scs._direct

    cone = format_and_copy_cone(cone)

    # creates new data dict
    # points to *new* array/matrix data if needed
    # does not modify original matrices/arrays
    data = check_data(data, cone)

    m, n = data['A'].shape
    sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))
    
    # copy (and do not modify) warm-start vectors
    if warm_start:
        for key in 'x', 'y', 's':
            sol[key][:] = warm_start[key]

    check_xys(sol['x'], sol['y'], sol['s'], m, n)

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

        self._cone = format_and_copy_cone(cone)

        self.data = check_data(data, self._cone)

        self._m, self._n = data['A'].shape

        # todo: does it make sense to have an indirect workspace?
        # should we only allow `direct` Workspaces?
        if self._settings['use_indirect']:
            cy = scs._indirect
        else:
            cy = scs._direct

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


        check_xys(sol['x'], sol['y'], sol['s'], self._m, self._n)
        check_bc(self.data['b'],self.data['c'], self._m, self._n)

        self._settings['warm_start'] = True
        self._work.solve(self.data['b'], self.data['c'], self._cone, sol, self._settings)
        del self._settings['warm_start']

        
        sol['info'] = self.info

        return sol

