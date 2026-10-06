'''Experiment 1 – the census of convex thrackles (validation of Theorem 1.4).

For each ``n`` the script performs the following steps:

1. Enumerate *every* convex thrackle by brute force and record its size.
2. Count the maximal ones (size ``n``) and group them by cycle length.
3. Re‑build every maximal thrackle from the odd subsets via the constructive
   route and check that the two sets agree.
4. Compare the observed counts with the closed form ``2^{n-1} - n`` and with
   ``binom(n, m)``.

The module can be executed directly or imported from tests.  Import errors are
handled gracefully by attempting to locate the ``thrackle`` package in the
repository's ``src`` directory.

Usage::

    python experiments/exp1_census.py [--max-n 11]
'''  # noqa: D400, D401

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Import the library code.  When the repository is executed from the source
# tree the ``thrackle`` package lives in ``../src`` relative to this file.  If
# the import fails we augment ``sys.path`` with that location and retry.  This
# makes the module robust both when run as a script and when imported by the
# test suite.
# ---------------------------------------------------------------------------
try:
    from thrackle.census import (  # type: ignore
        census,
        construct_all_maximal,
        cycle_length_census,
        enumerate_thrackles,
        predicted_maximal_counts,
    )
    from thrackle.chords import is_thrackle  # type: ignore
except ImportError:  # pragma: no cover – exercised only in the test harness
    # Resolve the path ``../src`` relative to this file's directory.
    src_path = Path(__file__).resolve().parents[1] / "src"
    if src_path.is_dir():
        sys.path.insert(0, str(src_path))
    else:
        raise ImportError(
            "Unable to locate the 'thrackle' package. Expected it in '../src'."
        ) from None
    # Re‑attempt the imports after the path adjustment.
    from thrackle.census import (  # type: ignore
        census,
        construct_all_maximal,
        cycle_length_census,
        enumerate_thrackles,
        predicted_maximal_counts,
    )
    from thrackle.chords import is_thrackle  # type: ignore

# Directory where JSON results are written.
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def run(max_n: int) -> Dict[int, Dict[str, Any]]:
    """Execute the census experiment up to ``max_n``.

    Parameters
    ----------
    max_n:
        The largest number of points ``n`` to analyse.  ``n`` must be at least
        three because a convex thrackle on fewer points is trivial.

    Returns
    -------
    dict[int, dict]
        A mapping from ``n`` to a dictionary containing the measured statistics
        and verification flags.
    """
    if max_n < 3:
        raise ValueError("max_n must be >= 3 for a non‑trivial convex thrackle.")

    results: Dict[int, Dict[str, Any]] = {}
    for n in range(3, max_n + 1):
        start = time.perf_counter()
        # 1. Brute‑force enumeration of all thrackles.
        all_thrackles = enumerate_thrackles(n)
        # 2. Census by size.
        size_census = census(n)
        # 3. Group maximal thrackles by their cycle length.
        by_cycle = cycle_length_census(n)
        # 4. Re‑construct maximal thrackles via the constructive method.
        constructed = construct_all_maximal(n)
        # Extract the maximal thrackles (size == n) from both sources.
        brute_max = {T for T in all_thrackles if len(T) == n}
        constructed_max = {T for lst in constructed.values() for T in lst}
        # Validate that every enumerated set is indeed a thrackle.
        all_valid = all(is_thrackle(T) for T in all_thrackles)
        # Theoretical prediction for the total number of maximal thrackles.
        predicted_total = 2 ** (n - 1) - n
        # Overall verification flag.
        ok = (
            all_valid
            and brute_max == constructed_max
            and by_cycle == predicted_maximal_counts(n)
            and len(brute_max) == predicted_total
        )
        elapsed = round(time.perf_counter() - start, 3)
        results[n] = {
            "total_thrackles": len(all_thrackles),
            "census_by_size": size_census,
            "maximal": len(brute_max),
            "by_cycle_length": by_cycle,
            "predicted_maximal": predicted_total,
            "predicted_by_cycle_length": predicted_maximal_counts(n),
            "all_thrackles_valid": all_valid,
            "routes_agree": brute_max == constructed_max,
            "seconds": elapsed,
            "verified": bool(ok),
        }
        # Human‑readable progress line.
        print(
            f"n={n:3d}  total={len(all_thrackles):>8d}  maximal={len(brute_max):>6d} "
            f"(predicted {predicted_total:>6d})  by-cycle "
            f"{'OK' if by_cycle == predicted_maximal_counts(n) else 'FAIL'}  "
            f"routes {'agree' if brute_max == constructed_max else 'DISAGREE'}  "
            f"[{elapsed:.2f}s]"
        )
    return results


def main() -> None:
    """Entry point for the command‑line interface.

    Parses ``--max-n`` and writes the JSON report to ``results/census.json``.
    The process exits with status ``0`` on success and ``1`` if any ``n``
    failed verification.
    """
    parser = argparse.ArgumentParser(description="Validate convex thrackle census.")
    parser.add_argument("--max-n", type=int, default=11, help="Maximum n to test (default: 11)")
    args = parser.parse_args()

    data = run(args.max_n)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "census.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump({str(k): v for k, v in data.items()}, fh, indent=1)

    failures = [n for n, v in data.items() if not v["verified"]]
    print(f"\nWrote {out_path}")
    if failures:
        print(f"FAILURES at n in {failures}")
    else:
        print("All checks passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
