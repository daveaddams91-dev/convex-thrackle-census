"""Exhaustive enumeration of the convex thrackles of a convex ``n``-gon.

A convex thrackle is a clique in the *meeting graph* on chords: its vertex set
is the set of ``binom(n, 2)`` chords and two chords are adjacent when they
meet.  We enumerate all cliques by a standard recursive branching on a
candidate list (Bron--Kerbosch without the "no common neighbour" pruning, which
is unnecessary here because we want *all* cliques, maximal or not).

Complexity.  The meeting graph on ``binom(n,2)`` vertices has ``Theta(n^4)``
edges and the output has ``a(n)`` elements, where ``a(n)`` is the total number
of convex thrackles.  The algorithm takes ``O(n^2 * a(n))`` set operations,
i.e. linear time in the output size up to the polynomial factor.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Iterator, Sequence

from .chords import Edge, all_chords, meet
from .structure import odd_subsets, thrackle_cycle, maximal_thrackle


def meeting_graph(n: int) -> tuple[list[Edge], list[set[int]]]:
    """Adjacency lists of the meeting graph on the chords of a convex ``n``-gon."""
    E = all_chords(n)
    adj: list[set[int]] = [set() for _ in E]
    m = len(E)
    for i in range(m):
        for j in range(i + 1, m):
            if meet(E[i], E[j]):
                adj[i].add(j)
                adj[j].add(i)
    return E, adj


def enumerate_thrackles(n: int) -> list[frozenset[Edge]]:
    """Every convex thrackle on ``n`` labelled convex points, including the empty one."""
    E, adj = meeting_graph(n)
    out: list[frozenset[Edge]] = []

    def rec(chosen: list[int], cand: list[int]) -> None:
        out.append(frozenset(E[i] for i in chosen))
        k = len(cand)
        for pos in range(k):
            v = cand[pos]
            nxt = [w for w in cand[pos + 1:] if w in adj[v]]
            rec(chosen + [v], nxt)

    rec([], list(range(len(E))))
    return out


def census(n: int) -> dict[int, int]:
    """``{ number of edges : number of thrackles }`` for a convex ``n``-gon."""
    c: Counter[int] = Counter(len(T) for T in enumerate_thrackles(n))
    return dict(sorted(c.items()))


def cycle_length_census(n: int) -> dict[int, int]:
    """``{ cycle length : number of maximal thrackles }`` for odd lengths."""
    from .chords import core_cycle_length

    c: Counter[int] = Counter()
    for T in enumerate_thrackles(n):
        if len(T) == n:
            c[core_cycle_length(T)] += 1
    return dict(sorted(c.items()))


# --------------------------------------------------------------------------
# The constructive (polynomial time) route to the same numbers
# --------------------------------------------------------------------------

def predicted_maximal_counts(n: int) -> dict[int, int]:
    """``{ cycle length : count }`` predicted by Theorem 1.4: ``binom(n, m)``."""
    from math import comb

    return {m: comb(n, m) for m in range(3, n + 1, 2)}


def construct_all_maximal(n: int) -> dict[int, list[frozenset[Edge]]]:
    """Build every maximal thrackle directly from the odd subsets.

    Runtime ``O(2^n * n^3)`` -- exponential, but with a far smaller constant
    than :func:`enumerate_thrackles` and it never materialises non-maximal
    thrackles.  Used to cross-validate the brute-force census.
    """
    out: dict[int, list[frozenset[Edge]]] = {m: [] for m in range(3, n + 1, 2)}
    for S in odd_subsets(n):
        T = maximal_thrackle(S, n)
        out[len(S)].append(T)
    return out
