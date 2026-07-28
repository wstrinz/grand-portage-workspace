# Scope: which mathematics this kernel is for

**The boundary is a semantic regime, not a syntax class.** "Polynomials" is too
broad to be a scope. The same polynomial `f` can be an equation generating an
ideal, an inequality `f ≥ 0`, an optimisation objective, a numerical residual,
or a formal term — and those have different notions of model, evidence, and
valid transport. Putting them under one transport table because they share
syntax would be the semantic conflation this project exists to prevent.

This document records the boundary. It does **not** reorganise the code, and
§4 says why not.

---

## 1. The regime this kernel owns

> **Exact affine.** Finitely presented polynomial models over explicit exact
> coefficient domains, with equations, nonvanishing conditions, polynomial and
> rational maps, base changes, finite case partitions, and algebraic evidence.

Concretely, what the six edge types and four claim kinds are *for*:

- models are ideals-with-open-conditions in a named ring over a named domain;
- claims are about points of those models, or about their coordinate rings;
- evidence is a certificate, a witness, or a reduction;
- transport is a ring map, a base change, a closure, or a case split.

Everything currently in `kernel.py` is a statement about that regime, and the
type table has now survived three foreign domains without needing a seventh
edge type. That is the evidence the nucleus is sound.

## 2. The regimes we have actually met

Not hypothetical. Each of these turned up in a live run and was recorded in
affine vocabulary because that was the vocabulary available.

### Exact real / semialgebraic

`f > 0`, positive definiteness, feasible regions, Euclidean-open sets, density
of real points.

**This is where our worst kernel defect came from.** `RESTRICTION` was earned by
a positivity-cone campaign, and its `zariski_dense` gate was found to be both
*insufficient* — the nodal cubic `y² = x²(x−1)` satisfies every word of it and
breaks the conclusion — and *beside the point*, because a restriction shares
its ideal and an `IDENTITY` is the same statement at both ends. The gate was
quietly serving a pointwise real-geometry claim inside a kernel whose
`IDENTITY` means membership in an ideal.

The split that matters: **algebraic open conditions (`f ≠ 0`, exactly a
localisation) belong here. Ordered-field inequalities (`f > 0`) do not.**

### Optimisation

Objectives, relaxations, primal/dual certificates, SOS decompositions, moment
matrices.

The border-rank campaign is the case study, and it is worth reading its claims:

| claim | typed as | what it actually is |
|---|---|---|
| `c.sos.identity.*` | `IDENTITY` | **genuinely exact affine** — a Gram identity in `ℚ[x,y]`, and now verified |
| `c.sos.qq` | `NONEMPTY` | SDP feasibility |
| `c.sos.motzkin` | `EMPTY` | non-membership of a convex cone |
| `c.sos.loud` | `PREDICATE` | **how the solver reports failure** — not mathematics at all |

So SOS work does not need to be abandoned or moved wholesale. Its algebraic
residue — the Gram identity — is exactly what this kernel can check, and it was
typed correctly. What has no home is nonnegativity, feasibility, and cone
membership. The last row is worse than mis-typed: a claim about tool behaviour
sitting in a slot reserved for claims about a variety.

### Finite census

Explicit manifests, dispositions, counts, cross-cuts. The `family` object and
`COUNT` kind already live at this boundary, and the kernel already refuses
`IDENTITY` at a family because *an index is not a ring*.

A live session then found the matching gap on the evidence side: **"established
by exhaustive finite enumeration" has no certificate kind.** The certificate
table is entirely algebraic, and certificates attach only to `EMPTY` claims.

Three of four `IDENTITY` claims in the border-rank campaign turned out to be
census facts — a recount, a retrodiction, a replayed verdict vector — typed
`IDENTITY` because it is the only kind meaning "these two things are equal".

### Bibliographic resolution

Which external object an identifier denotes.

**This regime appears on no standard list, and it is this project's trap
number one.** A live session established that a paper's "GGV1 Remark 7.10"
denotes what the arXiv source numbers 7.14, and that arXiv 7.10 is a *different
statement about the same subject* — so the naive resolution succeeds on the
wrong object rather than failing. It now has a typed home (`citation`), which
is the one piece of §2 that has been built rather than merely noticed.

