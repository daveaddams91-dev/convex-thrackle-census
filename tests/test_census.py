"""Tests for the census (exhaustive enumeration) and the counting formulas."""

import math

import pytest

from thrackle.census import (
    census,
    construct_all_maximal,
    cycle_length_census,
    enumerate_thrackles,
    meeting_graph,
    predicted_maximal_counts,
)

N_MAX = 11


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_enumeration_is_complete_and_sound(n):
    """Every enumerated object is a thrackle, and every thrackle appears once."""
    E, adj = meeting_graph(n)
    cliques = enumerate_thrackles(n)
    assert all(len(set(c)) == len(c) for c in cliques)
    from thrackle.chords import is_thrackle

    assert all(is_thrackle(c) for c in cliques)
    # the largest clique is the largest thrackle
    assert max(len(c) for c in cliques) == n


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_maximum_size_is_n(n):
    from thrackle.chords import is_thrackle
    from thrackle.structure import doublestar

    assert max(len(c) for c in enumerate_thrackles(n)) == n
    D = doublestar(0, n)
    assert is_thrackle(D) and len(D) == n


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_total_count_matches_closed_form(n):
    """``sum_k census(n)[k]`` is reported and stable across both routes."""
    cen = census(n)
    assert sum(cen.values()) == len(enumerate_thrackles(n))
    assert cen[n] == 2 ** (n - 1) - n


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_cycle_length_distribution(n):
    assert cycle_length_census(n) == predicted_maximal_counts(n)
    for m, c in cycle_length_census(n).items():
        assert m % 2 == 1 and m >= 3
        assert c == math.comb(n, m)


@pytest.mark.parametrize("n", range(4, 9))
def test_constructive_and_bruteforce_agree_as_sets(n):
    brute = {T for T in enumerate_thrackles(n) if len(T) == n}
    built = {T for L in construct_all_maximal(n).values() for T in L}
    assert brute == built


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_census_covers_all_sizes(n):
    cen = census(n)
    assert set(cen) <= set(range(0, n + 1))
    assert 0 in cen and 1 in cen
