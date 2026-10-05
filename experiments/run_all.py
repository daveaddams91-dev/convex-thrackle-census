"""Run every experiment and regenerate every figure and table.

Usage::

    python experiments/run_all.py                 # full run  (n <= 11, a few minutes)
    python experiments/run_all.py --quick         # fast run  (n <= 8)

Everything is deterministic: no random number generation is involved anywhere.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

FIGURES = os.path.join(ROOT, "figures")
RESULTS = os.path.join(ROOT, "results")


def sh(*args: str) -> None:
    print(f"\n$ {' '.join(args)}", flush=True)
    subprocess.run([sys.executable, *args], check=True, cwd=ROOT)


def make_figures(max_n: int) -> None:
    os.makedirs(FIGURES, exist_ok=True)
    import matplotlib.pyplot as plt  # noqa: F401

    from thrackle import drawing

    with open(os.path.join(RESULTS, "census.json"), encoding="utf-8") as fh:
        cen = {int(k): v for k, v in json.load(fh).items()}
    with open(os.path.join(RESULTS, "covers.json"), encoding="utf-8") as fh:
        cov = {int(k): v for k, v in json.load(fh).items()}

    drawing.figure_census({n: cen[n] for n in sorted(cen)}, os.path.join(FIGURES, "census.png"))
    drawing.figure_covers({n: cov[n] for n in sorted(cov)}, os.path.join(FIGURES, "covers.png"))
    drawing.figure_examples(9, os.path.join(FIGURES, "examples.png"))
    drawing.figure_doublestar(11, os.path.join(FIGURES, "doublestar.png"))
    drawing.figure_cover_example(min(9, max_n), os.path.join(FIGURES, "cover_example.png"))

    # copies for the manuscript
    paper_fig = os.path.join(ROOT, "paper", "figures")
    os.makedirs(paper_fig, exist_ok=True)
    for name in ("census.png", "covers.png", "examples.png", "doublestar.png", "cover_example.png"):
        src = os.path.join(FIGURES, name)
        with open(src, "rb") as a, open(os.path.join(paper_fig, name), "wb") as b:
            b.write(a.read())
    print("\nfigures written to figures/ and paper/figures/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="smaller n (fast smoke run)")
    ap.add_argument("--max-n", type=int, default=None)
    ap.add_argument("--restricted-max-n", type=int, default=None)
    args = ap.parse_args()
    if args.max_n is None:
        args.max_n = 8 if args.quick else 11
    if args.restricted_max_n is None:
        args.restricted_max_n = 7 if args.quick else 10

    t0 = time.perf_counter()
    os.makedirs(RESULTS, exist_ok=True)
    sh(os.path.join(HERE, "exp1_census.py"), "--max-n", str(args.max_n))
    sh(
        os.path.join(HERE, "exp2_covers.py"),
        "--max-n",
        str(args.max_n),
        "--restricted-max-n",
        str(args.restricted_max_n),
    )
    sh(os.path.join(HERE, "exp3_falsification.py"), "--max-n", str(min(args.max_n, 9)))
    sh(os.path.join(HERE, "exp4_scaling.py"), "--max-n", str(args.max_n))
    make_figures(args.max_n)
    print(f"\nALL EXPERIMENTS FINISHED in {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    main()
