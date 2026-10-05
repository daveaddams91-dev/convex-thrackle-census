"""A census of convex thrackles of a convex polygon.

Main results implemented / supported here:

* ``structure.maximal_thrackle`` -- Theorem 1.4: maximal convex thrackles are
  in bijection with the odd-sized subsets of size at least 3 of the vertex
  set, hence there are exactly ``2^{n-1} - n`` of them.
* ``census.census`` / ``census.cycle_length_census`` -- exhaustive verification.
* ``covers.chi`` / ``covers.chi_restricted`` -- exact cover numbers.
"""

from .chords import (
    Edge,
    EdgeSet,
    all_chords,
    core_cycle,
    core_cycle_length,
    crosses,
    diagonals,
    is_boundary,
    is_thrackle,
    meet,
    norm,
    polygon_edges,
    residue,
    residues_ok,
)
from .structure import (
    boundary_edge_family,
    boundary_edge_thrackle,
    doublestar,
    doublestars,
    extend_cycle,
    maximal_thrackle,
    odd_subsets,
    thrackle_cycle,
)
from .census import (
    census,
    construct_all_maximal,
    cycle_length_census,
    enumerate_thrackles,
    meeting_graph,
    predicted_maximal_counts,
)
from .covers import chi, chi_closed_form, chi_restricted, set_cover, trivial_bounds

__version__ = "1.0.0"

__all__ = [
    "Edge",
    "EdgeSet",
    "all_chords",
    "core_cycle",
    "core_cycle_length",
    "crosses",
    "diagonals",
    "is_boundary",
    "is_thrackle",
    "meet",
    "norm",
    "polygon_edges",
    "residue",
    "residues_ok",
    "boundary_edge_family",
    "boundary_edge_thrackle",
    "doublestar",
    "doublestars",
    "extend_cycle",
    "maximal_thrackle",
    "odd_subsets",
    "thrackle_cycle",
    "census",
    "construct_all_maximal",
    "cycle_length_census",
    "enumerate_thrackles",
    "meeting_graph",
    "predicted_maximal_counts",
    "chi",
    "chi_closed_form",
    "chi_restricted",
    "set_cover",
    "trivial_bounds",
    "__version__",
]
