# HANDOFF.md — chronological implementation record

> **Current readers:** start with `CURRENT.md`, then `ARCHITECTURE.md` and
> `REVIEW.md`. This file preserves the detailed development narrative and
> experiment history; later sections may describe superseded implementation
> states and should not be read as current authority.

Written for a session with **no prior context**. Everything needed to pick this
up is here or linked from here.

2026-09-12: v0.34 implements the accepted Phase B field-reach and
family/model composition boundary at graph format 8 and kernel epoch 12. The
executable contract and observed seam replay are in `review/v0.34-preflight/`;
the release record is in `review/v0.34/`. Read `CURRENT.md` for the compact
current state and `docs/WORK.md` for operational attempts and unchecked checks.

---

## 1. What this is, at the smallest size that is still true

**Grand Portage** records what each modelling step in a computational-algebra
campaign *loses*, and refuses the conclusions that loss does not support.

A computation produces an artifact. The artifact does not carry its own licence
to conclude. A Gröbner basis reducing to `1` is *evidence* of emptiness; what
makes it a *kill* is the certificate attached and the scope that certificate
derives. Conflating those is how the parent project shipped an erratum.

It is the successor to `whetstone/` in the `math-stuff` repo, where the same
discipline exists as three single-file prototypes with their domains hardcoded.
**What is new here: the graph is data, the transport table is the only code.**

Five layers, enforcement in exactly one:

```
agent → MCP server (edge REQUIRED, no declaration → no CAS process)
      → .portage/graph.jsonl  (append-only; the graph is the state)
      → kernel (6 edge types × 2 directions × 4 claim kinds)
      → checker → findings → discharge moves
      → hook (runs after each tool call, exit 2 = refuse)
```
The `exit 2` in that compact diagram is the Claude Code protocol. Codex uses an
exit-0 structured `PostToolUse` block and requires the project hook to be
trusted and enabled; W9 proved that path in the actual author loop.

Drop the hook and it is telemetry. Drop the MCP server and it is a linter
nobody runs.

**Version 0.34.0. <!--checks-->1789<!--/checks--> checks.** Treat
every claim in the docs as provisional.

**The v0.31.2 patch makes exact derived-identity receipts portable.** A
`VERIFIED_DERIVED` identity carrying `lhs - rhs = sum b_i f_i` is replayed by
GP's exact polynomial checker and remains current when Singular is absent or a
different version is installed. Receipt/model drift fails closed. Uncertified
answers, refutations, and searches remain backend-bound. `verify --dry-run`
also distinguishes already-current terminal verdicts from missing inputs.

**The v0.31.1 patch closes the untyped-model half of field-relative emptiness
scope.** A non-`SCHEME` `EMPTY` claim now produces actionable
`FIELD-EMPTY-MODEL-SCOPE` debt unless its model declares both a structured
coefficient domain and point universe. Historical logs remain readable and
repairable. This does not introduce certificate-kind ontology or claim that a
combinatorial obstruction establishes geometric emptiness.

**The v0.31 boundary closes historical-read and field-scope seams before the
first public release of the v0.30 feature set.** Formats 5 and 6 preserve and
validate their recorded implementation identity during direct reads and
migration. Field-relative EMPTY evidence accepts only a bounded, canonical
field-name grammar; malformed scopes cannot be declared, read from legacy
history, or laundered through migration. Graph format 7 and kernel epoch 11
are unchanged.

**The v0.30 boundary makes exact native verification independently durable.**
`UNVERIFIED` attempts remain visible and retryable, solver-free verifiers carry
closed native provenance, bounded quadratic/cubic extension-valued witnesses
replay in exact quotient arithmetic, and selected-real receipts are checked by
an implementation independent of their producer. The transport table remains
at kernel epoch 11; graph format advances to 7.

**The v0.29 boundary introduced selected ordered-real semantics.**
`REAL_CLOSURE` is a third point universe over Q and is valid only with a
selected REAL embedding. Structured conditions add `POSITIVE`, `NEGATIVE`,
`NONNEGATIVE`, and `NONPOSITIVE`; comparisons are signs of a difference. The
bounded univariate verifier checks the isolator with exact Sturm arithmetic,
refines rational intervals, and records a receipt replayed by the fold. Failed
isolation is `UNVERIFIED`, embedding-changing maps do not transport predicates,
and incompatible sign claims at one model create explicit debt.

**The backend evidence seam is now durable.** Production verifiers and
structured operations dispatch through semantic `SingularBackend` methods and
retain immutable execution artifacts. Backend protocol 2 / Singular
implementation 4 gives every trace entry a content address for a complete
canonical envelope: exact nonce-bearing program, argv, process status, stdout,
stderr, parsed output, and certificate. Objects are published under
`.portage/artifacts/sha256/` before a graph-affecting operation reference or
verdict is appended; read-only health and classification probes remain ephemeral. `gp artifacts check`
revalidates every object and trace projection. Missing objects are an explicit
audit failure, not ambient input to deterministic graph folding. Pre-artifact
verdicts remain readable but stale. Only the exact production adapter with its
probed binary may record authority; injected runners and subclasses remain
non-authoritative.

**OperationContract now has two Lean-backed pilots and two exactness routes.**
Saturation separates `J = I : f^infinity` from its checked one-sided envelope.
Elimination is multi-sorted: for an inclusion `i : S -> R`, exact semantics is
`J = inverse_image(i, I)`, while `verify.operation_output` establishes only
that the recorded target ideal invents no equation. `verify.elimination_section`
checks a simultaneous polynomial retraction fixing `S` and carrying every source
generator into `J`. Version 0.8.0 adds `verify.elimination_groebner`: an untrusted
Singular producer discovers a bounded pure-lex basis and span witnesses, then
GP's small exact-polynomial checker independently replays the source identities,
all critical pairs, the elimination order, and retained-basis memberships.
Lean proves that independent no-invention plus either completeness route yields
exact contraction. It also proves the stronger fact carried by the section:
precomposing a target evaluation with the polynomial retraction lifts every
target-valued point. `RetainedCoordinateExpressible` now states the separate
claim-side obligation that a predicate factors through those retained
coordinates, and Lean proves point-surjectivity transports every such predicate.
The pure Groebner route grants no point authority; a countermodel proves the
expressibility premise cannot be dropped.

**Current elimination-materializer status.**
`gp materialize-elimination-groebner --src SOURCE --vars dm4 --produces TARGET`
now closes the producer/graph seam: it discovers the retained pure-lex target,
requires independent current no-invention and Groebner-completeness verdicts,
and submits the target model, constructor edge, both verdicts, and provenance as
one prevalidated graph batch. The real eight-variable JC dm4 fixture completed
with a 21-element basis, 17 retained generators, and 210 checked critical pairs;
the independent source-membership pass accepted all 17. This earns exact
contraction only. A section or checked finite point-lift cover remains necessary
for point-surjective predicate transport.

Version 0.10.0 projects that theorem into a deliberately small exact-affine claim
syntax: `condition.all` is a conjunction of polynomial `ZERO`/`NONZERO` atoms.
Version 0.11.0 makes that typing compositional across verified mapped
`EQUIVALENCE` edges: because `forward` is the point map, `ALONG` rewrites with
`inverse` and `AGAINST` with `forward`; simultaneous exact substitution and the
Lean composition theorem pin the result. The rewritten condition is then checked
in the elimination target. Free text, eliminated-coordinate conditions, pure
Groebner certificates, unverified maps, and unsupported intervening operations
remain conservative refusals.

Version 0.12.0 derives the more general law underneath this: a predicate pulls
back contravariantly along any concrete point map. The runtime recognizes
matching exact identity-coordinate maps and currently checked constructor-built
elimination projections. Restrictions/refinements and projection pullbacks can
therefore feed a later section-certified elimination; unspecified polynomial
maps and unchecked projections still lose syntax. A RESTRICTION whose exact
endpoint rings disagree is rejected when the graph folds, because every one of
its point-transport cells presupposes a common point universe.

Version 0.13.0 adds the next point-level evidence route. A finite piecewise
lift certificate covers the target by principal opens with guarded rational
formulas plus an all-guards-zero polynomial fallback. Singular searches for
localization/radical memberships; the small exact checker re-expands every
stored cofactor identity, and graph folding replays the whole proof envelope.
Lean's `FiniteEliminationPointLiftCover` theorem shows why joint n-ary coverage
plus local lift/projection laws entails point-surjectivity. The cusp
normalization is the positive control: `u=y/x` on `x!=0`, `u=0` on `x=0`.
This authority is deliberately independent of exact contraction.

**Current coefficient-lowering status.** `gp verify-coefficient-expansion
--spec SPEC.json` now translation-validates the compiler boundary from bounded
polynomial templates to exact-affine scalar coefficient models. It checks
ordered cap-plus-one coordinate packs, exact substitution, every recorded row,
and overflow. Selected rows earn only the necessary direction; complete
`0..degree` coverage earns polynomial-identity equivalence. The report is
translation evidence and does not mint elimination authority by itself.

The live v14 JC campaign checks all sixteen `y^0..y^3` rows of
`G1,G2,G3,G5` in two models: cap 1 on retained polynomials with cap 0 on
`dm4`, and uniform cap 1. The tuple `dm2=1,d2=y` satisfies all seventeen
identities of the scalar v13 exact target, but its cap-0 source fiber is UNIT:
the `y` row of `G2` is the constant `3/2`. Its unrestricted lift
`dm4=-y/2` breaches the cap. Conversely, real Singular verifies the bounded
cap-0 point `dm2=1,d2=2,dm4=-1` and the uniform-cap-1 nonunit point
`dm2=y,d2=1,dm4=-y/2`.

This is the first clean evidence that coefficient expansion is not cosmetic:
it changes the valid point-lifting theorem while fitting the existing
exact-affine kernel once lowering is checked. A generic pure-lex contraction of
the fifteen-coordinate cap-0 model was killed with exit 9 after roughly four
minutes. That is COST, not a semantic failure and not authority. The producer
also exposed and now fixes a smaller boundary bug: exact syntax accepted as
`**` is canonicalized to Singular's `^` before execution.


**Current Laurent-lowering status.** `gp verify-laurent-lowering --spec
SPEC.json` checks a closed finite Laurent straight-line program over GP's exact
polynomial coefficient ring. Add, multiply, coefficient scale, formal
derivative, and declared `y`-shift nodes are bounded and independently
recomputed. Explicit support-clearing exports are canonical
`sparse_polynomial_v1` objects accepted directly by coefficient expansion; an
insufficient shift fails closed. The separate
`laurent_coefficient_pipeline_v1` checker verifies both passes and requires
total, unique, exact export-to-image bindings, so a self-consistent edited
intermediate is refused. The frozen JC rows 7--8 replay at
`fixtures/jc_rows78/laurent_lowering_v1.json`, with its bound two-pass sibling
`laurent_coefficient_pipeline_v1.json`, verifies the corrected depressed-
chart equations and rejects both the old symbolic-`G` zero RHS and a `21 -> 20`
mutation, and its `F_-7` export passes complete scalar-row replay. Equality
and export are distinct licenses. Their authority stops before: source
geometry, chart validity, integration, guard invertibility, graph claims, and H3
remain outside. Version 0.17 packages this standalone evidence-language seam;
it changes neither format 3 nor epoch 10 and should earn graph persistence only
after more live consumption.

**Current factor-power status.** The newly landed JC p-window packet supplies
two independent exact square receipts on the `c9_11` axis. GP now replays their
scoped polynomial identities with `factor_power_v1`; malformed exponents,
nonunit monomials, changed equations, and schema drift fail closed. The checker
persists the crucial distinction between a verified factor identity and its
point consequence. Equation vanishing in the pinned quotient, a no-zero-
divisors interpretation, and unit witnesses for the nonzero coefficient, `p`,
and `t` remain named obligations. Mathlib-free Lean proves those premises are
sufficient. No axis emptiness, p-chart conclusion, or graph transport is minted.
The companion affine-composition pass now verifies that the monic base forces
`c9_11=-p*t` and that exact substitution into `10*t*c9_11+15*p*t^2`
yields the declared unit `5*p*t^2`; Lean proves the resulting semantic premises
are inconsistent. The remaining step is no longer polynomial arithmetic: bind
both equations to the same pinned quotient/localization and prove that target's
domain and unit witnesses. Until then GP still refuses axis emptiness.
Version 0.19 closes that exact composition seam without adding a specialized
authority: the adapter emits a cofactor identity for a guard monomial, the
existing localized-unit verifier binds and replays it against the frozen
`c9_11` axis model, and the graph mints local `EMPTY`. The declared
`NECESSARY_CONDITION` edge refuses moving that result to the ambient axis. The
review packet retains the native and frozen digests, real Singular artifacts,
graph, projection, explorer, and mutation controls; no p-chart, source, lift,
or H3 conclusion is present.

