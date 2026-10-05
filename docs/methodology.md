# Methodology

How the experiments are designed, what each one is allowed to prove, and why the
validation strategy is what it is.

## Principles

1. **No random number generation.** Every number in `results/` is a
   deterministic output. `run_all.py` is reproducible bit for bit.
2. **Two independent routes for the main theorem.** Theorem 4.4 is checked
   twice: by brute-force enumeration of *all* convex thrackles (which enumerates
   far more than needed, including non-maximal ones), and by a constructive
   enumeration that emits exactly one object per odd subset. Agreement of the two
   *sets* (not just their sizes) is what we check.
3. **External validation against the literature.** We recompute `chi(D_n)` from
   scratch and compare against the published closed form. If our enumeration,
   our structural lemmas, and our ILP solver are all subtly wrong in a
   *correlated* way, this is unlikely to pass.
4. **Adversarial, not confirmatory, testing.** `exp3_falsification.py` is written
   to break claims. Each check enumerates configurations that *should* violate a
   lemma; finding one is a pass for the suite, not for the theory.
5. **Infeasible solver output is never trusted.** `set_cover` re-unions the
   chosen families and asserts the union is the full chord set, so an infeasible
   integer-program point is a hard error.

## What each experiment does

| script | what it computes | what it can establish |
|---|---|---|
| `exp1_census.py` | all convex thrackles for each `n`; size profile; maximal thrackles grouped by cycle length; constructive rebuild | Theorem 4.4 for `4 <= n <= 11`, by two routes |
| `exp2_covers.py` | `chi(D_n)` by 0/1 ILP over all thrackles; `chi_s(n)` for `s=1..n` | reproduction of the published `chi(D_n)`; exact `chi_s(n)`; the bounds of Prop. 6.1 |
| `exp3_falsification.py` | targeted searches for counterexamples to each lemma/theorem | falsification only; absence of counterexample up to `n=9` |
| `exp4_scaling.py` | wall-clock for both enumeration routes, object counts | measured complexity trends (not asymptotic claims) |

## Bounds on what the computation can prove

Exhaustive verification over all configurations with `n <= 11` is strong evidence
for the *combinatorial* statements (Lemmas 2.1, 3.1, 3.2, Theorems 4.1--4.4) but
it is not a proof for general `n`. Where the mathematical proof is incomplete we
say so explicitly and downgrade the theorem to its verified form rather than
letting the computation stand in for a proof. See manuscript §9.2.

## Complexity claims and their basis

* Building the meeting graph: `Theta(n^4)` time and space.
* Brute-force clique enumeration: `O(n^2 a(n))` set operations, where `a(n)` is
  the number of convex thrackles; output-bound.
* Constructive route: `O(2^n n^3)`, producing `2^{n-1}-n` objects.
* `chi(D_n)` and `chi_s(n)` by ILP: the constraint matrix has `C(n,2)` rows and
  `a(n)` columns with at most `n` nonzeros per column, i.e. `O(n a(n))`
  nonzeros. We do **not** claim a complexity bound for set cover; the exact
  values are simply what HiGHS returns.

The one asymptotic estimate we print without proving is the growth of `a(n)`;
`exp4_scaling.py` records the data and the manuscript flags it as open.

## Reproducibility

`results/run_all.log` is the log of the run that produced the committed
`results/*.json` and `figures/*.png`. `run_all.py` exits non-zero if any check
fails, so a clean exit is the reproducibility certificate.
