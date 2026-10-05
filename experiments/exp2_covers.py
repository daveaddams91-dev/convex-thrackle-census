"""Experiment 2 -- cover numbers: reproduce the literature, and the refinement chi_s(n).

* ``chi(D_n)`` is computed from scratch by 0/1 set-cover integer programming
  and compared with the published closed form
  ``n - floor(sqrt(2n + 1/4) - 1/2)``.  Agreement is an *external validation*
  of the whole pipeline (enumeration + ILP + the structural lemmas).
* ``chi_s(n)``, the minimum number of thrackles of size at most ``s`` needed to
  cover all chords, is computed exactly and compared with the two elementary
  bounds of :func:`thrackle.covers.trivial_bounds`.

Usage::

    python experiments/exp2_covers.py [--max-n 11] [--restricted-max-n 10]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thrackle.census import enumerate_thrackles  # noqa: E402
from thrackle.covers import chi_closed_form, set_cover, trivial_bounds  # noqa: E402

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")


def run(max_n: int, restricted_max_n: int) -> dict:
    out: dict[str, dict] = {}
    for n in range(4, max_n + 1):
        t0 = time.perf_counter()
        cols = enumerate_thrackles(n)
        t1 = time.perf_counter()
        opt, chosen = set_cover(cols, n)
        closed = chi_closed_form(n)
        rec = {
            "chi": opt,
            "chi_closed_form": closed,
            "matches_literature": opt == closed,
            "cover_sizes": sorted(len(cols[j]) for j in chosen),
            "enumeration_seconds": round(t1 - t0, 2),
            "solve_seconds": round(time.perf_counter() - t1, 2),
        }
        print(
            f"n={n:3d}  chi(D_n) = {opt:>3d}   published = {closed:>3d}   "
            f"{'match' if opt == closed else 'MISMATCH'}   [{rec['solve_seconds']:.2f}s]"
        )
        if n <= restricted_max_n:
            rec["chi_s"] = {}
            rec["bounds"] = {}
            for s in range(1, n + 1):
                t2 = time.perf_counter()
                sub = [T for T in cols if len(T) <= s]
                v = set_cover(sub, n)[0]
                lo, hi = trivial_bounds(n, s)
                rec["chi_s"][s] = v
                rec["bounds"][s] = [lo, hi]
                flag = "ok" if lo <= v <= hi else "BOUND VIOLATED"
                print(f"        s={s:>3d}  chi_s = {v:>5d}   [{lo}, {hi}]  {flag}  [{time.perf_counter()-t2:.2f}s]")
            bad = [s for s in rec["chi_s"] if not (rec["bounds"][s][0] <= rec["chi_s"][s] <= rec["bounds"][s][1])]
            rec["bounds_respected"] = not bad
        out[n] = rec
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=11)
    ap.add_argument("--restricted-max-n", type=int, default=10)
    args = ap.parse_args()
    data = run(args.max_n, args.restricted_max_n)
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "covers.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({str(k): v for k, v in data.items()}, fh, indent=1)
    bad = [n for n, v in data.items() if not v["matches_literature"]]
    bad += [n for n, v in data.items() if v.get("bounds_respected") is False]
    print(f"\nwrote {path}")
    print("all checks passed" if not bad else f"FAILURES at {sorted(set(bad))}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