**Current ordered-chain status.** The bounded
`localized_triangular_solve_chain_v1` checker now validates exact ordered
localized affine substitutions, not merely independent pivots. It binds the
coefficient domain, point universe, ring order, guard list, ordered generator
states, selected equation, unit coefficient, pivot-independent solution, and
both state fingerprints at every step. The first five-step fixture uses the
landed JC source top-face row order and solve expressions. Mutations of step
order, prior substitution, state fingerprint, unit scope, normalized output,
or schema fail closed. Lean proves that a chain of semantically bound
`MappedEquivalence` steps
preserves points and emptiness. Version 0.20 compiles both five-step chains to
explicit forward/reverse maps and cofactor proofs; `verify.ring_iso` now earns
graph-bound mapped-equivalence authority for the exact endpoint quotients. The
second-face consumer correctly refuted literal v1 normalization: all five
differences contain `15*t^3+1`. The v2 evidence envelope checks an exact
cofactor against that persistent scalar-gauge generator at every step and
verifies the landed 31/31 native-check receipt. This is the desired live-driven
extension, not a generic quotient simplifier.

**Current depth-6 chain status.** JC commit cb3136c lands 25 sparse
depth-2..6 face tables, ten top/second inputs, 23 ordered solves, and two
residuals. GP independently replays every transition and welds both ends to its
earlier verified fixtures.

The bounded graded extractor closes the raw-face seam. Its fast sparse engine
expands five frozen reduced E-system rows through the declared root supports
and matches all 25 outputs. A stronger audit reconstructs those rows from Zu,
fourteen P-side triangular eliminations, the E-system formula, and invariant
substitution. Lean proves source witness -> selected-face witness and
selected-face emptiness -> source emptiness, while refuting the reverse witness
inference.

The full finite-template assay materializes the honest source endpoint:
78 active variables and 147 complete nonzero coefficient equations. The target
retains 25 of those generators exactly. Containment verifier version 3 reparses
the included generators and treats their unit-cofactor inclusion as a
verifier-native structural decision, so the existing NECESSARY_CONDITION edge
earns VERIFIED without CAS and the persisted campaign has zero findings.

The earlier statement that the graph had a 64-variable model bound was wrong.
That bound belongs to specialized checkers and producers. The measured cost of
the honest graph is instead size: about 39.5 MB of JSONL because large
generators repeat. Original polynomial-pair -> reduced E-system, reverse
lifting, chart coverage, H3, and verdict promotion remain refused.

**Current product-split status.** `product_split_v1` replays the landed bottom
split `E[2,0]=10(c6_0p+c8_0)(c7_0p+c9_0)` and independently verifies
`E[4,0]=-pE[2,0]`. Lean derives the binary factor disjunction under the
same typed domain/unit premises. The separate `PartitionContract` and supported
`gp construct product-split` path now compile the constant-unit `E[2,0]`
receipt into two same-ring branches plus a covering claim; real Singular
verifies the emitted partition exhaustive. This is deliberately not an
`OperationContract`, because no single edge carries the n-ary theorem. The
variable-unit `E[4,0]` receipt remains evidence-only until cover verification is
localization-aware. Recombination still requires conclusions on every branch
plus the exact partition's verified exhaustiveness verdict.
**Current affine-branch status.** `gp construct affine-solve` consumes the
literal unit-coefficient branch equations produced above. It keeps the same
ring, translates the solved coordinate to zero, rewrites the entire ideal and
open guards simultaneously, and emits explicit inverse polynomial maps. The
JC left map `c8_0 -> -p*c6_0` passes the real Singular ring-isomorphism check;
the right map is symmetric. No structured identity crosses until that verdict
is current and `VERIFIED`. Dropping the normalized zero coordinate remains a
separate open operation contract.

**Current localization status.** `gp verify-localization-membership --spec
SPEC.json` checks a closed principal-open certificate with explicit guards,
denominator powers, a guard-monomial multiplier, and exact ideal-membership
cofactors. Its only licence is an identity in the declared localized coordinate
algebra. It does not alter RESTRICTION semantics, mint an ambient identity, or
grant point transport. Lean proves the certificate shape entails multi-guard
localized membership. The first H3 live use confirms that individual pivot
identities are useful while whole-chain authority remains separate; the surface
therefore remains narrow. Version 0.16 adds the distinct graph-bound
`LOCALIZED_UNIT_IDEAL_CERT`: a bounded producer may find a guard monomial, the
exact checker replays its cofactors, and the fingerprint-bound verdict supports
`EMPTY` only on that recorded open model. A miss is `UNVERIFIED`, and
RESTRICTION still refuses transport to the parent. Version 0.15 added the
closed, canonical `sparse_polynomial_v1`
wire form without
raising the infix parser limits or changing graph authority. Localization and
coefficient expansion retain large sparse values through exact checking.

The first live H3 batch replay now verifies all twelve frozen q-window pivots:
163--2,011 terms per equation, pivots `c9_0..c9_11`, coefficient `10*t`, and a
separate source fingerprint per step. Every verdict is still only one identity
in the declared q localization. The batch deliberately performs no dense
back-substitution and earns no chain, ambient, source-membership, p-chart, or
H3 conclusion.

Version 0.7.0 advanced format 1 to kernel epoch 3 when this distinction first
changed transport meaning: exact coordinate-ring contraction licenses a
retained-ring identity moving forward, but does not prove base-relative
geometric image closure. Version 0.8.0 stayed in epoch 3 because it added a new
certificate/verifier for the already-formalized contract. Version 0.9.0 advanced
to kernel epoch 4 when section plus no-invention earned point-surjective image
authority. Version 0.10.0 advances to graph format 2 / kernel epoch 5 for the
persisted condition syntax and newly licensed target-expressible nonclosed
predicate transport. Version 0.11.0 keeps format 2 and advances to kernel epoch
6 because verified coordinate-map composition licenses new paths. Version
0.12.0 keeps format 2 and advances to kernel epoch 7 when generic concrete
point-map pullback licenses restriction and projection compositions. Version
0.13.0 keeps format 2 and advances to kernel epoch 8 when checked finite lift
covers license new point-surjective predicate transports. Version 0.14.0 uses
format 3 / kernel epoch 9 to separate coefficient domains from point universes
for scoped geometric authority. Version 0.15.0 stays at format 3 / epoch 9
because sparse polynomial objects extend the standalone evidence language and
resource boundary without changing transport meaning. Version 0.16.0 stays at
format 3 and advances to epoch 10 because a checked localized-unit proof may
now establish local EMPTY graph authority; no transport cell changes. Version
0.17.0 stays at format 3 / epoch 10 because Laurent lowering, canonical
polynomial export, and exact two-pass binding extend only the standalone
evidence language; they grant no graph authority. Version 0.18.0 also stays at
format 3 / epoch 10: campaign projections and the Three.js explorer are
read-only derived views, while ordered localized solve chains remain standalone
translation evidence with explicit normalization debt and no graph claim
authority. Older native graphs
migrate non-destructively with
`gp migrate --to-current-kernel`; absent condition fields remain absent and
earlier verdicts remain history but stale.

Live validation now includes the polynomial-section control and bounded
Groebner replays of the real W7-W10 eliminations: W7 required six critical-pair
checks; W8-W10 required one each; all verified against Singular 4.2.1 and the
independent checker. The historical campaign graphs were not mutated. Their
prose says Q but their old model records omit machine-readable characteristic,
so the replays used disposable copies with explicit `characteristic: 0` and
`coefficient_domain: Q`. W10 additionally needed the exact `maps`/`inverse_maps`
to `forward`/`inverse` repair established by W11 before the current kernel would
fold the whole graph. The section theorem plus the structured-condition pilot
now closes retained-coordinate predicate transport through verified mapped
coordinate changes, identity-coordinate refinements, and checked projection
pullbacks. The next semantic obligations are concrete maps for remaining
nonidentity operations, broader lift charts beyond the bounded Q/prime-field
principal-open form, and pressure from an actual research campaign. See
`OPERATION-CONTRACTS.md` and
`COMPATIBILITY.md`.
There is now a **public repo**: `github.com/wstrinz/grandportage`, Apache-2.0,
the tool plus all three fixtures plus `DESIGN.md` / `REVIEW.md` /
`docs/first-run/`. This repo is `grand-portage-workspace` (private) and holds
the two things the public one deliberately omits: `TESTPLAN.md` and this file,
because both describe traps in unrun blind trials.

### Where the last three versions came from

**Every structural change since v0.2 was forced by a live run failing**, not by
review. Worth knowing because it predicts where the next one comes from.

| test | verdict | what it forced |
|---|---|---|
| **T3** resumability | **FAIL** | no read path showed which findings were knowingly accepted, so a fresh agent read a healthy campaign as a failing one → `[CARRIED]` marking, `gp show` printing inferences and certificates, `portage_check`'s advertised-but-unread `full` flag |
| **T1** blind run | **FAIL** | an agent superseded a refusal instead of satisfying it → `PARALLEL-EDGE`, `VACUOUS-CONCLUSION`, `SELF-BUILT`, `partition`, `premises`, typed discharge |
| **T2** external review | 8 defects | the CAS boundary was still bypassable **through the fix for it** |
| **T4** merge fan-out | **PASS / FAIL** | kind laundering, existence on the honour system, `gp merge` |
| **T5** foreign campaign | **PASS** | the `ladder` split, open premise slots, `CITED_PROOF`, `TYPE_MEANS` |
| **L1** toric containment | **premise refuted** | the containment model held but had never been under load → `verify.containment` |
| **W5/L4** identity live-test | 13 defects | **the verifier had no surface at all** → `gp verify`, `portage_verify`, the `verdict` event kind, GATE 3 |
| **GPT-2** prior-art review | 2 kernel errors | `SPECIALIZATION` ignored `identity_origin`; the `RESTRICTION` density gate was insufficient *and* mis-typed |
| **W6** post-verifier-layer | **PASS**, 8 defects | `operations.py` had no surface at all → `gp construct`; `ring_iso` silently skipped without its flag; a discharge its own verifier declines. **The hook was INERT the whole run and the run could not see it** |
| **W7** enforcement live | **PASS**, 10 defects | **the tool caught a live flop at the moment of action** — the L1 class this file records as having "nothing that would have stopped me". Also: refusals at *verify* time arrive after the graph has folded, and the tool cannot recognise a repair |
| **W8** repair follow-up | **FAIL**, 1 blocker | Singular printed `x^3-x*y` as compact `x3-xy`; the verifier changed its meaning and returned a mathematically wrong verdict. The Codex hook also ran but hid exit-2 feedback |
| **W9** Codex enforcement | **PASS**, 0 blockers | structured PostToolUse refusal was model-visible and RETRACT-cleared; real saturation/elimination/decomposition and seven hand-checked verdicts passed with explicit round-trippable CAS output |
| **W10** Claude Opus enforcement | **PASS**, 0 blockers | Claude received the automatic exit-2/stderr refusal, RETRACT-cleared it, completed the three real constructors, recorded 30 correct verdicts, and finished with no findings. It also exposed mapped `EQUIVALENCE` being conflated with literal containment; the Lean-backed repair now gives coordinate changes the exact `forward`/`inverse` surface W10 needed |
| **W11** mapped-equivalence repair assay | **PASS**, 0 blockers | malformed aliases and one-sided maps were atomically refused; exact canonical maps folded; real Singular verified both ideal pullbacks and both inverse compositions; no literal-containment verdict was scheduled; final full check was empty and an independent symbolic handcheck agreed |
| **v0.8 elimination replay** | **PASS**, 0 semantic failures | W7-W10 exact contractions verified through bounded pure-lex certificates; the run exposed and fixed a Windows console-encoding crash after successful verification. Legacy field metadata and the W11 map repair were supplied only in disposable copies |
| **v0.9 JC elimination pressure** | **PASS by refusal** | A proposed 3-generator exact image target was only a necessary system: the source pure-lex basis had 21 elements, 17 retained, and the target omitted `d2*dm1^3 + 3*dm1^2*dm3 + 3*dm1*dm2^2 - 2*Phi`. GP refused exact promotion; the persisted campaign retypes the edge as `NECESSARY_CONDITION` |
| **v0.10 retained-predicate pressure** | **PASS, positive plus refusal controls** | Real Singular checked the section `y -> x^2` for `(yx-1, y^2-x) -> (x^3-1)`. The resulting point-lift authority carried structured `x != 0`; both open and closed predicates naming eliminated `y` were refused as inexpressible at the target |
| **v0.11 mapped-predicate composition** | **PASS, positive plus refusal controls** | Real Singular verified the translation `x -> x+1` before the same section. `x+1 != 0` rewrote with the inverse map to `x != 0` and crossed; stale authority, a bare authored flag, and eliminated-coordinate controls remained refused |
| **v0.12 predicate-pullback composition** | **PASS, positive plus refusal controls** | The real Singular section assay pulled `x != 0` through a same-coordinate restriction and back through the checked elimination projection before reusing the section lift. Unspecified polynomial maps, unchecked projections, and characteristic-mismatched identity maps remained refused |
| **v0.13 finite point-lift cover** | **PASS, positive plus refusal controls** | Real Singular checked the cusp normalization with `u=y/x` on `x!=0` and fallback `u=0` on `x=0`. The fallback correctly required a radical witness (`y^2`, not `y`, lies in the augmented ideal). The persisted cover unlocked retained `NONZERO` predicate transport without minting exact contraction; a false fallback was refused |

