# Grand Portage: Design Direction

## Toward a proof-carrying transport calculus and event-sourced authority system for computational mathematics

**Status:** living design and prior-art memo

**Original date:** 2026-07-27

**Last reassessed:** 2026-09-12

**Project state:** originally written against v0.3; reassessed after v0.32.0 and
the Match4 hardening pass

**Purpose:** preserve the architectural thread while the implementation settles.
Nothing here is a commitment. Version numbers in the roadmap are candidate
release boundaries, not promises.

---

## Executive summary

Grand Portage is more than a checker wrapped around a computer algebra system.
The strongest current interpretation is:

> **Grand Portage is a proof-carrying transport calculus for computational
> mathematics, coupled to an event-sourced authority system.**

From the programming-languages side, this is nearly literal predicate-transformer
language: model transformations play the role of programs, mathematical claims
play the role of predicates, and checked evidence earns the capabilities needed
to transport those claims. The implementation today remains deliberately narrower:
its authority-bearing kernel is exact-affine, with adjacent family, selected-real,
and operational surfaces kept at explicit boundaries.

The operational loop is **CEGAR-shaped**: compute, type the transformation, localize a refusal, refine or re-derive, and replay. The relaxation fragment is partly **abstract-interpretation-shaped**. The implementation mechanism resembles an **effect-and-capability system**, where an operation's effect records what was lost and evidence capabilities determine what survives that loss. The certificate boundary aspires to **LCF-style discipline**, where strong conclusions can only be constructed from values minted by trusted verifiers. The graph is also beginning to behave like a **module system**, with models exposing interfaces, claims acting as exports, and derivations serving as implementations.

None of those analogies is the whole identity. The useful synthesis is:

- **Compiler architecture** explains the missing frontend: structured objects, semantic elaboration, a typed intermediate representation, backend emission, and good errors.
- **Predicate transformers and transport calculus** explain the mathematical
  kernel: forward and backward claim transformers, claim variance across model
  changes, partitions, field changes, closure operations, and descent.
- **CEGAR** explains the research loop: a refusal should identify the admissible refinement, and an unrelated retyping must not count as repair.
- **Effect systems** explain enforcement: every transformation declares what it loses, and those effects compose through joins.
- **LCF** explains the trust root: certificate scope should derive from verifier-produced capabilities, not caller-supplied labels.
- **Truth maintenance** explains immutable alternatives, support environments,
  staleness, supersession, and minimal proof slices; GP adds a semantic variance
  law to each support edge.
- **Provenance and workflow standards** explain interoperability and packaging, but not mathematical licensing.

The highest-leverage direction is therefore not more checker rules. It is an
**authority-centered semantic frontend** with:

1. one authority-binding boundary between checked evidence and current graph
   authority;
2. operation semantics compiled from capabilities rather than an expanding list
   of nominal edge types;
3. a tiny typed claim IR, followed only as needed by a typed CAS IR;
4. structured coefficient domains, rings, models, maps, and operations;
5. a separation between propositions and the evidence objects that support them;
6. explicit semantic regimes and explicit cross-regime conversions;
7. model interfaces distinct from private implementations;
8. first-class external derivations instead of conclusions hidden in notes;
9. positive user-facing proof slices and authority diffs;
10. standards adapters around the native graph rather than standards inside the
    kernel.

The core should remain narrow. The initial target is **CAS-backed polynomial-system campaigns centered in characteristic zero**, including controlled base change, elimination, saturation, case partitions, and finite-field reconnaissance. Grand Portage should not try to become a general theorem prover, a universal language for mathematics, or a replacement for Singular, Sage, or Macaulay2.

The current candidate release sequence is:

1. keep the Match4 `gp review`, witness-symbol refusal, and zero-ring diagnostic
   as post-v0.32 hardening; they do not change mathematical authority;
2. use v0.33 for an output-preserving extraction of the authority-binding nucleus;
3. use v0.34 / kernel epoch 12 for the already-gated field-reach and
   family-to-model composition work, compiling rules from checked capabilities;
4. add minimal proof slices and authority-aware diffing after the receipt boundary
   gives them one source of truth;
5. introduce typed claim fragments and explicit regime boundaries only where the
   family/model bridge and subsequent live campaigns force them.

---

## 1. Scope, thesis, and non-goals

### 1.1 The narrow thesis

The project should be scoped as:

> **A semantic frontend and transport checker for computational research pipelines in which polynomial-system models are repeatedly transformed, relaxed, projected, specialized, partitioned, and recombined.**

That scope is large enough to include the current Jacobian work, matroid realizability, algebraic statistics, reaction-network steady states, symbolic elimination, base-field transfer, and CAS-to-proof-assistant bridges. It is narrow enough that the system can know what the likely operations are and provide useful, specific failures.

The phrase "math exploration" is too broad. Friendly compiler errors require a partially closed world: the system can say "this is an image closure, so a closure point need not lift" only because it knows the operation and the relevant claim polarity. It cannot provide equally sharp guidance for arbitrary mathematics without becoming a theorem prover.

### 1.2 What Grand Portage should not become

Grand Portage should not attempt to be:

- a replacement CAS;
- a general theorem prover;
- a universal ontology for mathematical knowledge;
- a generic provenance database;
- an LLM-based authority on soundness;
- a workflow engine that owns scheduling, clusters, containers, and every backend;
- a proof of completeness for a research campaign;
- a guarantee that missing equations or missing model components have been discovered.

The existing project statement remains the right boundary:

> It routes attention to where mathematics is missing. It does not find the missing mathematics.

### 1.3 The trust boundary

The trusted core should be small and deterministic:

- semantic object validation;
- transport rules;
- partition rules;
- certificate capability derivation;
- graph folding and referential integrity;
- artifact verification;
- finding derivation and obligation inheritance.

The LLM belongs outside that boundary. It is the proposal, search, explanation, and repair policy. It may choose an operation, suggest a refinement, fill in a model declaration, or write a proof attempt. It does not decide whether the operation actually had the claimed semantics or whether the resulting evidence supports the conclusion.

---

## 2. The framing: a typed semantic frontend

### 2.1 The Elm analogy, refined

The useful design-room analogy is:

> **Grand Portage aims to be to Singular, Sage, and Macaulay2 what a typed frontend is to a lower-level execution target.**

Elm is a productive reference because it combines a constrained language, strong compiler guidance, a prescribed control loop, and carefully bounded interoperation. The analogy is not a claim that Grand Portage should reproduce Elm's language, governance, or ecosystem.

A precise public phrasing is better than "Elm for math":

> **Grand Portage is a typed semantic frontend for CAS-backed polynomial-system campaigns, with existing CASs as execution backends.**

The phrase "make the bad program inexpressible" should also be narrowed. Grand Portage cannot make false mathematics inexpressible. It can plausibly make certain unsupported transitions and silent seam errors difficult or impossible to express through supported paths:

- a CAS computation that produces a model without declaring its relation to the source;
- an emptiness claim with no evidence capability;
- an inference whose premises do not meet at a common model;
- a branch result generalized to a parent without an exhaustive partition;
- a supersession that routes around an inherited obligation;
- a raw solver program that bypasses identifier and output validation.

That is already an ambitious and valuable target.

