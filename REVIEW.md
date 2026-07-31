# Current review brief

This is the attack surface for the current release. The full historical review
through v0.18 is preserved in `HISTORY/REVIEW-through-v0.18.md`.

**Version <!--version-->0.19.0<!--/version-->, graph format
<!--graph-format-->3<!--/graph-format-->, kernel epoch
<!--kernel-epoch-->10<!--/kernel-epoch-->, and
<!--checks-->1268<!--/checks--> collected checks.**

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

The next composition target is the five-step ordered source ladder: bind its
fingerprinted states to exact graph models and earn mapped equivalence only
through explicit forward/reverse point-map premises.

## 7. Project-level falsification

`KILL-CRITERIA.md` remains binding. A6 is now live: validators have dedicated
test suites and the certifying checker is a real trust surface. The relevant
question is no longer whether validators are tiny, but whether they remain
bounded replay checkers, share a small exact substrate, resist differential
attacks, and compose into conclusions worth their cost.
