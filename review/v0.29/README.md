# Grand Portage v0.29 development record

Version: `0.29.0`

Graph format: `6`

Kernel epoch: `11`

Collected checks: `1498`

v0.29 introduces selected number-field embedding identity. A model may carry a
closed REAL isolating interval or COMPLEX isolating box, while omission/null
retains abstract-ring behavior. Endpoint and edge fingerprints bind the full
serialized map to both selected endpoint definitions.

An identity map between different selected embeddings is refused structurally.
A genuine polynomial field automorphism remains a ring equivalence, but no
longer copies a free predicate unchanged between selected images. Conflicting
model and edge IDs remain fail-closed; byte-identical redeclarations remain
idempotent for branch merges.

## CFG23 replay

- `22_4`: the false plus/minus identity is refused; `w -> -7-w` remains a
  polynomial automorphism; exact plus-root relabeling retains predicate
  transport.
- `Q(i)`: the false identity of `i` and `-i` is refused; `x -> -x` remains a
  polynomial conjugation equivalence.
- `26_4`: `REAL_CLOSURE` remains explicitly unsupported in this packet. Its
  ordered-real meaning is not inferred from the selected REAL interval.
- All six RFC v1.4 fixture families and all 26 adversarial mutations are
  represented in native GP tests. Required-ID reassignment, endpoint drift,
  map drift, and duplicate model/edge IDs all change custody or fail closed.

## Validation

- Full suite: `1448 passed, 50 skipped` in 40.60 seconds.
- RFC v1.4 reference checker: six clean fixtures, 26/26 mutations detected,
  and 3/3 required maps visited, passing, and semantically verified.

## Deliberate follow-up

This release does not add `REAL_CLOSURE`, ordered relations such as positivity
or comparison, real-locus transport, general polynomial-string normalization,
or contradiction detection for free predicates. Those remain a separate
ordered-real semantics packet.