### 2.2 What to copy from Elm

Three Elm ideas are worth keeping:

| Elm idea | Grand Portage interpretation | Design consequence |
|---|---|---|
| Constrained frontend | A typed algebraic IR instead of arbitrary solver strings | Unsupported solver programs become unrepresentable through normal APIs |
| Errors teach the next move | Refusal-to-discharge mapping | Keep discharge mostly declarative and local |
| Strong boundary to foreign code | First-class external derivations and explicit adapters | Outside work enters through typed ports rather than prose leaks |

A fourth idea needs reinterpretation. The Elm Architecture does not remove application-specific modeling; it standardizes the control loop around that modeling. Grand Portage already has a recognizable loop. What is missing is not one universal `Model/Update/View` shape, but reusable **campaign profiles**, **operation specifications**, and **read surfaces**.

### 2.3 Caution from the analogy

A constrained core can create ecosystem friction if every backend, domain extension, or escape hatch must be implemented centrally. Grand Portage should therefore be strict about semantic licensing but open about execution and interchange:

- small native kernel;
- versioned operation and adapter interfaces;
- multiple backend implementations;
- explicit external derivations;
- standards-based export and packaging;
- no requirement that every collaborator expose private derivations.

The safety should come from the boundary contract, not from owning the whole world.

---

## 3. Architecture, read as a compiler

### 3.1 The current imbalance

The checker and transport table are the most mature parts of the project. The frontend is mostly MCP schema, free-text descriptions, and caller-supplied classifications. That is backwards for a system whose largest open risk is induced mislabeling.

A checker can only validate what its input representation makes comparable. When fields, rings, ideals, maps, and certificate kinds are strings and booleans, many of the most important declarations are checked only against themselves.

### 3.2 The proposed pipeline

```text
Surface API / MCP request / project file
                 |
                 v
          Name resolution
                 |
                 v
       Semantic elaboration
  domains, rings, models, maps, operations
                 |
                 v
      Typed mathematical core IR
                 |
                 v
       Backend compilation/emission
      Singular first; others by adapter
                 |
                 v
   Execution + output/artifact verification
                 |
                 v
     Semantic graph + execution graph
                 |
                 v
  Transport checking + obligation generation
                 |
                 v
       LLM/human repair and replay
```

This separates several jobs that the earlier "canonicalization" label bundled together.

### 3.3 Name resolution versus semantic elaboration

**Name resolution** makes identities comparable:

- which variable is meant;
- which model or claim an identifier names;
- which external artifact an import refers to;
- which namespace owns a declaration.

**Semantic elaboration** constructs mathematical objects:

- a rational field or number field rather than free text;
- a polynomial ring with variables and term order;
- an ideal and open conditions;
- an explicit field embedding;
- a polynomial or rational map;
- a declared operation such as elimination, saturation, specialization, or adding equations.

The missing stage is primarily semantic elaboration, not merely canonical naming.

### 3.4 Candidate core objects

```text
CoefficientDomain
    RationalField
    NumberField(minimal_polynomial, chosen_embedding)
    FiniteField(characteristic, degree)
    SymbolicExtension(base, generators, relations)

Ring
    coefficient_domain
    variables
    term_order
    grading

Model
    ambient_ring
    equations
    open_conditions
    chart
    parameters

Map
    source_model
    target_model
    coordinate_expressions
    denominator_conditions

Operation
    AddEquations
    DropEquations
    Eliminate
    Saturate
    Radicalize
    BaseExtend
    Specialize
    ChangeCoordinates
    FormBranch
    CloseImage

Claim
    proposition
    model
    scope

Evidence
    artifact
    verifier
    capability

Justification
    premises
    conclusion
    rule
    engine
    bindings
```

These do not all need to ship at once. Structured coefficient domains, rings, polynomial expressions, ideals, and operation constructors are the first useful slice.

### 3.5 Derive transport from operations, not endpoint guesses

Structured endpoints are necessary but insufficient. Two models may differ in several ways at once: a run might extend the field, eliminate variables, saturate by a nonvanishing condition, and change coordinates.

Therefore the frontend should not infer the full relation merely by comparing source and target models. Instead:

1. a trusted operation constructor declares the mathematical operation;
2. that constructor derives a candidate transport contract;
3. the source and target objects are checked for coherence with the operation;
4. the compiled backend program is derived from the same operation value;
5. the resulting graph edge is generated rather than separately restated.

For example:

```text
BaseExtend(source_model, target_domain, embedding)
    -> candidate transport: BASE_EXTENSION

Eliminate(source_model, variables)
    -> candidate transport: IMAGE_CLOSURE

AddEquations(source_model, equations)
    -> candidate transport: NECESSARY_CONDITION
       with refinement = true and edge new -> old
```

The key benefit is not convenience alone. The transport declaration and the emitted computation come from the same semantic value, so they cannot silently drift.

### 3.6 Build small IRs before a language

The first IR should type the semantic fragments that Grand Portage transports,
not reproduce a CAS AST or a miniature proof assistant:

```text
RingContext
FieldContext
Expression[Context]
Equation[Context]
Predicate[Context]
Point[Model]
FamilyPredicate[Family]
```

This addresses a defect the Lean shadow exposed: some runtime gates ask whether
an expression is defined over a coefficient field only because the string-based
representation permits an ill-typed expression to be stated there. A small typed
claim IR can make such errors unrepresentable while retaining opaque payload escape
hatches.

A separate execution IR and builder API can then cover only the backend operations
that have earned support:

```text
PolynomialExpr
RingDecl
IdealExpr
GroebnerBasis
NormalForm
Saturation
Elimination
Resultant
OutputDecl
```

Compile that subset to Singular. Later backends implement only the operations whose
semantics they can faithfully support. The claim IR should not wait for, or grow
to the size of, the execution IR.

This avoids prematurely owning:

- parser syntax;
- editor tooling;
- package management;
- a general-purpose programming model;
- every feature of Singular or Macaulay2.

### 3.7 Emission makes provenance cheap, not automatic

Owning the IR makes the exact generated program available. It does not make the whole execution provenance free. A load-bearing run still needs:

- backend and version;
- command-line options;
- exact input and output digests;
- resource limits and timeout outcome;
- parser/verifier version;
- environment identity;
- execution status;
- the graph events produced.

The right architecture has a semantic graph and an execution/artifact graph that are linked but not conflated.

---

## 4. The semantic core: transport, effects, capabilities, and refinement

### 4.1 No single borrowed framework explains the whole system

The stronger prior-art map is:

| Family | What it explains | What Grand Portage adds |
|---|---|---|
| Predicate transformers, refinement calculus, dynamic logic | Relations/programs induce forward and backward transformations of predicates | Mathematical model changes, multiple claim sorts, and evidence-conditioned capabilities |
| Institutions and logical frameworks | Signatures, models, sentences, translations, satisfaction invariance | Deliberately lossy transformations and partial transport rather than invariance |
| ATMS and truth-maintenance systems | Justifications, assumption environments, alternatives, inconsistency, dependency maintenance | A mathematical variance law and semantic scope on every support edge |
| Certifying algorithms, skeptical checking, proof-carrying code | Untrusted producer plus independently checkable evidence | Binding evidence to the current model, inputs, interpretation, and transport law |
| Translation validation | Validate each concrete transformation rather than the transformer implementation | Validate which capabilities a deliberately lossy transformation earns, not only equivalence |
| Abstract interpretation and CEGAR | Approximation, precision loss, refusal, admissible refinement, replay | Base change, descent, partitions, evidence, and claim-specific variance |
| Effect and capability systems | Declared loss, required capability, composition failure | The mathematical reason a capability licenses a particular claim transport |
| LCF | Trusted constructors for theorem-like evidence | Event-sourced authority, computational artifacts, and model binding |
| PROV, in-toto, and SLSA-style attestations | Lineage, artifact identity, execution metadata, integrity, policy | What a mathematical result is permitted to imply |
| Assurance cases and SACM | Claims, evidence, arguments, defeaters | Executable rules for sound mathematical transport |
| Provenance semirings | Compositional dependency provenance | Refusal, partiality, semantic variance, scope, and certificate applicability |
| Module systems | Interfaces, private implementations, composition | Claim variance across model transformations |

This is a composition claim, not an absence or novelty claim. Grand Portage should
use each family where it fits and should not imply that a literature search proved
that no equivalent system exists.

### 4.2 Predicate-transformer logic is direct prior art

For a point relation `R` from a source model to a target model, the Lean shadow
defines the relational image and universal preimage:

```text
exists_R(P)(y) = exists x. P(x) and R(x, y)
forall_R(Q)(x) = forall y. R(x, y) implies Q(y)
```

and proves their adjunction. This is the strongest-postcondition /
weakest-precondition shape from predicate-transformer semantics, even though a GP
operation is a mathematical relaxation, closure, field change, restriction, or
cover rather than an executing CAS command. The analogy is the relational logic of
information flow, not a claim that model transformations are ordinary programs.

### 4.3 Truth maintenance is direct lifecycle prior art

An assumption-based truth-maintenance system preserves justifications under
multiple assumption environments and retains inconsistent alternatives instead of
destructively retracting them. Grand Portage's immutable history, supersession,
stale dependencies, partitions, doubts, open premises, carried debt, and multiple
derivations of one conclusion belong in that neighborhood.

The difference is load-bearing: support alone does not license a GP conclusion.
Each dependency has a semantic variance law, scope, and evidence contract. ATMS
techniques are therefore candidates for minimal/current support environments,
incremental invalidation, conflict sets, and proof slices—not a replacement for
the transport kernel.

### 4.4 The relaxation fragment is abstract-interpretation-shaped

Some current relations are naturally read as precision relations:

- `NECESSARY_CONDITION` produces a looser model by dropping constraints;
- `IMAGE_CLOSURE` replaces an exact constructible image by a closed over-approximation;
- coverage checks detect dimensions along which an abstraction declares no structure;
- refinement adds precision and should not reopen an empty branch.

This is strong prior art for reasoning about sound approximations and precision. It should inform the formal model of the relaxation fragment.

It should not swallow the whole design. `BASE_EXTENSION` changes coefficient domains; `SPECIALIZATION` relates different fibers; partitions reason over alternatives; identities travel contravariantly through coordinate rings. These require a broader transport calculus.

### 4.5 The operational loop is CEGAR-shaped

Grand Portage is not classical CEGAR because it does not yet synthesize abstract predicates or refinements automatically. The useful loop is nevertheless clear:

```text
compute
  -> type the transformation
  -> attempt to transport a claim or evidence object
  -> localize the refusal
  -> identify an admissible discharge
  -> derive / refine / retype / accept
  -> replay
```

The important v0.3 advance is that the obligation now constrains what counts as repair. If an obligation admits only `DERIVE`, declaring a more permissive parallel edge must not clear it. That is the genuinely CEGAR-like step: refinement is not just new state; it is a response to a specific counterexample or insufficiency.

### 4.6 Effects record loss; capabilities justify survival

The implementation analogy closest to the current mechanism is an effect-and-capability system.

An operation has a semantic effect:

```text
Eliminate      ! loses exact image / retains closure
DropEquations  ! loses constraints
BaseExtend     ! enlarges coefficient domain
Specialize     ! changes characteristic
Saturate       ! removes components / changes coordinate ring
```

A claim or evidence object carries capabilities:

```text
SchemeScopedEmptiness
FieldRelativeEmptiness(Q(sqrt(17)))
PointWitness(model, coordinates)
ClosedPredicate
AmbientIdentity
DerivedIdentity
DefinedOverBaseField
IntegralAtPrime(p)
RingIsomorphismWitness
```

The transport rule asks whether the capability is sufficient for the effect and direction.

This is no longer only a future formulation. Point transport already compiles the
surface edge types from relation totality and point-surjectivity plus a few
operation-specific refinements, while identity transport remains separate because
point semantics do not determine equality in coordinate rings. The Lean shadow
independently derived the same split.

The six current edge types should remain useful user-facing constructors, but new
operations should be admitted by specifying their point relation, contravariant
expression map, definedness, preserved extra structure, scope transformation, and
coverage contract. Evidence then establishes capabilities such as totality,
surjectivity, ideal carrying/reflection, predicate correspondence, or cover
exhaustiveness. Do not add a seventh type merely because a new operation resembles
an old one.

### 4.7 Partitions are not transport edges

The branch failure in the first live runs has already answered one important question: the next earned concept was not a sixth lossy edge type. It was a new inference form.

A branch is a piece of a parent:

```text
branch = parent AND branch_condition
```

A result on one branch does not transport to the parent. A result on every branch plus an exhaustiveness claim may support a joint conclusion. That is a partition rule, not an edge cell.

This distinction should guide future growth. When a new failure appears, first ask whether it demands:

- a new relation type;
- a new claim or evidence distinction;
- a new composition rule;
- or a new model constructor.

Do not reflexively add edge types.

### 4.8 Split propositions from evidence

The current `NONEMPTY` kind deliberately means an exhibited witness because existential nonemptiness and a particular witness transport differently through image closure. That is a sign that proposition and evidence are conflated.

A cleaner model is:

```text
Claim:
    ExistsPoint(M)

Evidence:
    PointWitness(M, p)
```

For a constructible image and its closure:

- `ExistsPoint(closure)` implies `ExistsPoint(image)` because the closure of an empty set is empty;
- a particular `PointWitness(closure, p)` need not lift to a witness of the image.

The proposition transports; the witness does not.

The same split generalizes:

| Proposition | Possible evidence |
|---|---|
| `Empty(M)` | unit ideal certificate, nonzero resultant, valuation collision |
| `ExistsPoint(M)` | point coordinates, parameterized family, external theorem |
| `Identity(M, lhs, rhs)` | ambient normalization, ideal-membership reduction |
| `Predicate(M, P)` | symbolic derivation, theorem citation, exhaustive check |

This suggests two related judgments:

```text
claim transport: what propositions remain true?
evidence transport: what evidence objects can be transformed or reused?
```

A claim/evidence split could remove known conservatisms while making certificate verification uniform. It is a major conceptual change and should be prototyped in a branch against existing fixtures before becoming the core representation.

### 4.9 Make the LCF analogy real

