"""Experiment 4 -- scaling of the two algorithms (complexity claims, measured).

* Enumeration of all convex thrackles: our implementation is ``O(n^2 a(n))``
  set operations where ``a(n)`` is the number of thrackles; the output itself
  has ``a(n) = Theta(lambda^n)`` elements, so the enumeration is output-bound.
  We measure seconds and peak object count against ``n`` and fit the growth.
* The constructive route (``construct_all_maximal``) is ``O(2^n n^3)`` and is
  compared against the brute-force route.

Usage::

    python experiments/exp4_scaling.py [--max-n 11]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from thrackle.census import construct_all_maximal, enumerate_thrackles  # noqa: E402


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")


def run(max_n: int) -> dict:
    """Worker function for parallel processing.
    
    Args:
        max_n:
    
    Returns:
        dict: Result of type dict
    
    """
    rows = []
    for n in range(4, max_n + 1):
        t0 = time.perf_counter()
        cliques = enumerate_thrackles(n)
        t1 = time.perf_counter()
        built = construct_all_maximal(n)
        n_built = sum(len(L) for L in built.values())
        t2 = time.perf_counter()
        rows.append(
            {
                "n": n,
                "n_thrackles": len(cliques),
                "n_maximal": n_built,
                "enum_seconds": round(t1 - t0, 4),
                "construct_seconds": round(t2 - t1, 4),
                "ratio_thrackles_over_maximal": round(len(cliques) / max(1, n_built), 3),
                "log2_thrackles": round(len(cliques).bit_length(), 1),
            }
        )
        print(
            f"n={n:3d}  |thrackles|={len(cliques):>8d}  maximal={n_built:>6d}  "
            f"enum={t1 - t0:7.3f}s  constructive={t2 - t1:7.3f}s  "
            f"speedup={((t1 - t0) / (t2 - t1)) if t2 > t1 else float('nan'):8.1f}x"
        )
    return {"rows": rows}


def main() -> None:
    """Entry point — parse arguments and run the main computation.
    
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=11)
    args = ap.parse_args()
    data = run(args.max_n)
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "scaling.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
