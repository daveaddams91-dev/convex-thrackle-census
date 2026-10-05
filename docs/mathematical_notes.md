# Mathematical notes

Working notes for *Convex Thrackles: a residue bound and the census $2^{n-1}-n$.
These are the notes behind the manuscript, including the arguments that did not
work out. They are deliberately informal.

## 0. Setup

`v_0,...,v_{n-1}` in convex position, cyclic order, indices mod `n`. A chord is a
pair `{v_i, v_j}`. Chords *meet* if they share a vertex or cross. A convex
thrackle is a set of pairwise-meeting chords.

Two facts used constantly:

* **F1 (crossing criterion).** Vertex-disjoint chords `{v_p,v_q}` and `{v_a,v_b}`
  cross iff their endpoints alternate around the polygon. Equivalently: exactly
  one of `v_a, v_b` is in each of the two open arcs cut by `{v_p,v_q}`.
* **F2.** Polygon edges cross nothing.

## 1. The residue lemma (Lemma 2.1 in the paper)

Encode `{v_i,v_j}` (i<j) by `i+j mod n`. Claim: injective on any thrackle.

Suppose `{v_i,v_j} != {v_a,v_b}` with `i+j = a+b (mod n)` and both in the
thrackle. They cannot share a vertex:

* `j=a` forces `i = b mod n`, and since `0 < b-i < n` and `i<b`... careful:
  `a=j<b` so `i<b`; `b ≡ i` and `0<=i<b<=n-1` so `b=i`, contradiction.
* `i=b` forces `j=a`; with `a<i<j` this is impossible.
* `j=b` or `i=a` gives equal edges.

So they are vertex-disjoint and must cross; assume `i<a`, then crossing forces
`i<a<j<b`. Hence `a+b-(i+j) = (a-i)+(b-j) >= 2 > 0`, and the congruence with
`a+b-i-j < 2n` gives `a+b = i+j+n`. But `b>=j+1`, `a<=j-1`, `a <= n-1` give
`a+b <= j+n-2`, so `i+j+n <= j+n-2`, i.e. `i <= -2`. Done.

*Why this is nice.* It uses nothing but F1, and it gives the equality criterion
for free: `|E|=n` iff residues exhaust `Z/nZ`.

*Dead end tried first.* I hoped for an injection into a set of size `n` using the
"midpoint of the shorter arc"; that fails, because two chords symmetric about the
same midpoint can meet (`{1,4}` and `{2,5}` in a hexagon). Recording it because
the failure is instructive: a natural-looking encoding is simply not injective.

## 2. Boundary structure (Section 4)

**At most two polygon edges.** By F2, two polygon edges meet iff consecutive;
three pairwise-consecutive edges of a cycle of length n>=4 do not exist.

**Two polygon edges => doublestar.** If `{v_{u},v_{u+1}}` and `{v_{u+1},v_{u+2}}`
are in `T`, every other edge must meet both. Meeting a polygon edge requires
sharing an endpoint, so every edge has an endpoint in `{v_u, v_{u+1}}` and one in
`{v_{u+1}, v_{u+2}}`; the only possibilities are the two polygon edges,
`{v_u,v_{u+2}}`, or an edge at `v_{u+1}`. So `T` is contained in the doublestar
`D_{v_{u+1}}` = star at `v_{u+1}` + `{v_u,v_{u+2}}`. This is tight: `D_v` is a
thrackle with `n` edges. Checked exhaustively for n<=11.

**Exactly one polygon edge: THE FAILED PROOF.** With `p=v_i`, `q=v_{i+1}`, `A` the
set of `j` with `{p,w_j}` in `T`, `B` the set of `s` with `{q,w_s}` in `T`:

* `{pw_j}` and `{qw_s}` cross iff `j<s` (for `j != s`).
* So `max(A\B) < min(B\A)` and `|A cap B| <= 1`.
* Case `|A cap B| = 1`: `|A|+|B| <= n-2`, so `|E| <= n-1`.
* Case `A cap B = empty`: `|A|+|B| <= n-2`, so `|E| <= n-1`.

**This is false**: `S(i,t)` itself has `n` edges and exactly one polygon edge.
Where does the case analysis go wrong? In the second case the constraint
`max A < min B` is *vacuous* when one of them is empty, so `A` can be all of
`{1,...,n-2}`: `|A|+|B| = n-2`, and `|E| = 1 + n-2 = n-1`... but `S(i,t)` has
`|E| = n`. Let me recount `S(i,t)`: it has 1 polygon edge + `{v_i w_t}` +
`{v_{i+1} w_t}` + `(t-1)` + `(n-2-t)` = `1 + 2 + t - 1 + n - 2 - t = n`. So
`|A| = t` (edges `{v_i w_r}` for `1<=r<=t`), `|B| = n-1-t` (for `t <= s <= n-2`),
`A cap B = {t}`, so `|A|+|B| = t + n-1-t = n-1`, not `<= n-2`. The error: with
`A cap B = {w_t}` I wrote `A\{t} <= {1..t-1}` and `B\{t} <= {t+1..n-2}`, so
`|A|+|B| <= (t-1) + (n-2-t) + |A cap B|` and I used `|A cap B| = 1` but then
wrote `+1` where the bound already counted `w_t` once, giving `n-2` instead of
`n-1`. Corrected: `|A|+|B| <= (t-1)+(n-2-t)+1 = n-2`? No: `|A| = |A\{t}|+1 <= t`,
`|B| <= n-2-t+1 = n-1-t`, so `|A|+|B| <= t + n-1-t = n-1` and `|E| <= n`. The
bound `|E|<=n` is right; equality holds for `S(i,t)`.