The rule "scope is derived, never declared" is an excellent policy. Since the
original v0.3 memo, the built-in exact verifier paths have moved materially toward
the LCF target: a declaration or standalone evidence report does not mint graph
authority, and current verifier verdicts bind exact receipts to graph subjects.
The remaining risk is that this binding responsibility is distributed rather than
represented by one unforgeable internal value.

The target is verifier-produced evidence values:

```text
VerifiedUnitIdealCertificate
VerifiedNonzeroResultantCertificate
VerifiedValuationCollisionCertificate
VerifiedPointWitness
VerifiedIdentityReduction
AssumedCertificate
```

Only trusted constructors can mint the verified forms:

```python
cert = verify_unit_ideal(run_artifact)
claim = empty_claim(model, cert)
```

The claim's scope then derives from the capability of `cert`, not from a free string.

Unchecked or external evidence remains representable, but it must carry its authority explicitly:

```text
AssumedCertificate(authority, artifact, stated_kind)
```

Downstream conclusions remain conditional on that assumption rather than silently acquiring scheme scope.

Certifying algorithms and proof-carrying code sharpen this boundary. They justify
trusting a checked output without trusting its producer, but acceptance of a
certificate is still not the same as authority in Grand Portage. The evidence must
also be bound to the exact model, current inputs, interpretation, scope, dependency
generation, and applicable transport law. Translation validation supplies the
matching backend posture: validate each concrete CAS-produced transformation or
receipt, rather than attempting to verify Singular or the discovery procedure.

### 4.10 Make authority binding an actual nucleus

The transition from checked evidence to current persisted authority is the most
important architectural seam and is currently distributed across storage,
checking, verification, operations, and provenance code. Extract an internal,
non-user-mintable receipt with at least:

```text
AuthorityReceipt
    proposition or licensed capability
    subject/model fingerprint
    interpretation/context fingerprint
    evidence contract and version
    checker identity and version
    checked premises and dependencies
    semantic scope
    source and artifact digests
    kernel epoch
```

There should be one conceptual operation:

```text
bind(CheckedEvidence, Context) -> AuthorityReceipt | Refusal
```

Search backends, certificate producers, CLI code, and administrative acceptance
must not construct this value directly. The v0.33 extraction should preserve
current judgments and serialized graph behavior; its purpose is to turn the
project's central trust-boundary sentence into a type boundary before epoch-12
certificate reach and family/model composition increase the state space.

### 4.11 The emerging formal object has five layers

The implementation now points to a smaller meta-structure than its product
surface suggests:

1. **Contexts/models** fix point universes, coefficient domains, coordinate
   algebras, guards, and selected structures. A chosen real embedding and a
   field-relative certificate scope are distinct axes.
2. **Model transformations** may carry a relation on points, a partial
   contravariant map on expressions or rings, a definedness/localization
   condition, and preservation of extra structure. Checked evidence establishes
   capabilities of these components.
3. **Claims indexed by contexts** already form multiple sorts: point existence,
   emptiness, universal predicates, and coordinate-ring identities live over
   models, while `COUNT` lives over a family.
4. **Evidence as capability proof** establishes a narrow proposition—ideal
   membership, point surjectivity on a locus, map equivalence, certificate
   stability, or enumeration exhaustiveness—before binding derives authority.
5. **Authority maintenance over time** records current, stale, superseded,
   unverified, carried, and open states. These are states of authority records,
   not truth values of mathematical propositions.

In categorical language this suggests indexed predicates or a hyperdoctrine,
relations with adjoint predicate transformers, contravariant algebra maps, and
multi-arrow cover structure. Those are explanatory targets and possible
compression theorems, not a reason to design a general "Grand Portage
bicategory" ahead of runtime evidence.

---

## 5. The graph as a semantic module system

### 5.1 The interface/implementation split already exists informally

The public fixtures cite derivations that live in a private research repository. Downstream work consumes the stated claims without seeing the entire implementation. That is already an interface/implementation boundary performed by convention.

Making it explicit would enable:

- public campaign interfaces with private derivations;
- alternative implementations of the same result;
- collaborator boundaries;
- blind trials without exposing hidden answer keys;
- substitution of a CAS certificate with a Lean proof or independent implementation;
- reusable modules across campaigns.

### 5.2 Model interfaces

A model interface should declare:

- its structured signature: coefficient domain, ring, variables, parameters, charts;
- assumptions and open conditions;
- exported claims;
- the evidence capabilities supporting each export;
- unresolved or carried obligations;
- version and content identity;
- admissible extension points.

Example:

```text
ModelInterface Gamma3Window
    domain: Q
    ring: Q[a,b,m10,...]

    assumptions:
        a != 0
        3ab + 1 = 0

    exports:
        CL-G3-EMPTY:
            proposition: Empty(Gamma3Window)
            evidence: SchemeScopedEmptiness

        CL-G3-CAP:
            proposition: ForAllPoints(deg_y(C_-k) <= k+2)
            scope: Gamma3Window only

    carries:
        OBL-GAMMA-TRANSFER
```

### 5.3 Implementations and sealing

An implementation contains:

- the operations and computations;
- private intermediate models;
- evidence artifacts;
- source citations;
- external derivations;
- justifications;
- accepted debts.

"Sealing" verifies that the implementation supports the exported interface:

- every exported claim has an admissible justification;
- every evidence capability is verified or explicitly assumed;
- no private obligation silently invalidates a public export;
- scope and model identity match;
- dependencies are pinned.

Another implementation can satisfy the same interface using a different backend or proof method.

### 5.4 Alternative justifications for one claim

The current graph should move toward a structure inspired by PML's `NodeSet` and `InferenceStep` distinction:

```text
ClaimContent
    canonical proposition

ClaimOccurrence
    content
    model
    scope

Justification
    conclusion
    premises
    rule
    engine
    bindings
    evidence artifacts
```

One conclusion can then have multiple justifications:

- Singular unit ideal;
- Macaulay2 independent computation;
- a Lean proof;
- a published theorem;
- a human derivation.

This gives a mechanical basis for "independently audited" rather than an unvalidated ladder label. Independence can be analyzed by comparing engines, implementations, and shared ancestors.

### 5.5 Institution theory as deeper prior art

Institution theory abstracts a logical system into signatures, sentences, models, and a satisfaction relation stable under change of notation. That vocabulary is unusually close to the module direction:

| Institution-style concept | Grand Portage analogue |
|---|---|
| Signature | domain, ring, variables, sorts, notation |
| Sentence | claim proposition |
| Model | algebraic model or solution object |
| Satisfaction | claim holds in model |
| Signature morphism | variable change, embedding, projection |
| Theory/view | model interface and relation |
| Architectural specification | interface plus implementations |

Grand Portage should not adopt CASL wholesale, but institution theory is valuable prior art for truth preservation under representation change and for structuring large specifications from smaller ones.

---

## 6. Campaign architecture: profiles, not one universal TEA

### 6.1 Grand Portage already has a control loop

The project has a stable operational shape:

```text
inspect campaign state
  -> choose a model operation
  -> execute and record artifacts
  -> declare or derive claims
  -> type-check transports and joins
  -> inspect live obligations
  -> discharge, carry, or branch
  -> merge and repeat
```

