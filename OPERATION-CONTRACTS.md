# Operation contracts

**Status:** two executable pilots
**Authoritative runtime semantics:** kernel epoch 3
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
no-invention check       J ⊆ ι⁻¹(I)
section certificate      r : R → S, r ∘ ι = id, r(I) ⊆ J
formal section theorem   ι⁻¹(I) ⊆ J
combined authority       J = ι⁻¹(I)
```

`verify.operation_output` checks the eliminated/retained variable partition,
expression typing, and source membership for every recorded target generator.
Its representation records the two ring sorts and proves only the first
inclusion.

`gp verify-elimination EDGE --section '{"y":"x^2"}'` checks the independent
reverse inclusion. The section must map exactly the eliminated variables to
polynomials in the retained variables; retained variables are fixed literally.
The checker applies the map simultaneously, proves each substituted source
generator belongs to `J`, and independently expands the membership cofactors.
The stored `polynomial_section_v1` object records every image, substitution, and
cofactor. A rejected section refutes that proof candidate, not exactness, and
cannot erase a previously verified certificate.

The first positive control eliminates `y` from
`(yx-1, y²-x) ⊂ Q[y,x]`, records `(x³-1) ⊂ Q[x]`, and uses `y ↦ x²`.
The two substituted generators are `x³-1` and `x⁴-x = x(x³-1)`.
The negative controls retain the old incomplete `(x) → (0)` example and the
hyperbola `(xy-1) → (0)`: the latter has exact contraction but no polynomial
section of this shape, so it stays conservative pending a general Gröbner
certificate.

Lean now defines `EliminationCompleteness`, proves that it combines with the
no-invention theorem to give `EliminationSemantics`, and proves that an
`EliminationSectionCertificate` entails completeness. The `(2) → (0)` model
separately proves that the cheap checked guarantee does not contain this new
authority.

## Authority and kernel epoch 3

Kernel epoch 2 correctly closed exact-dependent forward transport on locally
checked constructed eliminations. Epoch 3 makes the first reopening precise by
splitting two facts that the earlier `image_complete` gate conflated:

- **exact contraction** licenses `IMAGE_CLOSURE / ALONG / IDENTITY` for a
  denominator-free map, but only when both the no-invention and section
  verdicts are current;
- **geometric point closure** licenses a closed `PREDICATE` moving `ALONG` and
  remains false for constructor-built eliminations until a separate field- and
  radical-aware theorem is checked.

Manual `IMAGE_CLOSURE` declarations continue to state both exact semantic
relations. Constructed eliminations earn only what their evidence proves.
Format-1 graphs migrate non-destructively with:

```console
gp --graph old/.portage/graph.jsonl migrate --to-current-kernel
```

The source is untouched, prior verdicts remain history but stale, and the new
fold re-audits transport under epoch 3.

## Trust boundary

```text
operation contract       mathematical intent and transport theorems
backend lowering         concrete Singular/M2 program and decoder
translation validation  per-run typing, membership, and certificates
authority/provenance     who checked what, under which epoch and inputs
artifact store           exact immutable programs and raw transcripts
```

The next earned step is a general Gröbner completeness certificate for eliminations
without polynomial sections, alongside the separate geometric point-closure theorem.
Contracts remain compiled constructor metadata until the two pilots show that
persisting them in the IR buys more than it costs.
