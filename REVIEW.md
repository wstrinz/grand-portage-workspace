# Current review brief

This is the attack surface for the current release. The full historical review
through v0.18 is preserved in `HISTORY/REVIEW-through-v0.18.md`.

**Version <!--version-->0.22.0<!--/version-->, graph format
<!--graph-format-->4<!--/graph-format-->, kernel epoch
<!--kernel-epoch-->10<!--/kernel-epoch-->, and
<!--checks-->1408<!--/checks--> collected checks.**

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
