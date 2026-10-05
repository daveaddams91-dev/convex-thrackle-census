# v1.0.0 — Convex Thrackles: a residue bound and the census $2^{n-1}-n$

First public release. Software, manuscript, exhaustive verification and an
adversarial falsification suite for a study of **convex thrackles** — families of
chords of a convex $n$-gon in which every two members meet (share an endpoint or
cross).

---

## Research question

For $n$ labelled points in convex position, **how many maximal convex thrackles
are there, and how are they distributed by cycle length?**

## Main theorem

**Theorem (census).** Maximal convex thrackles on $\{v_0,\dots,v_{n-1}\}$ are in
bijection with the odd-sized subsets $S$ with $|S|\ge3$. The bijection sends $S$
to the thrackle in which each vertex of $S$ is joined to the vertex almost
antipodal to it, together with the forced pendant edges of the remaining
vertices. Consequently

$$\#\{\text{maximal convex thrackles}\}=\sum_{\substack{m\ge3\\ m\ \mathrm{odd}}}\binom{n}{m}=2^{\,n-1}-n,$$

refined: exactly $\binom{n}{m}$ of them have cycle of length $m$.

Supporting results, all with proofs in the manuscript:

* **Lemma 2.1 (residue encoding).** On any convex thrackle the map
  $\{v_i,v_j\}\mapsto i+j \bmod n$ is injective. This gives a two-paragraph proof
  of the classical bound $|E|\le n$ together with a criterion for equality.
* **Theorem 3.1.** A convex thrackle on $n\ge4$ convex points contains at most two
  polygon edges; with two it is contained in a *doublestar* (star at a vertex plus
  the chord joining its two neighbours), and there are exactly $n$ such thrackles.
* **Theorem 3.2 (partially proved, see below).** A convex thrackle with exactly
  one polygon edge has at most $n$ edges, with a complete characterisation of the
  equality case.
* **Theorem 4.1 / 4.3.** The unique thrackle cycle on an odd vertex set; the
  forced, unique attachment of every off-cycle vertex.
* **Proposition 6.1.** Two elementary bounds for the size-restricted cover number
  $\chi_s(n)$, the minimum number of thrackles of size $\le s$ covering all chords.

## Computational contribution

* **Exhaustive census for $4\le n\le11$** by *two independent routes* — brute-force
  enumeration of *all* convex thrackles, and a constructive enumeration emitting
  one object per odd subset. The two produce identical *sets* and match
  $2^{n-1}-n$ and $\binom{n}{m}$ exactly.
* **External validation:** $\chi(D_n)$ is recomputed from scratch by 0/1
  integer programming over all thrackles and matches the published closed form
  $n-\lfloor\sqrt{2n+\tfrac14}-\tfrac12\rfloor$ for every $n\le11$.
* **Exact values of $\chi_s(n)$** for $4\le n\le10$, all respecting the bounds of
  Proposition 6.1.
* **Falsification suite** (`experiments/exp3_falsification.py`) that searches for
  violations of every claim rather than for confirmations: no counterexample
  found up to $n=9$.
* 143 tests, each theorem statement covered; measured scaling of both routes.

## Reproducing

```bash
python -m pip install -e .       # numpy, scipy, matplotlib
python -m pytest -q              # 143 tests
python experiments/run_all.py    # full pipeline, ~4 min; exits non-zero on any failure
python experiments/run_all.py --quick
```

No random number generation anywhere; outputs are deterministic and committed
under `results/`.

## Novelty — stated precisely

| Claim | Status |
|---|---|
| $\|E\|\le n$ for convex thrackles | **Known** (convex case of Conway's conjecture). New short proof. |
| maximal thrackle = odd cycle + forced pendants | **Known / folklore** |
| $\chi(D_n)=n-\lfloor\sqrt{2n+\frac14}-\frac12\rfloor$ | **Known**, reproduced here, not claimed |
| residue encoding (Lemma 2.1) | **No prior statement found** |
| count $2^{n-1}-n$, profile $\binom{n}{m}$ (Theorem 4.4) | **No prior statement found** |
| $\chi_s(n)$ for $s<n$ | **New question as far as we know**; no formula claimed |

We did not find a priority claim and do not assert one.

## Known limitations (deliberate)

1. **Theorem 3.2 is only proved in machine-verified form** for $4\le n\le11$. The
   attempted proof is *wrong* and is reproduced in the manuscript with its
   arithmetic error visible (Remark 3.3) instead of being quietly patched. The
   statement is believed correct and is verified, but not proved.
2. The apex-uniqueness step of Theorem 4.3 is written as a case analysis whose
   intermediate step is asserted rather than derived; the conclusion is verified
   for all configurations with $n\le11$.
3. The growth rate of the total number of convex thrackles $a(n)$ is not
   analysed (data suggests $\Theta(3.64^{\,n})$).
4. **The manuscript has not been compiled** — no TeX distribution was available.
   Environment/brace balance and all five figure paths were checked mechanically.

## A falsification worth reading about

An earlier draft of this project attacked the cover number $\chi(D_n)$ directly
and, from an elementary double-counting bound matching exact values for
$n\le11$ and matching $\lfloor2n/3\rfloor$ for every $n\le60$, conjectured
$\chi(D_n)=\lfloor2n/3\rfloor$. A literature check showed $\chi(D_n)$ has been
known in closed form since 2006 and the conjecture is false from $n=14$. The line
was abandoned. It is documented in manuscript §9.3 and
`docs/mathematical_notes.md` §6 rather than quietly dropped, because agreement on
twelve consecutive values of $n$ was not evidence of anything.

## Citation

```bibtex
@misc{thracklecensus,
  title  = {Convex Thrackles: a residue bound and the census $2^{n-1}-n$},
  author = {{thrackle-census contributors}},
  year   = {2026},
  note   = {v1.0.0, \url{https://github.com/rajveersinh-is-dev/convex-thrackle-census}}
}
```

Manuscript: `paper/main.tex`. Notes: `docs/mathematical_notes.md`.
Methodology: `docs/methodology.md`. Licence: MIT.

*This release is software and a preprint. It has not been submitted to, accepted
by, or published in any peer-reviewed venue.*