### The reviews found the mathematics; the runs found the tool

Worth stating because it corrects a complacency this document used to carry.
For five live runs the score was **nine interaction defects to zero kernel
errors**, and I read that as the mathematics being settled. It was not — it was
nobody attacking it. An external review doing actual mathematics against the
table found two false licences in an afternoon (a nodal cubic and a
`p`-torsion example), both confirmed.

So the two channels find different things and neither substitutes for the
other. Live runs find what the tool does to a working user. Adversarial
mathematics finds what the table licenses. **Run both.**

Full results in `portage-depot/testing/`, each with its pass condition written
*before* the run.

**T5 is the one to read if you read one.** It pointed the tool at a border-rank
/ SOS campaign that had never heard of it: **zero false positives**, and the
checker escalated a finding to `UNSOUND_CONCLUSION` by noticing that a
refereed bound recorded elsewhere in the graph contradicted what the inference
would license. That reductio fell out of the fold. **The five edge types
survived foreign mathematics** — contrary to both my prediction and the
external review's, border rank did *not* break the ontology. Everything
*around* the types is what didn't fit.

### Where things are, physically

```
dev/
  grand-portage/            THE TOOL, private. github.com/wstrinz/
                            grand-portage-workspace
  grand-portage-public/     the public mirror, pushed to
                            github.com/wstrinz/grandportage (Apache-2.0).
                            Sync = copy grandportage/ tests/ fixtures/ docs/
                            DESIGN.md README.md REVIEW.md. Root-level files do
                            NOT sync, which is why DESIGN_DIRECTION.md and this
                            file stay private.
  portage-depot/            campaigns + testing evidence. Local only, no remote.
    campaigns/gamma-delta4/   the T1 run. Typing defects LEFT UNREPAIRED --
                              that graph is the evidence.
    campaigns/lsem-census/    the sustained run. See below.
    testing/                  T3/T4/T5 conditions + results, T1 runbook
    campaigns/jc2-chartmap/   the chart-map lead. NEXT: the GGV1 Prop 8.3
                              task extends this graph, which already carries
                              M1_G4, the P_GAMMA partition and INF_G4_HOLE_V2
    campaigns/borderrank/     S2, finished and green
    campaigns/toric-phases/   L1, finished. Refuted its own premise, usefully
    LANES.md                  candidate domains not yet started
    tools/wire_topcom.sh      TOPCOM is apt-installed as `topcom-*`; Sage wants
                              the bare names. Run once per fresh environment
    math-stuff/               one shared submodule, pinned e145e8e
  math-stuff/               THE RESEARCH REPO. READ-ONLY, always.
```

**Anything under a syncing path names no live research domain, on purpose.**
Code comments and test docstrings say "a live campaign" where they mean the
identifiability census, because the census is unpublished and its later
sessions are aimed at results worth first arrival on. Every design lesson
survives the generalisation; only the domain pointer is dropped.

The scrub is done **in this repo, not in the mirror**, so a sync stays a plain
copy. A sync that needs a manual scrub step is a step whose correctness depends
on someone remembering, which is the exact defect class §7 of REVIEW.md
tracks. If you write a new comment citing a campaign, write it generic here —
do not write it specific and plan to strip it later.

The public/private split is about DOMAIN, not about candour. Findings against
the tool itself stay fully specific in public: that is the point of the file.

### THE CENSUS IS SEALED. Do not write to it.

**`campaigns/lsem-census/.portage/` must not be written to before 2026-08-03.**
It is the subject of L3, the cold-return experiment, and its prose and scripts
are moved to `.sealed/`. Protocol and fixed grading criteria:
`portage-depot/testing/L3-PROTOCOL.md`, written before the run.

L3 gates the main JC(2) persistent investigation on three conditions: two
consecutive live sessions with no blocking tool defect, `portage_declare`
working end to end in a real campaign, and the cold return measured. Tool
changes during the gap are expected and are part of the test.

Historical status before W8 (retained to explain why W7 mattered):

**Gate status after W6 and W7: one of the two, not two.** W6 passed its own
clauses but ran with the **hook inert**, which it could not detect — so it
tested the checker and the verifiers and left the enforcement layer untouched.
It is recorded as *half*, and deliberately not counted. **W7 is the first
genuinely clean session**: enforcement confirmed live before any work, ten
defects, none blocking, twenty-two verdicts and none incorrect.

So **one more clean run with enforcement live closes this condition.** Both
runs declared end to end through `gp declare`, which retires the second
condition; only the cold return remains after that.

**Current gate status after W10: the consecutive-live-session condition is
closed.** W8 found a blocking verifier defect after W7, so consecutiveness
reset. W9 then proved the Codex structured-hook path, cleared one sparse
RETRACT, completed three real constructors, and hand-checked seven correct
verdicts. W10 immediately followed on the same build: Claude Opus 5 received
the automatic exit-2/stderr hook refusal, cleared it with a sparse RETRACT,
completed saturation, elimination and decomposition, recorded 30 correct
verdicts, and finished with plain `gp check` at exit 0 and no findings. Frozen
evidence is in `portage-depot/testing/W9-PASS-CONDITION.md`,
`portage-depot/campaigns/w9-two-component-curve/`,
`portage-depot/testing/W10-PASS-CONDITION.md`, and
`portage-depot/campaigns/w10-three-component-curve/`.

No Grand Portage code changed during either author session. The W10 follow-up
repair happened only after the frozen pass was complete, so it does not rewrite
the W9/W10 measurement. End-to-end declaration is already established. **Only
the sealed cold return remains.**

### The sustained run, now sealed

`campaigns/lsem-census` — generic identifiability of linear structural equation
models on small mixed graphs, via Macaulay2's `GraphicalModels`. A **census
rather than a conjecture**, so sessions end when a case finishes instead of
when someone gets stuck, and cases share models so the graph accumulates.

This is the first test of the claim the whole design rests on: *after three
weeks the graph is the state*. Every previous run was a single bounded task.

**The measurement that matters more than the mathematics:** do three or four
cases, let a week pass, return cold with no notes outside `.portage/` and no
scrollback, and time how long until productive. If a returning *human* cannot
resume from the graph, a returning agent certainly cannot.

### `gp migrate` — read this before bumping a required field

Required fields break existing graphs. That bill came due all at once:
`witness_kind` and the `ladder` vocabulary stopped **three live campaign logs**
from folding, including T1's own output.

`gp migrate` fills them with the **ignorance value** — `UNKNOWN`, `ASSERTED`.
The no-silent-defaults principle survives because those are not guesses; they
are true, the claim having been recorded before anyone was asked. Both report
as debt, so migrating makes the graph *louder*.

It **refuses to touch a field whose value is wrong rather than missing** and
exits nonzero. The T5 graph still does not fold for exactly this reason: four
`ladder` values need a human to decide whether they belong in `established_by`,
`caveat`, or are genuine strength claims.

**Candidate 16th design invariant: every required field ships with a migration
that fills the ignorance value.**

**The recurring shape, SEVEN instances now:** a premise that determines transport
and is taken on the author's word. Certificates (pre-v0.2), `identity_origin`
(pre-v0.3), `kind` (pre-v0.3.1), `ladder` (pre-v0.3.2, found by T5 when a
foreign campaign filled it with seven values and no overlap with the five it
declares), `established_by` (pre-v0.4), literal **`V(src) ⊆ V(dst)`** itself
(pre-v0.4.1), and the **mapped-vs-literal presentation of an EQUIVALENCE**
(pre-v0.4.2). Each was found by someone using the field or exploiting the
blind spot, never by review.

**The sixth exposed the deepest unchecked premise.** Before verification,
L1 could type a flop as an `EQUIVALENCE` even though neither variety contains
the other, and the result *"yields a false conclusion reported clean behind
one prose-dischargeable DEBT"* with *"nothing in the tool [that] would have
stopped me"*. `RESTRICTION` matches a flop on every clause except that one.

That repair is complete: models carry their ideals, literal containment is
checked by reducing `I(dst)` modulo `I(src)`, and the exact identity condition
`LHS − RHS ∈ I(dst)` is separately decided by the identity verifier. Computed
verdicts beat declarations everywhere they disagree.

**The seventh was the ontology overgeneralising its own repair.** W10 supplied
a mapped involution with a real inverse between two isomorphic varieties that
neither literally contains the other. The store accepted plausible inert field
names, and the verifier asked both the right mapped question and the wrong
literal one. The repair gives mapped EQUIVALENCE edges exact `forward` and
`inverse` substitution fields, refuses `maps`/`inverse_maps`, verifies both
ideal pullbacks and both inverse compositions, and skips literal containment.
The Lean theorem proves that witness transport does not imply either inclusion.

**The first post-W11 audit found that the surface repair was not yet the whole
repair.** Partial maps could fold and an `UNVERIFIED` result still licensed
transport; `forward` was implemented as the polynomial pullback despite being
documented as the source-to-target point map; non-string substitutions could
abort verification; a string-valued `ring_iso` was truthy; and a maps-only
negative verdict could condemn an equivalence that never declared a ring
isomorphism. The hardened path now requires exact variable coverage and
non-blank string expressions, requires a real boolean flag, pins point-forward
orientation with a non-involutive translation in both Lean and live Singular,
and fails closed: structured maps license IDENTITY transport only after
`VERIFIED`. Cited legacy edges without structured maps remain readable, but a
bare flag or point-level converse opens nothing. Refusals on mapped edges now
direct the author to verification, its recorded blocker, or replacement maps.

**THE REPAIR RULE, and it is the best general principle in this corpus:** make
it derivable, make it checkable, or make it compose with something already
checked — never "try harder to fill it in correctly." This belongs in
`DESIGN.md`'s design invariants and is currently only here.

**The fifth instance is the one to learn from, because it is a mutation.** The
first four were fields whose VALUE was taken on the author's word. The fifth
was a field whose ABSENCE switched off the check on a neighbour: every key in
`IMPOSSIBLE_EVIDENCE` matches on `established_by`, so omitting it meant the
pair evaluated was `(None, "exact-checked")`, which is in no table and
contradicts nothing. Optionality is not neutral when another rule keys on it.

**AND THE REPAIR IS STILL INCOMPLETE, so this is where to look next.**
`exact-checked` now forces you to say `RAN`, and `RAN` is the only value that
survives against it — but nothing requires a run ARTIFACT. You can still write
`established_by: RAN, ladder: exact-checked` with no evidence anywhere. That is
the honour system with one more word on it. The rule above says derivable *or*
checkable; what shipped is checkable-against-a-neighbour, which is weaker.
Deriving the rung from an artifact needs the run/artifact layer, deferred from
T5 and still deferred.

### What v0.2 changed, and why it is not a feature release

An external review (GPT) plus a working pass found **eight defects, seven of
them inside the parts the project advertises as its guarantees** rather than in
the mathematics. All are fixed; suite went 171 → 251 checks.

| where | was |
|---|---|
| `kernel` IDENTITY row | licensed `x = 0` escaping `V(x)` to the whole line; and lifting `p·x = 0` out of char `p` |
| `kernel` EQUIVALENCE | licensed IDENTITY on the strength of a **point**-level converse; `V(x²)` vs `V(x)` refutes it |
| `cas` boundary | `body` and declaration expressions went to Singular unvalidated — **the exact `poly g0 = ...` defect was rebuildable through the module claiming "there is no string path to a solver"** |
| `cas` verdicts | nonzero exits outside three codes read as `OK`; `ABORTED` minted a model and a semantic edge |
| `check` witness | `witness` was documented as evidence **against** an equivalence and accepted as documentation **for** one |
| `check` taint | one pass, so second-generation taint was invisible — and that is the generation nobody inspects, because the step producing it is clean |
| `store` certificates | a graph event could silently redefine a built-in, changing the field-scope of every emptiness citing it |
| `hook` baseline | keyed by a finding id that is stable by construction, so an acceptance outlived the meaning it was given for |

**The lesson worth carrying:** a green mutation suite tests *reachability*, not
*truth*. It asks "does editing this field change a verdict?" and presupposes the
verdicts are right. `test_identity_transport_turns_on_the_map_and_nothing_else`
asserted an unsound cell as its oracle and 171 checks agreed with it — **the
test's name was the false claim.** Gate 0 (`tests/test_cell_ledger.py`) is the
missing half: one row per cell, each with a proof or a counterexample.

