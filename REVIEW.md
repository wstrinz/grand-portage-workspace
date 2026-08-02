# Current review brief

This is the attack surface for the current release. The full historical review
through v0.18 is preserved in `HISTORY/REVIEW-through-v0.18.md`.

**Version <!--version-->0.22.0<!--/version-->, graph format
<!--graph-format-->4<!--/graph-format-->, kernel epoch
<!--kernel-epoch-->10<!--/kernel-epoch-->, and
<!--checks-->1447<!--/checks--> collected checks.**

## Highest-risk claim

Grand Portage now has a small semantic kernel and a nontrivial certifying-
checker trust base. Review both separately. A correct transport table does not
repair a parser, canonicalizer, cofactor replay, fingerprint binding, or
authority-projection defect.

## 1. Authority binding

Attack every path that turns a checked report into graph authority:

- mutate the model after producing evidence;
- change coefficient domain or point universe;
- reorder ring variables, generators, guards, or intermediate states;
- replay a certificate across charts or semantically similar model ids;
- preserve a verifier verdict while changing its representation;
- mix current and stale verdicts across supersession or merge;
- attempt to promote standalone evidence whose authority boundary says none.

The key positive control is exact replay against the same model fingerprint.
The key negative control is a locally verified result that still cannot travel
to a parent without a licensed transport or exhaustive cover.

## 2. Exact checker

Treat the polynomial representation, parser, canonicalizer, sparse arithmetic,
budgets, and certificate expanders as part of the trusted implementation.
Differentially attack them with external CAS systems as untrusted oracles:

- variable permutations and simultaneous substitutions;
- reordered generators and equivalent cofactor families;
- characteristic changes and inadmissible denominators;
- sparse/infix and Laurent/export round trips;
- large coefficients, exponents, term counts, and boundary budgets.

A bounded search miss is typed ignorance, never refutation.

## 3. Transport semantics

The transport table remains the most concentrated mathematical risk. In
particular review identity variance, point-universe scope, coefficient-domain
expressibility, partial maps, mapped predicate pullback, partition
recombination, and image-closure asymmetry.

Mapped `ring_iso` authority is no longer an unaudited boolean: current
verification checks both ideal pullbacks and both inverse-map compositions.
Attack the verifier and its graph binding rather than the obsolete declaration-
only design.

## 4. Merge and identity

The v0.19 fan-out assay now exercises two valid branches creating different ids
or normal forms for the same mathematical object. It confirms:

- differently normalized redeclarations of one id refuse with a field diff;
- cross-branch supersession exposes consumers still anchored to the old model;
- stale and current verdicts compose with only the current one effective.

It also exposes the remaining seam: exact affine objects under different ids
merge cleanly and require an explicit alias-audit view. GP correctly does not
infer full mathematical identity from names or a heuristic signature.

## 5. Read surfaces

Ask a cold reader:

- what is established;
- what is intentionally carried;
- what is stale or refused;
- why a conclusion is licensed;
- what the first unresolved authority seam is.

Compare the answer with the folded graph and accepted baseline. Projection and
visualization are useful only if they improve that answer without becoming a
second source of truth.

## 6. Current composition target

The JC `c9_11` p-axis is now the first complete end-to-end authority path. The
native receipt, standalone factor/affine replay, compiled localized-unit proof,
graph binding, real backend artifacts, and local `EMPTY` verdict are retained
in `review/v0.19/`. The parent edge remains a refusal control.

Both five-step source ladders now have graph-bound mapped-equivalence authority.
The next isolated composition target has also landed: JC commit `cb3136c` carries
25 exact sparse face tables, ten input bodies, 23 ordered solve transitions,
and two boundary residuals. `experiments/jc_h3_source_depth6/chain_adapter.py`
independently checks the chain, welds its inputs to GP's ladder fixtures, and
welds its outputs to GP's boundary fixture. The routine gate is fast; the full
ambient substitution replay takes about 80 seconds and is release/review-only.

The v0.22 extraction assay closes that specific open edge. A standalone
`graded_face_extraction_v1` checker reconstructs all 25 selected faces from five
reduced E-system rows, and its stronger mode reconstructs those rows from the
normalized root series, fourteen P-side eliminations, and the defining
E-system formula. Lean proves only the necessary-condition direction and
exhibits why reverse transport is invalid.

The graph-bound assay materializes the complete finite reduced E-system
template: 147 nonzero equations, 78 active variables, and 424,934 sparse
terms. The selected 25 equations occur verbatim. `verify.containment` v3
therefore checks the declared `NECESSARY_CONDITION` by exact parsed generator
inclusion, with no backend process. Attack malformed equal generators,
cross-context replay, direction reversal, old v2 verdict staleness, and any
attempt to promote selected-face survival, source membership, parent coverage,
H3, or the (75,125) verdict. Also scrutinize the roughly 39.5 MB persisted
graph: it is authoritative and usable, but exposes the need for a smaller
content-addressed review projection.

