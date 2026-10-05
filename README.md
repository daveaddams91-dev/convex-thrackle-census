# Convex Thrackles: a residue bound and the census $2^{n-1}-n$

**How many maximal convex thrackles does a convex $n$-gon admit? Exactly
$2^{n-1}-n$ — one for every odd-sized subset of at least three vertices.**

A *thrackle* is a geometric graph whose edges pairwise meet (shared endpoint or
proper crossing). Conway conjectured a thrackle on $n$ vertices has at most $n$
edges; for vertices in **convex position** (a *convex thrackle*) this is
classical. This project studies the individual convex thrackles: their
structure, their number, and how they meet the polygon boundary.

## TL;DR (for the impatient)

1. **Residue encoding.** Encode the chord $\{v_i,v_j\}$ by $i+j \bmod n$. On any
   convex thrackle this map is **injective** (Lemma 2.1), giving a two-paragraph
   proof of $|E|\le n$ plus an equality criterion.
2. **Boundary structure.** A convex thrackle contains **at most two polygon
   edges**; with two it is contained in a *doublestar* (star at a vertex + the
   chord joining its two neighbours), and there are exactly $n$ of those.
3. **The census.** Each odd set $S$ of $m\ge3$ convex vertices carries a
   **unique** thrackle Hamiltonian cycle (join every vertex to the almost
   antipodal one), and every vertex outside $S$ has a **forced, unique** way of
   attaching. Hence maximal convex thrackles are in bijection with odd subsets of
   size $\ge3$, and
   $$\#\{\text{maximal convex thrackles}\} = \sum_{\substack{m\ge3\\ m\ \mathrm{odd}}}\binom{n}{m} = 2^{\,n-1}-n,$$
   refined to exactly $\binom{n}{m}$ with cycle of length $m$.
4. **Everything is verified** exhaustively for $n\le11$ by two independent
   routes, and our solver independently reproduces the *published* value of the
   related cover number $\chi(D_n)$.

| $n$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|
| all convex thrackles | 8 | 36 | 152 | 600 | 2256 | 8208 | 29216 | 102496 | 356160 |
| maximal thrackles | 1 | 4 | 11 | 26 | 57 | 120 | 247 | 502 | 1013 |
| $2^{n-1}-n$ | 1 | 4 | 11 | 26 | 57 | 120 | 247 | 502 | 1013 |

## Research question

> Let $\V=\{v_0,\dots,v_{n-1}\}$ be $n$ labelled points in convex position and
> let $\mathcal{T}$ be a family of sets of chords in which every two members meet
> ("convex thrackles"). **How many maximal convex thrackles are there, and how
> are they distributed?**

## Main result

**Theorem (census).** Maximal convex thrackles on $\V$ are in bijection with the
odd-sized subsets $S\subseteq\V$ with $|S|\ge3$; the bijection sends $S$ to the
thrackle cycle in which every vertex of $S$ is joined to the vertex almost
opposite to it, together with the forced pendant edges. Consequently there are
exactly $2^{n-1}-n$ of them, of which exactly $\binom{n}{m}$ have cycle of
length $m$.

Supporting results: the residue injection (Lemma 2.1), the boundary
classification (Theorems 3.1 and 3.2), the two elementary bounds for the
size-restricted cover number $\chi_s(n)$ (Proposition 6.1).

## What is genuinely new here (and what is not)

Being precise about this matters more than sounding novel.