**New concept: `identity_origin`.** An `IDENTITY` claim must say where its
rewriting is valid — `AMBIENT` (holds before this model's equations, travels
both ways), `DERIVED` (follows from them, restricts only), or `UNKNOWN`. Blank
raises at fold time. `UNKNOWN` is the `UNTYPED` bargain one level down: the
honest answer is always available, which is what makes the field requirable.
Unlike `UNTYPED` it has a **mechanical** discharge — `cas_classify_identity`
reduces `LHS − RHS` and answers `AMBIENT` / `DERIVED` / `FALSE_AT_MODEL`, so the
tool names the computation instead of asking the author to introspect.

The retrodiction gates reproduce **identically** — same findings, same clean
inferences — but every `IDENTITY` verdict now rests on a stated reason instead
of a coincidence. `CL-KSYZ-ID` was confirmed `AMBIENT` by re-running
`divisor_syzygy.py` (7/7, C3 residual 0 by symbolic expansion).

---

## 2. Where to start, by what you are doing

| you want to… | do this |
|---|---|
| understand the design | `DESIGN.md`, then `REVIEW.md` (where it is weakest) |
| review / critique it | `REVIEW.md` — written as an attack brief, not a tour |
| know what to run next | `TESTPLAN.md` — 7 tests, pass conditions declared in advance |
| see how it behaves in real use | `docs/first-run/` — the user's own report, the maths, the graph |
| see what an audit found | `docs/first-run/T2-SYNTHESIS.md` — **start here if you only read one thing** |
| run the blind test (T1) | `cd C:\Users\wstri\dev\gamma-delta4 && claude` — see §6 |
| work on the tool | `cd C:\Users\wstri\dev\grand-portage && python -m pytest` (<!--checks-->1789<!--/checks--> checks, ~300 s on the current development machine) |

---

## 3. Where things live

```
C:\Users\wstri\dev\
  grand-portage\    THE TOOL.  git@github.com:wstrinz/grand-portage.git (PRIVATE)
                    HEAD 0d24d35, clean, pushed.  171 checks green.
                    Installed editable (`pip install -e .`), so `gp` is on PATH
                    and edits take effect everywhere immediately.
                    Two commands: `gp` and `gport`.  USE `gport` IN POWERSHELL
                    -- `gp` is a built-in alias for Get-ItemProperty and the
                    alias wins.

  grand-portage\lean\   THE SHADOW FORMALISATION.  Lean 4, Mathlib-FREE, so
                    `lake build` is seconds.  Not authoritative: its job is to
                    try to break the ontology, not to bless it.  Does not sync
                    to the public mirror (the sync copies an enumerated list).

                    It has already taken four transport gates apart, and none
                    was the shape it looked:

                      identity_origin       a COROLLARY -- contravariance from
                                            the zero ideal, true in any ring
                      coefficients_in_base  a TYPING ARTIFACT.  The formal
                                            version could not SEE the gate,
                                            because `f g : R` puts
                                            expressibility in the type -- and
                                            that absence is what proved it is
                                            an artifact of claims being strings
                      ring_iso              CARRIES and REFLECTS, decomposed
                                            into four checks a CAS can run
                      integral              PARTIALITY -- is the map defined

                    A SECOND CLASS, ALSO WITH TWO MEMBERS, and this one
                    predicts where to look next: AN ARGUMENT CORRECT OVER AN
                    ALGEBRAICALLY CLOSED FIELD, APPLIED BY A TOOL THAT WORKS
                    OVER Q.

                      IMAGE_CLOSURE  licensed on density, which concludes about
                                     points while the claim is about an ideal
                      exhaustiveness `intersect(I(B_i)) subset rad(I(parent))`
                                     is equivalent to the covering only by the
                                     NULLSTELLENSATZ. So the test PASSING is
                                     sound over any field, and the test FAILING
                                     says nothing over Q -- the parent may have
                                     no rational points, in which case the
                                     branches cover it vacuously and
                                     NOT_EXHAUSTIVE was calling a sound case
                                     analysis broken at UNSOUND_PREMISE.

                    Both were found by writing the statement down precisely
                    enough to be WRONG. Neither was found by review and neither
                    by a live run. When looking for the third, ask of any
                    verifier: what does its answer mean over a field that is
                    not algebraically closed, and does the message claim more?

                    THE TYPING-ARTIFACT CLASS NOW HAS TWO MEMBERS, which is
                    the first evidence that it is a class and not one oddity.
                    `ImageClosure.lean` found IMAGE_CLOSURE/ALONG/IDENTITY
                    licensed on DENSITY -- wrong twice over, since a set is
                    dense in its own closure by definition, and the argument
                    concludes about POINTS while an IDENTITY here is ideal
                    membership. The honest argument is the elimination theorem,
                    and what it needs is EXPRESSIBILITY: exactly the same
                    string-vs-term condition as `coefficients_in_base`. Not a
                    fifth gate -- `_MAP_POLYNOMIAL` stays, and expressibility
                    is checked (INEXPRESSIBLE-CONCLUSION) rather than gated,
                    for the same reason the other one is.

                    What it has caught: a bad counterexample of mine, a wrong
                    conjecture of mine, a mislabelling in its own file, a
                    sequential-substitution bug in `verify.ring_iso`, the
                    SPECIALIZATION non-inclusion, the RESTRICTION reading
                    (same ideal, not the localized algebra), and this one.  None of them "the table is
                    correct".  The method is: state what a gate MEANS
                    precisely enough to be wrong, then write the Python
                    verifier against that statement rather than an intuition.

  portage-depot\    Workspace where the FIRST RUN happened.  Local only, no remote.
                    HEAD 9d42f49, clean.  Has math-stuff as a pinned submodule.
                    Contains BRIEF.md and FINDINGS.md — see the T1 warning in §6.

  gamma-delta4\     STAGED AND UNTOUCHED: the blind run (T1).  Local only.
                    HEAD 195d9c5, clean.  See §6.

  math-stuff\       THE RESEARCH REPO.  READ-ONLY as far as this project is
                    concerned.  Nothing here has ever written to it and nothing
                    should.  Currently at a83b19f on branch
                    claude/d2-jacobian-counterexamples-sgp9in.
```

**Submodule pins.** `portage-depot` and `gamma-delta4` both pin `math-stuff` at
`86d8fb0`, deliberately: the campaign graph quotes that repo verbatim and those
quotes are only true against one commit. `math-stuff` has since advanced twice
(`0dd5f71 → 86d8fb0 → a83b19f`). The only cited file that changed is
`F2_TOWER.md`, and the change is a typo fix (`(7,2)` → `(7\5,2)`). **The
citations still hold — this has been checked, do not re-derive it.** Advancing a
pin is a decision, not a sync.

---

## 4. State

**Built and gated.** Kernel, store, checker, discharge, CAS boundary, MCP
server, enforcement hook, verifier. <!--checks-->1789<!--/checks--> checks,
live against Singular 4.2.1 via WSL. Two domains of retrodiction (JC(2) and
matroid realizability) against answer keys pinned before this code existed,
reproducing 4+6 flags with zero false positives and 15 clean positive controls.

### The verifier layer, as of 2026-07-29

Three verifiers a week ago, **seven now**, and all four new ones were wired up
over 27–28 July. `gp verify` runs every one that applies and records a `verdict`
event; `gp check` reads the verdicts and **the verdict beats the declaration**
everywhere it disagrees.

| verifier | decides | verdicts |
|---|---|---|
| `containment` | literal inclusion-style `V(src) ⊆ V(dst)`, by reduction; mapped equivalences are skipped | VERIFIED / NOT_BY_IDEAL |
| `identity` | the rewriting — **and mints cofactors** for a DERIVED one | AMBIENT / DERIVED / REFUTED |
| `unit_ideal` | an EMPTY's certificate, by expansion | VERIFIED / NOT_UNIT |
| `ring_iso` | a mapped EQUIVALENCE's two ideal pullbacks and two inverse compositions | VERIFIED / NOT_AN_ISOMORPHISM |
| `point_witness` | a NONEMPTY's `witness_point`, by substitution | VERIFIED / NOT_A_POINT |
| `partition_exhaustiveness` | **that the cases are all the cases** | VERIFIED / NOT_GEOMETRICALLY_EXHAUSTIVE |
| `operation_output` | that a constructor produced what it claims | VERIFIED / NOT_THE_STATED_OUTPUT |

Two things a fresh session should know before trusting any of it:

- **A certificate is now an artifact, not a word.** A verified membership hands
  back the cofactors, so `g = Σ bᵢfᵢ` can be re-expanded by a checker that
  shares no code path with the search. That is the bridge to a proof assistant:
  Lean checks a polynomial identity and should never run a Gröbner engine.
- **`operation_output` checks one direction only**, and says so. "Nothing was
  invented" is cheap and is the direction that makes EMPTY unsound. "Nothing
  was missed" is as hard as recomputing the answer and is **not** checked. A
  bounded saturation witness search that finds no exponent now returns
  `UNVERIFIED`; the search bound is never presented as non-membership.

`operations.py` has a fourth constructor, `decompose`, over `facstd` — the only
decomposition reachable inside the CAS boundary, since `primdecGTZ`,
`minAssGTZ` and `radical` all live in `primdec.lib`. It emits a partition whose
branches were *minted* rather than typed, and whose completeness premise a
verifier re-decides. **Anything a constructor mints carries its own ideal**,
which is the whole of the answer to "should models be required to carry
algebra": no requirement, no migration, and the checkable fraction of a
campaign rises as it uses constructors.

**Tested in anger repeatedly**, and that is where every structural change comes
from — see the table in §1. `docs/first-run/` is the one to read: a real agent
doing real open research, which produced genuine mathematics and a very good
bug report. Five campaigns now exist in `portage-depot/campaigns/`.

**Audited twice.** `docs/first-run/T2-SYNTHESIS.md` — four independent
auditors, four lenses, and **the audit FAILED its declared pass condition on
edge type.** Then an external prior-art review found two false licences in the
transport table itself, both confirmed and both fixed.

**Three gates now guard the classes of defect that keep recurring:**

| gate | what it prevents | how it was earned |
|---|---|---|
| **cell ledger** | a licensed cell with no argument behind it | 171 green checks once agreed with an unsound oracle |
| **GATE 2** (`test_surface_smoke`) | a construct correct everywhere except in being *reachable* | three constructs in a row crashed `gp check` on first live contact |
| **GATE 3** | a message naming a command that does not exist | `gp verify` was promised in two check rules for two releases and did not exist |

GATE 2 and GATE 3 are complements and neither subsumes the other. GATE 2 asks
whether every surface survives every event kind; GATE 3 asks whether every
surface we *name* is real. **Neither asks whether a capability has a surface at
all**, which is how `verify.py` shipped twice while being unreachable from
every user-facing path. If you add a fourth gate, that is the gap.

---

## 5. THE OPEN DECISIONS — these need a human

### D1. Gap B — how to express a case-split edge — **DECIDED AND BUILT (v0.3)**

**Resolved by evidence rather than by choosing.** T1 produced the same defect a
second time, independently: a blind agent typed a γ=4 branch as a total
containment, and its `EMPTY` result landed on the whole parent while its own
prose said "branch". An auditor who had never seen this section picked option 2
— branch models — on the merits and specified it.

Built as a `partition` event naming a parent, its branches, and an
**exhaustiveness claim that must exist in the graph** rather than in a note.
Plus `kernel.transport_over_partition`, because **a case split is not
transport**: per-leg auditing correctly refuses each branch alone (`EMPTY` does
not travel `ALONG` a `NECESSARY_CONDITION`), so it needed a second inference
rule beside the table, cited via `via_partition`.

The original text is kept below because the reasoning is still the record of
why it was left open.

---

*(original, superseded)*

Two independent auditors found that `GE7`/`GE8`/`GE9` are **case branches, not
relaxations**. γ is a function of the counterexample, so `V(src) ⊆ V(dst)` is
false as a total statement — only `V(REDUCED) ∩ {γ=k} ⊆ V(GCHART_Gk)` holds.
The type system has no vocabulary for that, so a branch gets typed as a total
containment and licenses transports that are false off-branch.

**This is the most important open question in the project.** Three candidate
designs, materially different:

1. a `holds_on:` branch condition on the edge
2. model each branch as its own source model (`REDUCED_G3`, `REDUCED_G2`, …)
3. a first-class case-partition construct

Option 3 is closest to what the original whetstone notes pinned as
`MISS-C0-PARTITION` and explicitly put out of scope. **Do not pick one
unilaterally.**

### D2. Should T1 run before or after fixing B? — **DECIDED: before.**

Argument for **before**: if a blind agent hits the same wall independently, that
confirms the gap is systematic rather than one agent's slip. That is evidence
you can only collect once, and fixing B first destroys it.
Argument for **after**: T1 then tests a tool that can express the truth.

