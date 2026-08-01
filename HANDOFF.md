# HANDOFF.md — chronological implementation record

> **Current readers:** start with `CURRENT.md`, then `ARCHITECTURE.md` and
> `REVIEW.md`. This file preserves the detailed development narrative and
> experiment history; later sections may describe superseded implementation
> states and should not be read as current authority.

Written for a session with **no prior context**. Everything needed to pick this
up is here or linked from here.

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

**Age: about nine days. Version 0.21.0. <!--checks-->1308<!--/checks--> checks.** Treat
every claim in the docs as provisional.

**The backend evidence seam is now durable.** Production verifiers and
structured operations dispatch through semantic `SingularBackend` methods and
retain immutable execution artifacts. Backend protocol 2 / Singular
implementation 3 gives every trace entry a content address for a complete
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

**Current depth-6 chain status.** JC commit `cb3136c` lands a compressed exact
certificate containing 25 sparse depth-2..6 face tables, the ten top/second
input bodies, 23 ordered solves, and two residuals. GP freezes the native bytes,
checks compressed and canonical digests, independently replays the ordered
prefix fingerprints, affine splits, t-unit witnesses, pin cofactors and solves,
and welds the endpoints to its existing ladder and boundary fixtures. The fast
integrity/solve gate takes a few seconds; a separate full ambient substitution
replay is green in about 80 seconds. Mutations of order, unit evidence, solved
values, or refusal scope fail closed. The resulting evidence intentionally has
`graph_effect: NONE`: `cb3136c` binds the extracted face bodies but does not
prove their derivation from the raw E-system. A bounded source-to-face
extraction certificate is the next composition seam; actual-source membership,
chart coverage, H3, and verdict promotion remain refused.

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
| work on the tool | `cd C:\Users\wstri\dev\grand-portage && python -m pytest` (<!--checks-->1308<!--/checks--> checks, ~40 s) |

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
server, enforcement hook, verifier. <!--checks-->1308<!--/checks--> checks,
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
