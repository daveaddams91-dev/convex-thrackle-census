"""Cover numbers: chromatic numbers of the convex segment disjointness graph.

Let ``D_n`` be the graph whose vertices are the ``binom(n,2)`` chords of a
convex ``n``-gon, with two chords adjacent when they are *disjoint*.  A colour
class of ``D_n`` is exactly a convex thrackle, so

    ``chi(D_n) = min { |T| : T a family of convex thrackles covering all chords }``

which we denote ``chi(n)``.  Following Araujo--Dumitrescu--Hurtado--Noy--
Urrutia (2005) and Fabila-Monroy--Wood, the exact value is known:

    ``chi(n) = n - floor( sqrt(2n + 1/4) - 1/2 )``.

Our own contribution (Section 6) is the *size-restricted* refinement

    ``chi_s(n) = min { |T| : T covers all chords, |T'| <= s for all T' in T }``

for which no closed form is known.  We compute both numbers exactly with
set-cover integer programming, and we reproduce the published formula for
``chi(n)`` as an external validation of the whole pipeline.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

from .chords import Edge, all_chords
from .census import enumerate_thrackles


def chi_closed_form(n: int) -> int:
    """The published exact value of ``chi(D_n)`` (Araujo et al. / Fabila-Monroy--Wood).

    ``chi(D_n) = n - floor( sqrt(2n + 1/4) - 1/2 )``, which is ``ceil((n-1)/2)``
    for small ``n`` and behaves like ``n - sqrt(2n)``.
    """
    return n - math.floor(math.sqrt(2 * n + 0.25) - 0.5)


def set_cover(columns: Sequence[frozenset[Edge]], n: int) -> tuple[int, list[int]]:
    """Exact minimum number of the given families needed to cover all chords.

    Returns ``(optimum, chosen_indices)``.  Solved as a 0/1 integer program
    with HiGHS through ``scipy.optimize.milp``.
    """
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import lil_matrix

    E = all_chords(n)
    pos = {e: i for i, e in enumerate(E)}
    A = lil_matrix((len(E), len(columns)), dtype=float)
    for j, S in enumerate(columns):
        for e in S:
            A[pos[e], j] = 1.0
    A = A.tocsr()
    con = LinearConstraint(A, lb=np.ones(len(E)), ub=np.full(len(E), np.inf))
    res = milp(
        c=np.ones(len(columns)),
        constraints=con,
        integrality=np.ones(len(columns)),
        bounds=Bounds(0, 1),
    )
    if res.x is None:
        raise RuntimeError("set cover infeasible (should not happen: singletons are allowed)")
    chosen = [j for j in range(len(columns)) if res.x[j] > 0.5]
    # independent verification: the chosen families really do cover everything
    union: set[Edge] = set()
    for j in chosen:
        union |= columns[j]
    assert union == set(E), "solver returned an infeasible cover"
    return len(chosen), chosen


def chi(n: int) -> int:
    """Exact value of ``chi(D_n)`` by brute-force set cover over all thrackles."""
    return set_cover(enumerate_thrackles(n), n)[0]


def chi_restricted(n: int, s: int) -> int:
    """Exact value of the size-restricted cover number ``chi_s(n)``."""
    if s >= n:
        return chi(n)
    cols = [T for T in enumerate_thrackles(n) if len(T) <= s]
    return set_cover(cols, n)[0]


def trivial_bounds(n: int, s: int) -> tuple[int, int]:
    """Elementary lower/upper bounds for ``chi_s(n)``.

    Lower bounds.  *Capacity*: ``t`` thrackles of size at most ``s`` cover at
    most ``t s`` chords, so ``t >= ceil(binom(n,2) / s)``.  *Polygon edges*:
    by Theorem 3.1 a convex thrackle contains at most two polygon edges, so
    covering all ``n`` of them needs ``t >= ceil(n / 2)``.

    Upper bound.  Take an optimal cover by ``chi(n)`` maximal thrackles and
    split each of them into blocks of size at most ``s``; every block is still
    a thrackle, giving ``chi(n) * ceil(n / s)``.
    """
    lower = max(-(-(n * (n - 1) // 2) // s), -(-n // 2))
    upper = chi_closed_form(n) * (-(-n // s))
    return lower, upper
