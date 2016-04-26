""" SCS: A Python interface for the SCS convex conic optimization solver.

Functions and Classes
---------------------
- `scs.solve()`: Solves the input conic optimization problem
- `scs.Workspace()`: Class for caching solver information to save time when
solving multiple, related problems
- `scs.version()`: The current version of SCS.
- `scs.default_settings()`: `dict` of the default solver settings.


Modules
-------
- `scs.examples`: Functions that provide data for example problems, for
bechmarking, testing, and demonstrating the data input format.

"""

from ._scs import solve, version, Workspace, default_settings
from . import examples