JC commit d4a18b4 adds a conditional original-pair seam manifest and verifier.
The positive result is only normalized Laurent-root data to the five exact
reduced rows. The exact source pair is not serialized, and the coefficient-level
target-pair to normalized-root map is explicitly UNMATERIALIZED_OPEN. The GP
adapter must keep graph effect NONE, reproduce all five row commitments, and
refuse any mutation that promotes strict source authority, moves the downstream
t pin into row derivation, or drops source-membership and H3 refusals.

## 7. Project-level falsification

`KILL-CRITERIA.md` remains binding. A6 is now live: validators have dedicated
test suites and the certifying checker is a real trust surface. The relevant
question is no longer whether validators are tiny, but whether they remain
bounded replay checkers, share a small exact substrate, resist differential
attacks, and compose into conclusions worth their cost.

## 8. S4 constructible-scope control

`experiments/jc_h3_s4_scope/adapter.py` is a deliberately standalone pressure
test for the distinction between one inhabited closed piece and an unresolved
complementary open piece. Review the frozen cubic-field evaluator, the exact
`p^2` coefficient slice, the rank-witness check, and the fixture/body digests.
The positive control is `NONEMPTY` on `C=C2=0` over the declared base field.
Mandatory refusal controls include any attempt to turn 24 nonsquare-seed
results into off-locus emptiness, omit the `C2!=0` branch, claim confinement of
all points, widen the point universe, or give the structural cover a union-wide
claim. The checked-in projection must retain graph effect `NONE`.

## 9. Unilateral recurrence control

`experiments/jc_h3_adjoint_recurrence/adapter.py` and
`lean/GrandPortage/ParametricRecurrence.lean` deliberately split instance
checking from semantic inference. Attack the declared unilateral start,
cutoff, shift convention, rational operator coefficients, finite-width padding,
zero-tail premise, and nonzero endpoint. The native correction must survive:
`S^8` annihilates, `S^7` does not, and every coefficient below shift eight
vanishes for any annihilator. Mutations restoring the original false prose,
widening to a bilateral domain, dropping H8 from outstanding premises, or
minting graph/H3 authority must refuse. Also scrutinize the excluded blanket
minimality claim: the final padded regimes are zero and admit the unit
annihilator even though `S-1` annihilates them.

## 10. First-order depth-eight fiber control

`experiments/jc_h3_depth8_fiber/adapter.py` freezes the landed composition
receipt and checks the exact middle scope between pointwise and componentwise
claims. Review the L-valued nonzero check for `Omega_comb`, the solved status
of `c7_4`, the free `c8_5` quantifier, and the separation between the selected
base witness and the rest of the 12-dimensional survivor. The positive result
is emptiness of the entire named **first-order** compatibility fiber only.

`lean/GrandPortage/FirstOrderFiber.lean` proves both the base-obstruction rule
and a separate conditional nonlinear bridge. The adapter instantiates only the
first theorem. Mutations promoting the result to nonlinear nonextension,
another base point, the component, K-valued scope, depth nine, source/H3
authority, or graph effect must refuse.

## 11. Graph-bound on-wall localized obstruction

`experiments/jc_h3_wall_ob_open/adapter.py` freezes the landed 502-term S2
dead-row equation and 499-term ambient obstruction. Attack the exact identity
`OB = value_24 + 45*c2_3*t*c8_9*R`, the `R=0` generator, the `OB!=0` guard,
the other declared chart guards, coefficient domain, point universe, source
digests, and graph fingerprint. The positive control is a current
`LOCALIZED_UNIT_IDEAL_CERT` that mints `LOCAL_EMPTY` only on the named dead-row
consequence model.

The complete nine-body parent and its edge to this consequence model do not
exist in the assay. Any component, source, H3, verdict, or complementary
`R=OB=0` conclusion is therefore an authority escalation. Also fuzz the
generic membership backend with sparse targets, generators, and cofactors:
none may be interpolated into Singular as Python or JSON dictionary syntax.

## 12. Localized ring-element class control

`experiments/jc_h3_b0_compatibility/adapter.py` checks a proposition sort not
represented by the model-level graph claims: whether one exact localized
coordinate-ring element is zero or a unit. Attack the five-row matrix and RHS,
the equality of its determinant with `det5`, every Lambda fiber part, the
`3/2` eliminant scalar, clearing exponent two, the full `Phi_b0_compat`, and
the specialization into the three-variable slice. Exponent one must retain a
nonzero remainder.

The adapter recomputes the resultant and first subresultant, strips only roots
shared with the exact guard product and `S11`, and checks both observations in
their quotient rings. Mutate the degree-14 modulus, `S10`, `S11`, `det5`, the
`OB` pivot, or either point direction. The positive conclusion is exactly
`nonzero AND nonunit`; attempts to infer nonzerodivisor status, component
geometry, `K`-rationality, wall survival/emptiness, lifting, source, H8, H3,
verdict, or graph authority must refuse. Review the deliberate choice to keep
this as standalone evidence with graph effect `NONE` rather than prematurely
adding a graph claim kind.

The fixture also embeds the later `compatibility_module/1` certificate. Check
that its principal generator digest is byte-identical to the independently
reconstructed `Phi`, that its `(5,1,1)` localized ranks and zero rank strata
remain scoped to the declared guards, and that its fiber semantics are labeled
as consumed frozen premises rather than GP-rederived facts.