The missing piece is not an abstract control loop. It is a reusable vocabulary for common campaign forms and a read surface that makes the current state intelligible.

### 6.2 Decompose the "95% modeling" cost

The reported split between modeling and typing should be instrumented more carefully. It likely combines:

1. discovering the mathematical objects;
2. discovering the real transformation between them;
3. clerically encoding already-understood objects;
4. assigning transport/evidence types;
5. repairing a refusal;
6. explaining state to the next agent.

A semantic frontend can reduce the clerical parts. It cannot and should not erase the research work of identifying the right models and transformations.

The decision to prescribe more campaign architecture should depend on which costs remain after structured objects and operation constructors land.

### 6.3 Optional campaign profiles

Before a universal architecture, define optional profiles that supply defaults and expected operations:

- **Elimination Campaign** - source ideal, projection, closure, lift obligations;
- **Case-Split Campaign** - parent, exhaustive partition, branch claims, recombination;
- **Base-Field Transfer Campaign** - field embeddings, relative/scheme claims, descent obligations;
- **Finite-Field Reconnaissance Campaign** - specialization runs explicitly barred from closing characteristic-zero cases;
- **Certificate Replay Campaign** - imported algebra, exact input assumptions, scope and transfer checks;
- **Formalization Bridge Campaign** - CAS artifact -> verified lemma -> proof assistant conclusion.

Profiles should improve ergonomics without adding kernel authority. A campaign can opt out or combine them.

### 6.4 Graduation criteria

Do not wait for an arbitrary number such as exactly ten campaigns. Promote a recurring shape into required architecture when:

- it appears across at least three genuinely different domains;
- independent operators use it successfully;
- several consecutive campaigns require no new top-level semantic construct;
- most operations fit existing operation specifications;
- encoding cost falls without hiding mathematical assumptions;
- adversarial trials do not discover a routine bypass.

---

## 7. External derivations: design the port

### 7.1 Notes are not a sufficient boundary

Mathematicians will always do work outside the supported system:

- a paper proof;
- a published theorem;
- a one-off script;
- an unsupported CAS;
- visual inspection;
- a finite hand check;
- a domain expert judgment;
- a numerical experiment;
- an explicit working assumption.

Trying to prohibit this would make the tool unusable. Letting conclusions enter as `note` events makes the semantic graph fictional.

### 7.2 First-class external derivations

Add a typed construct such as:

```json
{
  "ev": "external_derivation",
  "id": "XD-17",
  "premises": ["CL-A", "CL-B"],
  "conclusion": "CL-C",
  "method": "HUMAN_PROOF",
  "authority": "Will Strinz",
  "evidence": {
    "artifact": "proof-note.pdf",
    "digest": "sha256:...",
    "locator": "Lemma 4"
  },
  "assumptions": ["characteristic zero", "a != 0"],
  "verification": "UNVERIFIED"
}
```

Candidate methods:

```text
PUBLISHED_THEOREM
HUMAN_PROOF
EXTERNAL_CAS
NUMERICAL_EXPERIMENT
FINITE_MANUAL_CHECK
ORACLE
ASSUMPTION
```

### 7.3 Authority is part of the type

An external derivation is not simply "untyped." Its authority and verification status determine what it may support:

- `VERIFIED_BY_LEAN`;
- `INDEPENDENTLY_REPLAYED`;
- `CHECKED_BY_HUMAN`;
- `PUBLISHED_UNVERIFIED`;
- `AUTHOR_ASSUMPTION`;
- `NUMERICAL_ONLY`.

The system should not turn trust into a scalar confidence score. It should preserve explicit authority, method, artifact identity, and downstream dependence.

### 7.4 Ports should remain visible

Like a foreign-function boundary, external derivations should be:

- centralized and queryable;
- impossible to confuse with native verified evidence;
- explicit about assumptions and scope;
- attached to immutable artifacts where possible;
- propagated into dependent exports;
- easy to replace with stronger implementations later.

---

## 8. Positive utility: the carrots

Grand Portage currently earns attention mainly by refusing. Tools that only refuse are adopted by mandate, not by individual researchers who are trying to move quickly. The type discipline must become the price of useful capabilities.

### 8.1 One compact status surface

v0.32 has useful pieces in `gp review`, `gp doctor`, `gp project`, `gp history`,
and the campaign read models, but no single compact `gp status` command. Do not add
another broad report merely for the name; first define the smallest resumption
surface that is not already covered by `gp review`.

The first carrot should be a campaign brief that answers the question a fresh agent or collaborator actually has:

- What is the root research question?
- What is the current frontier?
- Which findings are live?
- Which findings are knowingly carried, and why?
- Which public exports depend on assumptions or carried debt?
- What changed since the last checkpoint?
- Which computations aborted or remain unaudited?
- What are the canonical next actions?
- What should be read first?

This directly addresses a failure already seen in a blind run: a healthy campaign carrying accepted debt was misread as a broken campaign.

"Recent" state should be defined by explicit session or batch identifiers and Git checkpoints rather than raw JSONL order, since merged append-only logs do not preserve one global wall-clock narrative.

### 8.2 `gp why`, `gp explain`, and `gp probe`

The cell ledger is a textbook disguised as a test file. Its content should become structured rule data from which the project generates:

- kernel tests;
- human documentation;
- runtime explanations;
- `gp why` output;
- counterexamples;
- known conservatisms;
- discharge suggestions.

Useful commands:

```text
gp why BASE_EXTENSION/ALONG/EMPTY
gp explain TRANSPORT:INF-C08-HIST
gp probe CL-X --across E7 --direction AGAINST
```

`probe()` is architecturally important. It is a query against the type system rather than an asserted program step. It should be a first-class CLI and MCP operation.

### 8.3 A ten-minute tutorial

The best introductory example is projection of the hyperbola:

```text
xy = 1  in A^2
project to the x-axis
```

The image is `x != 0`, while its Zariski closure is all of `A^1`. Elimination returns no polynomial constraint on `x`, so `x = 0` is a point of the closure but has no lift to the source variety.

That small campaign demonstrates:

- a correct CAS computation;
- a correct elimination artifact;
- an invalid witness inference;
- the difference between image and closure;
- a canonical refusal;
- a useful discharge.

A stranger should be able to install Grand Portage, run this example, and understand why the refusal is mathematically valuable in ten minutes.

### 8.4 The emitter as convenience

The long-term adoption strategy is that typing should save work:

- no hand-written ring setup;
- no identifier collisions;
- no ad hoc output parsing;
- automatic artifact capture;
- generated transport edges;
- automatic scope/evidence checks;
- backend substitution where supported.

When the semantic declaration generates the solver program and provenance, the type annotation stops being pure tax.

---

## 9. Validation, soundness, and empirical measurement

### 9.1 Retrodiction is necessary but not transfer

The current fixtures show that the generalized graph can reproduce known failures and preserve positive controls. That is an essential regression gate.

It does not yet establish transfer to:

- an independent operator;
- a campaign whose answer key was not written by the author;
- another mathematical domain;
- multi-agent merges under real pressure;
- a workflow with different backend semantics.

The next credibility gains come from blind and external use, not another internal fixture alone.

### 9.2 Soundness and precision ledger

