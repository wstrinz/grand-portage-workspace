# Operation contracts

**Status:** two executable pilots
**Authoritative runtime semantics:** kernel epoch 2
**Formal shadow:** `lean/GrandPortage/OperationContract.lean`

Grand Portage now has a small operation-contract foundation. Its first job is
to keep three statements from collapsing into one:

1. **Intended semantics** — what an exact mathematical implementation produces.
2. **Checked guarantee** — what local translation validation establishes about
   this particular output.
3. **Licensed consequences** — what follows from that checked guarantee.

A backend success, a parsed result, and a locally verified output do not by
themselves prove that the backend returned the complete mathematical object.

## Contract shape

The Lean core is:

```text
OperationContract Params Source Target
    precondition
    semanticRelation
    checkedGuarantee
    semantics_entails_checked
```

The theorem points from exact semantics to the checked guarantee, never in the
tempting reverse direction. Claim transformers are theorems derived from these
relations, not strings stored inside the contract. The immutable values in
`grandportage/contracts.py` are runtime shadows for constructors, verifiers,
and audits; they are not proof objects.

## Saturation pilot

For source ideal `I`, polynomial `f`, and recorded output ideal `J`:

```text
exact semantics          J = I : f^∞
checked containment      I ⊆ J
checked generators       each recorded generator of J lies in I : f^∞
formal generated lift    J ⊆ I : f^∞
open                     I : f^∞ ⊆ J
```

Lean proves the one-sided lift and pins the completeness gap with `I = (6)`,
`f = 2`, `J = (6)`: all local checks pass, while `3 ∈ (6) : 2^∞` and
`3 ∉ (6)`. Source containment still licenses the existing
`NECESSARY_CONDITION / AGAINST / IDENTITY` move.

## Elimination pilot

Elimination is genuinely multi-sorted. Let `R` be the source ring, `S` the
retained-coordinate ring, `ι : S → R` the coordinate inclusion, `I` the source
ideal, and `J` the recorded output ideal:

```text
exact semantics          J = ι⁻¹(I)
runtime typing check     each recorded generator elaborates in S
runtime certificate      each recorded g satisfies ι(g) ∈ I
formal generated lift    J ⊆ ι⁻¹(I)
open                     ι⁻¹(I) ⊆ J
```

Typing the generator as an element of `S` absorbs expressibility into the Lean
type. At the string boundary, `verify.operation_output` separately checks the
eliminated/retained variable partition, expression typing, and source
membership. The verifier representation records both ring sorts and the
partition.

The checked envelope licenses target identities pulling back to the source,
source points mapping to the target, and target emptiness implying source
emptiness. It does **not** license a source-derived identity moving along to the
recorded target. That direction needs completeness.

Lean pins this with the small counterexample `I = (2)`, `J = (0)`, identity
inclusion, and no recorded generators. Every local generator check passes
vacuously, but `2 = 0` holds modulo `I` and fails modulo `J`. The polynomial
version is eliminating `y` from `(x) ⊂ k[x,y]` while incorrectly recording the
zero ideal in `k[x]`.

## Authority and kernel epoch 2

This counterexample found a real authority gap. Kernel epoch 1 licensed
`IMAGE_CLOSURE / ALONG / IDENTITY` from the map kind alone, even on a
constructor-built elimination whose current verdict explicitly means only
“nothing invented.” Kernel epoch 2 keeps the abstract exact-image rule but
requires exact-output authority for the two forward consequences that depend on
completeness:

- `IMAGE_CLOSURE / ALONG / IDENTITY`;
- `IMAGE_CLOSURE / ALONG / PREDICATE` for a closed predicate.

Manual `IMAGE_CLOSURE` declarations still state the exact mathematical
relation. A constructor-built `Eliminate` fails closed on those two moves until
a future `VERIFIED_EXACT`-class certificate exists. Its checked pullback and
point-map directions remain available.

Format-1/kernel-epoch-1 graphs migrate non-destructively with:

```console
gp --graph old/.portage/graph.jsonl migrate --to-kernel2
```

The source is untouched, prior verdicts remain present but stale, and the new
fold re-audits transport under epoch 2.

## Trust boundary

```text
operation contract       mathematical intent and transport theorems
backend lowering         concrete Singular/M2 program and decoder
translation validation  per-run typing, membership, and certificates
authority/provenance     who checked what, under which epoch and inputs
artifact store           exact immutable programs and raw transcripts
```

The next earned step is a completeness certificate design for elimination—not
a Boolean assertion—and then a third contract chosen from live campaign demand.
Contracts remain compiled constructor metadata until the two pilots show that
persisting them in the IR buys more than it costs.
