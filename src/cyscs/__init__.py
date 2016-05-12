""" CySCS: A Cython wrapper for the SCS convex optimization solver.

Functions and Classes
---------------------
- `cyscs.solve()`: Solves the input conic optimization problem
- `cyscs.Workspace()`: Class for caching solver information to save time when
solving multiple, related problems
- `cyscs.version()`: The current version of the CySCS wrapper.
- `cyscs.scs_version()`: The current version of the underlying SCS C library.
- `cyscs.default_settings()`: `dict` of the default solver settings.


Modules
-------
- `cyscs.examples`: Functions that provide data for example problems, for
bechmarking, testing, and demonstrating the data input format.

"""

from ._scs import solve, version, scs_version, Workspace, default_settings
from . import examples
