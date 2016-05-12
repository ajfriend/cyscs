""" Python layer of the CySCS interface.

Code Organization
-----------------

This cySCS Cython interface is broken up into three layers:
- the C SCS layer of underlying C code
- the Cython wrapper layer exposing the C code to python
- the Python layer, which depends on the Cython layer, providing a nice user interface

The Cython layer is intended to be as **light** a wrapper around
the C code as possible. This mostly involves calling C functions
and converting dictionaries to the appropriate C structs.
There is also a **Cython** `Workspace` class which encapsulates the
various C structs and cleans up memory when garbage collected.
The **Python** `Workspace` class contains an instance of the 
**Cython** `Workspace`.

The Python layer provides various datatype conversion functionality,
a nice user interface, and checks for data correctness.
The hope is to keep as much of this logic in the Python level as possible,
for easy maintenance.
"""
import pkg_resources

import numpy as np

from ._direct import version as scs_version

import cyscs._direct
import cyscs._indirect

from ._util import (default_settings, format_and_copy_cone,
                  cone_len, not_met, check_data, check_xys, check_bc)


def version():
    """ Returns the current version of the CySCS Python wrapper.
    """
    return pkg_resources.get_distribution("cyscs").version


def solve(data, cone, warm_start=None, **settings):
    """ Solve conic optimization problem given by dictionaries `data` and `cone`.

    Parameters
    ----------
    data : dict
        Dictionary providing `scipy.sparse` CSC matrix `A`,
        and `numpy` arrays `b`, `c`.
    cone : dict
        Dictionary describing the sizes of the conic constraints.
        Optional Keys: `f`, `l`, `q`, `s, `ep`, `ed`, `p`.
        See the documentation or `cyscs.examples` for more information.
    warm_start : Optional[dict]
        Warm start the solver with arrays `x`, `y`, `s`.
        All three arrays must be present.
        Copies and does not modify the input arrays.
    **settings
        Settings can be given as keyword arguments.
        For the possible keys, see the documentation and
        `cyscs.default_settings()`.

    Returns
    -------
    dict
        Dictionary with keys `x`, `y`, and `s`, describing solution.
        Key `info` gives solver exit information.
    """
    stg = default_settings()
    stg.update(settings)

    if stg['use_indirect']:
        cy = cyscs._indirect
    else:
        cy = cyscs._direct

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
    """ `Workspace` objects cache SCS solver information to be reused between solves.

    Once created, calling `Workspace.solve()` will solve the problem
    based on the current `Workspace` attributes.

    Typically, users can change `b`, `c` and some of the solver settings
    between solves. The `A` matrix cannot be changed after
    initialization.

    Parameters
    ----------
    data : dict
        Dictionary providing `scipy.sparse` CSC matrix `A`,
        and `numpy` arrays `b`, `c`.
    cone : dict
        Dictionary describing the sizes of the conic constraints.
        Optional Keys: `f`, `l`, `q`, `s, `ep`, `ed`, `p`.
        See the documentation or `cyscs.examples` for more information.
    **settings
        Settings can be given as keyword arguments.
        For the possible keys, see the documentation and
        `cyscs.default_settings()`.

    Attributes
    ----------
    data : dict
        Dictionary with keys `b`, `c`, which can change between solves.
        Note that `A` is not present because it cannot be changed.
    settings : dict
        All the solver settings for this `Workspace`.
    fixed : dict
        Solver settings which cannot be changed after initialization.
    info : dict
        Solver status info, including solve time and problem setup time.


    Development Notes
    -----------------
    It is this object's responsibility to keep an internal *copy* of cone.
    The underlying Cython layer will create and use numpy memory in C calls.
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
            cy = cyscs._indirect
        else:
            cy = cyscs._direct

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
                msg = 'Setting {} has been changed from Workspace initialization.'
                raise Exception(msg.format(key))

    def solve(self, new_bc=None, warm_start=None, **settings):
        """ Solve conic optimization problem based on `Workspace` attributes.

        Parameters
        ----------
        new_bc : Optional[dict]
            Dictionary providing optional `numpy` arrays `b`, `c`.
            Will replace keys in `Workspace.data` before calling solver,
            and changes persist after calling `solve()`.
        warm_start : Optional[dict]
            Warm start the solver with arrays `x`, `y`, `s`.
            All three arrays must be present.
            Copies and does not modify the input arrays.
        **settings
            Settings can be given as keyword arguments.
            For the possible keys, see the documentation and
            `cyscs.default_settings()`.
            Will replace settings in `Workspace.settings`, so changes
            persist after the call to `solve()`.

        Returns
        -------
        dict
            Dictionary with keys `x`, `y`, and `s`, describing solution.
            Key `info` gives solver exit information.
        """
        self._settings.update(settings)
        self.check_settings()

        if new_bc is not None:
            for key in 'b', 'c':
                if key in new_bc:
                    self.data[key] = new_bc[key]

        sol = dict(x=np.zeros(self._n), y=np.zeros(self._m),
                   s=np.zeros(self._m))
        
        # copy (and do not modify) warm-start vectors
        if warm_start:
            for key in 'x', 'y', 's':
                sol[key][:] = warm_start[key]


        check_xys(sol['x'], sol['y'], sol['s'], self._m, self._n)
        check_bc(self.data['b'],self.data['c'], self._m, self._n)

        self._settings['warm_start'] = True
        self._work.solve(self.data['b'], self.data['c'],
                         self._cone, sol, self._settings)
        del self._settings['warm_start']

        
        sol['info'] = self.info

        return sol

