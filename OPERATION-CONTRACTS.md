# Operation contracts

**Status:** two executable pilots
**Authoritative runtime semantics:** kernel epoch 4
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
retained-coordinate ring, `i : S -> R` the coordinate inclusion, `I` the source
ideal, and `J` the recorded output ideal:

```text
exact semantics             J = inverse_image(i, I)
no-invention check          J subset inverse_image(i, I)
section completeness        r : R -> S, r o i = id, r(I) subset J
Groebner completeness       checked pure-lex basis gives inverse_image(i, I) subset J
combined ideal authority    J = inverse_image(i, I)
section point authority     every target-valued point lifts through r
```

`verify.operation_output` checks the eliminated/retained variable partition,
expression typing, and source membership for every recorded target generator.
It proves only no-invention.

`gp verify-elimination EDGE --section '{"y":"x^2"}'` checks a polynomial
retraction. Retained variables are fixed literally; eliminated variables map to
polynomials in the retained ring; every substituted source generator is proved
inside `J` with independently expanded cofactors. This is stronger than ideal
completeness: evaluating the checked polynomials at any target-valued point
produces a source-valued point that projects back identically.

`gp verify-elimination-groebner EDGE` covers eliminations with no polynomial
section. Singular searches for a bounded pure-lex basis and representation
witnesses; GP's backend-neutral exact checker replays source span, every
critical pair, the elimination order, and retained-basis membership. This earns
ideal completeness only. Search is untrusted and point lifting is not inferred.

The positive section control eliminates `y` from `(yx-1, y^2-x)` and uses
`y -> x^2`. The hyperbola `(xy-1) -> (0)` is the decisive separation: its
elimination ideal is exact and the Groebner route can certify it, but the target
point `x=0` has no lift. Exact contraction is therefore not point-surjectivity.

A harder eight-variable live pressure test exercised the other failure mode. A
plausible three-generator retained system was not the full elimination ideal: a
21-element pure-lex basis contained 17 retained elements and exposed a concrete
missing relation. The verifier refused exact promotion, preserving the target as
a sound necessary system. This is the intended operational value of separating
the contract from the backend program.

Lean defines `EliminationCompleteness`, the section and basis boundaries, and a
coefficient-algebra-relative `EliminationPointSurjective` proposition. It proves
that the section lifts every valid target evaluation, and separately provides a
countermodel showing exact contraction alone has no point-lifting consequence.

## Authority and kernel epoch 4

Kernel epoch 4 derives two different authorities from the evidence method:

- **exact contraction** requires current no-invention plus either a checked
  polynomial section or a checked pure-lex certificate;
- **point-surjective image authority** requires current no-invention plus a
  checked polynomial section. A pure Groebner certificate never opens it.

Point-surjectivity is actually strong enough for any target-expressible
predicate. The current claim IR does not yet type retained-coordinate
expressibility, so the runtime conservatively uses it only to reopen the
existing Zariski-closed `PREDICATE / ALONG` cell. This is an explicit false
refusal boundary, not evidence that closedness is mathematically necessary once
a section exists.

Manual `IMAGE_CLOSURE` declarations continue to state their semantic relation.
Constructed eliminations earn only what their current evidence proves. Because
this changes transport meaning for existing section verdicts, format 1 advances
from kernel epoch 3 to 4 and section-verifier version 2. Migration remains
non-destructive:

```console
gp --graph old/.portage/graph.jsonl migrate --to-current-kernel
```

The source is untouched, prior verdicts remain history but stale, and the new
fold re-audits transport under epoch 4.

## Trust boundary

```text
operation contract       mathematical intent and transport theorems
backend lowering         concrete Singular/M2 program and decoder
translation validation  per-run typing, membership, and certificates
authority/provenance     who checked what, under which epoch and inputs
artifact store           exact immutable programs and raw transcripts
```

The next earned step is a separately typed point-lifting certificate beyond
global polynomial sections, exercised against harder live eliminations. Contracts
remain compiled constructor metadata until the pilots show that persisting them
in the IR buys more than it costs.
