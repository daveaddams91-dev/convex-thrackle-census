"""Tests for the primitive chord combinatorics."""

from thrackle.chords import (
    all_chords,
    core_cycle,
    core_cycle_length,
    crosses,
    degrees,
    diagonals,
    is_boundary,
    is_thrackle,
    meet,
    norm,
    polygon_edges,
    residue,
    residues_ok,
)


def test_norm_is_idempotent_and_canonical():
    for a in range(6):
        for b in range(6):
            if a != b:
                e = norm(a, b)
                assert e[0] < e[1]
                assert e == norm(*e)


def test_chord_counts():
    for n in range(3, 12):
        assert len(all_chords(n)) == n * (n - 1) // 2
        assert len(polygon_edges(n)) == n
        assert len(diagonals(n)) == n * (n - 3) // 2


def test_boundary_edges_are_n_distinct_for_n_ge_4():
    for n in range(4, 12):
        E = polygon_edges(n)
        assert len(set(E)) == n


def test_crossing_criterion_matches_brute_force():
    """Crossing in a convex polygon <=> alternating endpoints."""
    from itertools import combinations

    n = 8
    for e, f in combinations(all_chords(n), 2):
        if set(e) & set(f):
            assert not crosses(e, f)
            assert meet(e, f)
        else:
            assert crosses(e, f) == ((e[0] < f[0] < e[1] < f[1]) or (f[0] < e[0] < f[1] < e[1]))


def test_meet_implies_non_disjoint_or_crossing():
    n = 7
    for e in all_chords(n):
        for f in all_chords(n):
            if e != f:
                assert meet(e, f) == bool(set(e) & set(f)) or crosses(e, f)


def test_residue_map_values_and_injectivity_on_thrackles():
    # the "thrackle cycle" on a convex 7-gon (each vertex joined to the almost antipodal one)
    n = 7
    pen = frozenset(norm(i, (i + 3) % n) for i in range(n))
    assert is_thrackle(pen)
    assert residues_ok(pen, n)
    assert sorted(residue(e, n) for e in pen) == list(range(n))


def test_core_cycle_of_the_thrackle_cycle():
    n = 7
    pen = frozenset(norm(i, (i + 3) % n) for i in range(n))
    assert core_cycle_length(pen) == 7
    assert core_cycle(pen) == pen


def test_degrees_sum_to_twice_edges():
    for n in (5, 6, 7):
        E = all_chords(n)[: 5]
        assert sum(degrees(E).values()) == 2 * len(E)


def test_is_thrackle_rejects_a_non_crossing_pair():
    n = 6
    # (0,1) is a polygon edge and crosses nothing
    assert not is_thrackle(frozenset({(0, 1), (2, 3)}))
    assert is_boundary((0, 1), 6)
    assert not is_boundary((0, 2), 6)
