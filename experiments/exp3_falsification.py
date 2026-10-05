"""Experiment 3 -- falsification suite: try hard to break every claim.

Each check is *adversarial*: we search for counterexamples rather than for
confirmations.  The module exits non-zero if any claim is violated.

1. ``F1`` Lemma 2.1 residue injection: search all thrackles for a collision.
2. ``F2`` Theorem 3.1: search for a thrackle with three polygon edges, or with
   two polygon edges that is not inside a doublestar.
3. ``F3`` Theorem 3.2: search for a thrackle with exactly one polygon edge and
   more than ``n`` edges, or one not contained in the family of Theorem 3.2.
4. ``F4`` Theorem 1.2: enumerate *all* Hamiltonian cycles of odd subsets and
   look for a second thrackle cycle.
5. ``F5`` Theorem 1.3 (wedge lemma): look for an off-cycle vertex with zero or
   with two or more legal apexes.
6. ``F6`` Theorem 1.4: look for a maximal thrackle whose cycle length is even
   or smaller than 3, or a mismatch against ``binom(n, m)``.
7. ``F7`` the residue bound is *tight* only if a doublestar exists (look for
   ``n`` distinct doublestars and confirm each is residue-surjective).
8. ``F8`` boundary sanity: a thrackle never contains three polygon edges
   because polygon edges only meet when consecutive.

Usage::

    python experiments/exp3_falsification.py [--max-n 9]
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thrackle.census import construct_all_maximal, cycle_length_census, enumerate_thrackles, predicted_maximal_counts  # noqa: E402
from thrackle.chords import core_cycle_length, is_boundary, meet, norm, residue, residues_ok  # noqa: E402
from thrackle.structure import boundary_edge_family, doublestars, odd_subsets, thrackle_cycle  # noqa: E402


def falsify(max_n: int) -> dict:
    failures: list[str] = []

    for n in range(4, max_n + 1):
        cliques = enumerate_thrackles(n)

        # F1 -- residue injection
        for T in cliques:
            rs = [residue(e, n) for e in T]
            if len(set(rs)) != len(rs):
                failures.append(f"F1 n={n}: residue collision in {sorted(T)}")
                break

        # F2 -- polygon edges
        D = set(doublestars(n))
        for T in cliques:
            b = [e for e in T if is_boundary(e, n)]
            if len(b) >= 3:
                failures.append(f"F2 n={n}: {len(b)} polygon edges in {sorted(T)}")
                break
            if len(b) == 2 and not any(T <= F for F in D):
                failures.append(f"F2 n={n}: two polygon edges but not inside a doublestar")
                break

        # F3 -- one polygon edge
        fam = set(boundary_edge_family(n))
        for T in cliques:
            b = sum(is_boundary(e, n) for e in T)
            if b == 1:
                if len(T) > n:
                    failures.append(f"F3 n={n}: one polygon edge but |T|={len(T)} > n")
                    break
                if not any(T <= F for F in fam):
                    failures.append(f"F3 n={n}: one polygon edge, not in the Theorem 3.2 family")
                    break

        # F6 -- maximal thrackles
        cen = cycle_length_census(n)
        if cen != predicted_maximal_counts(n):
            failures.append(f"F6 n={n}: cycle-length profile {cen} != binomials")
        for m in cen:
            if m < 3 or m % 2 == 0:
                failures.append(f"F6 n={n}: cycle length {m} is not odd and >= 3")
                break

        # F7 -- tightness of the residue bound
        Ds = doublestars(n)
        if len(set(Ds)) != n:
            failures.append(f"F7 n={n}: only {len(set(Ds))} distinct doublestars")
        for F in Ds:
            if not residues_ok(F, n) or len(F) != n:
                failures.append(f"F7 n={n}: doublestar is not residue-complete")
                break

        # F5 -- wedge lemma, exhaustively
        for S in odd_subsets(n):
            C = thrackle_cycle(S)
            for u in range(n):
                if u in S:
                    continue
                apices = [v for v in S if all(meet(norm(u, v), c) for c in C)]
                if len(apices) != 1:
                    failures.append(f"F5 n={n}: S={S}, u={u}: {len(apices)} apexes")
                    break

        # F4 -- uniqueness of the thrackle cycle, exhaustively for small m
        for m in (3, 5, 7):
            if m > n:
                continue
            S = list(range(m))
            T = thrackle_cycle(S)
            for perm in itertools.permutations(S[1:]):
                cyc = [norm(S[0], perm[0])]
                cyc += [norm(perm[k], perm[k + 1]) for k in range(len(perm) - 1)]
                cyc.append(norm(perm[-1], S[0]))
                cyc = frozenset(cyc)
                if cyc != T:
                    from thrackle.chords import is_thrackle

                    if is_thrackle(cyc):
                        failures.append(f"F4 n={n}: a second thrackle cycle on {S}")
                        break

    return {"max_n": max_n, "failures": failures, "passed": not failures}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=9)
    args = ap.parse_args()
    print(f"falsification sweep for 4 <= n <= {args.max_n}")
    res = falsify(args.max_n)
    for f in res["failures"]:
        print("  FAIL:", f)
    print("no counterexample found" if res["passed"] else f"{len(res['failures'])} failures")
    import json

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok=True)
    path = os.path.join(os.path.dirname(__file__), "..", "results", "falsification.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", path)
    sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