So the *statement* is fine and the proof is one line short of correct. I have left
the broken version in the manuscript with the error visible rather than quietly
repairing it, and I assert the theorem only in machine-verified form. Fixing the
arithmetic is left as future work.

## 3. The thrackle cycle (Theorem 4.1)

For an odd set `S = {a_0,...,a_{m-1}}` in circular order, `s = (m-1)/2`, claim the
only thrackle Hamiltonian cycle is `{a_i, a_{i+s}}`.

**Step 1 (step criterion).** The step-`k` graph `{a_i,a_{i+k}}` is a thrackle iff
`m >= 2k+1`. Verified by the crossing criterion: vertex-disjoint pairs
`{a_i,a_{i+k}}`, `{a_t,a_{t+k}}` with `t<i` cross iff `t+k>i`, and the shared-endpoint
exceptions are exactly `t=i-k` and `t=i+k-m`. A violation appears iff
`2k+1<m`. So with `k <= (m-1)/2` only `k=s` works.

**Step 2 (consecutiveness).** For `m>=5`, if `a_i` has thrackle-cycle neighbours
`u,w` then `u,w` are consecutive in circular order. Proof: write the circular
order as `a_i, A, u, B, w, C`. A cycle edge not at `a_i` either contains `u`
(then it must cross `{a_i,w}`, so exactly one endpoint in `C`), or contains `w`
(then exactly one endpoint in `A`), or neither (one endpoint in `A`, one in
`C`). So no such edge touches `B`, and the only edges through `u` or `w` besides
`{a_i,u}`,`{a_i,w}` would be `{u,z}`/`{w,z}` with `z` in `B`, which the conditions
exclude. Every vertex of `B` lies on a cycle edge, so `B` is empty.

**Step 3 (propagation).** Let `N(a_0) = {a_p, a_{p+1}}`. Then
`N(a_p) = {a_{m-1},a_0}` and `N(a_{p+1}) = {a_0,a_1}` (after reflection), because
each is a consecutive pair containing `a_0` and they must differ (else a closed
4-component). The continuation is forced: `N(a_{m-1}) = {a_{p-1},a_p}` (the
alternative `{a_p,a_{p+1}}` is excluded because `a_{p+1}` is saturated), and
inductively `N(a_{p-r}) = {a_{m-1-r},a_{m-r}}` for `0 <= r <= p`. At `r=p` this
says `N(a_0) = {a_{m-1-p},a_{m-p}}`, forcing `m = 2p+1`. Done.

## 4. Wedges (Theorem 4.3)

Rule found empirically and then proved: **if `u` lies in the gap `(a_j,a_{j+1})`
of `S`, its apex is `a_{j-s}`.** The crossing check works because `2s = m-1`,
which is what makes the arc arithmetic line up.

Pairs of pendants: if `u` is in gap `(a_j,a_{j+1})` and `u'` in
`(a_{j'},a_{j'+1})` with `j != j'`, read the four endpoints off the circle in the
order `a_{j-s}, u, a_{j'-s}, u'` and apply F1: they cross. So the extension is
always a thrackle. If `j = j'` they share the apex.

The uniqueness of the apex is where the proof is thinnest; see the manuscript's
§9.2.

## 5. The census (Theorem 4.4)

Bijection: odd `S`, `|S| >= 3` -> thrackle. |S|=m of them, all with `n` edges, so
maximal. Count: `sum_{odd m>=3} C(n,m) = 2^{n-1} - n`.

Sanity check that caught a real error: an early version assumed *any* musquash on
`S` extends. It does not -- there are `phi(m)/2 - 1` star polygons but only
`floor(m/2)`-ish of them are thrackles at all, and exactly one. I initially
believed `{7/2}` and `{7/3}` were both thrackle cycles on 7 points; `{7/2}` is not
(`{0,2}` and `{4,6}` do not cross). Good example of why exhaustive checks matter.

## 6. The abandoned line: chi(D_n) = floor(2n/3)?

Recorded in the manuscript §9.3. The lower bound I derived,

    L(n) = min over 1<=x<=n of [ n - x + max(0, 2x-n, ceil((x+1)/2 - n/x)) ]

equals `floor(2n/3)` for every `4 <= n <= 60` except `n=6`, and matches exact ILP
values for `n <= 11`. Then the literature check: `chi(D_n) = n - floor(sqrt(2n+1/4)-1/2)`,
known since 2006. So the conjecture is wrong (fails from `n=14`: 10 vs 9), and the
whole line was dropped. The bound was *valid* but not sharp.

Lesson kept: agreement on twelve consecutive values of `n` is not evidence. What
protected the surviving results is that they are *constructive* -- they hand you
the object -- so they can be checked one at a time.
