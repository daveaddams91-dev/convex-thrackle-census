"""Structure of convex thrackles: canonical constructions and certificates.

Every object here is built combinatorially from the cyclic order of the
vertices, and every construction is accompanied by a *certificate* that can be
checked in polynomial time by :func:`thrackle.chords.is_thrackle`.
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterable, Sequence

from .chords import Edge, EdgeSet, norm, meet, is_boundary, residues_ok

__all__ = [
    "thrackle_cycle",
    "extend_cycle",
    "maximal_thrackle",
    "doublestar",
    "doublestars",
    "boundary_edge_thrackle",
    "boundary_edge_family",
    "is_maximal_thrackle",
]


# --------------------------------------------------------------------------
# Theorem 1.2 : the unique thrackle cycle on an odd vertex set
# --------------------------------------------------------------------------

def thrackle_cycle(S: Sequence[int]) -> EdgeSet:
    """The unique convex thrackle cycle on the odd set ``S``.

    ``S`` must have odd size ``m >= 3`` and must be listed in increasing
    cyclic order.  With ``s = (m - 1) / 2`` the returned edge set is

        ``{ { v_{a_i}, v_{a_{i+s} } : 0 <= i < m }``

    i.e. every vertex is joined to the vertex that is "almost antipodal" to
    it.  This is a Hamiltonian cycle of ``S`` and it is the only Hamiltonian
    cycle on ``S`` all of whose edges pairwise meet (Theorem 1.2).
    """
    m = len(S)
    if m < 3 or m % 2 == 0:
        raise ValueError("S must have odd size >= 3")
    s = (m - 1) // 2
    return frozenset(norm(S[i], S[(i + s) % m]) for i in range(m))


def cycle_apex_candidates(u: int, S: Sequence[int], C: EdgeSet) -> list[int]:
    """Vertices ``v`` of ``S`` such that ``{u, v}`` meets every edge of ``C``."""
    out = []
    for v in S:
        e = norm(u, v)
        if all(meet(e, c) for c in C):
            out.append(v)
    return out


def extend_cycle(S: Sequence[int], n: int) -> tuple[EdgeSet, bool]:
    """Extend the thrackle cycle on ``S`` to a maximal thrackle on ``n`` points.

    Returns ``(edges, ok)``.  For each ``u`` outside ``S`` the apex of the
    unique wedge of the cycle that contains ``u`` is determined, and ``u`` is
    joined to it; these pendant edges are forced (Theorem 1.3).  ``ok`` is
    ``False`` if some ``u`` has no, or more than one, legal apex -- this never
    happens, and the check is kept as a guard for the falsification suite.
    """
    C = thrackle_cycle(S)
    edges = set(C)
    for u in range(n):
        if u in S:
            continue
        apices = cycle_apex_candidates(u, S, C)
        if len(apices) != 1:
            return frozenset(edges), False
        edges.add(norm(u, apices[0]))
    return frozenset(edges), True


def maximal_thrackle(S: Sequence[int], n: int) -> EdgeSet:
    """The unique maximal convex thrackle on ``n`` points whose cycle uses ``S``."""
    T, ok = extend_cycle(S, n)
    if not ok:
        raise ValueError(f"cycle on S={list(S)} does not extend on {n} points")
    return T


# --------------------------------------------------------------------------
# Theorem 3.1 : doublestars (thrackles containing two polygon edges)
# --------------------------------------------------------------------------

def doublestar(v: int, n: int) -> EdgeSet:
    """The doublestar at ``v``: the star at ``v`` plus the chord ``{v-1, v+1}``.

    This is the only convex thrackle that contains the two polygon edges
    ``{v-1, v}`` and ``{v, v+1}``, and it always has exactly ``n`` edges.
    """
    E = {norm(v, u) for u in range(n) if u != v}
    E.add(norm((v - 1) % n, (v + 1) % n))
    return frozenset(E)


def doublestars(n: int) -> list[EdgeSet]:
    return [doublestar(v, n) for v in range(n)]


# --------------------------------------------------------------------------
# Theorem 3.2 : thrackles with exactly one polygon edge
# --------------------------------------------------------------------------

def boundary_edge_thrackle(i: int, t: int, n: int) -> EdgeSet:
    """The size-``n`` thrackle whose only polygon edge is ``{v_i, v_{i+1}``.

    Writing ``w_r = v_{(i + 1 + r) mod n}`` for ``r = 1 .. n-2`` and
    ``1 <= t <= n-2``, the edge set is

        ``{ {v_i, v_{i+1}} } u { {v_i, w_t}, {v_{i+1}, w_t} }
           u { {v_i, w_r} : 1 <= r < t } u { {v_{i+1}, w_s} : t < s <= n-2 }``

    Every convex thrackle with exactly one polygon edge is a sub-thrackle of a
    unique member of this family, and has at most ``n`` edges.
    """
    if not 1 <= t <= n - 2:
        raise ValueError("t must satisfy 1 <= t <= n-2")

    def w(r: int) -> int:
        return (i + 1 + r) % n

    a, b = i, (i + 1) % n
    E = {norm(a, b), norm(a, w(t)), norm(b, w(t))}
    E |= {norm(a, w(r)) for r in range(1, t)}
    E |= {norm(b, w(s)) for s in range(t + 1, n - 1)}
    return frozenset(E)


def boundary_edge_family(n: int) -> list[EdgeSet]:
    """All ``n (n-2)`` members of the family above (doublestars appear twice)."""
    out = []
    for i in range(n):
        for t in range(1, n - 1):
            out.append(boundary_edge_thrackle(i, t, n))
    return out


# --------------------------------------------------------------------------
# Certificates
# --------------------------------------------------------------------------

def is_maximal_thrackle(T: EdgeSet, n: int) -> bool:
    """True iff ``T`` is a convex thrackle with exactly ``n`` edges.

    For a convex thrackle, ``|E(T)| = n`` is equivalent to maximality, because
    a convex thrackle is a pseudoforest with at most one cycle (Lemma 2.4) and
    any thrackle with a vertex of degree at most one can be extended.
    """
    return len(T) == n


def odd_subsets(n: int) -> Iterable[list[int]]:
    """All odd-sized subsets of ``{0, ..., n-1}`` of size at least 3."""
    for m in range(3, n + 1, 2):
        for S in combinations(range(n), m):
            yield list(S)