### Certified numerics

Approximate points, enclosures, conditioning, homotopy paths. **Not yet met in
any campaign.** Listed because it is the obvious next regime and because
transport there is quantitative — an error transformer, not a licensed/refused
table.

## 3. Non-goals for this kernel

Stated so the supported core reads as larger, not smaller:

- arbitrary inequalities and ordered-field topology;
- floating-point results and error propagation;
- optimisation bounds, relaxation hierarchies, attainability;
- analytic or transcendental functions, differential equations;
- noncommutative algebra;
- general projective gluing and sheaf cohomology;
- arbitrary CAS scripts (there is a boundary, and it is a denylist over a real
  language — see `REVIEW.md`);
- discovering missing equations. The discharge machinery *routes attention to
  where an equation is missing*; it does not find it.

## 4. Why the code is not being reorganised yet

The carve above is a boundary, not an architecture. Splitting `kernel.py` into
a core plus profiles is a large refactor whose payoff is clarity, and nearly
all of that clarity is available from this document today. Three specific
reasons to wait:

1. **The enumeration is already incomplete.** Bibliographic resolution appears
   on no prior-art list and turned up within one session of looking. A plugin
   architecture frozen now would be frozen around the wrong set.
2. **One campaign per regime is thin evidence.** We have one real-geometry
   case, one optimisation case, two census cases. That is enough to see the
   boundary and not enough to design the seams.
3. **The kill criteria say the nucleus is fine.** `A7` — "the relation
   vocabulary does not transfer beyond polynomial systems" — is *not firing*.
   Six types survived border rank and toric geometry. The problem has never
   been the transport table; it is what we have been absorbing *into* it by
   flattening.

**What to do instead, and it costs nothing:** tag each campaign with the
regimes it spans, and when something is recorded in affine vocabulary that is
not affine, say so in the record. That is data collection for a split we are
not yet ready to design, and it converts a refactor decision into a
measurement.

| campaign | regimes |
|---|---|
| `lsem-census` | exact affine + finite census |
| `borderrank` | exact affine + optimisation + finite census |
| `gamma-delta4` | exact affine |
| `jc2-chartmap` | exact affine + bibliographic |
| `toric-phases` | exact affine |

## 5. The cut that decides what gets automated

> **Automate the bookkeeping until it disappears; keep the judgment expensive
> on purpose.**

Bookkeeping is: which edge type, which direction, what scope this certificate
carries. Judgment is: whether a join between two independently-sound
computations is licensed at all.

The two halves want opposite things and must not be traded off against each
other. **The failure mode of any round of ergonomics work is easing friction on
the judgment half**, because there the friction is the feature.

The case that pins it down is a live one. Two computations, each individually
well-evidenced, sharing not one variable, joined by a sentence in a `print`
statement. No evidence grade catches that: grading either half tells you
nothing whatever about the seam, and typing the bridge does not discharge it.
Discharging it requires somebody asserting that one layer *refines* the other
and being accountable for the assertion.

So:

- **Never infer a join.** A constructor must not emit a multi-premise
  inference implicitly. `premises` stays something a person or agent states
  and owns.
- **Never self-certify exhaustiveness.** A partition constructor emits the
  branches *and the obligation*; it does not discharge it.
- **Never collapse typed uncertainty into a score.** "CITED but unchecked",
  "exact but the parser is unaudited", and "formal but an interface assumption
  is unsealed" are different debts. A number erases the difference.

Everything else — the type, the orientation, the target presentation, the
program, the scope a certificate carries — should be derived if it can be.

## 6. The test for whether something belongs

For any proposed feature:

1. Does it use the same notion of **model** — a finitely presented algebra with
   open conditions?
2. Can one concrete run be **locally validated**, rather than labelled by the
   caller?
3. Does its transport **compose** with the existing operations?
4. Can its evidence be represented **without collapsing proposition and
   witness**?
5. Is **ignorance expressible** honestly?
6. Has a **real campaign** needed it?

If 1–3 fail, it is another kernel. If only 5 fails, the representation is not
ready. If only 6 fails, defer it.
