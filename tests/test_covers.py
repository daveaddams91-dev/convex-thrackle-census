"""Tests for the cover numbers, including reproduction of the published formula."""

import math

import pytest

from thrackle.covers import chi, chi_closed_form, chi_restricted, trivial_bounds

N_MAX = 11


@pytest.mark.parametrize("n", range(4, N_MAX + 1))
def test_ilp_reproduces_published_formula(n):
    """External validation: our exact set-cover solver agrees with the literature."""
    assert chi(n) == chi_closed_form(n)


def test_closed_form_small_values():
    # hand-checkable values
    expected = {4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 6, 10: 6, 11: 7}
    for n, e in expected.items():
        assert chi_closed_form(n) == e


@pytest.mark.parametrize("n", range(4, 9))
def test_chi_restricted_is_monotone_in_s(n):
    """Larger allowed size can only help, so chi_s(n) is non-increasing in s."""
    vals = [chi_restricted(n, s) for s in range(1, n + 1)]
    assert vals == sorted(vals, reverse=True)
    assert vals[-1] == chi(n)


@pytest.mark.parametrize("n", range(4, 9))
def test_chi_restricted_lower_bounds_hold(n):
    for s in range(1, n + 1):
        lo, hi = trivial_bounds(n, s)
        v = chi_restricted(n, s)
        assert lo <= v <= hi


def test_chi_1_is_all_singletons():
    for n in (5, 6, 7):
        assert chi_restricted(n, 1) == n * (n - 1) // 2


def test_chi_restricted_capacity_bound_small_n():
    # for small s the capacity bound is the binding one
    n = 6
    for s in range(1, 5):
        cap = -(-(n * (n - 1) // 2) // s)
        assert chi_restricted(n, s) >= cap
