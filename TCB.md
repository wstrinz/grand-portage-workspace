# Phase 0c trust observations
This is a feasibility record, not checker admission or a Phase1 kernel contract.

## Installed toolchain
Lean4.32.1, commit f054605aea4b840552cca2e725580bffd1e1b704. Existing C: binaries are read-only. New packages, dependency checkouts, cache downloads, generated artifacts and fixtures live on F:. Executable/library/compiler integrity is assumed when interpreting native runs. Exact file digests are recorded in the spike reports.

## Mathlib-free toy
Spike.lean models natural-number equality and finite named context sets. Its checker compares the actual two naturals; declarations alone cannot hold a claim. Receipts bind claim ID, both operands, exact requested scope, model key/digest and checker digest. Current source registrations override prior registrations. Narrowing requires a held parent and subset contexts; stale parents cannot support children. The bounded recursive lookup rejects cycles by exhaustion.
Source digests are opaque strings in Lean. The Python validation driver hashes actual fixture/case/source bytes; the spike does not implement cryptographic hashing, authenticated source registration, a general statement AST, complete provenance or all K1-K6.
checked_equality proves equality from the actual checked Boolean definition. Its axiom audit is propext only. This is not a proof of the complete custody fold.
Array scans and bounded recursion are toy implementations. Empty scopes are permitted; extra JSON fields are ignored. Resource caps, duplicate JSON-key policy, normalized scope identity, retraction and independent-warrant survival are not settled here.

## Exact univariate rational replay
Spike.Poly uses Lean Rat, finite sparse exponent/coefficient lists, explicit cofactor-count equality and exact coefficient comparison up to the maximum degree in the computed products/target. Duplicate exponent terms are summed; zero denominators and negative/non-natural exponents are refused.
The exact cofactor test is executed, but no theorem relating this implementation to Mathlib Polynomial has been proved. It is not an admitted unit-ideal checker. No multivariate encoding, arbitrary CAS export parser or resource bound is supplied.

## External process
CheckerMain calls the private fraction_checker.py through IO.Process.output with the exact input string on stdin. Acceptance requires exit0, valid=true, exact echoed request bytes (after JSON string decoding), and checker label fraction-cofactor-v1. Hostile output binding/version controls were exercised.
Python/Fraction, its interpreter, script contents, process transport and invocation path are additional TCB for this route. Validation pins script and executable hashes; the Lean wrapper itself does not enforce a pre-execution SHA-256 check or prevent TOCTOU. Echoing input binds a response; it does not establish checker honesty.
Production would need checker admission, executable/version integrity, soundness, resource handling and cryptographic source binding. None is inferred from this successful process experiment.

## Installed LRAT
Std.Tactic.BVDecide.LRAT.check_sound proves successful checking implies UNSAT of its typed CNF. Axiom audit: propext, Classical.choice, Quot.sound.
The spike uses exact typed contradictory unit clauses [(0,true)],[(0,false)] and a parsed text certificate '3 0 1 2 0'. The installed conversion increments zero-based variables to DIMACS numbering and prepends the clause-index sentinel; this mapping was inspected.
Runtime positive, satisfiable-CNF, invalid-hint and malformed-text controls are included. A shortened hint list was genuinely valid for this example; it is not counted as a refusal.
Plain decide, decide +kernel and bounded full-definition import attempts did not reduce the checker at this pin. The preserved failed experiment is reproduction data, not an admitted theorem or a global impossibility result.
The successful native_decide theorem adds nativeCheck._native.native_decide.ax_1_1. Native UNSAT therefore depends on compiler/runtime plus that generated Boolean-result axiom. Module rechecking accepts declared axioms; it does not discharge this axiom.
This is a usable native LRAT evaluation candidate with explicit trust, not an axiom-free LRAT replay claim. Arbitrary DIMACS ingestion, census-to-CNF encoding correctness/completeness, DRAT conversion, large-certificate performance and independent checker admission remain outside this miniature spike.

## Mathlib binding
The separate pinned package formalizes actual GP-A08b/GP-A05 obligations. Its own report records exact Mathlib/dependency pins, theorem hypotheses, positive contrasts, axioms and timings. New module kernel replay does not recheck every imported Mathlib declaration. Cached dependencies are distinguished from a clean dependency build.
Neither a theorem pointer nor matching typeclass names implement GP's statement/input/hypothesis/scope binding. G1 must decide and specify that layer.

## Corpus preservation and performance interpretation
The 459-case-sized load test binds case IDs/digests to deliberately trivial equalities. It measures serialization/fold plumbing, not the mathematical cases or harvested exports. Full oracle replay is unchanged. Unsupported routes/formats remain unsupported.

## Phase 2 native receipt path — 2026-09-30

The Mathlib-free test stub decodes actual univariate rational generators, targets and cofactors, then recomputes coefficient identities. Lean proves receipt acceptance yields the uniquely registered clause’s formal polynomial-span meaning with exact claim/version/binding equality. The receipt-only fold-to-formal-span composition is proved: held claims have registered true formal-span clauses, and warrant-ID uniqueness follows from actual resolution. Generic runtime truth still uses explicit validator and projection contracts; whole-profile scope/rule semantics remain open.

The host adapter must faithfully translate the original fixture contract, select identities, hash the configured data, invoke the pinned compiled executable and interpret its output. Digest strings are compared inside Lean; Lean does not establish their relationship to original bytes or intended meaning. Native execution relies on the Lean compiler/runtime, rational implementation, operating system and executable/input integrity. Independent leanchecker replay checks proof declarations, not those host assumptions.

Raw registry/events reject duplicate keys, malformed fields/types and unknown constructors. Theorem pointers, proof/rule/narrow capabilities are refused in the receipt-only registry. No geometric interpretation, general profile adoption or native LRAT admission is supplied by this formal span stub. Earlier Phase 0 observations above retain their historical scope.

