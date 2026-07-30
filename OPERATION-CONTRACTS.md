# Operation contracts

**Status:** two executable pilots
**Authoritative runtime semantics:** graph format 2, kernel epoch 6
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
    transportObligations
    semantics_entails_checked
    claimTransformerTheorems
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
It now also defines `RetainedCoordinateExpressible`: a source predicate factors
through the target evaluation on retained coordinates. Lean proves that
point-surjectivity transports every such predicate, and gives a countermodel
showing that point-surjectivity alone cannot transport an unrelated predicate.

## Authority and kernel epoch 6

Kernel epoch 6 keeps five facts separate:

- **exact contraction** requires current no-invention plus either a checked
  polynomial section or a checked pure-lex certificate;
- **geometric closure authority** is enough for a closed predicate but not an
  arbitrary point predicate;
- **point-surjective image authority** requires current no-invention plus a
  checked polynomial section. A pure Groebner certificate never opens it;
- **retained-coordinate expressibility** belongs to the claim, not the map;
- **coordinate-rewrite authority** requires a literal identity map or a current
  verified ring isomorphism, with predicate syntax moving contravariantly.

The runtime projection of the last item is intentionally small:

```json
{"condition":{"all":[
  {"relation":"ZERO","expression":"x^2-1"},
  {"relation":"NONZERO","expression":"x"}
]}}
```

Every atom is parsed in the source model's exact polynomial ring. Before a
section-certified constructed elimination, the runtime may reindex that syntax
through any chain of checked coordinate changes. `forward` is the source-to-
target point map, so `ALONG` expression rewriting uses `inverse`, while
`AGAINST` uses `forward`. Substitution is simultaneous and exact. A literal
`IDENTITY_MAP` preserves syntax; a nonidentity mapped equivalence requires both
an authored `ring_iso: true` contract and a current `VERIFIED` verdict.

The rewritten expressions must parse in the retained-coordinate target ring.
An all-`ZERO` conjunction thereby establishes closedness; a conjunction
containing `NONZERO` can travel by the stronger point-lifting theorem. A
structured condition naming an eliminated coordinate is refused even if it is
closed, and a manually asserted `zariski_closed` flag cannot override that type
failure. Free-text predicates remain legal and conservative. Unsupported or
unverified passes may still transport the proposition abstractly, but they lose
machine-readable expression typing and cannot unlock a later elimination.

Lean defines predicate reindexing on `MappedEquivalence`, proves the
contravariant orientation, composes verified coordinate changes, and proves
that rewriting through the composite equals rewriting step by step. The Python
projection evaluates the corresponding exact polynomial substitutions; it does
not persist a synthesized claim or mutate the campaign graph.

Manual `IMAGE_CLOSURE` declarations continue to state their closure relation but
do not mint point-surjectivity. Constructed eliminations earn only what their
current evidence proves. The persisted condition syntax advances graph format 1
to 2, and the newly licensed nonclosed predicate transport advances kernel epoch
4 to 5; verified coordinate-map composition then advances the runtime to epoch
6 without changing graph syntax. Migration remains non-destructive:

```console
gp --graph old/.portage/graph.jsonl migrate --to-current-kernel
```

The source is untouched, prior verdicts remain history but stale, absent
`condition` fields stay absent, and the new fold re-audits transport under epoch
6.

## Trust boundary

```text
operation contract       mathematical intent and transport theorems
backend lowering         concrete Singular/M2 program and decoder
translation validation  per-run typing, membership, and certificates
authority/provenance     who checked what, under which epoch and inputs
artifact store           exact immutable programs and raw transcripts
```

The next earned steps are rewrite contracts for operations other than verified
coordinate equivalence and a separately typed point-lifting certificate beyond
global polynomial sections, both exercised against harder live eliminations. Contracts remain
compiled constructor metadata until the pilots show that persisting them in the
IR buys more than it costs.
