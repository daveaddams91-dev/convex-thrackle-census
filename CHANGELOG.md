# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-05

### Added

- `src/thrackle/chords.py` — chord primitives: crossing and meeting criteria,
  polygon edges, the residue map, residue-injectivity certificate, and degree-1
  peeling to extract the unique cycle of a thrackle.
- `src/thrackle/structure.py` — the canonical constructions: the unique thrackle
  cycle on an odd vertex set (Lemma 4.1), forced pendant attachment / wedge
  lemma (Theorem 4.3), doublestars (Theorem 3.1) and the one-polygon-edge family
  (Theorem 3.2).
- `src/thrackle/census.py` — exhaustive enumeration of all convex thrackles as
  cliques of the meeting graph, plus the constructive route that emits one object
  per odd subset (Theorem 4.4).
- `src/thrackle/covers.py` — exact 0/1 set cover (HiGHS via `scipy.optimize.milp`)
  with an internal feasibility re-check, `chi(D_n)`, the size-restricted number
  `chi_s(n)`, and elementary bounds.
- `src/thrackle/drawing.py` — all five figures.
- `experiments/` — census cross-check, cover numbers against the published
  closed form, an adversarial falsification suite, scaling measurements, and
  `run_all.py`.
- `tests/` — 143 tests; every theorem statement in the manuscript has a matching
  test, several of them exhaustive over all configurations for small `n`.
- `paper/main.tex`, `paper/references.bib` — the manuscript.
- `docs/mathematical_notes.md`, `docs/methodology.md` — long-form proofs,
  dead ends, and the validation protocol.
- Committed reference outputs in `results/`.

### Known issues

- Theorem 3.2 is asserted only in machine-verified form for `4 <= n <= 11`; the
  attempted proof is reproduced in the manuscript with its arithmetic error
  visible (Remark 3.3) rather than repaired.
- The apex-uniqueness step of Theorem 4.3 is written as a case analysis whose
  intermediate step is asserted rather than derived.
- The growth rate of the total number of convex thrackles `a(n)` is not analysed.

### Removed

- The abandoned line of work on conjecturing `chi(D_n) = floor(2n/3)`. The
  literature check showed `chi(D_n) = n - floor(sqrt(2n+1/4)-1/2)` is known, so
  the conjecture was false for `n >= 14`. Retained as a documented falsification in
  manuscript §9.3 and `docs/mathematical_notes.md` §6 rather than silently
  dropped.

[1.0.0]: https://github.com/rajveersinh-is-dev/convex-thrackle-census/releases/tag/v1.0.0
