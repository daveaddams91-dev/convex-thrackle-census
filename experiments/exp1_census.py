"""Experiment 1 -- the census of convex thrackles (validation of Theorem 1.4).

For each ``n`` we

1. enumerate *every* convex thrackle by brute force and record its size;
2. count the maximal ones (= size ``n``) and group them by cycle length;
3. rebuild every maximal thrackle from the odd subsets via the constructive
   route and check that the two sets agree;
4. compare with the closed form ``2^{n-1} - n`` and with ``binom(n, m)``.

Usage::

    python experiments/exp1_census.py [--max-n 11]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thrackle.census import (  # noqa: E402
    census,
    construct_all_maximal,
    cycle_length_census,
    enumerate_thrackles,
    predicted_maximal_counts,
)
from thrackle.chords import is_thrackle  # noqa: E402

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")


def run(max_n: int) -> dict:
    out = {}
    for n in range(3, max_n + 1):
        t0 = time.perf_counter()
        cliques = enumerate_thrackles(n)
        cen = census(n)
        by_cycle = cycle_length_census(n)
        built = construct_all_maximal(n)
        brute_max = {T for T in cliques if len(T) == n}
        built_max = {T for L in built.values() for T in L}
        all_valid = all(is_thrackle(T) for T in cliques)
        predicted_total = 2 ** (n - 1) - n
        ok = (
            all_valid
            and brute_max == built_max
            and by_cycle == predicted_maximal_counts(n)
            and len(brute_max) == predicted_total
        )
        out[n] = {
            "total_thrackles": len(cliques),
            "census_by_size": cen,
            "maximal": len(brute_max),
            "by_cycle_length": by_cycle,
            "predicted_maximal": predicted_total,
            "predicted_by_cycle_length": predicted_maximal_counts(n),
            "all_thrackles_valid": all_valid,
            "routes_agree": brute_max == built_max,
            "seconds": round(time.perf_counter() - t0, 3),
            "verified": bool(ok),
        }
        print(
            f"n={n:3d}  total={len(cliques):>8d}  maximal={len(brute_max):>6d} "
            f"(predicted {predicted_total:>6d})  by-cycle {'OK' if by_cycle == predicted_maximal_counts(n) else 'FAIL'}  "
            f"routes {'agree' if brute_max == built_max else 'DISAGREE'}  [{out[n]['seconds']:.2f}s]"
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=11)
    args = ap.parse_args()
    data = run(args.max_n)
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "census.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({str(k): v for k, v in data.items()}, fh, indent=1)
    bad = [n for n, v in data.items() if not v["verified"]]
    print(f"\nwrote {path}")
    print("all checks passed" if not bad else f"FAILURES at n in {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