The current registers should be described precisely:

- `KNOWN_UNSOUND` records deliberate or known false licensing. It should normally be empty and should block release.
- `KNOWN_CONSERVATISM` records deliberate loss of precision: sound steps refused because the kernel uses a simpler sufficient condition.

"Soundiness" is useful vocabulary for the first category and for explicit external-oracle modes. Conservatism is incompleteness, not unsoundness.

Together they form a **soundness/precision ledger**.

### 9.3 Measure conservative refusals

Instrument every conservative refusal with:

```text
cell
campaign
claim and evidence kind
why refused
whether a stronger check was available
whether the stronger check licensed it
human minutes spent
agent tokens spent
solver runs added or avoided
eventual discharge
whether the user attempted to route around it
```

Metrics:

```text
refusal rate
avoidable-refusal rate
median discharge cost
bug-prevention yield
solver spend avoided
solver spend added
bypass-attempt rate
unknown/undecidable rate
```

A refusal should count as unnecessary only when an independent stronger verifier, proof, or pinned answer key establishes the route was sound. The final conclusion merely being true is not enough; judging the route from the outcome repeats the project's central failure mode.

### 9.4 Structure the cell ledger

Each rule should be one structured object:

```text
CellRule
    relation
    direction
    claim or evidence kind
    verdict
    proof sketch
    counterexample
    side conditions
    citation
    known conservatism
    discharge
```

Generate the table, tests, documentation, and `gp why` from it. This reduces the chance that a test name, comment, runtime explanation, and design document carry different semantics.

### 9.5 Testing layers

The validation stack should include:

1. **Cell proofs/counterexamples** - is the semantic rule correct?
2. **Mutation tests** - is the declared attribute load-bearing?
3. **Boundary adversarial tests** - can the solver or importer be reached around?
4. **Retrodiction fixtures** - do known incidents reproduce from data?
5. **Positive controls** - are sound steps accepted?
6. **Blind live campaigns** - can an agent work without laundering a refusal?
7. **Cross-domain transfer** - does the vocabulary survive outside the source campaign?
8. **Merge trials** - do real independent branches compose or fail loudly?
9. **Read-surface tests** - can a fresh reader correctly summarize campaign state?

---

## 10. Interoperability: standards around the core

### 10.1 Native graph as semantic source of truth

Grand Portage should keep its native append-only graph as the authoritative semantic state. External standards should handle adjacent concerns through adapters:

```text
Grand Portage semantic graph
  models, claims, evidence, transports,
  partitions, justifications, obligations
                    |
        execution/artifact layer
     activities, plans, agents, digests
          /          |          \
       PROV       RO-Crate     in-toto
   interchange    packaging   attestation
```

### 10.2 What to adopt

| Framework | Recommendation | Adopted role |
|---|---|---|
| W3C PROV | Public provenance vocabulary and export | entities, activities, agents, plans, usage, generation, bundles |
| PML / Inference Web | Borrow justification anatomy | explicit conclusions, ordered premises, alternative justifications, engines, bindings |
| WINGS / ProvONE | Borrow plan-versus-run distinction | operation specifications, typed ports, workflow templates, execution instances |
| RO-Crate | Adopt for campaign packaging | project artifacts, metadata, profiles, publication bundles |
| in-toto / DSSE | Adopt for immutable artifact assertions | digests, typed predicates, optional signatures |
| OpenLineage | Adapter only | data-platform runs and versioned extension facets |
| CWLProv / Workflow Run RO-Crate | Import/export where users already have workflows | existing plan and execution traces |

### 10.3 The semantic firewall

A generic provenance relation must never mint a mathematical license.

```text
B prov:wasDerivedFrom A
```

means that B was produced using or based on A. It does not say whether witnesses lift, emptiness descends, predicates survive, or coordinate-ring identities transport.

Import policy:

1. generic entities, activities, agents, uses, and generations may enter as provenance;
2. generic derivations remain provenance-only;
3. an imported relation with a recognized, versioned Grand Portage extension may reconstruct a typed edge after validation;
4. otherwise it enters semantic quarantine as `UNTYPED` debt;
5. imported certificate assertions remain unverified until a registered verifier accepts them.

### 10.4 Adapters are themselves transports

Every export should declare what it preserves and loses:

```yaml
adapter: gp-to-prov-o
preserves:
  - entity identity
  - activity usage and generation
  - agent attribution
  - artifact derivation

drops:
  - executable transport semantics
  - checker severity derivation
  - baseline blocking policy
  - supersession discharge enforcement
```

This is an opportunity to dogfood Grand Portage's central idea at its own ecosystem boundary.

### 10.5 Recommended adoption sequence

1. add artifact/activity identities internally;
2. make inference conclusions first-class claims;
3. emit unsigned in-toto Statements for load-bearing artifacts;
4. implement `gp pack` using RO-Crate;
5. add a read-only PROV export;
6. define a Grand Portage Campaign Profile;
7. add import adapters only after the native model is stable.

The first standards-focused work should not require changes to `kernel.py`.

---

## 11. Roadmap from v0.32

The older phase list mixed already-delivered work, architectural prerequisites,
and speculative product features. The dependency order is now clearer.

### Post-v0.32 hardening - no semantic release required

- keep `gp review` as the checked, full, history-aware cold-reader preset;
- refuse free witness parameters before invoking a CAS;
- label quotient identities as vacuous on a currently verified zero-ring model;
- update this prior-art and architecture record.

These changes improve refusal quality and resumption but do not alter graph format,
kernel epoch, transport cells, or mathematical authority. They may ride on `master`
until a distribution artifact is otherwise needed; the feedback packet alone does
not justify a version bump.

### Candidate v0.33 - authority-binding nucleus

- define internal `CheckedEvidence`, `ContextBinding`, `AuthorityReceipt`, and
  explicit refusal values;
- route every existing authority-producing path through one binder;
- prevent backends, producers, CLI handlers, and administrative acceptance from
  minting receipts;
- retain byte-compatible graph events and current checker judgments;
- add characterization tests comparing old and new authority frontiers on all
  frozen fixtures and historical generations.

**Exit condition:** there is one auditable code path from checked evidence to
current authority, and the extraction changes no existing licensed conclusion.
Keep kernel epoch 11 if persisted semantics and fingerprints truly remain unchanged.

### Candidate v0.34 / kernel epoch 12 - capability-bound composition

- implement the frozen field vocabulary and certificate-specific reach rules;
- bind point universe, witness field, embeddings, coefficient maps, and semantic
  scope into authority fingerprints;
- implement an explicit family-to-model composition contract as the first
  cross-regime bridge;
- preserve enumeration debt, evidence direction, stale premises, exclusions, and
  open branches as load-bearing inputs;
- derive operation transport from checked capabilities where the point fragment
  already demonstrates the pattern;
- keep CLI, MCP, schema, migration, fingerprints, supersession, and Lean shadow in
  parity.

**Exit condition:** the epoch-12 matrices and counterexamples in the v0.32
preflight and handoff pass; old readable events do not retain authority merely
because they deserialize.

### After the receipt boundary - explanation and authoring

- add `gp explain <claim|inference|finding>` as a minimal current proof slice or
  exact first failed judgment;
