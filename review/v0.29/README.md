# Grand Portage v0.29 development record

Version: `0.29.0`

Graph format: `6`

Kernel epoch: `11`

Collected checks: `1515`

v0.29 introduces selected number-field embedding identity. A model may carry a
closed REAL isolating interval or COMPLEX isolating box, while omission/null
retains abstract-ring behavior. Endpoint and edge fingerprints bind the full
serialized map to both selected endpoint definitions.

An identity map between different selected embeddings is refused structurally.
A genuine polynomial field automorphism remains a ring equivalence, but no
longer copies a free predicate unchanged between selected images. Conflicting
model and edge IDs remain fail-closed; byte-identical redeclarations remain
idempotent for branch merges.

The same unreleased boundary now also includes bounded ordered-real semantics.
`REAL_CLOSURE` is supported over Q only when coupled to a selected REAL
embedding. Structured predicates may assert exact signs of a univariate
polynomial at that selected root. The verifier checks root isolation with
Sturm arithmetic, refines exact rational intervals, and records a deterministic
receipt that the graph fold replays before activating the verdict.

## CFG23 replay

- `22_4`: the false plus/minus identity is refused; `w -> -7-w` remains a
  polynomial automorphism; exact plus-root relabeling retains predicate
  transport.
- `Q(i)`: the false identity of `i` and `-i` is refused; `x -> -x` remains a
  polynomial conjugation equivalence.
- `26_4`: the selected real root in `(1,2)` is a valid `REAL_CLOSURE` model and
  its positivity verifies exactly; a decoy interval with no root is
  inconclusive and grants no authority.
- All six RFC v1.4 fixture families and all 26 adversarial mutations are
  represented in native GP tests. Required-ID reassignment, endpoint drift,
  map drift, and duplicate model/edge IDs all change custody or fail closed.

## Validation

- Full suite: `1465 passed, 50 skipped` in 53.32 seconds.
- RFC v1.4 reference checker: six clean fixtures, 26/26 mutations detected,
  and 3/3 required maps visited, passing, and semantically verified.

## Remaining boundary

This bounded slice does not claim multivariate real-locus decision procedures,
quantifier elimination, arbitrary semialgebraic transport, or ordering changes
through field automorphisms. Comparisons reuse the one-expression condition
grammar (`a < b` is `NEGATIVE(a-b)`). Nontrivial embedding-changing maps still
refuse predicate transport, while incompatible exact sign assertions at one
selected model create visible debt.
