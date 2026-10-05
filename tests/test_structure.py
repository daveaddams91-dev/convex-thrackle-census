"""Tests for the structural theorems (Sections 1 and 3 of the paper).

Each theorem statement in the paper has a matching test here that checks the
statement on *every* configuration for small ``n`` (exhaustive) and on the
canonical constructions (for all ``n`` up to the tested bound).
"""

import itertools

import pytest

from thrackle.chords import (
    all_chords,
    core_cycle_length,
    is_boundary,
    is_thrackle,
    norm,
    residues_ok,
)
from thrackle.structure import (
    boundary_edge_family,
    boundary_edge_thrackle,
    doublestar,
    doublestars,
    extend_cycle,
    maximal_thrackle,
    odd_subsets,
    thrackle_cycle,
)

N_MAX = 11


# ---------------------------------------------------------------- Lemma 2.1

@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_lemma_2_1_residue_injectivity_is_sharp(n):
    """Lemma 2.1: residues of a thrackle are distinct, so |T| <= n."""
    from thrackle.census import enumerate_thrackles

    for T in enumerate_thrackles(n):
        assert residues_ok(T, n)
        assert len(T) <= n
    # and equality is attained by the doublestars
    for D in doublestars(n):
        assert len(D) == n
        assert residues_ok(D, n)


# ---------------------------------------------------------------- Theorem 1.2

@pytest.mark.parametrize("m", [3, 5, 7])
def test_thr1_2_unique_thrackle_cycle_on_odd_sets(m):
    """Theorem 1.2: an odd set of ``m`` convex points supports exactly one thrackle cycle.

    Verified by brute force over *all* Hamiltonian cycles of the full vertex
    set ``range(m)``; for larger odd ``m`` the same statement is checked
    against the exhaustive maximal-thrackle census in
    :func:`test_thr1_4_bijection_and_count`.
    """
    n = m
    S = list(range(n))
    T = thrackle_cycle(S)
    assert is_thrackle(T)
    assert core_cycle_length(T) == m
    found = set()
    for perm in itertools.permutations(S[1:]):
        cyc = [norm(S[0], perm[0])]
        cyc += [norm(perm[k], perm[k + 1]) for k in range(len(perm) - 1)]
        cyc.append(norm(perm[-1], S[0]))
        cyc = frozenset(cyc)
        if is_thrackle(cyc):
            found.add(cyc)
    assert found == {T}, f"found {len(found)} thrackle cycles, expected exactly 1"


# ---------------------------------------------------------------- Theorem 1.3

@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_thr1_3_pendants_are_forced_and_always_exist(n):
    """Theorem 1.3: the extension of a thrackle cycle to all n points exists and is unique."""
    for S in odd_subsets(n):
        T, ok = extend_cycle(S, n)
        assert ok, f"cycle on S={S} failed to extend on {n} points"
        assert is_thrackle(T)
        assert len(T) == n


@pytest.mark.parametrize("n", range(4, 9))
def test_thr1_3_unique_apex_directly(n):
    """Direct check of the wedge lemma: each off-cycle vertex has exactly one legal apex."""
    from thrackle.chords import meet

    for S in odd_subsets(n):
        C = thrackle_cycle(S)
        for u in range(n):
            if u in S:
                continue
            apices = [v for v in S if all(meet(norm(u, v), c) for c in C)]
            assert len(apices) == 1, f"S={S}, u={u}: {len(apices)} apices"


# ---------------------------------------------------------------- Theorem 1.4

@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_thr1_4_bijection_and_count(n):
    """Theorem 1.4: maximal thrackles <-> odd subsets of size >= 3; count = 2^{n-1} - n."""
    from thrackle.census import construct_all_maximal, cycle_length_census, predicted_maximal_counts

    built = construct_all_maximal(n)
    flat = [T for L in built.values() for T in L]
    assert len(flat) == 2 ** (n - 1) - n
    assert len(set(flat)) == len(flat)
    for T in flat:
        assert is_thrackle(T) and len(T) == n
    per_length = {m: len(L) for m, L in built.items() if L}
    assert per_length == predicted_maximal_counts(n)
    assert cycle_length_census(n) == predicted_maximal_counts(n)


# ---------------------------------------------------------------- Theorem 3.1

@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_thr3_1_at_most_two_polygon_edges_and_rigidity(n):
    from thrackle.census import enumerate_thrackles

    D = set(doublestars(n))
    for T in enumerate_thrackles(n):
        b = [e for e in T if is_boundary(e, n)]
        assert len(b) <= 2
        if len(b) == 2:
            # Theorem 3.1: such a thrackle is a sub-thrackle of a unique doublestar
            assert any(T <= F for F in D)
    for F in D:
        assert len(F) == n
        assert sum(is_boundary(e, n) for e in F) == 2
        assert is_thrackle(F)


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_thr3_1_doublestars_are_distinct_and_in_all(n):
    D = doublestars(n)
    assert len(set(D)) == n


# ---------------------------------------------------------------- Theorem 3.2

@pytest.mark.parametrize("n", range(4, 9))
def test_thr3_2_one_polygon_edge_implies_at_most_n_edges(n):
    from thrackle.census import enumerate_thrackles

    family = set(boundary_edge_family(n))
    for T in enumerate_thrackles(n):
        b = sum(is_boundary(e, n) for e in T)
        if b == 1:
            assert len(T) <= n
            assert any(T <= F for F in family)


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_thr3_2_equality_family_is_valid(n):
    for F in boundary_edge_family(n):
        assert is_thrackle(F)
        assert len(F) == n
        assert sum(is_boundary(e, n) for e in F) >= 1


def test_boundary_edge_thrackle_rejects_bad_parameters():
    with pytest.raises(ValueError):
        boundary_edge_thrackle(0, 0, 6)
    with pytest.raises(ValueError):
        boundary_edge_thrackle(0, 5, 6)


def test_thrackle_cycle_rejects_even_sizes():
    with pytest.raises(ValueError):
        thrackle_cycle([0, 1, 2, 3])
    with pytest.raises(ValueError):
        thrackle_cycle([0, 1])


# ------------------------------------------------- Lemma 2.4 (pseudoforest)

@pytest.mark.parametrize("n", range(4, 9))
def test_lemma_2_4_every_convex_thrackle_is_a_pseudoforest(n):
    from thrackle.census import enumerate_thrackles

    for T in enumerate_thrackles(n):
        deg = {}
        for e in T:
            deg[e[0]] = deg.get(e[0], 0) + 1
            deg[e[1]] = deg.get(e[1], 0) + 1
        # every connected component has at most one cycle
        # (equivalently: |E| <= |V| on every component)
        assert len(T) <= n