- add `gp diff --authority A B` for gained, lost, narrowed, widened, or stale
  authority rather than raw event differences;
- let truth-maintenance algorithms optimize support slicing and invalidation while
  leaving semantic licensing in the kernel;
- make campaign identity/root mandatory for authority-affecting mutations;
- retain only high-level operation and claim constructors earned by live use.

**Exit condition:** a cold reader can identify why one conclusion is licensed and
what authority changed without reconstructing the full event history.

### Later - typed claims, regimes, and formal compression

- introduce the smallest typed claim fragments that remove demonstrated runtime
  ambiguity;
- expose exact-affine, ordered-real, finite-family, and any future certified-numeric
  regime boundaries without prematurely freezing a plugin architecture;
- test another independent cross-regime bridge before generalizing the common core;
- continue Lean extraction around capability generation, healthiness conditions,
  certificate stability, and selected composition laws;
- formalize a paper-style nucleus only after those laws survive multiple regimes.

Do not rewrite Grand Portage in Lean, build a universal proof language, or design a
general categorical architecture ahead of live failures.

---

## 12. Design invariants

The following should be treated as architectural laws unless live evidence forces revision:

1. **No computation that creates a model runs without an explicit or operation-derived semantic relation.**
2. **No generic provenance import mints a transport license.**
3. **No caller-supplied certificate label mints verifier-level capability.**
4. **No raw string reaches a solver through the supported typed path.**
5. **No note can serve as a hidden premise.**
6. **Every premise in a joint inference must meet at a common semantic context, except an explicitly licensed partition rule.**
7. **Branches are pieces, not relaxations of the whole parent.**
8. **Obligations survive supersession unless discharged by an admitted move.**
9. **Accepted debt remains visible to readers and downstream exports.**
10. **Claim truth and evidence transport are distinct questions.**
11. **Evidence quality never silently changes transport semantics.**
12. **The LLM proposes; deterministic verifiers and the kernel decide.**
13. **Every adapter declares what it preserves and drops.**
14. **Every refusal should name a legitimate next action, while admitting when no automatic action can find the missing mathematics.**
15. **The native graph remains the semantic source of truth; external formats are projections or packages.**

---

## 13. Open questions to push on

### 13.1 Composite operations

Should one graph edge represent only one primitive semantic operation, or may a trusted constructor produce a composite edge carrying several effects? Primitive edges improve explanation and reuse; composite edges may match actual CAS calls better. A likely compromise is a composite operation whose compiled semantic path remains inspectable.

### 13.2 Structured fields and embeddings

How much field structure is required before the system can safely unify `integral` and `coefficients_in_base`? The minimum useful representation may be smaller than a full computer algebra field hierarchy, but it must represent explicit embeddings and coefficient membership.

### 13.3 Exact identity transport

The current `AMBIENT` versus `DERIVED` distinction is a safe approximation. The exact test for pushing an identity into a looser model is edge-relative: whether `lhs - rhs` lies in the target ideal. Should this become a verifier-produced evidence capability rather than a claim-origin label?

### 13.4 Claim/evidence migration

Can the current fixtures be represented with separate propositions and evidence without making ordinary use intolerably verbose? The prototype should measure graph size, user burden, and which known conservatisms disappear.

### 13.5 Authority profiles

What may an external derivation support in exploratory mode, publication mode, and formalization mode? Authority policy should be configurable without changing mathematical transport semantics.

### 13.6 Quantitative transport

A future scientific extension may need error transformers rather than booleans:

```text
claim with error epsilon
  -- discretization(delta) -->
claim with error at most f(epsilon, delta)
```

This could reach certified numerics and physics, but it should not enter the core until exact symbolic transport is mature.

### 13.7 Campaign profiles

Which recurring shapes survive independent use? Profiles should be extracted from campaigns, not imagined from the source project.

### 13.8 Bounded research questions

Several questions are now precise enough to record without turning the product
into a theory project:

1. **Representation of point transport.** Which `EMPTY`, `NONEMPTY`, and
   `PREDICATE` tables are generated completely by relations with totality,
   surjectivity, and predicate-correspondence capabilities?
2. **Healthiness of operation semantics.** Which monotonicity, join/meet,
   identity, and composition laws characterize admissible GP predicate
   transformers and reject malformed operation contracts structurally?
3. **Certificate-typed transportability.** Can each certificate family be
   associated with the maximal class of model transformations under which its
   validity is stable, with a theorem or counterexample establishing the class?
4. **Authority-preserving translation validation.** Can validation return the
   precise capabilities earned by one deliberately lossy mathematical
   transformation rather than a single equivalent/not-equivalent verdict?
5. **Truth maintenance with semantic edges.** Can support labels carry a support
   environment, semantic scope, and authority contract while preserving efficient
   incremental invalidation?
6. **Semantic attestations for computational claims.** Can checked mathematical
   receipts reuse attestation envelopes without pretending that supply-chain
   integrity alone establishes semantic authority?

---

## 14. Recommended project language

### 14.1 One-sentence description

> **Grand Portage is a proof-carrying transport calculus for computational
> mathematics, coupled to an event-sourced authority system: it records what each
> model transformation loses, checks what claims and evidence may cross it, and
> turns unsupported reuse into explicit obligations.**

### 14.2 Longer description

> Computational research pipelines routinely connect individually correct artifacts with semantically invalid transitions: a closure point is treated as a witness, a field-relative certificate becomes a geometric conclusion, one branch is generalized to a whole case split, or two computations are joined without a common model. Grand Portage makes those seams first-class. A small deterministic kernel checks claim and evidence transport across typed model transformations, while an append-only graph preserves campaign state and an LLM or human drives the repair loop outside the trust boundary.

### 14.3 Internal taxonomy

- **Core semantic object:** typed transport and evidence calculus;
- **Logical account:** indexed claims and relational predicate transformers;
- **Execution architecture:** compiler frontend plus backend adapters;
- **Operational loop:** verifier-guided, CEGAR-shaped refinement;
- **Implementation mechanism:** effect-and-capability system;
- **Authority lifecycle:** event-sourced truth maintenance with semantic edges;
- **Composition architecture:** semantic module system;
- **Interchange architecture:** PROV, RO-Crate, in-toto, and workflow adapters;
- **Trust architecture:** LCF-like verified evidence constructors.

### 14.4 What is plausibly novel

The novelty claim should remain narrow and conditional. It is not supported by an
absence search:

> Existing systems describe workflows, provenance, proofs, abstractions, and certificates. Grand Portage treats the semantic permission to reuse a result across heterogeneous mathematical models as a first-class executable contract, enforces that contract at the computational boundary, preserves its obligations across autonomous-agent handoff and supersession, and compiles refusals into concrete research actions.

That is a systems contribution even where every individual ingredient has ancestors.

---

## 15. What would change this picture

The architecture should be reconsidered if any of the following occurs:

- an independent campaign shows that the five current relation families are too domain-specific;
- structured elaboration fails to reduce clerical modeling cost;
- claim/evidence separation adds substantial burden without removing conservatism or bugs;
- operators routinely choose `UNTYPED` or external assumptions and make no progress toward stronger evidence;
- typed emission cannot cover enough useful CAS work to be a carrot;
- model interfaces cannot hide implementations without hiding load-bearing obligations;
- conservative refusal costs outweigh prevented errors in measured use;
- a simpler existing framework can express Grand Portage's licensing semantics without weakening them;
- blind agents consistently route around the boundary through a pattern the architecture cannot represent cleanly.