**Resolved in the v0.2 session, and the GPT review did not change it.** The
distinction that settled it: v0.2's fixes split into *what the tool licenses*
(table cells, witness polarity) and *boundary/bookkeeping* (CAS validation,
taint, baseline). The second class is invisible to an agent doing honest
modelling, so fixing it costs T1 nothing. The first class had to be fixed
because T1 would otherwise audit against a broken oracle. **Gap B is in
neither** — it is a missing expressive feature, and leaving it open is what
makes T1 informative about it.

**So: T1 is now unblocked and is the next thing to run.**

### D4. Should IDENTITY transport become edge-relative? *(new, not urgent)*

`AMBIENT` is *sufficient* but not *necessary* for a rewriting to survive
widening. The exact condition is `LHS − RHS ∈ I(dst)` — edge-relative — and a
`DERIVED` identity satisfies it whenever it follows from equations the target
keeps. Verified: `x = 0` is `DERIVED` at `V(x,y)` and reduces to 0 at `V(x)`.

**Registered as a deliberate conservatism**, not fixed, because the exact test
needs the target's ideal and **a model in this system carries `desc`, `cite`,
`chart`, `universe`, `declares`, `touches`, `reads` — it is a description, not
an object with equations.** Requiring machine-readable ideals on every model
changes what a model *is*.

Cost so far: **zero**. Two `IDENTITY` claims exist across the whole corpus, both
`AMBIENT`, both licensed; none at all in the matroid domain, the γ-window graph
or the live first-run campaign.

**The upgrade path, when a real false refusal appears:** put the evidence on the
**inference**, not the model — an inference declares it checked the difference
lies in the target's ideal, with the computation attached, and that unlocks the
one cell. Same shape as `certificate` on an `EMPTY` claim. Do not reach for it
before a campaign actually hits the refusal; the point of registering the
conservatism is that it becomes visible when it starts to bite.

### D3. `portage_suggest_edge` — build it or not

The first run's cost split was ~2/3 genuine modelling, 1/3 transcription, and
the transcription was always *"say again what you said for the neighbouring
edge, with one field changed."* So the fix is a **sibling-edge diff**, not
type-guessing.

**But it may destroy the tool's best property.** The single best finding of the
first run — a determinant of −2 showing GGV3's "automorphism" is a 2-fold cover,
and thence the congruence structure GGV3 leaves unexplained — came from having
to fill in `map_kind` *from scratch*. A diff that pre-fills it means that
finding does not happen. `TESTPLAN.md` T6 says: measure both sides or do not
build it.

---

## 6. What is staged and ready: T1, the blind run

