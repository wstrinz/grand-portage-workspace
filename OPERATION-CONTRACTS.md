# Operation contracts

**Status:** first executable pilot
**Authoritative runtime semantics:** kernel epoch 1 remains unchanged
**Formal shadow:** `lean/GrandPortage/OperationContract.lean`

Grand Portage now has a small operation-contract foundation. It is deliberately
not a new graph schema or a Python framework for every constructor. The first
job is to keep three statements from collapsing into one:

1. **Intended semantics** — what an exact mathematical implementation of the
   operation would produce.
2. **Checked guarantee** — what the current local validators establish about
   this particular output.
3. **Licensed consequences** — what follows from that checked guarantee.

A backend success, a parsed result, and a locally verified output are not by
themselves a proof that the backend returned the complete mathematical object.
That is the motivating invariant of this layer.

## Contract shape

The Lean core is:

```text
OperationContract Params Source Target
    precondition
    semanticRelation
    checkedGuarantee
    semantics_entails_checked
```

The source and target types are the operation's model sorts. The required
theorem points from exact semantics to the checked guarantee. It does not point
backwards.

Claim transformers are theorems derived from a contract's semantic relation or
checked guarantee. They are not string fields inside the contract. Backend
program compilation, certificate formats, verifier authority, and provenance
belong to the separate lowering and evidence layers.

The Python value in `grandportage/contracts.py` is an immutable runtime shadow.
It makes the same boundary inspectable by constructors and tests; it is not a
proof object and does not override the kernel.

## Saturation pilot

For source ideal `I`, polynomial `f`, and recorded output ideal `J`:

```text
intended semantics       J = I : f^∞

checked by containment   I ⊆ J
checked by output cert   every recorded generator of J has a witness in I : f^∞
formal generated lift    J ⊆ I : f^∞

still open               I : f^∞ ⊆ J
                         (output completeness)
```

The checks establish source containment and generator-level soundness. Lean now
models ideal generation by its universal property inside the ring's family of
admissible ideal predicates. When the runtime endpoint is the ideal generated
by exactly the recorded output generators, their certificates lift to the
ideal-level sound envelope `J ⊆ I : f^∞`. This still does not establish equality
with the full saturation. Lean pins the remaining gap with the concrete
counterexample `I = (6)`, `f = 2`, `J = (6)`: the sound directions hold, but
`3 ∈ (6) : 2^∞` and `3 ∉ (6)`.

Source containment licenses the current
`NECESSARY_CONDITION / AGAINST / IDENTITY` move: an identity in the source
ideal also holds in the built ideal. Even exact saturation does not license a
derived identity in the saturated ideal to travel back to the source.

## Trust boundary

The layers are:

```text
operation contract       mathematical intent and transport theorems
backend lowering         concrete Singular/M2 program and decoder
translation validation  per-run containment and output certificates
authority/provenance     who checked what, under which epoch and inputs
```

Keeping these separate prevents two invalid promotions:

- “the certificate checks” → “the declared operation was computed completely”;
- “the operation is mathematically sound” → “this backend run implemented it
  correctly.”

## What this pilot does not do

- It does not change any kernel-epoch-1 transport cell.
- It does not add contract records to the persisted event format.
- It does not claim completeness for saturation output.
- It does not formalize the raw generator/cofactor certificate format in Lean.
- It does not duplicate the store, CLI, backend orchestration, or provenance
  system in Lean.
- It does not instantiate speculative contracts for every existing operation.

## Next earned steps

1. Keep the two-pole saturation gate: a real Singular result and a
   deliberately incomplete fake result whose local checks pass without gaining
   exactness authority.
2. Instantiate elimination. It has the same soundness/completeness split but
   changes expression and point sorts, so it is the first real multi-sorted
   stress test.
3. Only after those two pilots, decide whether contracts belong in the
   persisted IR or remain compiled constructor metadata.
4. Derive more runtime transport cells from proved claim transformers before
   replacing the current table as the authoritative lookup.