## Phase 2 scoped runner

ScopedSpan derives both replay clauses and semantic clauses from the same decoded rows. Its concrete fold-to-registered-meaning theorem discharges receipt truth through exact Rat replay and narrowing through the actual statement/inclusion checks. Scope IDs denote finite named test contexts; Holds is the formal polynomial-span predicate, independent of context. They do not encode fields or geometric regions. Selected object labels are part of statement equality. Host byte/digest fidelity and intended interpretation remain adapter contracts.

ScopedRunner uses the same admission for held and why-not. Caller claimed keys, obligation links and open IDs affect earned reporting only. Proof and general rule capabilities refuse; conflict detection is not implemented in this stub. The receipt-only runner retains its earlier capability boundary.

## Phase 2 checked cover path

Registry schema 3 adds cover rule names, destinations and ordered premise-claim lists. Actual finite context coverage is recomputed; no caller success flag supplies coverage or branch truth. Runtime resolves exact premise-warrant IDs and proves those premise records belong to the snapshot. The combined receipt/cover/narrowing fold-to-registered-meaning theorem discharges these admission contracts and derives ID uniqueness. This remains the formal Rat/named-context stub; conflict/release handling and faithful translations of conditional geometric fixtures are separate work. Schema 2 continues to refuse general rules.


## Phase 2 release review

Generic Conflict uses the profile's sound contradiction test and an Overlap checker that returns an actual shared context with a proved membership contract. Review pairs supported, exactly bound warrants and preserves the complete runtime state. A confirmed conflict excludes joint semantic truth; unknown overlap does not freeze release. ScopedRunner invokes this review separately from held/why-not/earned. The positive-only rational stub declares no contradictory pairs, so its production findings are empty. Test-only compromised admission exercises the alarm; it is not an admitted checker or a real corpus conflict pass. Full provenance adapters retain mismatches and complete current/stale records; native replay, rather than historical backend descriptors, supplies identity authority.


## Approved conditional fixture harness

A16 uses a separate test-only interpreter with arbitrary parent and branch predicates over every point type. Its explicit theory hypotheses are the supplied branch-emptiness and exhaustive-cover premises. Exact bound assumption warrants are sound within that theory; the checked two-premise rule proves parent emptiness. Lean proves the actual validator and arbitrary-event fold sound, including warrant-ID uniqueness from resolution. Host SHA-256 binds unchanged source bytes to input/scope identity. Native decoding rejects unknown input fields and wrong types. Expected verdict metadata supplies no authority. Conditional corpus passes establish the stated inference under its named premises, without certifying those premises' algebraic truth or adopting a production profile.

Named partition fixtures X183/X184/X186 use the same conditional boundary with explicit parent/left/right predicates. Coverage is a separate assumption warrant, and the actual composition rule requires its exact ID and full record in the dependency list. Missing branch premises produce no records. Held coverage omitted from the argument does not authorize parent emptiness. Actual validator/fold soundness is proved over arbitrary events and interpretations satisfying the named assumptions; no production profile is adopted.

Conditional route fixtures X177/X178 preserve two fixed predicate identities while the existing acceptsNarrow checker restricts loose/side scopes to tight under explicit inclusion hypotheses. The exact join additionally requires both literal routes to be licensed. Its conclusion includes licensing globally, so empty regions cannot erase an absent route. Native execution instantiates Point with Unit; admission_point_independent and native_fold_held_sound transfer the exact executable fold to arbitrary point types. This remains test-only conditional interpretation, with host byte/digest fidelity and no production profile adoption.

Conditional point-route fixtures X179/X180 retain a named exhibited SIDE witness. Its SIDE and TIGHT membership are distinct global statements; K2 cannot change that selected model identity. The supplied universal predicate genuinely narrows through acceptsNarrow. Lean proves the actual validator/fold sound over arbitrary point types under explicit universal truth, SIDE membership and inclusion hypotheses, plus a countermodel with empty TIGHT. Separate accepting controls add TIGHT membership for that same witness, with an inhabited interpretation; they do not validate lifting from inclusion alone. Execution uses the pinned Lean runtime. Direct compilation and independent kernel checking are bound to local dependency, harness and toolchain hashes. This remains conditional test-only interpretation; no underlying algebraic certification or production profile is admitted.

Recorded-use coverage fixtures X193–X198 check finite inventory containment in Lean: construction and conclusion indices are combined separately for each asserted dimension. General checker/missing-set theorems and actual validator/fold soundness prove that held coverage covers those recorded labels. Complete literal serialization and host SHA-256 bind receipts and the two-premise join; expected verdict metadata supplies no authority. Empty recorded uses make this structural obligation vacuous, without establishing discovery of all real uses or sufficiency of represented components. Labels remain exact; infinity and inf are distinct. This is a test-only finite structural contract, with the pinned Lean runtime and independently checked compiled declarations, not mathematical profile adoption.

Conditional admission fixtures A27 (six variants) bind named synthetic admitted-check and successful-check hypotheses for one fixed field and candidate object. Lean proves the actual validator/fold sound under those explicit hypotheses: held targets are the exact full claim, unconditional or restricted to a GRH context, never global truth. GRH_cannot_be_dropped and quotient_does_not_imply_full keep narrowing directional. Heuristic and producer-label variants supply no authority. Complete literal serialization and host SHA-256 bind the claim digest, scope and contract versions; expected verdicts supply no authority. No class-group arithmetic, real checker admission or profile adoption is certified, and frozen oracle observations remain UNSUPPORTED. Compilation and independent kernel checking are bound to the normalized harness, with only standard axioms.