`C:\Users\wstri\dev\gamma-delta4\` — clean directory, own pinned submodule,
campaign graph and baseline carried forward, MCP + hook wired, `TASK.md` and
nothing else.

**To run it:** `cd C:\Users\wstri\dev\gamma-delta4` then `claude`. MCP servers
register at session start, so this only works from that directory — starting
anywhere else points `GP_ROOT` at the wrong campaign.

**The task:** derive Δ′₄, the reduced polygon for the γ=4 chart, turning the
window cap α from an obligation into a number. Real, bounded, and the
campaign's own named discharge for `GE10`.

### Preserving blindness — this is the whole point of T1

The first run's agent had read a brief naming mislabelling as the worst failure
mode and blessing `UNTYPED`. It then avoided mislabelling and used `UNTYPED`
correctly. **That is an observer effect and the finding is close to worthless.**

So:

- **Do not let the T1 agent read** `BRIEF.md`, `FINDINGS.md`, `TESTPLAN.md`,
  `REVIEW.md`, `HANDOFF.md` or `T2-*`. They live in `grand-portage\docs\` and
  `portage-depot\`. `gamma-delta4` is deliberately clean of all of them.
- **Do not tell it anything is being tested.** Give it `TASK.md` and the tools.
- **The α = 4^(3−γ) trap is left in on purpose.** It fits both known values and
  hands you γ=4 for free. `TASK.md` does *not* warn against it — an earlier
  draft did and that was removed, because warning in prose tests only whether an
  agent can follow an instruction. The warning lives in the **graph**, as
  `GI-G4-CAP-EXTRAPOLATION` and its baseline reason, reachable through
  `portage_check`.

So T1 also asks: **does a standing obligation reach someone who was never told
it exists?**

**Prediction, on the record before the run:** it will pick a
defensible-but-wrong type at least once, most likely `NECESSARY_CONDITION` where
the truth is `IMAGE_CLOSURE` — "this step drops conditions" is the easiest story
to tell about almost any step.

---

## 7. Open findings, prioritized

Full detail in `docs/first-run/T2-SYNTHESIS.md`.

| # | gap | status |
|---|---|---|
| **A** | **the certificate is never validated against the computation** | still open — but see below, v0.2 built the *pattern* for it |
| **B** | **no vocabulary for a case-split edge** | needs D1 |
| **C** | an inference can attach to a **proxy edge** — nothing checks the path is the step `asserted` describes | not built |
| **D** | **no retraction mechanism** — a wrong edge cannot be corrected without hand-editing an append-only log | not built |
| **E** | `ev: "note"` **bypasses the checker entirely** | not built |

**A is a soundness hole and should probably be fixed before anything else.**
The evidence for it is that *I* got it wrong: `GC-A2-KILL` in this repo's own
fixture declares `UNIT_IDEAL_CERT` for an ideal where `1 ∉ I` (verified: basis
size 19, exhibited point satisfies every generator). `a2_certificate()` exhibits
nilpotency, and its own docstring says it is "NOT a scalar syzygy". The
certificate is the one field `derive_scope` trusts blindly to mint
field-independence.

**The cheap fix:** `cas_ideal_is_unit` already knows whether the basis came back
`1`, so the checker can cross-reference any `UNIT_IDEAL_CERT` claim against a
recorded computation, and flag claims whose certificate has no computation
behind it at all. That would have caught mine.

**v0.2 built this pattern once already, for a different field.**
`cas_classify_identity` decides `identity_origin` by computation instead of
asking for it, and the design generalises directly: a tool that *answers* the
question, a field the author still has to *declare*, and a checker that can tell
a declaration with a computation behind it from one without. Deliberately kept
separate — a tool that both decides a field and writes it leaves nobody holding
the claim.

Certificates are the harder instance and that is the only reason they are not
done: *"does this computation support this certificate kind?"* needs
interpretation, whereas origin classification is a normal-form reduction with a
three-way answer and no room to argue. **Do A next if T1 is blocked for any
reason** — the shape is now proven.

**Known campaign-level errors** (in `portage-depot`'s graph, not the tool):
`GE10` drawn backwards; `E-G3_ELIM_KILL` should be `NECESSARY_CONDITION` not
`IMAGE_CLOSURE`; `GE9`'s witness is wrong and a correct one is already in the
graph unused; `GC-A5-DERIVED` graded `exact-checked` for a slope the producing
code labels FITTED; 10 of the headline "30/30 published data points" are
vacuous by construction. **None of these has been fixed** — see gap D for why
that is awkward.

---

## 8. Gotchas that will bite you

- **`python - <<'PY'` heredocs in the Bash tool mangle backslash escapes.**
  `\n` inside a patch string becomes a real newline and silently corrupts source
  files, or silently fails to match and the patch never applies. This happened
  three times. **Use the Write/Edit tools for code, not shell heredocs.**
- **A POSIX path expanded inside a `python -c "..."` string is not MSYS-path-
  converted** (only standalone arguments are), so it reaches Windows Python
  unresolvable. The hook then finds no graph and **correctly fails open** — a
  false pass that looks like a fix. Use `cygpath -w`, or pass paths as argv.
- **Seed the baseline before wiring the hook.** On a graph with existing
  findings the hook blocks *every* tool call. `gp accept -m "why"` first. The
  first block now names this, but it is still the day-one trap.
- **The graph is append-only and conflicting redeclaration is a hard error.**
  There is no retraction mechanism (gap D). You cannot "just fix" an edge.
- **`math-stuff` is read-only.** It is a live research repo with its own
  103-checker suite. Nothing here has ever written to it.
- **Subagents inherit the parent session's MCP tools**, which is why T1 can be
  orchestrated from a session started in `gamma-delta4` — and cannot from
  anywhere else.

---

## 9. What not to do

- Do not advance a submodule pin without re-checking the graph's citations.
- Do not fix gap B unilaterally — see D1.
- Do not let the T1 agent see the meta-documents.
- Do not treat `docs/first-run/FINDINGS.md` as neutral evidence; it argues for
  its own edges, which is why the T2 auditors were barred from it.
- Do not add a detection to the coverage rule without removing one from the
  known-misses list. That discipline is inherited from whetstone and it is what
  keeps the limitations honest.
- Do not claim this finds equations. It routes attention to where one is
  missing. Every actual advance in the parent campaign was an equation.

---

## 2026-08-01 — aggregate JC H3 depth-6 replay gate

`experiments/jc_h3_source_depth6/replay_all.py` now composes the conditional
source seam, graded face extraction, complete finite template, ordered chain,
and boundary projection into one post-receipt ledger. Fast mode checks the
frozen welds in roughly five seconds and marks expensive graph authorities
deferred. Full mode rederives the five rows, verifies exact inclusion of 25
selected rows in the 147-row/78-variable template, replays all 25 ambient
substitutions, and checks both boundary equivalences; the measured run was 160
seconds. `--native-replay` separately ran all five native upstream checkers and
refused nine mutations in 55 seconds.

All modes retain aggregate graph effect `NONE` and terminate successfully at
`VERIFIED_TO_EXPLICIT_OPEN_OBLIGATION`. The first missing authority is still
`target_pair_to_normalized_laurent_root`; original-pair membership, reverse
lifting, coverage, H3, and verdict promotion remain refused. The coordinator
usage packet and two real review ledgers live beside the assay and under
`review/` respectively.

---

## 2026-08-01 — corrected R1--R7 promotion firewall and replay tiers

The coordinator correction at math-stuff `fb18749` is now frozen in
`r1_r7_seam_adapter.py`. Seven LF-normalized source bindings preserve the exact
distinctions the audit required: branch A is refuted in every gauge only under
its premises; pair positive-j is forced; Q positive-j remains open; and the
`(1,2)` point is actual nonzero only in the landed normalization. Ten named
mutations independently refuse every requested scope widening. The adapter has
graph effect `NONE` and runs no native checker unless explicitly requested.

Aggregate schema v2 exposes R5, R6, R7, `R6.Q_side_relocation`, and
`target_pair_to_normalized_laurent_root` as a typed open frontier. Old v1
ledgers migrate only through a visibly lossy record; no R1--R7 authority is
invented. `status_block.py` projects supported/not-supported authority between
one exact delimiter pair, is a no-op when delimiters are absent, refuses bad
boundaries, and reaches a fixed point. It does not edit any JC file.

The replay gate now has three authority tiers:

- `--preflight`: about 1.2s, bindings/digests/rung welds, no sparse decoding,
  verdict `PREFLIGHT_BINDINGS_ONLY`;
- `--seam`: about 3.9s without and 4.8s with live sibling bindings, identical
  verdict and licenses to the former fast gate;
- `--full`: the existing complete authority recomputation, most recently
  310.6s under machine load, including 242.7s in the full chain replay.

That full measurement reproduces the previously reported 255-second chain
signature; the seam chain is only 2.7s. Full replay or an equivalent path plus
load is therefore the evidence-backed explanation, although the earlier argv
was not preserved. An fsynced append-only JSONL journal now records each
completed stage independently of the atomic final ledger, and is explicitly
diagnostic-only. Real schema-v2 seam and full ledgers plus a generated status
projection are checked in under `review/`.

---

## 2026-08-01 — coordinator consumer and S4 scope assay

The first independent coordinator invocation produced
`review/jc-h3-depth6-fast-replay.json` and its diagnostic stage journal. It
reproduced the seam-tier authority boundary in 5.054 seconds: graph effect
`NONE`, conditional normalized-root-to-depth-6 authority only, and the same
five explicit open-frontier entries. The journal's `rss_mb: null` values
exposed a Windows-only diagnostic bug, not a semantic failure. `_rss_mb()` now
declares the 64-bit Windows process handle and `GetProcessMemoryInfo` call
types; the interrupted-journal test requires positive numeric samples.

`experiments/jc_h3_s4_scope/adapter.py` consumes the landed S4 point receipt as
a separate, bounded constructible-scope assay. Fixture construction executes
the native producer only on explicit request. Normal verification instead
decodes and checks frozen sparse bodies for the 952-term `C`, its exact 24-term
`p^2` coefficient `C2`, and the 12-term rank witness over
`K=QQ[t]/(15*t^3+1)`. It verifies one exact point on `C=C2=0`, records
`C=0,C2!=0` as `OPEN`, and treats the 24 failed seeds as bounded provenance
only. The structural two-piece cover has no union claim and graph effect is
`NONE`. This required no new kernel relation, claim kind, graph field, or
epoch change.

---

## 2026-08-01 — Lean-backed unilateral recurrence assay

The corrected JC adjoint receipt now drives a bounded
`parametric_recurrence_v1` experiment. GP independently decodes the frozen
padded five-by-two sparse operator matrices, reconstructs jumps exactly at
depths 7, 9, 11, and 13, verifies the zero tail from depth 14, and verifies
that `B_13` is nonzero. The current native producer independently passes
44/44 checks; the earlier packet's 43/43 count was stale, while its certificate
digest remains unchanged.

`lean/GrandPortage/ParametricRecurrence.lean` supplies the previously required
semantic interface without Mathlib. For finite constant-coefficient shift
operators padded to sufficient width, a unilateral sequence starting at `s`,
zero from `N`, and nonzero at `N-1` is annihilated exactly when every
coefficient below shift `N-s` vanishes. The live instance uses rational
operator coefficients acting faithfully on exact sparse matrices, `s=6`, and
`N=14`; hence the annihilator ideal is `(S^8)`, `S^7` fails, and no operator
with nonzero constant term can reconstruct backward.

The native assumptions P1--P5, S2, the pin, and H8 remain explicit. Cokernel
bases, straggler identities, additive values, geometric conclusions, source
membership, H3, and graph authority stay outside the adapter. The report also
does not adopt blanket minimality of `S-1` inside the final zero regimes. This
is a standalone evidence schema and does not change the package API, graph
format, kernel epoch, relation set, or claim kinds.

---

## 2026-08-01 — scoped depth-eight first-order fiber assay

The newer JC straggler/zero-block composition supersedes the earlier reading
of the depth-eight obstruction as merely a fixed `c7_4`, `c8_5=0` witness.
On the nine-relation locus, the exact zero-block equation solves `c7_4`
affinely in `c8_5`; the rotated combined cokernel has rank four, and the exact
L-valued `Omega_comb` is nonzero at the landed base witness. Since the scalar
does not vary with `c8_5`, the first-order incompatibility covers that base
witness's entire free fiber.

GP freezes this as `first_order_fiber_obstruction_v1`. The runtime verifies
the native and transitive bindings, exact L-coordinate nonvanishing, unit/rank
premises, and scope text. Lean proves that a nonzero base-only necessary scalar
excludes every point in the named fiber. A second Lean theorem records the
nonlinear consequence only under a supplied sound linearization map; this live
adapter deliberately does not instantiate it.

Accordingly the Galois conjugate, every other base direction, the full
12-dimensional survivor, nonlinear lifting, component exclusion, source
authority, H3, depth nine, and verdict promotion remain open or refused. The
checked report is `review/jc-h3-depth8-fiber-v1.json`; graph effect is `NONE`.

---

## 2026-08-01 — graph-bound S2 wall obstruction

The landed JC on-wall receipt proves the exact dead-row identity
`value_24 = OB - 45*c2_3*t*R*c8_9`. GP freezes the 502-term dead row and
499-term ambient obstruction, independently checks
`OB = value_24 + 45*c2_3*t*c8_9*R`, and compiles it through the existing
`localization_membership_v1` / `LOCALIZED_UNIT_IDEAL_CERT` authority path. A
real WSL/Singular run recorded a current verifier verdict and minted
`LOCAL_EMPTY` for the exact `R=0, OB!=0` dead-row consequence model.

The complete nine-body parent, the edge showing that this equation is its
necessary consequence, the complementary `R=OB=0` piece, component exclusion,
source membership, H3, and verdict promotion remain unmaterialized or refused.
No relation, claim kind, evidence schema, graph field, or kernel epoch was
added. The large sparse fixture did expose a general implementation defect:
membership targets, generators, and cofactors could reach Singular as Python
dictionary syntax. The CAS boundary now parses and canonically renders every
exact polynomial before emitting either membership program.

The focused wall/backend suite passes 26 checks in about 36 seconds. The full
non-live suite passes 1,392 checks with one skip and 40 live deselections in
188.44 seconds on the current development machine.

---

## 2026-08-02 — localized `b=0` compatibility class

The JC coordinator supplied a bounded rendezvous packet for the exact
materialized-depth locus `X_b : b=R=A=OB=0`, localized at `c2_3`, `p`, and
`det5`. GP now freezes and independently replays the five-row affine chart,
proves its determinant is the committed `det5`, reconstructs the 3,137-term
`Phi_b0_compat = det5^2 Lambda|det5-solve`, and checks that one power of
`det5` is insufficient. It then recomputes the degree-26 resultant and first
subresultant.

Two exact observations classify the element. In a nontrivial quadratic
quotient its image is a unit and therefore nonzero. In a nontrivial degree-14
quotient its image is zero while `det5`, the `OB` pivot, and the subresultant
coefficient remain invertible. Hence the source class is not a unit.
`lean/GrandPortage/RingElementClass.lean` proves precisely these reusable
semantic implications without assuming a richer algebra library.

The earned statement is only that `Phi_b0_compat` is **nonzero and nonunit** in
the declared localized materialized-depth ring. Despite the native enum name
`GENERIC_NONZERO_DIVISOR`, neither GP nor the native receipt proves
nonzerodivisor status. The witness is not promoted to a `K`-point or an
all-orders/source lift. The assay uses standalone
`localized_ring_element_class_v1` evidence and graph effect `NONE`; it adds no
graph relation, claim kind, field, or kernel epoch. Routine replay takes about
one minute because it recomputes the Cramer and subresultant determinants.

The subsequently landed native `compatibility_module/1` packet is bound to the
identical `Phi_b0_compat` digest. GP consumes its principal-compatibility-ideal
and fiber-semantics statements as frozen native premises, while retaining the
independently rederived Cramer and quotient checks as a distinct trust layer.
The native module replay passes 32/32. The final full non-live GP suite passes
1,406 checks with one skip and 40 live deselections in 302.04 seconds.

---

## 2026-08-02 — `b=0` free-plane exceptional-factor ledger

The native free-plane receipt landed as a complete finite object, so GP did
not need a new graph relation or claim. The new
`exceptional_factor_column_v1` assay freezes all 35 loaded coefficient rows
(31 distinct bodies), verifies that only `E321`, `VD`, and two depth-seven
rung values touch `(c7_4,c8_5)`, and matches all four exact coefficient hashes
from the native certificate.

Independent exact arithmetic recovers the ambient exceptional factors
`(b,Delta)`, their S2 contraction to `(b)`, and the unique `c8_5` column
`15*b*t^2`. The mutation controls explicitly show that wall-only `R=0` revives
that column and that omitting S2 revives `E321`; neither broader freeness claim
is licensed.

The sole on-`X_b` survivor is the depth-seven row-one rung solving `c9_7`.
Its `c7_4` coefficient is `-(3/2)*c2_3` and its march pivot is `10*t`, so the
correct reading is the reversible affine normalization
`c9_7 <-> c9_7+(3/2)*c2_3*c7_4`. It is a determination, not a compatibility
equation, and `c9_7` is absent from all eight downstream equations. Lean's
`PivotIndependent` theorem now formalizes why such a translation leaves the
downstream model unchanged.

The report is `review/jc-h3-b0-free-plane-v1.json`, has graph effect `NONE`,
and leaves the minimal depth-eight request open: six coefficients, namely the
`c8_5` and `c9_7` columns of `E[2,19]`, `E[3,20]`, and `E[4,22]` on `X_b`.
The final full non-live suite passes 1,419 checks with one skip and 40 live
deselections in 480.50 seconds on a contended development machine.

---

## 2026-08-02 — transported depth-eight affine fiber block

JC commit `033f63a` fulfilled the six-coefficient request and supplied the
invariant transported block. GP freezes all nine raw coefficient columns,
matches their native commitments, composes against the previously verified
`c9_7` pivot prerequisite, and independently checks the exact `3x2` block,
minors, left syzygy, and symbolic augmented determinant. The native replay
passes 40/40.

The block has constant rank two on the declared localization: `E[2,19]`
determines `c8_5`, `E[3,20]` determines transported `c7_4`, and the remaining
row contributes the symbolic compatibility `Psi8=a*r8_1+2*r8_3`. The native
chain-rule assembly includes earlier solved-coordinate sensitivities and is
explicitly labeled consumed frozen semantics; GP does not reconstruct it from
the six direct coefficients alone.

`lean/GrandPortage/AffineFiberBlock.lean` adds the reusable semantic contract:
a correctly characterized determined block is inhabited exactly on its
compatibility locus, and its solved coordinates are unique. The current
instance is standalone `affine_fiber_block_v1` evidence with graph effect
`NONE`. The next missing authority object is `r8`, the three boundary residuals
after earlier legal solves on `X_b`. Without it, `Psi8` is not an explicit
polynomial and no complete-fiber/source equivalence or sufficiency follows.
The final full non-live suite passes 1,434 checks with one skip and 40 live
deselections in 370.01 seconds.

---

## 2026-08-02 - explicit `Psi8` and constrained `Omega8` replay

The JC coordinator fulfilled the residual request after GP commit `20bd252`.
The landed sequence ends at math-stuff commit `b7abb3c` and supplies two exact
native handoff layers:

1. `f2_h3_b0_depth8_psi8_certificate.json` exports `r8_1` and `r8_3` and the
   709-term polynomial `Psi8 = c2_3*r8_1 + 2*r8_3`. It intentionally does not
   construct `r8_2`, because the verified left syzygy `(c2_3,0,2)` makes that
   coordinate irrelevant to the compatibility scalar. The fast checker passes
   22/22 in under one second and reports `DEPTH8_SCALAR_NONZERO_NONUNIT`.
2. `f2_h3_b0_psi8_constrained_pullback_certificate.json` substitutes the exact
   landed depth-6/7 block solve and clears only the already legal factor
   `5*c2_3^4*c3_5*t*det5^2`, producing a 4,123-term base polynomial `Omega8`.
   Its fast checker passes 18/18 and proves `Omega8` is a unit in the frozen
   degree-14 compatible witness algebra.

Both native replays were rerun successfully from this GP session immediately
before the adapter work began.

### Completed GP implementation loop

`experiments/jc_h3_b0_free_plane/depth8_residual_adapter.py` preserves the
native certificates as immutable external inputs and completes the requested
bounded replay:

1. it binds the prior depth-eight block report, decodes
   `r8_1` and `r8_3`, and independently recomputes the exact 709-term `Psi8`;
2. it verifies the residual-to-block compatibility identity and
   mutation-tests the syzygy scalars, sparse bodies, ring order, field pin,
   source digests, and missing-middle-coordinate rationale;
3. it replays the constrained fiber substitution and complete exceptional-factor
   ledger to obtain `Omega8`, without silently cancelling unit factors;
4. it independently checks the frozen quotient algebra and the coprimality/unit
   witness, with a mutation control for the witness polynomial and slice;
5. it emits `review/jc-h3-b0-depth8-psi8-omega8-v1.json` with graph effect
   `NONE`, reusing `affine_fiber_block_v1`. No relation, claim kind, graph
   field, or evidence schema was added.

The GP replay reconstructs the 709-term `Psi8` and 4,123-term `Omega8` term for
term. It audits and retains the exceptional content `c2_3^26*c3_5^2`, verifies
that the denominator clearing introduces no new inversion, rechecks the
degree-14 compatible quotient equations, and independently recomputes that
`gcd(Omega8,r_final)` has degree zero. The two native fast replays also pass
40/40 in aggregate. Fourteen focused GP tests include mutations of the syzygy
body, ring order, field pin, source digest, missing-middle rationale,
exceptional-factor policy, witness slice, and quotient modulus.
The final non-live gate passes 1,448 tests with one expected skip and 40 live
deselections in 396.39 seconds.

The semantic ceiling is exact and important: this can exclude the frozen
finite compatible witness and establish a necessary depth-eight scalar on the
constrained fiber. It cannot exclude a whole component of `Z(Phi) cap X_b`,
decide the off-slice zero locus of `Omega8`, prove complete source-fiber
equivalence or sufficiency, reach depth nine, or change H8, H3, or `(75,125)`.

`JC-COORDINATOR-NEXT-PACKET.md` is the stable coordinator rendezvous path. It
remains HOLD / NO NEW REQUEST because the replay exposed no smaller precise
missing native receipt. The next work is an internal decision about the
off-slice locus or a separately bounded component model, not a request to
repeat or widen the fulfilled residual computation.

## 2026-08-03 - scoped H8 premise propagation and first `frontier/v1`

The web review correctly identified the missing composition layer: accurate
`first_open_obligation` strings were still local report fields rather than a
global, scope-safe research frontier. `grandportage/frontier.py` now provides
that derived layer. Every item names a stable semantic ID, proposition,
premises, exact scope, blocked downstream work, superseding evidence, smallest
next artifact, estimated cost, and potential impact. Discharges are immutable
overlays. They apply only to enumerated scope IDs, and closed results propagate
only through explicit `exports_to_scopes`; the code deliberately performs no
geometric containment or assumption weakening.

The first bounded consumer is `experiments/jc_h3_frontier/adapter.py`. Its
frozen fixture binds the H8 schedule plus the depth-8, depth-9, and uniform
depths-10--15 P3/P4 receipts. Those receipts discharge the final named H8
transfer premise over the complete depth-8--15 range under P1--P5 and the pin,
with S2 retained on the S2-scoped degree-34 consumer. The derived projection
therefore changes H8 from `OPEN_PREMISE` to `DISCHARGED` and removes the H8
qualifier from the operator schedule and exact degree-34 depth-nine pairing.
Historical statuses remain present and fingerprinted.

The consumer also binds the exact `c7_9` source-family certificate. It marks
only the recorded codimension-five family closed by the unit `face(8,1)` and
keeps full `b=0` source exclusion open. Its next artifact is the ranked
pin-ablation result: for each relaxation of `c2_1`, `c2_2`, `c7_10`, then `b`
and `R`, record surviving guards, the exact identity or first defect term, and
the maximal licensed scope. The latest reviewed estimate for the load-bearing
replay is about 140 seconds and is machine-load sensitive. The math-stuff agent
owns that native lane; GP asks for no release gate and will consume its landed
receipt later.

The projection and checked-in compact review receipt have graph effect `NONE`.
No relation, claim kind, graph field, or evidence schema was added.

The LSEM cold return then completed in a separate context-free Codex task after
the precommitted 2026-08-03 seal date. It produced a strong semantic result:
correct settled/carried/open orientation before mutation, no unseal request,
one appropriately narrowed R3 algebraic-identifiability inference, zero final
findings, and preserved original history. The strict preregistered verdict is
`INCONCLUSIVE`, not PASS, because literal `portage_declare` was not exposed.
The equivalent `gp.exe declare` path needed three attempts: epoch-0 refusal,
then a failed global `--graph` redirect whose writer still targeted the default
graph, then success in an isolated epoch-1 root. This is exactly the useful
backward-compatibility/interface split the test was meant to expose. The
complete call ledger and belief corrections are in
`portage-depot/campaigns/lsem-census/L3-RETURN.md`; do not rewrite the result
after seeing it.

Verification for the GP change is green. Focused coverage includes the generic
frontier compiler, both independent native consumers, exact review
regeneration, declaration target selection, repeated-target refusal, and the
unchanged epoch-0 boundary. The five native receipt digests and verdicts match
without running the math-stuff release gate.

## 2026-08-03 - declaration targeting repair and second frontier consumer

The LSEM return separated one intentional compatibility boundary from two
current-path defects. Refusing epoch-1 events on an unversioned epoch-0 log is
correct and remains byte-preserving. What was wrong was that global `--graph`
selected a graph for every read surface while `gp declare` ignored it and
wrote through `--root`.

`store.append` now accepts one exact graph path in addition to its historical
campaign-root form. `cmd_declare` refuses repeated `--graph` values before it
reads stdin, sends a single selected path through the same transactional fold,
and prints the absolute destination on success. Four regressions pin explicit
sidecar selection, ambiguous-target refusal, unchanged epoch-0 refusal, and
root-graph byte preservation.

MCP already advertised `portage_declare`; the cold task missed it because its
Codex project root was `dev`, so the campaign's nested `.mcp.json` was not
loaded. The package now also installs literal `portage_declare` and
`portage-declare` console entry points. Both call the same CLI/store transaction
and accept `--root`, one `--graph`, and `--file` or stdin. This is a fallback
for task-host discovery, not a second writer implementation.

The depth-six generated status ledger is now the second independent consumer
of `frontier/v1`. `experiments/jc_h3_source_depth6/frontier_adapter.py` binds
the checked seam ledger digest and compiles R5, R6, R7, Q-side relocation, and
the parent normalized-root seam to stable semantic IDs. An explicit
`frontier_state: OPEN` preserves domain statuses such as
`CHECKED_PREMISE_BOUND` and `INFERRED_UNBOUND_75_125_IDENTIFICATION` without
teaching the generic compiler JC vocabulary. The parent seam retains its own
scope, all five items remain open, no discharge is invented, and graph effect
stays `NONE`. The older Markdown status block remains a compatibility surface;
`review/jc-h3-depth6-frontier-v1.json` is the compact current receipt.

The focused declaration/frontier/surface/architecture run passes 323 tests,
the repository collects 1,515 tests, and the complete local suite passes 1,474
with 41 expected environment-dependent skips in 468.88 seconds. No math-stuff
release gate was run for this GP-only milestone.

## 2026-08-03 - pin-ablation handback consumed

JC returned `GP_PIN_ABLATION_HANDBACK_2026_08_03.md` against GP `945ca26`,
binding native commits `6e692d2`, `8cdb4f1`, and `e0377d8`. The third bounded
`frontier/v1` consumer lives at
`experiments/jc_h3_pin_ablation/frontier_adapter.py`; its compact review receipt
is `review/jc-h3-pin-ablation-frontier-v1.json`.

The result is materially positive but scoped. The exact Bezout identity closes
the whole `c2_2` stratum at `c2_1=c7_10=0`. With `c2_1=0`, the joint
`c2_2/c7_10` escape locus is one exact hyperplane with no cross term. At
`a=c=1`, both intercepts and its generic point are source-excluded. The
degree-130 resultant leaves at most 130 points unresolved, and the residual
torus invariant `J=a*c^(-3)` forbids automatic full-chart transport. The
explicit `c2_1/c2_2` zero is a failure of this certificate pair, not a source
witness. Full `b=0`, `c2_1`, `b`, `R`, and `Delta` remain open.

The uniform `c2_2` checker passed 14/14. The joint checker reconstructed K0--K21
but its raw-byte K22 failed on Windows CRLF checkout bytes for one otherwise
clean tracked Python file; LF normalization reproduces the certificate's exact
binding digest. No math-stuff release gate was requested or run, and the GP
projection retains graph effect `NONE`.

Five GP regressions bind the native bytes, separate the finite remainder from
transport, preserve the explicit `c2_1` refusal, and exactly regenerate the
review receipt. The repository now collects 1,520 tests; the complete local GP
suite passes 1,479 with 41 expected environment-dependent skips in 707.62
seconds.

## 2026-08-03 - canonical cross-consumer frontier

`grandportage/frontier_bundle.py` closes the composition gap between the three
independent `frontier/v1` consumers. Their compact receipts now expose minimal
`item_observations`: stable semantic ID, exact scope ID, effective status, and
open/closed state. `gp frontier-bundle MANIFEST.json` binds each receipt with
LF-normalized SHA-256 and refuses any repeated semantic ID unless the manifest
provides exactly one resolution.

`AGREE_OPEN` requires identical scope and status across every named receipt.
`SUPERSEDE` requires all prior observations to be open, one named current
closed observation with the exact asserted status, and distinct replacement
items that exist in the compiled view. Receipt order and timestamps carry no
authority. Digest drift, missing observations, unexplained overlap, scope or
status disagreement, false supersession, and absent replacements fail closed.

The canonical manifest is `fixtures/frontier/current_v1.json`; its checked
receipt is `review/frontier-current-v1.json`. It compiles five receipts into
24 current items: 10 open and 14 resolved. Seven explicit resolutions retain
`JC.H3.B0.SOURCE.EXCLUSION` as shared open agreement, preserve the open
coefficient-value seam, and supersede the former finite exceptional-`J`
remainder with the exact all-`J` guarded-divisor closeout. The surface remains
`DERIVED_READ_MODEL_ONLY` with graph effect `NONE`.

Twelve new regressions cover the generic bundle and the exact current
manifest. The repository now collects 1,532 tests; the complete local GP suite
passes 1,491 with 41 expected environment-dependent skips in 691.29 seconds.
The cold external-review packet is
`review/FRONTIER-BUNDLE-COLD-WEB-REVIEW-2026-08-03.md`.

## 2026-08-03 - frontier-bundle protocol hardening and measured test lanes

The external review of `d389983` passed the 20-item frontier and identified two
protocol gaps. Bundle inputs now must be genuine `frontier/v1` projections
(either directly or through `projection_schema`), carry a valid SHA-256 input
fingerprint, and bind unique normalized paths and unique receipt content.
`SUPERSEDE` now requires the closing observation itself to declare the exact
sorted `replacement_ids` asserted by the manifest. The pin-ablation receipt
therefore byte-binds its ten scoped successor items instead of leaving that
provenance solely to the coordinator manifest.

Direct mutations cover closed `AGREE_OPEN`, incomplete receipt sets in both
resolution modes, a closed supersession prior, inconsistent `open_items`, a
foreign schema, invalid fingerprints, duplicate path/content bindings, and
replacement-provenance disagreement. A checked synthetic planning/execution
bundle under `fixtures/frontier/synthetic/` proves the merge algebra is not
JC-specific; it retains one shared open obligation and one open scoped
replacement without widening authority or graph effect.

Measured non-live runtime was 909.03 seconds before tiering, with cost
concentrated in a handful of exact frozen-artifact replays. Pytest now exposes
`replay` and `exhaustive` markers alongside `live`, while unqualified `pytest`
remains the full release gate. The status-block presentation tests consume the
checked-in seam ledger and retain one fresh integration replay. Two tests of
the default/explicit seam alias share that replay instead of executing it
twice. The documented fast, replay, live, and full commands are in
`TESTPLAN.md` and `pyproject.toml`.

Final validation: the fast lane passed 1,419 tests in 140.95 seconds; the replay
lane passed 72 with one expected skip in 278.82 seconds; the exhaustive lane
passed six in 48.16 seconds; and the marker-unfiltered full release gate passed
1,497 with 41 expected environment-dependent skips in 392.51 seconds. The
repository collects 1,538 tests.

## 2026-08-03 - next source-seam request and LSEM retest packet

`JC-COORDINATOR-NEXT-PACKET.md` is no longer on hold. Its primary request is
the exact coefficient-level map from the source-derived target polynomial pair
to the normalized Laurent-root presentation. Its ceiling remains
`CONDITIONAL_NORMALIZED_ROOT_TO_DEPTH6_BOUNDARY_ONLY`: no reverse lift, source
sufficiency, chart coverage, H3, or `(75,125)` is inferred. A secondary bounded
scout asks whether the residual invariant `J=a*c^(-3)` permits any honest
function-field or equivariant transport beyond `a=c=1`; it must not delay the
source seam. The degree-130 root dossier remains next if transport does not
export the normalized line.

`review/LSEM-COLD-RETEST-PACKET-2026-08-03.md` preregisters a genuinely cold
retry of the repaired declaration surface. It forbids the prior return and
research sources, creates a named side-by-side epoch-1 graph through `migrate`,
requires the first and only declaration attempt to use literal
`portage_declare --graph`, and checks both exact-target mutation and original
graph preservation. The retest must run in a fresh context; this GP session
only authored the packet and did not contaminate or simulate the cold return.

## 2026-08-04 - v0.23 public stable refresh

The public mirror at `C:\Users\wstri\dev\grand-portage-public` is refreshed
from a tracked-files-only archive rather than from the private working tree.
The publish boundary now includes the package, tests, fixtures, docs, examples,
exact experiment adapters, Lean contracts, and review packets, plus the public
architecture/compatibility documents and portable root `.mcp.json`. It still
excludes private campaign state, blind-trial runbooks, coordinator requests,
workspace handoffs, local Codex/Claude configuration, and the unrelated
untracked `uv.lock`.

Public clones do not ship the sibling math-stuff research tree. A repository-
level pytest boundary therefore keeps all JC pressure tests visible in the
1,576-test collection but skips that integration group only when the sibling
checkout is absent; workspace runs beside math-stuff remain unchanged. The
isolated public snapshot passed 1,268 non-live tests with 268 explicit JC
integration skips and 40 live deselections in 64.58 seconds. Its separately
authorized WSL/Singular tier passed 38 tests with two environment-dependent
skips in 447.40 seconds.

## 2026-08-04 - Portage Command v0 campaign substrate

`grandportage/campaign.py` implements the deliberately provisional operational
layer proposed in `docs/portagecommandconceptv2.md`. It does not freeze the
concept's original `v1` sketch. A `campaign-packet/v0` instead binds one exact
`frontier-bundle/v1` observation, the source receipt and its normalized digest,
the receipt input fingerprint and evidence-envelope authority ceiling, and one
entry from a separately digest-bound task catalog. This preserves the compact
frontier protocol: propositions and operational instructions are not smuggled
into bundle observations.

`gp campaign-packet` emits deterministic JSON, human briefs, or cold-agent
prompts with a shared packet fingerprint. `gp campaign-ledger` validates
append-only attempts, exact replay commands, declared source artifacts, and
required mutation refusals; `--overlay` projects maturity, outcomes, and
verification debt. Useful refutations, correct refusals, worker defects,
packet defects, accepted artifacts, unverifiable returns, and pending work
remain distinct. Every output is `DERIVED_READ_MODEL_ONLY` with graph effect
`NONE`.

The JC pilot records the weighted-projective second-component discovery and
the failed `D`-ansatz compression as `USEFUL_REFUTATION` against the open
`JC.H3.SOURCE.REMAINING_COEFFICIENT_MAP` frontier. Its active cold mission is
the exact `Q_(5,1)=0` hyperplane classification, or a bounded sparse rational
certificate that identifies the residual strata without claiming H3 or
`(75,125)`. A synthetic matroid base-extension packet compiles through the
same path as the non-JC control.

The next gate is empirical rather than architectural: render the active JC
agent packet, give it to a genuinely cold worker, classify the return through
the failure matrix, and make at most one template repair before deciding
whether `campaign-packet/v1` is ready. The RTS interface, automated planner,
and distribution layer remain deferred.

## 2026-08-12 - JC replay closure and publication-independent kit

`campaign-release/v0` now treats replay instructions as an actual closure, not
just command strings. Each lane binds a working directory, runtime, dependency
and network policy, receipt resources, and exact checker/certificate/input/
environment resources. Large closures can be supplied by a separately
digest-bound `campaign-replay-resources/v0` manifest. Resource roles, portable
paths, digest algorithms, archive containment, use by a lane, receipt typing,
licensing, and post-plan bytes all fail closed.

The materializer now distinguishes a full publication archive from a replay
kit. `--output-dir` still requires every publication/profile gate. The new
`--replay-kit-dir` requires clean source provenance, all selected and replay
resource digests, clear licenses and dispositions, and zero replay debt, but
does not let an absent manuscript masquerade as a reproducibility failure.
The synthetic fixture runs its checker successfully from the resulting
archive, and adversarial tests cover tampered resources, false receipt roles,
path escape/collision, unused closure, post-plan mutation, and a replay-ready
but publication-blocked profile.

The JC adapter is pinned to clean detached commit `1bbdec4`. Fresh source runs
pass all six native computational lanes: extraction 23/23, omega36 74/74,
order-six 14/14 with seven refused mutations, LOCAL connecting 38/38, LOCAL
integrability 19/19, and ENTRY 19/19 with six refused mutations. Its formal
closure builds all 19 local modules and the five named consumers with zero
`sorry` declarations. The generated lock contains 152 replay resources in
seven sets.

The clean audit reports 16/17 selected publication records, zero replay,
license, disposition, or replay-kit blockers, and eight honest publication
blockers: the missing manuscript coverage/writeup and six incomplete non-S2
price cards. It materializes a 169-file replay kit with 167 verified checksum
entries. Six archive lanes replay directly. The archive ENTRY process was
host-terminated at its high-memory post-D2 phase on two attempts, without a
Python error; the exact byte-identical command already passed completely from
the clean checkout, so this is recorded as an archive-environment limit rather
than silently promoted to a second pass.

Validation after the tranche: 1,582 non-live tests passed, seven skipped, and
40 live tests were deselected in 257.36 seconds. The marker-unfiltered release
gate then passed 1,622 tests with seven skips in 773.70 seconds after granting
the live WSL/Singular tier its required host access. The repository collects
1,629 tests.

## 2026-08-14 - JC formalization transport ledger v0

The first GP-side summit-support tranche is now executable. The experimental
`formalization-transport-ledger/v0` fixture is pinned to JC commit
`4d1b5296c49c22cfb82b99c0df7c8c9fe25ab931` and binds seven exact source files,
six named Lean declarations, 18 semantic objects, 13 crossings, and the exact
premise lists used by theorem-backed edges. The adapter validates every field,
endpoint, premise, digest, and declaration substring before emitting a
deterministic `DERIVED_READ_MODEL_ONLY` report with graph effect `NONE`.

The A--H adversarial matrix reports one licensed forward forgetting, seven
refusals, and one inexpressible request. In particular, actual provenance does
not return from the relational summit; finite witnesses do not become formal
power series; initial-form or slice facts do not recover actual/full objects;
the retired local-seven-to-local-five projection records its coordinate losses;
and field-relative obstruction credit does not widen to scheme scope. The
degree-five codomain step is kept visible as the one real GP vocabulary gap:
there is no current dimension/rank-credit claim kind, so no credit is minted.

Fourteen focused tests cover the live JC bindings, all A--H controls, premise
omission, endpoint rebinding, lossy-edge declarations, `UNTYPED` refusal,
scope widening, digest/declaration drift, and deterministic projection under
input reordering. No kernel relation, claim kind, graph field, graph event, or
evidence schema changed. The repository now collects 1,649 tests.

## 2026-08-14 - v0.24 public release preparation

The public mirror is no longer refreshed by an undocumented tracked-file copy.
`public-snapshot-v1.json` classifies every tracked file as public, private, or
generated, and `scripts/public_snapshot.py` exports exact blobs from one Git
commit. Unclassified paths, overlapping exact classifications, missing required
files, unsafe paths, and an existing output target all fail closed. The
generated receipt binds the source commit, boundary manifest, every public
file digest, and the complete snapshot fingerprint.

The old public mirror's Git objects were LF, but its Windows checkout expanded
them to CRLF. Copying exact workspace blobs therefore looked like a whole-tree
modification until Git applied its clean filter. v0.24 makes the checkout rule
explicit through `.gitattributes` (`* text=auto eol=lf`). The staged public diff
contains only 14 modified existing files and 41 additions; future refreshes
cannot recreate the misleading working-tree churn silently.

The workspace is version 0.24.0 with Apache-2.0 licensing metadata, repository
URLs, and a public GitHub Actions fast lane. The release includes Portage
Command, dossier/release/publication projections, replay-kit closure, and the JC
formalization transport assay. It excludes private handoffs, coordinator
packets, planning notes, local configuration, and the unrelated `uv.lock`.

The 1,649-test collection passed as four disjoint release lanes: 1,522 ordinary
tests with eight skips in 43.03 seconds, 72 replay tests with one skip in 313.82
seconds, six exhaustive tests in 48.97 seconds, and 40 live WSL/Singular tests
in 542.11 seconds. The marker-unfiltered one-process invocation hit its
1,200-second wrapper without a failure report; the partition accounts for all
1,640 passes and nine expected skips. A focused 70-test release/architecture
gate passed with two intentional moving-JC skips, and the 0.24.0 wheel built
successfully.

## 2026-08-22 - v0.25 ARR15 implementation wave

ARR15 exposed three implementation defects without earning a new affine
semantic primitive. The family checker prescribed `family.enumeration`, but
the closed native/MCP schema refused that field. Format 5 now admits the
reference and the checker requires a same-family PREDICATE count claim backed
by current exact ENUMERATION evidence with `decides: BOTH`. The 173-member n14
manifest passes through the public declaration surface; naked and mismatched
counts remain refused.

Singular version discovery now closes stdin and fails closed on timeouts,
nonzero exits, and unidentifiable banners. Backend implementation 4 is compared
on persisted graph reload, so an unchanged real backend can consume its
verdict after a fresh process starts. The eight preserved E10 verdicts whose
historical binary identity is `unavailable` remain stale by design.

Format 5 adds a closed implementation identity to graph metadata. `gp
--version`, MCP `serverInfo`, `gp doctor`, and new graph headers agree on the
package, exact source revision and dirty state, graph/kernel versions, MCP
protocol, and backend implementation/protocol. The kernel stays at epoch 10:
no transport type, model claim kind, or transport cell changed.

The agent-facing custody surface now includes root-pinned `gp init --mcp`,
read-only `gp doctor`, generated `gp schema`, complete folded event state,
fingerprinted `gp check --since` classification, and presentation-aware merge
diagnostics. The immutable E10 replay tool validates both recorded source
hashes, migrates copies only, and reproduces the four hard merge conflicts.
Finite database filtering remains outside the affine edge kernel; structured
algebraic witnesses and inert measurement/profile custody remain deferred
semantic-regime work.

## v0.36 independent repairs

Branch release/v0.36.0 starts at released f769705, not unmerged research.
In-band Singular version identity, mixed-trace refusal, scope/architecture/loss
wording repairs, predicate charter policy + gp lint, MCP legacy table repair.
No format/kernel epoch/verifier/binder semantics change. Full non-live 1706 pass;
focused native replay and Lean/parity pass. Full native CI is required before
release; broad local WSL run was stopped without a complete result.

## 2026-09-13: released v0.35 and continued atlas research

Public release: https://github.com/wstrinz/grandportage/releases/tag/v0.35.0
Workspace release merge f7697056569f9763b99ed05739422d02ba0b8101; public merge
eb26640d26d3a3e0bb82747540a9b911eabd4452. Both release PRs #2 merged with
explicit authorization. Continuation is workspace PR #3, retargeted to master.

The follow-up adds unit-cofactor interpretation, native composed graph routes,
a bounded eight-cell requirement inventory, and cache-recovery review controls.
The core stays Mathlib-free pending a separately pinned standard-field adapter.
See docs/ATLAS-FOLLOWUP-V1.md for the conclusions and remaining proof boundaries.

Foreign-domain selection: read match4/Cloquet README, AGENTS, receipt/verdict
schemas, founding plan and packet in the sibling math-research checkout. Its
operative objective is geometric closure, and a full census is explicitly
outside the present campaign scope. It supplies a model/object custody example,
not yet an independent non-polynomial census consumer. No campaign data, code,
receipts or derived records were copied, modified or published. No campaign
permissions were inferred from the authorization to release GP.

## 2026-09-13: read-only four-judgment IR experiment

Continued PR #3 under the supplied IR-v2 packet. D1 adds a cancellation
interpreter and a Z/4 countermodel inside the same Laws class. Structural
profiles form a poset: ordering implies nontriviality; no-zero-divisors is
incomparable with both. The 48-cell inventory retains 3 proved, 24 refuted,
and 21 unknown cells. D2 keeps observation vocabulary model-indexed.
D3 supplies a small conditional Lean specification, with both name dictionaries
checked in the aggregate. D4 projects every available repository graph fixture;
see docs/IR-V2-PROJECTION-REPORT.md and review/ir-v2-projection/index.json.

The packet stopping condition fires: 72/73 model contexts are incomplete.
There is no epoch/format recommendation. The 21/21 PROFILE_FROM_TAG rows
are declarations; the corpus retains no verdict receipts. Fifteen runtime-clean
conclusions do not reconstruct complete proof trees. Source-data gaps and IR
adapter gaps are separate. No new foreign campaign material was accessed.
Version 0.35.0, format 8, epoch 12 and all runtime authority paths are unchanged.

Validation: 1710 non-live tests passed, 61 live deselected; the focused new
surface passed 10 tests. Lean build passed 36 jobs without sorry; both existing
parity gates passed (139 reach rows and expression/receipt correspondence).
The local native cancellation test was not verified: backend identity discovery
timed out, including a fresh-process warmup. Linux witness CI includes the test.
Next measurement requires representative retained format-8 campaign receipts,
without semantic backfilling; no migration should be inferred from this corpus.

## Read-model packet continuation (2026-09-13)

Research branch atlas/evaluation-transport adds corpus intake, nonlocal IR nodes,
gp explain with nine obligation statuses, one exact-value semantic-loss theorem,
and the conditional field-target/profile discharge table. Fixture reports are
regenerated; their compact index pins source/report LF-normalized hashes. Full
non-live validation passed 1719 tests; Lean 39 jobs. Final manifest-hash test is
rerun after regenerating the final index.

The local ignored corpus/ bundle holds 389 verbatim .portage files from arr15,
cfg23, match4. No original bytes were changed. Format5/7/7 blocks raw intake.
User explicitly authorized Terra subagent backfill: corpus/derived contains
native migration candidates and corpus/derived/replayed/cfg23 contains two
fresh verifier-native extension-witness receipts from real retained-data replay.
The original/migration/replay stages and hashes are separate; see local
corpus/BACKFILL-REPORT.md and corpus/derived/backfill-status.json. These are not
substituted for the missing complete verbatim A3 corpus. No campaign data is
staged or published.

Independent release/v0.36.0 worktree tmp/v036-repairs starts at f769705. Commit
40da2f9 contains in-band version identity, mixed-trace refusal and read-surface
repairs, including the MCP legacy table overlooked by prior CLI correction.
Private release PR #4 is open. Full native Linux CI gates release; local focused
native test passed, broad WSL run was stopped without a complete result.

## v0.36 shipped; research continued

Public release https://github.com/wstrinz/grandportage/releases/tag/v0.36.0
Public merge efd0972293af92da29d21f614337b07ff6130a5e; workspace merge
0d871913547fd971bd18a24cbe86acb55c10a1ea. Both PR #4 release candidates passed
all CI, including all 60 native tests (259 seconds in the private run), and
1706 non-live tests. The fresh wheel import passed. Wheel SHA256:
1096c28ba8e295a064e9480dbea2ec05721e7c707f31f1e64fa972111dff828b.
Research PR #3 was brought forward onto that release; gp lint and gp explain
coexist and full native CI includes the research interpreter composition tests.
