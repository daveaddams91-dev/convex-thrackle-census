"""Primitive combinatorics of chords of a convex polygon.

Throughout, a *convex position* set of ``n`` points is identified with the
cyclic sequence ``v_0, v_1, ..., v_{n-1}`` (indices taken modulo ``n``).
A *chord* is an unordered pair of distinct indices.

All results in this module are exact and combinatorial: no floating point
arithmetic is used anywhere.
"""

from __future__ import annotations

from typing import Iterable, Iterator, Sequence


Edge = tuple[int, int]
EdgeSet = frozenset[Edge]


def norm(a: int, b: int) -> Edge:
    """Return the canonical representative ``(min, max)`` of a chord."""
    return (a, b) if a < b else (b, a)


def all_chords(n: int) -> list[Edge]:
    """All ``binom(n, 2)`` chords of a convex ``n``-gon, in canonical form."""
    if n < 2:
        return []
    return [(a, b) for a in range(n) for b in range(a + 1, n)]


def is_boundary(e: Edge, n: int) -> bool:
    """True iff ``e`` is an edge of the polygon itself."""
    a, b = e
    return (b - a) % n in (1, n - 1)


def polygon_edges(n: int) -> list[Edge]:
    """The ``n`` boundary chords, for ``n >= 3``."""
    return [norm(i, (i + 1) % n) for i in range(n)]


def diagonals(n: int) -> list[Edge]:
    """All chords that are not polygon edges."""
    return [e for e in all_chords(n) if not is_boundary(e, n)]


def crosses(e: Edge, f: Edge) -> bool:
    """True iff the two chords cross in the interior (no shared endpoint).

    ``e`` and ``f`` must be vertex-disjoint; if they share an endpoint the
    function returns ``False``.
    """
    a, b = e
    c, d = f
    if a == c or a == d or b == c or b == d:
        return False
    return (a < c < b < d) or (c < a < d < b)


def meet(e: Edge, f: Edge) -> bool:
    """True iff the two closed segments intersect (cross or share a vertex)."""
    a, b = e
    c, d = f
    return a in (c, d) or b in (c, d) or crosses(e, f)


def is_thrackle(T: Iterable[Edge], n: int | None = None) -> bool:
    """True iff every two distinct chords of ``T`` *meet*."""
    items = sorted({norm(*e) for e in T})
    for i, item in enumerate(items):
        for j in range(i + 1, len(items)):
            if not meet(item, items[j]):
                return False
    return True


def residue(e: Edge, n: int) -> int:
    """The residue ``(i + j) mod n`` of a chord ``{v_i, v_j}``.

    Lemma 2.1 of the paper: on any convex thrackle this map is injective.
    """
    a, b = e
    return (a + b) % n


def residues_ok(T: Iterable[Edge], n: int) -> bool:
    """Certificate for Lemma 2.1: the residue map is injective on ``T``.

    Equivalently, ``|T| <= n`` holds with equality exactly when every residue
    class of ``Z / nZ`` is used once.
    """
    seen: set[int] = set()
    for e in T:
        r = residue(e, n)
        if r in seen:
            return False
        seen.add(r)
    return True


def degrees(T: Iterable[Edge]) -> dict[int, int]:
    """Degrees.
    
    Args:
        T:
    
    Returns:
        The computed result
    
    """
    d: dict[int, int] = {}
    for a, b in T:
        d[a] = d.get(a, 0) + 1
        d[b] = d.get(b, 0) + 1
    return d


def core_cycle(T: Iterable[Edge]) -> EdgeSet:
    """Return the unique cycle of a convex thrackle (as a set of chords).

    Implements the "peeling" characterisation: repeatedly delete degree-one
    vertices.  For a convex thrackle (a pseudoforest with at most one cycle,
    Lemma 2.4) what survives is exactly that cycle.  If no cycle is present
    the empty set is returned.
    """
    items = [norm(*e) for e in T]
    deg = degrees(items)
    alive = set(deg)
    d = dict(deg)
    changed = True
    while changed:
        changed = False
        for v in [x for x in list(alive) if d[x] <= 1]:
            alive.discard(v)
            changed = True
            for e in items:
                if v in e:
                    w = e[0] if e[1] == v else e[1]
                    if w in alive:
                        d[w] -= 1
    return frozenset(norm(*e) for e in items if e[0] in alive and e[1] in alive)


def core_cycle_length(T: Iterable[Edge]) -> int:
    """Length of the unique cycle of a maximal convex thrackle."""
    return len(core_cycle(T))