| Claim | Status |
|---|---|
| $|E(\mathcal{T})\le n$ for convex thrackles | **Known** (convex case of Conway's conjecture, Erdős 1956; Woodall 1981). We give a new one-paragraph proof. |
| Maximal convex thrackle = odd cycle + pendant edges; pendants forced into wedges | **Known / folklore** (e.g. Araujo–Dumitrescu–Hurtado–Noy–Urrutia 2006). |
| $\chi(D_n) = n-\lfloor\sqrt{2n+\frac14}-\frac12\rfloor$ | **Known and not claimed.** We only reproduce it computationally as a pipeline check. |
| The residue encoding $e\mapsto i+j \bmod n$ (Lemma 2.1) | **We did not find a prior statement.** |
| The count $2^{n-1}-n$ and the profile $\binom{n}{m}$ (Theorem 4.4) | **We did not find a prior statement.** |
| $\chi_s(n)$ for $s<n$, its bounds and exact small values | **New question as far as we know**; no formula claimed. |

## Repository structure
```
src/thrackle/chords.py     chord primitives, crossing, residues, cycle peeling
src/thrackle/structure.py  thrackle cycles, wedges, doublestars, boundary family
src/thrackle/census.py     exhaustive enumeration + the constructive route
src/thrackle/covers.py     exact set cover (HiGHS), chi(D_n), chi_s(n)
src/thrackle/drawing.py    figures
tests/                     143 tests; every theorem statement is covered
experiments/exp1_census.py         census and cross-check of the two routes
experiments/exp2_covers.py         chi(D_n) vs literature; chi_s(n)
experiments/exp3_falsification.py  adversarial search for counterexamples
experiments/exp4_scaling.py        measured scaling
experiments/run_all.py            all of the above, regenerates figures
paper/main.tex             the manuscript
results/*.json             committed reference outputs
figures/*.png              generated figures
docs/mathematical_notes.md  long-form proofs and dead ends
docs/methodology.md         how the experiments are designed and validated
```

## Reproducing the results

```bash
python -m pip install -e .            # numpy, scipy, matplotlib
python -m pytest -q                   # 143 tests
python experiments/run_all.py         # full run: census, covers, falsification, scaling, figures
python experiments/run_all.py --quick # fast smoke run (n <= 8)
```

No random number generation is used anywhere, so the pipeline is deterministic.
Reference outputs are committed under `results/`; `run_all.py` overwrites them
and exits non-zero if any check fails.

### About the manuscript

`paper/main.tex` is the LaTeX source (standard `article` class; needs
`amsmath, amsthm, mathtools, graphicx, booktabs, hyperref, ulem, enumitem,
microtype`). **We could not compile it in the environment where it was
written** — no TeX distribution was available — so compilation is *unverified*.
What *was* checked mechanically: `\begin`/`\end` environments balance (45/45),
braces balance (653/653), and all five `\includegraphics` targets exist under
`paper/figures/`. Expect to need minor fixes on a first build.

## Examples

```python
from thrackle import maximal_thrackle, thrackle_cycle, doublestar, chi

thrackle_cycle([0, 1, 2, 3, 4, 5, 6])      # the unique thrackle cycle on 7 points
maximal_thrackle([0, 2, 5], n=9)            # the unique maximal thrackle with that cycle
doublestar(0, 9)                            # star at v_0 plus {v_8, v_1}
chi(9)                                      # 6, matching n - floor(sqrt(2n+1/4)-1/2)
```

## Limitations (read this before citing the paper)

* **Theorem 3.2 (exactly one polygon edge) is only proved in machine-verified
  form** for $4\le n\le11$. The proof we attempted is *wrong* and is
  deliberately reproduced with its gap visible (Remark 3.3) rather than patched.
* **The apex-uniqueness step of Theorem 4.3** is written as a case analysis whose
  intermediate step is asserted from the circular order rather than derived; the
  conclusion is verified for all configurations with $n\le11$.
* **Novelty is searched for, not established.** For the residue encoding and the
  census we report "we did not find a prior result"; we make no priority claim.
* The growth rate of the *total* number of convex thrackles $a(n)$ is open
  here; our data suggests $\Theta(3.64^{\,n})$ but we prove nothing about it.

## Related work

See `paper/references.bib`. Key items: Erdős (1956) and Woodall (1981) for the
convex case of the thrackle bound; Cairns–Nikolayevsky (2000, 2012); Fulek–Pach
(2011); Araujo–Dumitrescu–Hurtado–Noy–Urrutia (2006), Dujmović–Wood (2013) and
Fabila-Monroy–Wood (2014) for $\chi(D_n)$; Flajolet–Noy (1999) for analytic
combinatorics of convex configurations.

## Citation

```bibtex
@misc{thracklecensus,
  title  = {Convex Thrackles: a residue bound and the census $2^{n-1}-n$},
  author = {{thrackle-census contributors}},
  year   = {2026},
  note   = {Manuscript available at paper/main.tex; software at
             \url{https://github.com/daveaddams91-dev/convex-thrackle-census}}
}
```

## License

MIT — see `LICENSE`.