Conversely, the picture strengthens if:

- independent campaigns reuse the same operation and claim vocabulary;
- certificate capabilities eliminate mislabeling in live work;
- the frontend reduces both solver boilerplate and semantic mistakes;
- interfaces allow private and alternative implementations to compose;
- `gp status` makes cold resumption reliable;
- measured refusals save solver spend or prevent published errors at acceptable cost;
- a Lean-CAS bridge demonstrates that Grand Portage cleanly owns the portage between trusted tools.

---

## Appendix A. Candidate event and object sketches

These sketches are illustrative, not schema commitments.

### A.1 Operation and execution

```json
{
  "ev": "operation",
  "id": "OP-17",
  "kind": "ELIMINATE",
  "source": "MODEL-SRC",
  "variables": ["y"],
  "produces": "MODEL-ELIM"
}
```

```json
{
  "ev": "activity",
  "id": "RUN-17",
  "operation": "OP-17",
  "engine": "Singular 4.2.1",
  "program_digest": "sha256:...",
  "input_digests": ["sha256:..."],
  "output_digests": ["sha256:..."],
  "status": "OK"
}
```

### A.2 Evidence capability

```json
{
  "ev": "evidence",
  "id": "EV-UNIT-17",
  "kind": "VERIFIED_UNIT_IDEAL",
  "artifact": "basis.json",
  "artifact_digest": "sha256:...",
  "verified_by": "grandportage.verify_unit_ideal/v1",
  "supports": ["EMPTY", "SCHEME_SCOPE"]
}
```

### A.3 Claim and justification

```json
{
  "ev": "claim",
  "id": "CL-EMPTY-17",
  "model": "MODEL-ELIM",
  "proposition": {"kind": "EMPTY"},
  "evidence": ["EV-UNIT-17"]
}
```

```json
{
  "ev": "justification",
  "id": "J-17",
  "premises": ["CL-A", "CL-B"],
  "conclusion": "CL-EMPTY-17",
  "rule": "PARTITION_EXHAUSTION",
  "via_partition": "P-3"
}
```

### A.4 Model interface

```json
{
  "ev": "interface",
  "id": "IF-GAMMA3-v1",
  "signature": "SIG-GAMMA3",
  "exports": ["CL-G3-EMPTY", "CL-G3-CAP"],
  "carries": ["OBL-GAMMA-TRANSFER"],
  "implementation": "private:gamma3-campaign@commit"
}
```

---

## Appendix B. Ten-minute tutorial outline

1. Declare the source model `xy - 1 = 0` over `Q[x,y]`.
2. Run the typed `Eliminate(y)` operation.
3. Observe that the elimination ideal in `Q[x]` is zero, so the target closure is all of `A^1`.
4. Declare the target witness `x = 0`.
5. Attempt to carry that witness against the image-closure edge.
6. Grand Portage refuses: a point of the closure need not lift to the image.
7. Ask `gp why IMAGE_CLOSURE/AGAINST/PointWitness`.
8. Ask `gp probe ExistsPoint` across the same edge and observe the proposition/evidence distinction in the experimental model.
9. Discharge by adding the open condition `x != 0` or by exhibiting a preimage for a different target point.
10. Run `gp review` and `gp doctor`; identify what a future compact status surface
    would still need to add.

The tutorial should end with one sentence: **the CAS was right; the unsupported conclusion was at the seam.**

---

## Appendix C. Selected adjacent work

1. Patrick Cousot and Radhia Cousot, "Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints," POPL 1977. https://doi.org/10.1145/512950.512973
2. John M. Lucassen and David K. Gifford, "Polymorphic Effect Systems," POPL 1988. https://doi.org/10.1145/73560.73564
3. M. Gordon, R. Milner, L. Morris, M. Newey, and C. Wadsworth, "A Metalanguage for Interactive Proof in LCF," POPL 1978. https://doi.org/10.1145/512760.512773
4. Ben Livshits, "In Defense of Soundiness: A Manifesto," Communications of the ACM 58(2), 2015.
5. Maria Christakis, Peter Mueller, and Valentin Wuestholz, "An Experimental Evaluation of Deliberate Unsoundness in a Static Program Analyzer," VMCAI 2015.
6. Joseph Goguen and Rod Burstall, "Institutions: Abstract Model Theory for Specification and Programming," Journal of the ACM 39(1), 1992. https://doi.org/10.1145/147508.147524
7. W3C PROV family of specifications. https://www.w3.org/TR/prov-overview/
8. Proof Markup Language Primer, Inference Web Group, 2007. https://inference-web.org/2007/primer/
9. WINGS semantic workflow system. https://wings-workflows.org/
10. RO-Crate Metadata Specification 1.3. https://www.researchobject.org/ro-crate/specification/1.3/
11. in-toto Attestation Framework, Statement v1. https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
12. The Elm Architecture and Elm ports. https://guide.elm-lang.org/architecture/ and https://guide.elm-lang.org/interop/ports
13. Edsger W. Dijkstra, "Guarded Commands, Nondeterminacy and Formal Derivation of Programs," Communications of the ACM 18(8), 1975. https://doi.org/10.1145/360933.360975
14. Johan de Kleer, "An Assumption-Based TMS," Artificial Intelligence 28(2), 1986. https://doi.org/10.1016/0004-3702(86)90080-9
15. Ross M. McConnell, Kurt Mehlhorn, Stefan Näher, and Pascal Schweitzer, "Certifying Algorithms," Computer Science Review 5(2), 2011. https://doi.org/10.1016/j.cosrev.2010.09.009
16. George C. Necula, "Proof-Carrying Code," POPL 1997. https://doi.org/10.1145/263699.263712
17. Amir Pnueli, Michael Siegel, and Ofer Shtrichman, "Translation Validation for Synchronous Languages," ICALP 1998. https://cs.nyu.edu/home/people/in_memoriam/pnueli/transval-icalp98.html
18. Object Management Group, Structured Assurance Case Metamodel 2.1, 2020. https://www.omg.org/spec/SACM/2.1
19. Todd J. Green, Grigoris Karvounarakis, and Val Tannen, "Provenance Semirings," PODS 2007. https://doi.org/10.1145/1265530.1265535
20. SLSA Provenance specification. https://slsa.dev/spec/v1.2/provenance

---

## Closing recommendation

Keep the native graph small and exact. Extract the authority-binding nucleus before
expanding certificate reach. Let operations construct semantic components, let
checked evidence establish capabilities, and let the binder alone construct
current authority. Build typed claim fragments only where they eliminate a
demonstrated ambiguity; keep standards at the packaging and interchange boundary.
Use the LLM aggressively as the search and repair policy, but keep every licensing
decision in deterministic code or an external trusted verifier.

The durable thesis is not that Grand Portage invents a new proof system. It is that autonomous computational research needs a typed, persistent account of the semantic seams between otherwise valid artifacts. That is the layer to build.
